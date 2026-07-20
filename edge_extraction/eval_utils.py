import os
import numpy as np
import json
import point_cloud_utils as pcu
import math
import random
from pathlib import Path
import sys
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
from utils.vis_utils import get_fancy_color
import torch
from tqdm import tqdm

import matplotlib.pyplot as plt

def visualize_pred_gt(all_pred_points, all_gt_points, pred_colors,
                      name, save_fig=False, show_fig=True, vis_dir='./', gt_points_color=None,
                      azim=60, elev=60, roll=0):
    range_size = [0, 1]
    # 绘制并保存Prediction散点图
    fig_pred = plt.figure(dpi=120)
    ax_pred = fig_pred.add_subplot(projection='3d')
    x_pred = [k[0] for k in all_pred_points]
    y_pred = [k[1] for k in all_pred_points]
    z_pred = [k[2] for k in all_pred_points]
    ax_pred.scatter(x_pred, y_pred, z_pred, c=pred_colors, marker='o', s=0.5, linewidth=1, alpha=1, cmap='spectral')
    ax_pred.view_init(azim=azim, elev=elev, roll=roll)
    ax_pred.set_zlim3d(range_size[0], range_size[1])
    # plt.axis([range_size[0], range_size[1], range_size[0], range_size[1], range_size[0], range_size[1]])
    ax_pred.set_xlim([range_size[0], range_size[1]])
    ax_pred.set_ylim([range_size[0], range_size[1]])
    ax_pred.set_zlim([range_size[0], range_size[1]])
    plt.axis('off')
    if save_fig:
        plt.savefig(os.path.join(vis_dir, name + "_pred.png"), bbox_inches='tight', dpi=300)
    if show_fig:
        plt.show()
    plt.close(fig_pred)  # 关闭Prediction图

    # 绘制并保存Ground Truth散点图
    fig_gt = plt.figure(dpi=120)
    ax_gt = fig_gt.add_subplot(projection='3d')
    x_gt = [k[0] for k in all_gt_points]
    y_gt = [k[1] for k in all_gt_points]
    z_gt = [k[2] for k in all_gt_points]
    if gt_points_color is None:
        ax_gt.scatter(x_gt, y_gt, z_gt, c='g', marker='o', s=0.5, linewidth=1, alpha=1, cmap='spectral')
    else:
        ax_gt.scatter(x_gt, y_gt, z_gt, c=gt_points_color, marker='o', s=0.5, linewidth=1, alpha=1, cmap='spectral')
    ax_gt.view_init(azim=azim, elev=elev, roll=roll)
    ax_gt.set_zlim3d(range_size[0], range_size[1])
    ax_gt.set_xlim([range_size[0], range_size[1]])
    ax_gt.set_ylim([range_size[0], range_size[1]])
    ax_gt.set_zlim([range_size[0], range_size[1]])
    # plt.axis([range_size[0], range_size[1], range_size[0], range_size[1], range_size[0], range_size[1]])
    plt.axis('off')
    if save_fig:
        plt.savefig(os.path.join(vis_dir, name + "_gt.png"), bbox_inches='tight', dpi=300)
    if show_fig:
        plt.show()
    plt.close(fig_gt)


def set_random_seeds(seed=42):
    np.random.seed(seed)
    random.seed(seed)


def load_from_json(filename: Path):
    """Load a dictionary from a JSON filename."""
    assert filename.suffix == ".json"
    with open(filename, encoding="UTF-8") as file:
        return json.load(file)


