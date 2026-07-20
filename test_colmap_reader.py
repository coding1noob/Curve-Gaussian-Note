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
    print("\nCOLMAP read summary")
    print(f"train cameras: {len(scene_info.train_cameras)}")
    print(f"test cameras:  {len(scene_info.test_cameras)}")
    print(f"ply path:      {scene_info.ply_path}")
    # 最远相机中心到平均相机中心的距离
    print(f"nerf radius:   {scene_info.nerf_normalization['radius']}")

    if pcd is None:
        print("point cloud:   None")
        return

    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    normals = np.asarray(pcd.normals)
    print(f"colmap得到点数:   {points.shape[0]}")
    print(f"points shape:  {points.shape}")
    print(f"colors shape:  {colors.shape}")
    # 存的全是0
    print(f"normals shape: {normals.shape}")
    if points.shape[0] > 0:
        # 计算点云的边界框
        print(f"xyz min:       {points.min(axis=0)}")
        print(f"xyz max:       {points.max(axis=0)}")
        print(f"first point:   {points[0]}")
        print(f"first color:   {colors[0] if colors.shape[0] else 'None'}")

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
        points, colors, normals = Simplyfill(points, colors, normals, grid_resX=50, grid_resY=50, grid_resZ=20)
        input_filled_ply_path = os.path.join(model_path, "input_filled.ply")
        storePly(input_filled_ply_path, points, colors * 255.0)
        print(f"wrote input_filled.ply: {input_filled_ply_path}")
        print(f"填充点云后点数: {points.shape[0]} points")


if __name__ == "__main__":
    main()
