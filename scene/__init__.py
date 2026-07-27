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
from scipy.spatial import ConvexHull, cKDTree


# ============================================ 在这里加额外的致密策略 ==============================================

def _camera_centers_from_cameras(cameras):
    centers = []
    for cam in cameras:
        world_to_camera_rot = cam.R.transpose().astype(np.float32)
        world_to_camera_t = cam.T.astype(np.float32)
        world_to_camera = np.eye(4, dtype=np.float32)
        world_to_camera[:3, :3] = world_to_camera_rot
        world_to_camera[:3, 3] = world_to_camera_t
        camera_to_world = np.linalg.inv(world_to_camera)
        centers.append(camera_to_world[:3, 3])
    return np.asarray(centers, dtype=np.float32)

def _trajectory_up_axis(cameras):
    camera_centers = _camera_centers_from_cameras(cameras)
    if camera_centers.shape[0] < 3:
        return None

    centered = camera_centers - camera_centers.mean(axis=0)
    _, _, Vt = np.linalg.svd(centered, full_matrices=False)
    return Vt[-1]

def _min_area_rect_basis(points, up_axis=None):
    centroid = points.mean(axis=0)
    centered = points - centroid
    if up_axis is None:
        _, _, Vt = np.linalg.svd(centered, full_matrices=False)
        e1, e2, up_axis = Vt[0], Vt[1], Vt[2]
    else:
        up_axis = np.asarray(up_axis, dtype=np.float64)
        up_axis = up_axis / max(np.linalg.norm(up_axis), 1e-12)
        projected = centered - (centered @ up_axis)[:, None] * up_axis[None, :]
        _, _, Vt_plane = np.linalg.svd(projected, full_matrices=False)
        e1 = Vt_plane[0]
        e1 = e1 - np.dot(e1, up_axis) * up_axis
        e1 = e1 / max(np.linalg.norm(e1), 1e-12)
        e2 = np.cross(up_axis, e1)
        e2 = e2 / max(np.linalg.norm(e2), 1e-12)

    pts2d = np.stack([centered @ e1, centered @ e2], axis=1)
    hull = ConvexHull(pts2d)
    hull_pts = pts2d[hull.vertices]
    n = len(hull_pts)

    best_area = np.inf
    best_angle = 0.0
    for i in range(n):
        edge = hull_pts[(i + 1) % n] - hull_pts[i]
        angle = np.arctan2(edge[1], edge[0])
        c, s = np.cos(angle), np.sin(angle)
        rot = np.array([[c, -s], [s, c]])
        rotated = hull_pts @ rot
        w = rotated[:, 0].max() - rotated[:, 0].min()
        h = rotated[:, 1].max() - rotated[:, 1].min()
        area = w * h
        if area < best_area:
            best_area = area
            best_angle = angle

    c, s = np.cos(best_angle), np.sin(best_angle)
    u2d, v2d = np.array([c, s]), np.array([-s, c])
    u3d = u2d[0] * e1 + u2d[1] * e2
    v3d = v2d[0] * e1 + v2d[1] * e2

    w = (pts2d @ u2d).max() - (pts2d @ u2d).min()
    h = (pts2d @ v2d).max() - (pts2d @ v2d).min()
    axis0, axis1 = (u3d, v3d) if w >= h else (v3d, u3d)

    Vt_final = np.stack([axis0, axis1, up_axis], axis=0)
    return centroid, Vt_final

