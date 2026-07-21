#
# Copyright (C) 2023, Inria
# GRAPHDECO research group, https://team.inria.fr/graphdeco
# All rights reserved.
#
# This software is free for non-commercial, research and evaluation use 
# under the terms of the LICENSE.md file.
#
# For inquiries contact  george.drettakis@inria.fr
#

import os
import random
import json
from utils.system_utils import searchForMaxIteration
from scene.dataset_readers import sceneLoadTypeCallbacks, storePly
from scene.gaussian_model import GaussianModel, BasicPointCloud
from scene.gaussian_curve_model import GaussianCurveModel
from arguments import ModelParams
from utils.camera_utils import cameraList_from_camInfos, camera_to_JSON

import numpy as np
import open3d as o3d


# ============================================ 在这里加额外的致密策略 ==============================================
def Simplyfill(points, colors, normals, grid_resX=50, grid_resY=50, grid_resZ=50):
    xyz_min = points.min(axis=0)
    xyz_max = points.max(axis=0)

    xs = np.linspace(xyz_min[0], xyz_max[0], grid_resX)
    ys = np.linspace(xyz_min[1], xyz_max[1], grid_resY)
    zs = np.linspace(xyz_min[2], xyz_max[2], grid_resZ)

    gx, gy, gz = np.meshgrid(xs, ys, zs)
    grid_pts = np.stack([gx.ravel(), gy.ravel(), gz.ravel()], axis=1).astype(np.float32)

    new_points  = np.vstack([points, grid_pts])
    new_colors  = np.vstack([colors,  np.tile([1.0, 0.0, 0.0], (len(grid_pts), 1)) ])   # 红色
    new_normals = np.vstack([normals, np.zeros((len(grid_pts), 3))])
    return new_points, new_colors, new_normals

def _Planefill3_single(points, colors, normals, view_cam, view_depth=20.0, depth_samples=200,
                       outer_count_threshold=500, center_ratio=0.5, plane_fill_ratio=0.1,
                       angle_sum_threshold=20.0):
    depth_step = view_depth / depth_samples
    half_depth_window = depth_step * 0.5
    sample_depths = np.linspace(depth_step, view_depth, depth_samples, dtype=np.float32)

    world_to_camera_rot = view_cam.R.transpose().astype(np.float32)
    world_to_camera_t = view_cam.T.astype(np.float32)
    points_cam = points.astype(np.float32) @ world_to_camera_rot.T + world_to_camera_t

    z = points_cam[:, 2]
    valid_depth = (z > 0.0) & (z <= view_depth + half_depth_window)
    points_cam = points_cam[valid_depth]
    z = points_cam[:, 2]

    tan_half_fovx = np.tan(view_cam.FovX * 0.5)
    tan_half_fovy = np.tan(view_cam.FovY * 0.5)

    chosen_depth = None
    chosen_outer_count = None
    chosen_outer_points_cam = None

    for depth in sample_depths:
        depth_mask = np.abs(z - depth) <= half_depth_window
        if not np.any(depth_mask):
            continue

        slice_points = points_cam[depth_mask]
        slice_z = slice_points[:, 2]
        proj_x = slice_points[:, 0] / slice_z
        proj_y = slice_points[:, 1] / slice_z

        in_full_view = (np.abs(proj_x) <= tan_half_fovx) & (np.abs(proj_y) <= tan_half_fovy)
        in_center = (
            (np.abs(proj_x) <= tan_half_fovx * center_ratio) &
            (np.abs(proj_y) <= tan_half_fovy * center_ratio)
        )
        in_outer_ring = in_full_view & (~in_center)
        outer_count = int(np.sum(in_outer_ring))

        if outer_count <= outer_count_threshold:
            continue

        chosen_depth = float(depth)
        chosen_outer_count = outer_count
        chosen_outer_points_cam = slice_points[in_outer_ring]

    if chosen_depth is None:
        return np.empty((0, 3), dtype=np.float32), np.empty((0, 3), dtype=np.float32), np.empty((0, 3), dtype=np.float32)

    ox = chosen_outer_points_cam[:, 0]
    oy = chosen_outer_points_cam[:, 1]
    oz = chosen_outer_points_cam[:, 2]
    pitch_mean = float(np.mean(np.degrees(np.arctan2(oy, oz))))
    yaw_mean = float(np.mean(np.degrees(np.arctan2(ox, oz))))

    angle_means = np.array([pitch_mean, yaw_mean], dtype=np.float32)
    if np.any(np.abs(angle_means) > angle_sum_threshold):
        print(
            f"Planefill3 skip {view_cam.image_name}: "
            f"pitch_mean={pitch_mean:.2f}, yaw_mean={yaw_mean:.2f}, "
            f"outer_count={chosen_outer_count}"
        )
        return np.empty((0, 3), dtype=np.float32), np.empty((0, 3), dtype=np.float32), np.empty((0, 3), dtype=np.float32)

    center_half_width = chosen_depth * tan_half_fovx * center_ratio
    center_half_height = chosen_depth * tan_half_fovy * center_ratio
    fill_step_x = max(center_half_width * 2.0 * plane_fill_ratio, 1e-6)
    fill_step_y = max(center_half_height * 2.0 * plane_fill_ratio, 1e-6)

    fill_x = np.arange(-center_half_width, center_half_width + fill_step_x * 0.5, fill_step_x, dtype=np.float32)
    fill_y = np.arange(-center_half_height, center_half_height + fill_step_y * 0.5, fill_step_y, dtype=np.float32)
    yy, xx = np.meshgrid(fill_y, fill_x, indexing="ij")
    zz = np.full_like(xx, chosen_depth, dtype=np.float32)
    fill_cam_points = np.stack([xx, yy, zz], axis=-1).reshape(-1, 3)

    world_to_camera = np.eye(4, dtype=np.float32)
    world_to_camera[:3, :3] = world_to_camera_rot
    world_to_camera[:3, 3] = world_to_camera_t
    camera_to_world = np.linalg.inv(world_to_camera)

    fill_cam_points_h = np.concatenate([
        fill_cam_points,
        np.ones((fill_cam_points.shape[0], 1), dtype=np.float32)
    ], axis=1)
    fill_world_points = (camera_to_world @ fill_cam_points_h.T).T[:, :3]

    fill_colors = np.tile([0.0, 0.0, 1.0], (fill_world_points.shape[0], 1))
    fill_normals = np.zeros_like(fill_world_points)
    return fill_world_points, fill_colors, fill_normals

