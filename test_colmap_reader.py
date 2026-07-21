import argparse
import os
import sys

root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import numpy as np
import open3d as o3d

from scene.dataset_readers import readColmapSceneInfo, storePly

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


def Planefill(points, colors, normals, view_cam, view_depth=20.0, depth_samples=200,
              outer_count_threshold=500, center_ratio=0.5, plane_fill_ratio=0.1):
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

    if chosen_depth is None:
        return points, colors, normals, np.empty((0, 3), dtype=np.float32), [], []

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

    fill_colors = np.tile([1.0, 0.0, 0.0], (fill_world_points.shape[0], 1))
    fill_normals = np.zeros_like(fill_world_points)

    new_points = np.vstack([points, fill_world_points])
    new_colors = np.vstack([colors, fill_colors])
    new_normals = np.vstack([normals, fill_normals])
    return new_points, new_colors, new_normals, fill_world_points, [chosen_depth], [chosen_outer_count]

def Planefill2(points, colors, normals, view_cam, view_depth=20.0, depth_samples=200,
               outer_count_threshold=500, center_ratio=0.5, plane_fill_ratio=0.1,
               ransac_distance_threshold=0.05, ransac_min_inliers=50,
               ransac_num_iterations=1000):
    depth_step = view_depth / depth_samples
    half_depth_window = depth_step * 0.5
    sample_depths = np.linspace(depth_step, view_depth, depth_samples, dtype=np.float32)

    world_to_camera_rot = view_cam.R.transpose().astype(np.float32)
    world_to_camera_t = view_cam.T.astype(np.float32)
    world_to_camera = np.eye(4, dtype=np.float32)
    world_to_camera[:3, :3] = world_to_camera_rot
    world_to_camera[:3, 3] = world_to_camera_t
    camera_to_world = np.linalg.inv(world_to_camera)
    camera_center = camera_to_world[:3, 3]
    camera_to_world_rot = camera_to_world[:3, :3]

    points_world = points.astype(np.float32)
    points_cam = points_world @ world_to_camera_rot.T + world_to_camera_t

    z = points_cam[:, 2]
    valid_depth = (z > 0.0) & (z <= view_depth + half_depth_window)
    points_cam = points_cam[valid_depth]
    points_world = points_world[valid_depth]
    z = points_cam[:, 2]

    tan_half_fovx = np.tan(view_cam.FovX * 0.5)
    tan_half_fovy = np.tan(view_cam.FovY * 0.5)

    chosen_depth = None
    chosen_outer_count = None
    chosen_plane_model = None

    for depth in sample_depths:
        depth_mask = np.abs(z - depth) <= half_depth_window
        if not np.any(depth_mask):
            continue

        slice_points_cam = points_cam[depth_mask]
        slice_points_world = points_world[depth_mask]
        slice_z = slice_points_cam[:, 2]
        proj_x = slice_points_cam[:, 0] / slice_z
        proj_y = slice_points_cam[:, 1] / slice_z

        in_full_view = (np.abs(proj_x) <= tan_half_fovx) & (np.abs(proj_y) <= tan_half_fovy)
        in_center = (
            (np.abs(proj_x) <= tan_half_fovx * center_ratio) &
            (np.abs(proj_y) <= tan_half_fovy * center_ratio)
        )
        in_outer_ring = in_full_view & (~in_center)
        outer_count = int(np.sum(in_outer_ring))

        if outer_count <= outer_count_threshold:
            continue

        outer_points_world = slice_points_world[in_outer_ring]
        if outer_points_world.shape[0] < max(3, ransac_min_inliers):
            continue

        outer_pcd = o3d.geometry.PointCloud()
        outer_pcd.points = o3d.utility.Vector3dVector(outer_points_world)
        plane_model, inliers = outer_pcd.segment_plane(
            distance_threshold=ransac_distance_threshold,
            ransac_n=3,
            num_iterations=ransac_num_iterations,
        )

        if len(inliers) < ransac_min_inliers:
            continue

        chosen_depth = float(depth)
        chosen_outer_count = outer_count
        chosen_plane_model = np.asarray(plane_model, dtype=np.float32)

    if chosen_plane_model is None:
        return points, colors, normals, np.empty((0, 3), dtype=np.float32), [], []

    ray_count = max(2, int(np.ceil(1.0 / plane_fill_ratio)) + 1)
    u_vals = np.linspace(-center_ratio, center_ratio, ray_count, dtype=np.float32)
    v_vals = np.linspace(-center_ratio, center_ratio, ray_count, dtype=np.float32)
    vv, uu = np.meshgrid(v_vals, u_vals, indexing="ij")

    ray_dirs_cam = np.stack([
        uu * tan_half_fovx,
        vv * tan_half_fovy,
        np.ones_like(uu),
    ], axis=-1).reshape(-1, 3)
    ray_dirs_world = ray_dirs_cam @ camera_to_world_rot.T

    plane_normal = chosen_plane_model[:3]
    plane_d = chosen_plane_model[3]
    denom = ray_dirs_world @ plane_normal
    numer = -(camera_center @ plane_normal + plane_d)
    valid_rays = np.abs(denom) > 1e-6
    t_vals = np.zeros_like(denom, dtype=np.float32)
    t_vals[valid_rays] = numer / denom[valid_rays]
    valid_rays &= t_vals > 0.0

    fill_world_points = camera_center[None, :] + t_vals[:, None] * ray_dirs_world
    fill_points_cam = fill_world_points @ world_to_camera_rot.T + world_to_camera_t
    valid_rays &= (fill_points_cam[:, 2] > 0.0) & (fill_points_cam[:, 2] <= view_depth + half_depth_window)
    fill_world_points = fill_world_points[valid_rays]

    if fill_world_points.shape[0] == 0:
        return points, colors, normals, np.empty((0, 3), dtype=np.float32), [], []

    fill_colors = np.tile([0.0, 1.0, 0.0], (fill_world_points.shape[0], 1))
    fill_normals = np.zeros_like(fill_world_points)

    new_points = np.vstack([points, fill_world_points])
    new_colors = np.vstack([colors, fill_colors])
    new_normals = np.vstack([normals, fill_normals])
    return new_points, new_colors, new_normals, fill_world_points, [chosen_depth], [chosen_outer_count]