def Simplyfill2(points, colors, normals, grid_resX=50, grid_resY=50, grid_resZ=50, up_axis=None):
    # 使用贴合场景的坐标系；只保留落在已有点水平膨胀区域内的竖向补点线
    clean_centroid, Vt = _min_area_rect_basis(points, up_axis=up_axis)
    centered = points - clean_centroid
    pts_pca = centered @ Vt.T

    pca_min = pts_pca.min(axis=0)
    pca_max = pts_pca.max(axis=0)
    bbox_length = pca_max[0] - pca_min[0]
    bbox_width = pca_max[1] - pca_min[1]
    half_expand_length = bbox_length / 20.0
    half_expand_width = bbox_width / 20.0

    xs = np.linspace(pca_min[0], pca_max[0], grid_resX)
    ys = np.linspace(pca_min[1], pca_max[1], grid_resY)
    zs = np.linspace(pca_min[2], pca_max[2], grid_resZ)

    gx, gy = np.meshgrid(xs, ys, indexing="ij")
    candidate_xy = np.stack([gx.ravel(), gy.ravel()], axis=1)
    point_xy = pts_pca[:, :2]
    tree = cKDTree(point_xy)
    search_radius = max(half_expand_length, half_expand_width)
    neighbor_lists = tree.query_ball_point(candidate_xy, r=search_radius, p=np.inf)

    keep_column = np.zeros(candidate_xy.shape[0], dtype=bool)
    for idx, neighbor_idx in enumerate(neighbor_lists):
        if len(neighbor_idx) == 0:
            continue
        delta = np.abs(point_xy[neighbor_idx] - candidate_xy[idx])
        keep_column[idx] = np.any(
            (delta[:, 0] <= half_expand_length) &
            (delta[:, 1] <= half_expand_width)
        )

    valid_xy = candidate_xy[keep_column]
    if len(valid_xy) > 0:
        grid_pca = np.stack([
            np.repeat(valid_xy[:, 0], grid_resZ),
            np.repeat(valid_xy[:, 1], grid_resZ),
            np.tile(zs, len(valid_xy)),
        ], axis=1).astype(np.float32)
    else:
        grid_pca = np.empty((0, 3), dtype=np.float32)
    grid_pts = grid_pca @ Vt + clean_centroid

    new_points = np.vstack([points, grid_pts])
    new_colors = np.vstack([colors, np.tile([1.0, 0.0, 0.0], (len(grid_pts), 1))])
    new_normals = np.vstack([normals, np.zeros((len(grid_pts), 3))])
    return new_points, new_colors, new_normals


def _Planefill3_single(points, colors, normals, view_cam, view_depth, depth_samples,
                       outer_count_threshold, center_ratio, plane_fill_ratio,
                       angle_sum_threshold, inner_count_threshold):
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

    candidate_planes = []

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
        inner_count = int(np.sum(in_full_view & in_center))

        if outer_count <= outer_count_threshold:
            continue
        if inner_count >= inner_count_threshold:
            continue

        candidate_planes.append((outer_count, float(depth), slice_points[in_outer_ring]))

    if len(candidate_planes) == 0:
        return np.empty((0, 3), dtype=np.float32), np.empty((0, 3), dtype=np.float32), np.empty((0, 3), dtype=np.float32)

    world_to_camera = np.eye(4, dtype=np.float32)
    world_to_camera[:3, :3] = world_to_camera_rot
    world_to_camera[:3, 3] = world_to_camera_t
    camera_to_world = np.linalg.inv(world_to_camera)

    fill_world_points_list = []
    candidate_planes = sorted(candidate_planes, key=lambda x: x[0], reverse=True)[:5]
    for chosen_outer_count, chosen_depth, chosen_outer_points_cam in candidate_planes:
        ox = chosen_outer_points_cam[:, 0]
        oy = chosen_outer_points_cam[:, 1]
        oz = chosen_outer_points_cam[:, 2]
        pitch_mean = float(np.mean(np.degrees(np.arctan2(oy, oz))))
        yaw_mean = float(np.mean(np.degrees(np.arctan2(ox, oz))))

        angle_means = np.array([pitch_mean, yaw_mean], dtype=np.float32)
        if np.any(np.abs(angle_means) > angle_sum_threshold):
            print(
                f"Planefill3 skip {view_cam.image_name}: "
                f"depth={chosen_depth:.2f}, pitch_mean={pitch_mean:.2f}, yaw_mean={yaw_mean:.2f}, "
                f"outer_count={chosen_outer_count}, inner_count_threshold={inner_count_threshold}"
            )
            continue

        fill_depths = [
            chosen_depth - half_depth_window,
            chosen_depth,
            chosen_depth + half_depth_window,
        ]
        fill_cam_points_list = []
        for fill_depth in fill_depths:
            if fill_depth <= 0.0:
                continue

            full_half_width = fill_depth * tan_half_fovx
            full_half_height = fill_depth * tan_half_fovy
            fill_step_x = max(full_half_width * 2.0 * plane_fill_ratio, 1e-6)
            fill_step_y = max(full_half_height * 2.0 * plane_fill_ratio, 1e-6)

            fill_x = np.arange(-full_half_width, full_half_width + fill_step_x * 0.5, fill_step_x, dtype=np.float32)
            fill_y = np.arange(-full_half_height, full_half_height + fill_step_y * 0.5, fill_step_y, dtype=np.float32)
            yy, xx = np.meshgrid(fill_y, fill_x, indexing="ij")
            zz = np.full_like(xx, fill_depth, dtype=np.float32)
            fill_cam_points_list.append(np.stack([xx, yy, zz], axis=-1).reshape(-1, 3))

        if len(fill_cam_points_list) == 0:
            continue

        fill_cam_points = np.concatenate(fill_cam_points_list, axis=0)
        fill_cam_points_h = np.concatenate([
            fill_cam_points,
            np.ones((fill_cam_points.shape[0], 1), dtype=np.float32)
        ], axis=1)
        fill_world_points_list.append((camera_to_world @ fill_cam_points_h.T).T[:, :3])

    if len(fill_world_points_list) == 0:
        return np.empty((0, 3), dtype=np.float32), np.empty((0, 3), dtype=np.float32), np.empty((0, 3), dtype=np.float32)

    fill_world_points = np.concatenate(fill_world_points_list, axis=0)
    fill_colors = np.tile([0.0, 0.0, 1.0], (fill_world_points.shape[0], 1))
    fill_normals = np.zeros_like(fill_world_points)
    return fill_world_points, fill_colors, fill_normals