def Planefill3(points, colors, normals, cam_infos, view_depth=20.0, depth_samples=200,
               outer_count_threshold=500, center_ratio=0.5, plane_fill_ratio=0.1,
               angle_sum_threshold=20.0):
    if cam_infos is None:
        return points, colors, normals
    if not isinstance(cam_infos, (list, tuple)):
        cam_infos = [cam_infos]

    fill_points_list = []
    fill_colors_list = []
    fill_normals_list = []

    for view_cam in cam_infos:
        fill_points, fill_colors, fill_normals = _Planefill3_single(
            points, colors, normals, view_cam,
            view_depth=view_depth,
            depth_samples=depth_samples,
            outer_count_threshold=outer_count_threshold,
            center_ratio=center_ratio,
            plane_fill_ratio=plane_fill_ratio,
            angle_sum_threshold=angle_sum_threshold,
        )
        if fill_points.shape[0] == 0:
            continue
        fill_points_list.append(fill_points)
        fill_colors_list.append(fill_colors)
        fill_normals_list.append(fill_normals)

    if len(fill_points_list) == 0:
        return points, colors, normals

    points = np.vstack([points, np.concatenate(fill_points_list, axis=0)])
    colors = np.vstack([colors, np.concatenate(fill_colors_list, axis=0)])
    normals = np.vstack([normals, np.concatenate(fill_normals_list, axis=0)])
    return points, colors, normals
# ==============================================================================================================