def chamfer_distance(x, y, return_index=False, p_norm=2, max_points_per_leaf=10):
    """
    Compute the chamfer distance between two point clouds x, and y

    Args:
        x : A m-sized minibatch of point sets in R^d. i.e. shape [m, n_a, d]
        y : A m-sized minibatch of point sets in R^d. i.e. shape [m, n_b, d]
        return_index: If set to True, will return a pair (corrs_x_to_y, corrs_y_to_x) where
                    corrs_x_to_y[i] stores the index into y of the closest point to x[i]
                    (i.e. y[corrs_x_to_y[i]] is the nearest neighbor to x[i] in y).
                    corrs_y_to_x is similar to corrs_x_to_y but with x and y reversed.
        max_points_per_leaf : The maximum number of points per leaf node in the KD tree used by this function.
                            Default is 10.
        p_norm : Which norm to use. p_norm can be any real number, inf (for the max norm) -inf (for the min norm),
                0 (for sum(x != 0))
    Returns:
        The chamfer distance between x an dy.
        If return_index is set, then this function returns a tuple (chamfer_dist, corrs_x_to_y, corrs_y_to_x) where
        corrs_x_to_y and corrs_y_to_x are described above.
    """

    dists_x_to_y, corrs_x_to_y = pcu.k_nearest_neighbors(
        x, y, k=1, squared_distances=False, max_points_per_leaf=max_points_per_leaf
    )
    dists_y_to_x, corrs_y_to_x = pcu.k_nearest_neighbors(
        y, x, k=1, squared_distances=False, max_points_per_leaf=max_points_per_leaf
    )

    dists_x_to_y = np.linalg.norm(x[corrs_y_to_x] - y, axis=-1, ord=p_norm).mean()
    dists_y_to_x = np.linalg.norm(y[corrs_x_to_y] - x, axis=-1, ord=p_norm).mean()

    Comp = np.mean(dists_x_to_y)
    Acc = np.mean(dists_y_to_x)
    cham_dist = Comp + Acc

    if return_index:
        return cham_dist, corrs_x_to_y, corrs_y_to_x

    return cham_dist, Acc, Comp


def compute_chamfer_distance(pred_sampled, gt_points):
    """
    Compute chamfer distance between predicted and ground truth points.

    Args:
        pred_sampled (numpy.ndarray): Predicted point cloud.
        gt_points (numpy.ndarray): Ground truth points.

    Returns:
        float: Chamfer distance.
    """
    chamfer_dist, acc, comp = chamfer_distance(pred_sampled, gt_points)
    return chamfer_dist, acc, comp


def f_score(precision, recall):
    """
    Compute F-score.

    Args:
        precision (float): Precision.
        recall (float): Recall.

    Returns:
        float: F-score.
    """
    return 2 * precision * recall / (precision + recall)

# 一条曲线的长度可以写成：length = ∫ ||B'(t)|| dt, t from 0 to 1
# 其中：
# B(t)  是 Bezier 曲线位置
# B'(t) 是 Bezier 曲线的一阶导数，也就是切线速度
# ||B'(t)|| 是当前 t 处的速度大小
def bezier_curve_length(control_points, num_samples):
    def binomial_coefficient(n, i):
        return math.factorial(n) // (math.factorial(i) * math.factorial(n - i))

    # 算 B'(t)
    def derivative_bezier(t):
        n = len(control_points) - 1
        point = np.array([0.0, 0.0, 0.0])
        for i, (p1, p2) in enumerate(zip(control_points[:-1], control_points[1:])):
            point += (
                    n
                    * binomial_coefficient(n - 1, i)
                    * (1 - t) ** (n - 1 - i)
                    * t ** i
                    * (np.array(p2) - np.array(p1))
            )
        return point

    # 用 Simpson 积分法估算一小段区间 [a, b] 里的曲线长度
    def simpson_integral(a, b, num_samples):
        h = (b - a) / num_samples
        sum1 = sum(
            np.linalg.norm(derivative_bezier(a + i * h))
            for i in range(1, num_samples, 2)
        )
        sum2 = sum(
            np.linalg.norm(derivative_bezier(a + i * h))
            for i in range(2, num_samples - 1, 2)
        )
        return (
                (
                        np.linalg.norm(derivative_bezier(a))
                        + 4 * sum1
                        + 2 * sum2
                        + np.linalg.norm(derivative_bezier(b))
                )
                * h
                / 3
        )

    # Compute the length of the 3D Bezier curve using composite Simpson's rule
    length = 0.0
    for i in range(num_samples):
        t0 = i / num_samples
        t1 = (i + 1) / num_samples
        length += simpson_integral(t0, t1, num_samples)

    return length


