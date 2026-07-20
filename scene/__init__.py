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
        points, colors, normals = Simplyfill(points, colors, normals, grid_resX=50, grid_resY=50, grid_resZ=20)
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