def Planefill3(points, colors, normals, cam_infos, view_depth, depth_samples,
               outer_count_threshold, center_ratio, plane_fill_ratio,
               angle_sum_threshold, inner_count_threshold): 
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
            inner_count_threshold=inner_count_threshold 
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
        # radius 按场景对角线长度（用 1%-99% 分位数估计，避免飘远的杂乱点把尺度撑大）的 1% 自动计算
        pcd_o3d = o3d.geometry.PointCloud()
        pcd_o3d.points = o3d.utility.Vector3dVector(points)
        pcd_o3d.colors = o3d.utility.Vector3dVector(colors)
        p_low = np.percentile(points, 1, axis=0)
        p_high = np.percentile(points, 99, axis=0)
        scene_diag = float(np.linalg.norm(p_high - p_low))
        radius = scene_diag * 0.01
        print(f"scene diagonal (1-99 percentile): {scene_diag:.3f}, outlier radius: {radius:.3f}")
        pcd_clean, _ = pcd_o3d.remove_radius_outlier(nb_points=30, radius=radius)
        print(f"radius outlier 去除后点数: {len(pcd_clean.points)} points")

        # remove_statistical_outlier: 每个点到最近 nb_neighbors 个邻居的平均距离，
        # 若超过 全局均值 + std_ratio*标准差 则视为离群点删除，能滤掉主体点云外围
        # 整体飘远但内部略微聚集的杂乱点簇
        pcd_clean, _ = pcd_clean.remove_statistical_outlier(nb_neighbors=30, std_ratio=2.0)
        points = np.asarray(pcd_clean.points)
        colors = np.asarray(pcd_clean.colors)
        normals = np.zeros_like(points)
        print(f"离群点去除后点数: {points.shape[0]} points")

        if args.fill_method == "planefill":
            points, colors, normals = Planefill3(
                        points, colors, normals, scene_info.train_cameras,
                        view_depth=args.Planefill3_view_depth,
                        depth_samples=200,
                        outer_count_threshold=args.Planefill3_outer_count_threshold,
                        center_ratio=0.5,
                        plane_fill_ratio=args.plane_fill_ratio,
                        angle_sum_threshold=args.Planefill3_angle_sum_threshold,
                        inner_count_threshold=args.inner_count_threshold
                    )
        elif args.fill_method == "simplefill":
            trajectory_up_axis = None
            if args.trajectory_root:
                trajectory_up_axis = _trajectory_up_axis(scene_info.train_cameras)
                if trajectory_up_axis is None:
                    print("trajectory_root 启用失败: 训练相机数量少于 3，仍使用点云 PCA 的 z 轴")
                else:
                    print(f"trajectory_root z/up axis: {trajectory_up_axis}")
            points, colors, normals = Simplyfill2(
                points, colors, normals,
                grid_resX=args.fill_grid_resX,
                grid_resY=args.fill_grid_resY,
                grid_resZ=args.fill_grid_resZ,
                up_axis=trajectory_up_axis
            )
        else:
            raise ValueError(f"Unknown fill_method: {args.fill_method}")
        input_filled_ply_path = os.path.join(self.model_path, "input_filled.ply")
        storePly(input_filled_ply_path, points, colors * 255.0)
        print(f"wrote input_filled.ply: {input_filled_ply_path}")
        print(f"增加平面后点数: {points.shape[0]} points")

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