def compute_precision_recall_IOU(
        pred_sampled, gt_points, metrics, thresh_list=[0.02], edge_type="all"
):
    """
    Compute precision, recall, F-score, and IOU.

    Args:
        pred_sampled (numpy.ndarray): Predicted point cloud.
        gt_points (numpy.ndarray): Ground truth points.
        metrics (dict): Dictionary to store metrics.

    Returns:
        dict: Updated metrics.
    """
    if edge_type == "all":
        for thresh in thresh_list:
            dists_a_to_b, _ = pcu.k_nearest_neighbors(
                pred_sampled, gt_points, k=1
            )  # k closest points (in pts_b) for each point in pts_a
            correct_pred = np.sum(dists_a_to_b < thresh)
            precision = correct_pred / len(dists_a_to_b)
            metrics[f"precision_{thresh}"].append(precision)

            dists_b_to_a, _ = pcu.k_nearest_neighbors(gt_points, pred_sampled, k=1)
            correct_gt = np.sum(dists_b_to_a < thresh)
            recall = correct_gt / len(dists_b_to_a)
            metrics[f"recall_{thresh}"].append(recall)

            fscore = 2 * precision * recall / (precision + recall)
            metrics[f"fscore_{thresh}"].append(fscore)

            intersection = min(correct_pred, correct_gt)
            union = (
                    len(dists_a_to_b) + len(dists_b_to_a) - max(correct_pred, correct_gt)
            )

            IOU = intersection / union
            metrics[f"IOU_{thresh}"].append(IOU)
        return metrics
    else:
        correct_gt_list = []
        correct_pred_list = []
        _, acc, comp = compute_chamfer_distance(pred_sampled, gt_points)
        for thresh in thresh_list:
            dists_b_to_a, _ = pcu.k_nearest_neighbors(gt_points, pred_sampled, k=1)
            correct_gt = np.sum(dists_b_to_a < thresh)
            num_gt = len(dists_b_to_a)
            correct_gt_list.append(correct_gt)
            dists_a_to_b, _ = pcu.k_nearest_neighbors(pred_sampled, gt_points, k=1)
            correct_pred = np.sum(dists_a_to_b < thresh)
            correct_pred_list.append(correct_pred)
            num_pred = len(dists_a_to_b)

        return correct_gt_list, num_gt, correct_pred_list, num_pred, acc, comp


