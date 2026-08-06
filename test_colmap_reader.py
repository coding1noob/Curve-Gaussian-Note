import argparse
import os
import sys

root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import numpy as np
import open3d as o3d
from scipy.spatial import ConvexHull, cKDTree

from scene.dataset_readers import readColmapSceneInfo, storePly

# PCA（主成分分析）是一种数学方法，找到数据分布的主要方向（方差最大的轴）

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
    # 求点云质心（几何中心），后面所有坐标都以它为原点
    centroid = points.mean(axis=0)
    # 把点云平移到原点，SVD/PCA 要求数据是零均值的
    centered = points - centroid
    if up_axis is None:
        # SVD 分解：Vt 的每一行是一个主轴方向，按方差从大到小排列
        # Vt[0] = 方差最大的方向，Vt[2] = 方差最小的方向
        _, _, Vt = np.linalg.svd(centered, full_matrices=False)
        # 假设：房间/走廊的“高度”方向方差最小（人在走廊里，天花板到地板的起伏）分布得"聚拢"、跨度小
        # 远小于沿走廊走、左右张望时的位置变化），所以拿 Vt[2] 近似当“上”方向
        # e1, e2 是另外两个方差较大的方向，它们和 up_axis 互相垂直，张成一个水平面
        e1, e2, up_axis = Vt[0], Vt[1], Vt[2]
    else:
        # 轨迹模式：人在同一平面移动拍摄时，相机中心变化最小的方向更接近真实“上”方向
        up_axis = np.asarray(up_axis, dtype=np.float64)
        up_axis = up_axis / max(np.linalg.norm(up_axis), 1e-12)
        projected = centered - (centered @ up_axis)[:, None] * up_axis[None, :]
        _, _, Vt_plane = np.linalg.svd(projected, full_matrices=False)
        e1 = Vt_plane[0]
        e1 = e1 - np.dot(e1, up_axis) * up_axis
        e1 = e1 / max(np.linalg.norm(e1), 1e-12)
        e2 = np.cross(up_axis, e1)
        e2 = e2 / max(np.linalg.norm(e2), 1e-12)

    # 把每个 3D 点投影到 (e1, e2) 水平面上，变成 2D 点，接下来只在这个平面里找方向
    pts2d = np.stack([centered @ e1, centered @ e2], axis=1)

    # 求这些 2D 点的凸包（能把所有点包起来的最小多边形），
    # 最小面积包围矩形必然有一条边和凸包的某条边重合，所以只需要遍历凸包的边即可
    hull = ConvexHull(pts2d)
    # 取出凸包顶点坐标，按顺序排列成多边形
    hull_pts = pts2d[hull.vertices]
    # 凸包顶点个数
    n = len(hull_pts)

    # 记录当前找到的最小矩形面积和对应的旋转角度
    best_area = np.inf
    best_angle = 0.0
    # 遍历凸包每一条边
    for i in range(n):
        # 当前边的方向向量（从顶点 i 指向下一个顶点）
        edge = hull_pts[(i + 1) % n] - hull_pts[i]
        # 这条边相对于 x 轴的角度
        angle = np.arctan2(edge[1], edge[0])
        c, s = np.cos(angle), np.sin(angle)
        # 构造旋转矩阵：把整个点集旋转 -angle，使这条边转到和 x 轴平行
        rot = np.array([[c, -s], [s, c]])
        # 旋转后的所有凸包点坐标
        rotated = hull_pts @ rot
        # 旋转后，用轴对齐的方式量出包围这条边方向的矩形的宽
        w = rotated[:, 0].max() - rotated[:, 0].min()
        # 和高
        h = rotated[:, 1].max() - rotated[:, 1].min()
        # 这个角度下轴对齐矩形的面积，即“沿这条边方向摆放”的包围矩形面积
        area = w * h
        # 保留目前遇到的最小面积及其角度
        if area < best_area:
            best_area = area
            best_angle = angle

    # 用最优角度重新算出这个矩形的两条边方向（在 e1,e2 平面内的 2D 单位向量）
    c, s = np.cos(best_angle), np.sin(best_angle)
    u2d, v2d = np.array([c, s]), np.array([-s, c])
    # 把这两条 2D 方向映射回 3D 空间（因为 pts2d 只是 e1,e2 平面上的坐标）
    u3d = u2d[0] * e1 + u2d[1] * e2
    v3d = v2d[0] * e1 + v2d[1] * e2

    # 分别算出点云沿 u3d 和 v3d 方向的跨度（矩形的两条边长）
    w = (pts2d @ u2d).max() - (pts2d @ u2d).min()
    h = (pts2d @ v2d).max() - (pts2d @ v2d).min()
    # 谁的跨度大就是“长边”，定义为 axis0（走廊延伸方向/房间长边）；短边为 axis1
    axis0, axis1 = (u3d, v3d) if w >= h else (v3d, u3d)

    # 把最终的三个正交方向按 (长边, 短边, 上) 顺序打包成一个 3x3 旋转矩阵
    Vt_final = np.stack([axis0, axis1, up_axis], axis=0)
    # 返回质心（用于后续把点云搬回原点）和这个旋转矩阵（用于把点云转到“对齐”坐标系）
    return centroid, Vt_final