class Scene:

    gaussians : GaussianModel
    gaussian_curve_model: GaussianCurveModel

    def __init__(self, args : ModelParams, gaussians : GaussianModel, load_iteration=None, shuffle=True, resolution_scales=[1.0]):
        """b
        :param path: Path to colmap scene main folder.
        """
        self.model_path = args.model_path
        self.loaded_iter = None
        self.gaussians = gaussians

        if load_iteration:
            if load_iteration == -1:
                self.loaded_iter = searchForMaxIteration(os.path.join(self.model_path, "point_cloud"))
            else:
                self.loaded_iter = load_iteration
            print("Loading trained model at iteration {}".format(self.loaded_iter))

        self.train_cameras = {}
        self.test_cameras = {}

        # 在这里调用 dataset_readers.py 里的 sceneLoadTypeCallbacks ，然后使用 readColmapSceneInfo 读取
        if os.path.exists(os.path.join(args.source_path, "sparse")):
            scene_info = sceneLoadTypeCallbacks["Colmap"](args.source_path, args.images, args.depths,
                                                          args.eval, args.train_test_exp, detector=args.detector,
                                                          init_voxel_size=args.init_voxel_size)
        elif os.path.exists(os.path.join(args.source_path, "transforms_train.json")):
            print("Found transforms_train.json file, assuming Blender data set!")
            scene_info = sceneLoadTypeCallbacks["Blender"](args.source_path, args.white_background,
                                                           args.depths, args.eval, detector=args.detector)
        elif os.path.exists(os.path.join(args.source_path, "meta_data.json")):
            print("Found transforms_train.json file, assuming Blender data set!")
            scene_info = sceneLoadTypeCallbacks["emap"](args.source_path, args.white_background,
                                                           args.depths, args.eval, detector=args.detector)

        else:
            assert False, "Could not recognize scene type!"

        # ============================================ 在这里加额外的致密策略 ==============================================
        points = np.asarray(scene_info.point_cloud.points)
        colors = np.asarray(scene_info.point_cloud.colors)
        normals = np.asarray(scene_info.point_cloud.normals)
        print(f"colmap得到点数:   {points.shape[0]}")

        # 先去除离群点，再填充
        # remove_radius_outlier: 某个点在 radius 半径内邻居数少于 nb_points 个，就认为是离群点删除
        # nb_points 越大、radius 越小，滤除越激进
        # radius 按场景对角线长度的 1% 自动计算，避免场景尺度不同时 radius 设死导致全被删
        pcd_o3d = o3d.geometry.PointCloud()
        pcd_o3d.points = o3d.utility.Vector3dVector(points)
        pcd_o3d.colors = o3d.utility.Vector3dVector(colors)
        scene_diag = float(np.linalg.norm(points.max(axis=0) - points.min(axis=0)))
        radius = scene_diag * 0.01
        print(f"scene diagonal: {scene_diag:.3f}, outlier radius: {radius:.3f}")
        pcd_clean, _ = pcd_o3d.remove_radius_outlier(nb_points=30, radius=radius)
        points = np.asarray(pcd_clean.points)
        colors = np.asarray(pcd_clean.colors)
        normals = np.zeros_like(points)
        print(f"离群点去除后点数: {points.shape[0]} points")

        # 无脑填充点云，生成一个网格点云
        # points, colors, normals = Simplyfill(points, colors, normals, grid_resX=50, grid_resY=50, grid_resZ=20)
        points, colors, normals = Planefill3(
                    points, colors, normals, scene_info.train_cameras,
                    view_depth=args.Planefill3_view_depth,
                    depth_samples=200,
                    Planefill3_outer_count_threshold=args.Planefill3_outer_count_threshold,
                    center_ratio=0.5,
                    plane_fill_ratio=0.05,
                    angle_sum_threshold=args.Planefill3_angle_sum_threshold,
                )
        input_filled_ply_path = os.path.join(self.model_path, "input_filled.ply")
        storePly(input_filled_ply_path, points, colors * 255.0)
        print(f"wrote input_filled.ply: {input_filled_ply_path}")
        print(f"填充点云后点数: {points.shape[0]} points")

        # 把填充后的点云写回 scene_info，这样后续 create_from_pcd 才真正用填充后的点初始化曲线
        from scene.gaussian_model import BasicPointCloud
        scene_info = scene_info._replace(
            point_cloud=BasicPointCloud(points=points, colors=colors, normals=normals)
        )
        # ==============================================================================================================

        if not self.loaded_iter:
            if not args.simple:
                with open(scene_info.ply_path, 'rb') as src_file, open(os.path.join(self.model_path, "input.ply") , 'wb') as dest_file:
                    dest_file.write(src_file.read())
                json_cams = []
                camlist = []
                if scene_info.test_cameras:
                    camlist.extend(scene_info.test_cameras)
                if scene_info.train_cameras:
                    camlist.extend(scene_info.train_cameras)
                for id, cam in enumerate(camlist):
                    json_cams.append(camera_to_JSON(id, cam))
                with open(os.path.join(self.model_path, "cameras.json"), 'w') as file:
                    json.dump(json_cams, file)

        if shuffle:
            random.shuffle(scene_info.train_cameras)  # Multi-res consistent random shuffling
            random.shuffle(scene_info.test_cameras)  # Multi-res consistent random shuffling

        self.cameras_extent = scene_info.nerf_normalization["radius"]

        for resolution_scale in resolution_scales:
            print("Loading Training Cameras")
            self.train_cameras[resolution_scale] = cameraList_from_camInfos(scene_info.train_cameras, resolution_scale, args, scene_info.is_nerf_synthetic, False)
            print("Loading Test Cameras")
            self.test_cameras[resolution_scale] = cameraList_from_camInfos(scene_info.test_cameras, resolution_scale, args, scene_info.is_nerf_synthetic, True)

        if self.loaded_iter:
            self.gaussians.load_ply(os.path.join(self.model_path,
                                                           "point_cloud",
                                                           "iteration_" + str(self.loaded_iter),
                                                           "point_cloud.ply"), args.train_test_exp)
        else:
            if scene_info.point_cloud is not None:
                print(f"Initial point cloud points: {scene_info.point_cloud.points.shape[0]}")
            self.gaussians.create_from_pcd(scene_info.point_cloud, scene_info.train_cameras, self.cameras_extent)

    def save(self, iteration):
        point_cloud_path = os.path.join(self.model_path, "point_cloud/iteration_{}".format(iteration))
        self.gaussians.save_ply(os.path.join(point_cloud_path, "point_cloud.ply"))
        exposure_dict = {
            image_name: self.gaussians.get_exposure_from_name(image_name).detach().cpu().numpy().tolist()
            for image_name in self.gaussians.exposure_mapping
        }

        with open(os.path.join(self.model_path, "exposure.json"), "w") as f:
            json.dump(exposure_dict, f, indent=2)

    def getTrainCameras(self, scale=1.0):
        return self.train_cameras[scale]

    def getTestCameras(self, scale=1.0):
        return self.test_cameras[scale]