def get_gt_points(
        scan_name,
        edge_type="all",
        interval=0.005,
        return_direction=False,
        data_base_dir=None,
):
    """
    Get ground truth points from a dataset.

    Args:
        name (str): Name of the dataset.

    Returns:
        numpy.ndarray: Raw and processed ground truth points.
    """
    objs_dir = os.path.join(data_base_dir, "obj")
    obj_names = os.listdir(objs_dir)
    obj_names.sort()
    index_obj_names = {}
    for obj_name in obj_names:
        index_obj_names[obj_name[:8]] = obj_name

    json_feats_path = os.path.join(data_base_dir, "chunk_0000_feats.json")
    with open(json_feats_path, "r") as f:
        json_data_feats = json.load(f)
    json_stats_path = os.path.join(data_base_dir, "chunk_0000_stats.json")
    with open(json_stats_path, "r") as f:
        json_data_stats = json.load(f)

    # get the normalize scale to help align the nerf points and gt points
    [
        x_min,
        y_min,
        z_min,
        x_max,
        y_max,
        z_max,
        x_range,
        y_range,
        z_range,
    ] = json_data_stats[scan_name]["bbox"]
    scale = 1 / max(x_range, y_range, z_range)
    poi_center = (
            np.array([((x_min + x_max) / 2), ((y_min + y_max) / 2), ((z_min + z_max) / 2)])
            * scale
    )
    set_location = [0.5, 0.5, 0.5] - poi_center  # based on the rendering settings
    obj_path = os.path.join(objs_dir, index_obj_names[scan_name])

    with open(obj_path, encoding="utf-8") as file:
        data = file.readlines()

    vertices_obj = [each.split(" ") for each in data if each.split(" ")[0] == "v"]
    vertices_xyz = [
        [float(v[1]), float(v[2]), float(v[3].replace("\n", ""))] for v in vertices_obj
    ]

    edge_pts = []
    edge_pts_raw = []
    edge_pts_direction = []
    edge_pts_colors = []
    num_colors = 30
    color_rank = 0
    fancy_colors = get_fancy_color(num_colors)
    fancy_colors = fancy_colors[torch.randperm(num_colors)]
    rename = {
        "BSpline": "curve",
        "Circle": "curve",
        "Ellipse": "curve",
        "Line": "line",
    }
    for each_curve in json_data_feats[scan_name]:
        color_rank += 1
        if edge_type != "all" and rename[each_curve["type"]] != edge_type:
            continue

        if each_curve["sharp"]:  # each_curve["type"]: BSpline, Line, Circle
            each_edge_pts = [vertices_xyz[i] for i in each_curve["vert_indices"]]
            edge_pts_raw += each_edge_pts

            gt_sampling = []
            gt_sampling_color = []
            each_edge_pts = np.array(each_edge_pts)
            for index in range(len(each_edge_pts) - 1):
                next = each_edge_pts[index + 1]
                current = each_edge_pts[index]
                num = int(np.linalg.norm(next - current) // interval)
                linspace = np.linspace(0, 1, num)
                gt_sampling.append(
                    linspace[:, None] * current + (1 - linspace)[:, None] * next
                )
                gt_sampling_color.append(fancy_colors[color_rank%num_colors][None].repeat(num,1).numpy())

                if return_direction:
                    direction = (next - current) / np.linalg.norm(next - current)
                    edge_pts_direction.extend([direction] * num)
            each_edge_pts = np.concatenate(gt_sampling).tolist()
            each_edge_pts_colors = np.concatenate(gt_sampling_color).tolist()
            edge_pts += each_edge_pts
            edge_pts_colors += each_edge_pts_colors

    if len(edge_pts_raw) == 0:
        return None, None, None, None

    edge_pts_raw = np.array(edge_pts_raw) * scale + set_location
    edge_pts = np.array(edge_pts) * scale + set_location
    edge_pts_direction = np.array(edge_pts_direction)
    edge_pts_colors = np.array(edge_pts_colors)

    return (
        edge_pts_raw.astype(np.float32),
        edge_pts.astype(np.float32),
        edge_pts_direction,
        edge_pts_colors
    )


def get_pred_points_and_directions(
        json_path,
        sample_resolution=0.005,
):
    # 读取训练阶段导出的参数化边缘 JSON，里面主要包含 Bezier 控制点和线段端点。
    with open(json_path, "r") as f:
        json_data = json.load(f)

    # 取出所有 Bezier 曲线控制点；JSON 中每条曲线是 4 个 3D 控制点。
    curve_paras = np.array(json_data["curves_ctl_pts"]).reshape(-1, 3)
    # reshape 成 [num_curves, 4, 3]，即每条 Bezier 曲线有 4 个控制点，每个点是 xyz
    curves_ctl_pts = curve_paras.reshape(-1, 4, 3)
    # 统计 Bezier 曲线数量
    num_curves = len(curves_ctl_pts)
    # 有些结果可能没有直线段字段，这种情况下线段数量为 0。
    if "lines_end_pts" not in json_data:
        num_lines = 0
        lines_end_pts = np.empty((0, 2, 3))
    else:
        # 取出所有线段端点，reshape 成 [num_lines, 2, 3]，每条线段有起点和终点。
        lines_end_pts = np.array(json_data["lines_end_pts"]).reshape(-1, 2, 3)
        # 统计线段数量。
        num_lines = len(lines_end_pts)

    # 给每条曲线/线段分配一个可视化颜色，多加 1 是为了避免颜色数量边界问题。
    fancy_colors = get_fancy_color(num_curves + num_lines + 1)
    # 随机打乱颜色，避免相邻曲线颜色过于接近。
    fancy_colors = fancy_colors[torch.randperm(num_curves + num_lines)]
    # 打印当前要采样的曲线数量和线段数量。
    print('number of curves/lines:', num_curves, num_lines)

    # 保存 Bezier 曲线采样出来的 3D 点。
    all_curve_points = []
    # 保存每个 Bezier 采样点对应的曲线方向，也就是切线方向。
    all_curve_directions = []
    # 保存每个 Bezier 采样点的可视化颜色。
    all_curve_colors = []

    # -----------------------------------for Cubic Bezier-----------------------------------
    # 给 Bezier 曲线采样循环加进度条；如果没有曲线，就直接跳过。
    curve_iter = tqdm(curves_ctl_pts, desc="Sampling Bezier curves", leave=True) if num_curves > 0 else curves_ctl_pts
    if num_curves > 0:
        for i, each_curve in enumerate(curve_iter):
            # 当前曲线的 4 个控制点，形状固定为 [4, 3]。
            each_curve = np.array(each_curve).reshape(4, 3)
            # 根据曲线长度和 sample_resolution 估算一条 3D Bezier 曲线的弧长，来决定采样点数量
            # num_samples 表示估算曲线长度的积分精度；sample_resolution 是最终采样点之间的大致间隔，越大越快
            sample_num = int(
                bezier_curve_length(each_curve, num_samples=100) // sample_resolution
            )
            # 在 t=[0, 1] 上均匀采样 sample_num 个参数位置。
            t = np.linspace(0, 1, sample_num)
            # 构造 [t^3, t^2, t, 1]，用于矩阵形式计算三次 Bezier 曲线点。
            matrix_u = np.array([t ** 3, t ** 2, t, [1] * sample_num]).reshape(
                4, sample_num
            )

            # 三次 Bezier 从幂基到控制点基的系数矩阵。
            matrix_middle = np.array(
                [[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]]
            )

            # 计算当前 Bezier 曲线上所有采样点，输出形状为 [sample_num, 3]。
            matrix = np.matmul(
                np.matmul(matrix_u.T, matrix_middle), each_curve
            ).reshape(sample_num, 3)

            # 把当前曲线采样点追加到总点列表。
            all_curve_points += matrix.tolist()
            # 当前曲线的所有采样点使用同一个曲线颜色。
            all_curve_colors += fancy_colors[i][None, :].repeat(matrix.shape[0], 1).numpy().tolist()

            # 计算 Bezier 曲线导数需要的 t 项：d(t^3)/dt = 3t^2。
            derivative_u = 3 * t ** 2
            # 计算 Bezier 曲线导数需要的 t 项：d(t^2)/dt = 2t。
            derivative_v = 2 * t

            # 分别计算 x/y/z 三个坐标维度上的 Bezier 一阶导数。
            # dx 是每个采样点处切线方向的 x 分量。
            dx = (
                    (
                            -3 * each_curve[0][0]
                            + 9 * each_curve[1][0]
                            - 9 * each_curve[2][0]
                            + 3 * each_curve[3][0]
                    )
                    * derivative_u
                    + (6 * each_curve[0][0] - 12 * each_curve[1][0] + 6 * each_curve[2][0])
                    * derivative_v
                    + (-3 * each_curve[0][0] + 3 * each_curve[1][0])
            )

            # dy 是每个采样点处切线方向的 y 分量。
            dy = (
                    (
                            -3 * each_curve[0][1]
                            + 9 * each_curve[1][1]
                            - 9 * each_curve[2][1]
                            + 3 * each_curve[3][1]
                    )
                    * derivative_u
                    + (6 * each_curve[0][1] - 12 * each_curve[1][1] + 6 * each_curve[2][1])
                    * derivative_v
                    + (-3 * each_curve[0][1] + 3 * each_curve[1][1])
            )

            # dz 是每个采样点处切线方向的 z 分量。
            dz = (
                    (
                            -3 * each_curve[0][2]
                            + 9 * each_curve[1][2]
                            - 9 * each_curve[2][2]
                            + 3 * each_curve[3][2]
                    )
                    * derivative_u
                    + (6 * each_curve[0][2] - 12 * each_curve[1][2] + 6 * each_curve[2][2])
                    * derivative_v
                    + (-3 * each_curve[0][2] + 3 * each_curve[1][2])
            )
            # 把每个采样点的导数向量归一化，作为该采样点的方向。
            for i in range(sample_num):
                direction = np.array([dx[i], dy[i], dz[i]])
                norm_direction = direction / np.linalg.norm(direction)
                all_curve_directions.append(norm_direction)

    # 保存线段采样出来的 3D 点。
    all_line_points = []
    # 保存每个线段采样点对应的方向。
    all_line_directions = []
    # 保存每个线段采样点的可视化颜色。
    all_line_colors = []

    # -------------------------------------for Line-----------------------------------------
    # 给线段采样循环加进度条；如果没有线段，就直接跳过。
    line_iter = tqdm(lines_end_pts, desc="Sampling line segments", leave=True) if num_lines > 0 else lines_end_pts
    if num_lines > 0:
        for i, each_line in enumerate(line_iter):
            # 当前线段包含两个端点，形状为 [2, 3]。
            each_line = np.array(each_line).reshape(2, 3)
            # 根据线段长度和 sample_resolution 决定采样点数量。
            sample_num = int(
                np.linalg.norm(each_line[0] - each_line[-1]) // sample_resolution
            )
            # 在线段参数 t=[0, 1] 上均匀采样。
            t = np.linspace(0, 1, sample_num)

            # 构造线性插值矩阵中的 [t, 1]。
            matrix_u_l = np.array([t, [1] * sample_num])
            # 线段从端点形式转换到线性插值形式的系数矩阵。
            matrix_middle_l = np.array([[-1, 1], [1, 0]])

            # 计算当前线段上的所有采样点，输出形状为 [sample_num, 3]。
            matrix_l = np.matmul(
                np.matmul(matrix_u_l.T, matrix_middle_l), each_line
            ).reshape(sample_num, 3)
            # 把当前线段采样点追加到总点列表。
            all_line_points += matrix_l.tolist()
            # 当前线段的所有采样点使用同一个线段颜色。
            all_line_colors += fancy_colors[i + num_curves][None, :].repeat(matrix_l.shape[0], 1).numpy().tolist()

            # 线段方向就是终点减起点。
            direction = each_line[1] - each_line[0]
            # 归一化线段方向，1e-6 用于避免零长度线段除零。
            norm_direction = direction / (np.linalg.norm(direction) + 1e-6)

            # 当前线段上的所有采样点共享同一个方向。
            for point in matrix_l:
                all_line_directions.append(norm_direction)

    # 把 Bezier 采样点列表转换为 numpy 数组，形状为 [num_curve_samples, 3]。
    all_curve_points = np.array(all_curve_points).reshape(-1, 3)
    # 把线段采样点列表转换为 numpy 数组，形状为 [num_line_samples, 3]。
    all_line_points = np.array(all_line_points).reshape(-1, 3)
    # 把 Bezier 采样点颜色转换为 numpy 数组。
    all_curve_colors = np.array(all_curve_colors).reshape(-1, 3)
    # 把线段采样点颜色转换为 numpy 数组。
    all_line_colors = np.array(all_line_colors).reshape(-1, 3)
    # 返回曲线采样点、线段采样点、对应方向、对应颜色，以及原始曲线/线段数量。
    return all_curve_points, all_line_points, all_curve_directions, \
        all_line_directions, all_curve_colors, all_line_colors, num_curves, num_lines


def downsample_point_cloud_average(
        points, num_voxels_per_axis=256, min_bound=None, max_bound=None
):
    """
    Downsample a point set based on the number of voxels per axis by averaging the points within each voxel.

    Args:
        points: a [#v, 3]-shaped array of 3d points.
        num_voxels_per_axis: a scalar or 3-tuple specifying the number of voxels along each axis.

    Returns:
        A [#v', 3]-shaped numpy array of downsampled points, where #v' is the number of occupied voxels.
    """

    # Calculate the bounding box of the point cloud
    if min_bound is None:
        min_bound = np.min(points, axis=0)
    else:
        min_bound = np.array(min_bound)

    if max_bound is None:
        max_bound = np.max(points, axis=0)
    else:
        max_bound = np.array(max_bound)

    # Determine the size of the voxel based on the desired number of voxels per axis
    if isinstance(num_voxels_per_axis, int):
        voxel_size = (max_bound - min_bound) / num_voxels_per_axis
    else:
        voxel_size = [
            (max_bound[i] - min_bound[i]) / num_voxels_per_axis[i] for i in range(3)
        ]

    # Use the existing function to downsample the point cloud based on voxel size
    downsampled_points = pcu.downsample_point_cloud_on_voxel_grid(
        voxel_size, points, min_bound=min_bound, max_bound=max_bound
    )

    return downsampled_points