def Simplyfill(points, colors, normals, grid_resX=50, grid_resY=50, grid_resZ=50, up_axis=None):
    # 和 Simplyfill2 使用同一套贴合场景的坐标系，但不做分段过滤，直接填满整个局部 bounding box
    clean_centroid, Vt = _min_area_rect_basis(points, up_axis=up_axis)
    centered = points - clean_centroid
    pts_pca = centered @ Vt.T

    pca_min = pts_pca.min(axis=0)
    pca_max = pts_pca.max(axis=0)

    xs = np.linspace(pca_min[0], pca_max[0], grid_resX)
    ys = np.linspace(pca_min[1], pca_max[1], grid_resY)
    zs = np.linspace(pca_min[2], pca_max[2], grid_resZ)

    gx, gy, gz = np.meshgrid(xs, ys, zs)
    grid_pca = np.stack([gx.ravel(), gy.ravel(), gz.ravel()], axis=1).astype(np.float32)
    grid_pts = grid_pca @ Vt + clean_centroid

    new_points  = np.vstack([points, grid_pts])
    new_colors  = np.vstack([colors,  np.tile([1.0, 0.0, 0.0], (len(grid_pts), 1)) ])   # 红色
    new_normals = np.vstack([normals, np.zeros((len(grid_pts), 3))])
    return new_points, new_colors, new_normals

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