def Planefill3(points, colors, normals, view_cam, view_depth=20.0, depth_samples=200,
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
        return points, colors, normals, np.empty((0, 3), dtype=np.float32), [], []

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
        return points, colors, normals, np.empty((0, 3), dtype=np.float32), [], []

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

    new_points = np.vstack([points, fill_world_points])
    new_colors = np.vstack([colors, fill_colors])
    new_normals = np.vstack([normals, fill_normals])
    return new_points, new_colors, new_normals, fill_world_points, [chosen_depth], [chosen_outer_count]

def main():
    parser = argparse.ArgumentParser(description="Test COLMAP-format scene loading without training.")
    parser.add_argument("-s", "--source_path", required=True, help="Path to the COLMAP-format dataset root.")
    parser.add_argument("--images", default="images", help="Image folder name relative to source_path.")
    parser.add_argument("--depths", default="", help="Depth folder name relative to source_path, if used.")
    parser.add_argument("--eval", action="store_true", help="Use eval camera split logic.")
    parser.add_argument("--train_test_exp", action="store_true", help="Pass train_test_exp flag through to reader.")
    parser.add_argument("--detector", default="PidiNet", choices=["PidiNet", "DexiNed"], help="Edge detector folder to read.")
    parser.add_argument("--llffhold", type=int, default=8, help="LLFF holdout interval when --eval is used.")
    parser.add_argument("--init_voxel_size", type=float, default=0.0, help="Voxel size for optional initial point cloud downsampling.")
    parser.add_argument("-m", "--model_path", default=None, help="Optional output directory for writing input.ply.")
    args = parser.parse_args()

    source_path = os.path.abspath(os.path.expanduser(args.source_path))
    print(f"Reading COLMAP scene: {source_path}")
    print(f"images={args.images}, detector={args.detector}, eval={args.eval}, init_voxel_size={args.init_voxel_size}")

    scene_info = readColmapSceneInfo(
        path=source_path,
        images=args.images,
        depths=args.depths,
        eval=args.eval,
        train_test_exp=args.train_test_exp,
        llffhold=args.llffhold,
        detector=args.detector,
        init_voxel_size=args.init_voxel_size,
    )

    pcd = scene_info.point_cloud
    print("\nCOLMAP 读取点云信息:")
    # print(f"train cameras: {len(scene_info.train_cameras)}")
    # print(f"test cameras:  {len(scene_info.test_cameras)}")
    # print(f"ply path:      {scene_info.ply_path}")
    # 最远相机中心到平均相机中心的距离
    # print(f"nerf radius:   {scene_info.nerf_normalization['radius']}")

    if pcd is None:
        print("point cloud:   None")
        return

    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    normals = np.asarray(pcd.normals)
    print(f"colmap得到点数:   {points.shape[0]}")
    if points.shape[0] > 0:
        # 计算点云的边界框
        print(f"xyz min:       {points.min(axis=0)}")
        print(f"xyz max:       {points.max(axis=0)}")

    if args.model_path:
        model_path = os.path.abspath(os.path.expanduser(args.model_path))
        os.makedirs(model_path, exist_ok=True)
        input_ply_path = os.path.join(model_path, "input.ply")
        storePly(input_ply_path, points, colors * 255.0)
        print(f"wrote input.ply: {input_ply_path}")

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
        # input_filled_ply_path = os.path.join(model_path, "input_filled.ply")
        # storePly(input_filled_ply_path, points, colors * 255.0)
        # print(f"wrote input_filled.ply: {input_filled_ply_path}")
        # print(f"填充点云后点数: {points.shape[0]} points")

        # 遍历所有训练相机
        if len(scene_info.train_cameras) > 0:
            base_points = points
            base_colors = colors
            base_normals = normals

            fill_points_list = []
            fill_colors_list = []

            input_planefilled_ply_path = os.path.join(model_path, "input_planefilled123.ply")

            # ============ 用 Planefill 补平面点 ==============
            # planefill_points_count = 0
            # planefill_depths = []
            # for cam_idx, view_cam in enumerate(scene_info.train_cameras):
            #     _, _, _, plane_points, filled_depths, outer_counts = Planefill(
            #         base_points, base_colors, base_normals, view_cam,
            #         view_depth=20.0,
            #         depth_samples=200,
            #         outer_count_threshold=70,
            #         center_ratio=0.5,
            #         plane_fill_ratio=0.05
            #     )
            #     if plane_points.shape[0] == 0:
            #         continue
            #     fill_points_list.append(plane_points)
            #     fill_colors_list.append(np.tile([1.0, 1.0, 1.0], (plane_points.shape[0], 1)))
            #     planefill_points_count += plane_points.shape[0]
            #     planefill_depths.extend(filled_depths)

            # print(f"原始方法补white点")
            # print(f"Planefill points: {planefill_points_count} points")
            # print(f"Planefill filled farthest depth slices: {len(planefill_depths)} / {len(scene_info.train_cameras)}")

            # # ============ 用 Planefill2 补平面点 ==============
            # planefill2_points_count = 0
            # planefill2_depths = []
            # for cam_idx, view_cam in enumerate(scene_info.train_cameras):
            #     _, _, _, plane_points, filled_depths, outer_counts = Planefill2(
            #         base_points, base_colors, base_normals, view_cam,
            #         view_depth=20.0,
            #         depth_samples=200,
            #         outer_count_threshold=70,
            #         center_ratio=0.5,
            #         plane_fill_ratio=0.05,
            #         ransac_distance_threshold=0.05,
            #         ransac_min_inliers=50,
            #         ransac_num_iterations=1000,
            #     )
            #     if plane_points.shape[0] == 0:
            #         continue
            #     fill_points_list.append(plane_points)
            #     fill_colors_list.append(np.tile([0.0, 1.0, 0.0], (plane_points.shape[0], 1)))
            #     planefill2_points_count += plane_points.shape[0]
            #     planefill2_depths.extend(filled_depths)

            # print(f"2方法补green点")
            # print(f"Planefill2 points: {planefill2_points_count} points")
            # print(f"Planefill2 filled farthest depth slices: {len(planefill2_depths)} / {len(scene_info.train_cameras)}")

            # ============ 用 Planefill3 补平面点，默认只补墙面（角度和小于 15° 的相机） ==============
            planefill3_points_count = 0
            planefill3_depths = []
            for cam_idx, view_cam in enumerate(scene_info.train_cameras):
                _, _, _, plane_points, filled_depths, outer_counts = Planefill3(
                    base_points, base_colors, base_normals, view_cam,
                    view_depth=20.0,            # buaa_net2 是 20.0， buaa_net 是 5.0
                    depth_samples=200,
                    outer_count_threshold=70,
                    center_ratio=0.5,
                    plane_fill_ratio=0.05,
                    angle_sum_threshold=15.0,
                )
                if plane_points.shape[0] == 0:
                    continue
                fill_points_list.append(plane_points)
                fill_colors_list.append(np.tile([1.0, 0.0, 0.0], (plane_points.shape[0], 1)))
                planefill3_points_count += plane_points.shape[0]
                planefill3_depths.extend(filled_depths)

            print(f"3方法补red点")
            print(f"Planefill3 points: {planefill3_points_count} points")
            print(f"Planefill3 filled farthest depth slices: {len(planefill3_depths)} / {len(scene_info.train_cameras)}")


            # 最终转化输出
            if len(fill_points_list) > 0:
                plane_points = np.concatenate(fill_points_list, axis=0)
                plane_colors = np.concatenate(fill_colors_list, axis=0)
                plane_normals = np.zeros_like(plane_points)
                points = np.vstack([base_points, plane_points])
                colors = np.vstack([base_colors, plane_colors])
                normals = np.vstack([base_normals, plane_normals])
            else:
                plane_points = np.empty((0, 3), dtype=np.float32)

            storePly(input_planefilled_ply_path, points, colors * 255.0)

if __name__ == "__main__":
    main()