def Planefill3(points, colors, normals, view_cam, view_depth, depth_samples,
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
        return points, colors, normals, np.empty((0, 3), dtype=np.float32), [], []

    world_to_camera = np.eye(4, dtype=np.float32)
    world_to_camera[:3, :3] = world_to_camera_rot
    world_to_camera[:3, 3] = world_to_camera_t
    camera_to_world = np.linalg.inv(world_to_camera)

    fill_world_points_list = []
    valid_fill_depths = []
    fill_outer_counts = []
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
            valid_fill_depths.append(float(fill_depth))
            fill_outer_counts.append(chosen_outer_count)

        if len(fill_cam_points_list) == 0:
            continue

        fill_cam_points = np.concatenate(fill_cam_points_list, axis=0)
        fill_cam_points_h = np.concatenate([
            fill_cam_points,
            np.ones((fill_cam_points.shape[0], 1), dtype=np.float32)
        ], axis=1)
        fill_world_points_list.append((camera_to_world @ fill_cam_points_h.T).T[:, :3])

    if len(fill_world_points_list) == 0:
        return points, colors, normals, np.empty((0, 3), dtype=np.float32), [], []

    fill_world_points = np.concatenate(fill_world_points_list, axis=0)

    fill_colors = np.tile([0.0, 0.0, 1.0], (fill_world_points.shape[0], 1))
    fill_normals = np.zeros_like(fill_world_points)

    new_points = np.vstack([points, fill_world_points])
    new_colors = np.vstack([colors, fill_colors])
    new_normals = np.vstack([normals, fill_normals])
    return new_points, new_colors, new_normals, fill_world_points, valid_fill_depths, fill_outer_counts

def main():
    parser = argparse.ArgumentParser(description="Test COLMAP-format scene loading without training.")
    parser.add_argument("-s", "--source_path", required=True, help="Path to the COLMAP-format dataset root.")
    parser.add_argument("--images", default="images", help="Image folder name relative to source_path.")
    parser.add_argument("--depths", default="", help="Depth folder name relative to source_path, if used.")
    parser.add_argument("--eval", action="store_true", help="Use eval camera split logic.")
    parser.add_argument("--train_test_exp", action="store_true", help="Pass train_test_exp flag through to reader.")
    parser.add_argument("--detector", default="PidiNet", choices=["PidiNet", "DexiNed"], help="Edge detector folder to read.")
    parser.add_argument("--llffhold", type=int, default=8, help="LLFF holdout interval when --eval is used.")
    # colmap点降采样
    parser.add_argument("--init_voxel_size", type=float, default=0.0, help="Voxel size for optional initial point cloud downsampling.")
    parser.add_argument("-m", "--model_path", default=None, help="Optional output directory for writing input.ply.")
    parser.add_argument("--method", type=int, default=0, help="Optional method for add points in .ply.")
    parser.add_argument("--trajectory_root", action="store_true",
                        help="Use the least-variance axis of the camera trajectory as the z/up axis for Simplyfill2.")
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

    if pcd is None:
        print("point cloud:   None")
        return

    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    normals = np.asarray(pcd.normals)
    print(f"colmap得到点数:   {points.shape[0]}")

    if args.model_path:
        model_path = os.path.abspath(os.path.expanduser(args.model_path))
        os.makedirs(model_path, exist_ok=True)
        input_ply_path = os.path.join(model_path, "input.ply")
        storePly(input_ply_path, points, colors * 255.0)
        print(f"wrote input.ply: {input_ply_path}")

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
        pcd_clean, _ = pcd_o3d.remove_radius_outlier(nb_points=180, radius=radius)      # nb_points=180
        print(f"radius outlier 去除后点数: {len(pcd_clean.points)} points")

        # remove_statistical_outlier: 每个点到最近 nb_neighbors 个邻居的平均距离，
        # 若超过 全局均值 + std_ratio*标准差 则视为离群点删除，能滤掉主体点云外围
        # 整体飘远但内部略微聚集的杂乱点簇
        pcd_clean, _ = pcd_clean.remove_statistical_outlier(nb_neighbors=30, std_ratio=2.0)
        points = np.asarray(pcd_clean.points)
        colors = np.asarray(pcd_clean.colors)
        normals = np.zeros_like(points)
        print(f"离群点去除后点数: {points.shape[0]} points")

        # 遍历所有训练相机
        if len(scene_info.train_cameras) > 0:
            base_points = points
            base_colors = colors
            base_normals = normals

            fill_points_list = []
            fill_colors_list = []

            input_planefilled_ply_path = os.path.join(model_path, "input_planefilled123.ply")

            # ============ 无脑补平面点 ==============
            if args.method == 0:
                trajectory_up_axis = None
                if args.trajectory_root:
                    trajectory_up_axis = _trajectory_up_axis(scene_info.train_cameras)
                    if trajectory_up_axis is None:
                        print("trajectory_root 启用失败: 训练相机数量少于 3，仍使用点云 PCA 的 z 轴")
                    else:
                        print(f"trajectory_root z/up axis: {trajectory_up_axis}")
                # grid_resA，grid_resB，grid_resC 分别是沿长轴方向、宽度方向、高度方向的网格分辨率
                points, colors, normals = Simplyfill2(points, colors, normals, grid_resX=100, grid_resY=100, grid_resZ=100,
                                                      up_axis=trajectory_up_axis)
                input_filled_ply_path = os.path.join(model_path, "input_filled.ply")
                storePly(input_filled_ply_path, points, colors * 255.0)
                print(f"wrote input_filled.ply: {input_filled_ply_path}")
                print(f"填充点云后点数: {points.shape[0]} points")

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
            if args.method == 2:
                planefill3_points_count = 0
                planefill3_depths = []
                for cam_idx, view_cam in enumerate(scene_info.train_cameras):
                    _, _, _, plane_points, filled_depths, outer_counts = Planefill3(
                        base_points, base_colors, base_normals, view_cam,
                        view_depth=5.0,            # buaa_net2 是 20.0， buaa_net 是 5.0
                        depth_samples=200,
                        outer_count_threshold=70,
                        center_ratio=0.5,
                        plane_fill_ratio=0.05,
                        angle_sum_threshold=15.0,
                        inner_count_threshold=5
                    )
                    if plane_points.shape[0] == 0:
                        continue
                    fill_points_list.append(plane_points)
                    fill_colors_list.append(np.tile([1.0, 0.0, 0.0], (plane_points.shape[0], 1)))
                    planefill3_points_count += plane_points.shape[0]
                    planefill3_depths.extend(filled_depths)

                print(f"3方法补red点")
                print(f"Planefill3 points: {planefill3_points_count} points")
                print(f"Planefill3 filled plane layers: {len(planefill3_depths)} / {len(scene_info.train_cameras) * 5 * 3}")

            # ============ 用 Planefill4 基于 Planefill3 候选面向四边扩张补黄色点 ==============
            # planefill4_points_count = 0
            # planefill4_depths = []
            # for cam_idx, view_cam in enumerate(scene_info.train_cameras):
            #     _, _, _, plane_points, filled_depths, outer_counts = Planefill4(
            #         base_points, base_colors, base_normals, view_cam,
            #         view_depth=5.0,            # buaa_net2 是 20.0， buaa_net 是 5.0
            #         depth_samples=200,
            #         outer_count_threshold=70,
            #         center_ratio=0.5,
            #         plane_fill_ratio=0.02,
            #         angle_sum_threshold=10.0,
            #         inner_count_threshold=50
            #     )
            #     if plane_points.shape[0] == 0:
            #         continue
            #     fill_points_list.append(plane_points)
            #     fill_colors_list.append(np.tile([1.0, 1.0, 0.0], (plane_points.shape[0], 1)))
            #     planefill4_points_count += plane_points.shape[0]
            #     planefill4_depths.extend(filled_depths)

            # print(f"4方法扩张补yellow点")
            # print(f"Planefill4 points: {planefill4_points_count} points")
            # print(f"Planefill4 expanded planes: {len(planefill4_depths)}")


            # # 最终转化输出
            # if len(fill_points_list) > 0:
            #     plane_points = np.concatenate(fill_points_list, axis=0)
            #     plane_colors = np.concatenate(fill_colors_list, axis=0)
            #     plane_normals = np.zeros_like(plane_points)
            #     points = np.vstack([base_points, plane_points])
            #     colors = np.vstack([base_colors, plane_colors])
            #     normals = np.vstack([base_normals, plane_normals])
            # else:
            #     plane_points = np.empty((0, 3), dtype=np.float32)

            # storePly(input_planefilled_ply_path, points, colors * 255.0)

if __name__ == "__main__":
    main()
