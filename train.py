import torch.nn.functional as F
import os
import open3d as o3d
import torch
import numpy as np
from random import randint
from utils.loss_utils import l1_loss, ssim,  edge_aware_loss
from gaussian_renderer import render
import sys
from edge_extraction.merging import merge_endpoints
from scipy.spatial import cKDTree
from scene import Scene, GaussianCurveModel
from utils.general_utils import safe_state
import uuid
import torch.nn.functional as F
import json
from tqdm import tqdm
from einops import rearrange
from utils.image_utils import psnr
from argparse import ArgumentParser, Namespace
from arguments import ModelParams, PipelineParams, OptimizationParams, OptimizationParamsPidinet, OptimizationParamsReplica
from plyfile import PlyData, PlyElement
from utils.sh_utils import RGB2SH
try:
    from torch.utils.tensorboard import SummaryWriter
    TENSORBOARD_FOUND = True
except ImportError:
    TENSORBOARD_FOUND = False

try:
    from fused_ssim import fused_ssim
    FUSED_SSIM_AVAILABLE = True
except:
    FUSED_SSIM_AVAILABLE = False

try:
    from diff_cur_rasterization import SparseGaussianAdam
    SPARSE_ADAM_AVAILABLE = True
except:
    SPARSE_ADAM_AVAILABLE = False

# 用 CPU 时间换 GPU 显存
def _find_sparse_curve_endpoint_pairs(curve_points, distance_threshold):
    # 我改的地方：这里只收集距离足够近的端点对，用于端点连接 loss。
    # 替代原来直接构造 2N x 2N 全量距离矩阵的写法，避免显存/内存爆炸。
    start_points = curve_points[:, 0].detach().cpu().numpy()
    end_points = curve_points[:, -1].detach().cpu().numpy()
    all_points = np.concatenate([start_points, end_points], axis=0)
    if all_points.shape[0] < 2:
        return np.empty((0,), dtype=np.int64), np.empty((0,), dtype=np.int64)

    tree = cKDTree(all_points)
    sparse_dist = tree.sparse_distance_matrix(tree, distance_threshold, output_type='coo_matrix')
    if sparse_dist.nnz == 0:
        return np.empty((0,), dtype=np.int64), np.empty((0,), dtype=np.int64)

    num_curves = curve_points.shape[0]
    curve_ids = np.concatenate([
        np.arange(num_curves, dtype=np.int64),
        np.arange(num_curves, dtype=np.int64),
    ])
    valid = sparse_dist.row < sparse_dist.col
    valid &= curve_ids[sparse_dist.row] != curve_ids[sparse_dist.col]
    rows = sparse_dist.row[valid].astype(np.int64, copy=False)
    cols = sparse_dist.col[valid].astype(np.int64, copy=False)
    return rows, cols


def _inverse_sigmoid_np(x):
    # PLY 里保存的是 3DGS 习惯使用的未激活 opacity 参数，
    # 这里要把 [0, 1] 的概率值转回 logit，保证 3DGS_NOTE 读入后数值语义一致。
    x = np.clip(x, 1e-6, 1.0 - 1e-6)
    return np.log(x / (1.0 - x))


@torch.no_grad()
def save_curve_gaussians_for_3dgs_note(gaussians, path, sh_degree=3):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # 取出当前训练完成后的曲线高斯中心点，作为后续 3DGS_NOTE 的几何初始化。
    xyz = gaussians.get_xyz.detach().cpu().numpy().astype(np.float32)
    normals = np.zeros_like(xyz, dtype=np.float32)

    # CurveGaussian 更偏几何先验，颜色本身没有被 RGB 图像监督训练。
    # 所以这里输出中性灰的 SH 初值，让 3DGS_NOTE 后续重新从图像学习高保真颜色。
    neutral_rgb = torch.full((xyz.shape[0], 3), 0.5, dtype=torch.float32, device="cuda")
    f_dc = RGB2SH(neutral_rgb).detach().cpu().numpy().astype(np.float32)
    # 高阶 SH 系数直接置零，避免把 CurveGaussian 的边缘风格错误带到 3DGS_NOTE 里。
    f_rest = np.zeros((xyz.shape[0], 3 * ((sh_degree + 1) ** 2 - 1)), dtype=np.float32)

    # opacity / scale / rotation 都转换成 3DGS 标准可读格式。
    opacity = gaussians.get_opacity.detach().cpu().numpy().astype(np.float32)
    opacity = _inverse_sigmoid_np(opacity)

    scales = gaussians.get_scaling.detach().cpu().numpy().astype(np.float32)
    # 3DGS 里保存的是 log(scale)，这里要手动取对数。
    scales = np.log(np.maximum(scales, 1e-8)).astype(np.float32)

    rotations = gaussians.get_rotation.detach().cpu().numpy().astype(np.float32)

    # 按 3DGS_NOTE / 3DGS 约定拼出 vertex 属性表。
    attributes = np.concatenate((xyz, normals, f_dc, f_rest, opacity, scales, rotations), axis=1)
    attr_names = ["x", "y", "z", "nx", "ny", "nz"]
    attr_names += [f"f_dc_{i}" for i in range(3)]
    attr_names += [f"f_rest_{i}" for i in range(f_rest.shape[1])]
    attr_names += ["opacity"]
    attr_names += [f"scale_{i}" for i in range(3)]
    attr_names += [f"rot_{i}" for i in range(4)]

    dtype_full = [(name, "f4") for name in attr_names]
    elements = np.empty(xyz.shape[0], dtype=dtype_full)
    elements[:] = list(map(tuple, attributes))
    # 直接写成标准 PLY，供 3DGS_NOTE 后续读取初始化。
    PlyData([PlyElement.describe(elements, "vertex")], text=False).write(path)
    print(f"Saved {path} for 3DGS_NOTE initialization.")

def Loss_part(dataset, viewpoint_cam, image, rend_alpha, iteration, opt):
    if dataset.use_RGB:
        if viewpoint_cam.original_rgb is None:
            raise RuntimeError(
                "RGB mode requires viewpoint_cam.original_rgb"
            )
        if viewpoint_cam.edge_mask is None:
            raise RuntimeError(
                "RGB mode requires viewpoint_cam.edge_mask"
            )

        gt_rgb = viewpoint_cam.original_rgb
        edge_mask = viewpoint_cam.edge_mask

        # 几何监督：alpha 应该接近输入边缘 mask。
        geometry_loss = torch.abs(rend_alpha - edge_mask).mean()

        # RGB 监督只发生在边缘区域。
        rgb_mask = edge_mask.expand_as(image)
        rgb_error = torch.abs(image - gt_rgb)

        rgb_loss = (
            (rgb_error * rgb_mask).sum()
            / rgb_mask.sum().clamp_min(1e-6)
        )

        # 让 RGB loss 从 0 逐渐增加到完整权重。
        rgb_warmup = min(
            1.0,
            iteration / max(opt.rgb_warmup, 1),
        )

        Ll1 = geometry_loss
        loss = (
            opt.lambda_mse * geometry_loss
            + opt.lambda_rgb * rgb_warmup * rgb_loss
        )
    else:
        # 保持原来的非 RGB 模式。
        # 新改动兼容三通道, 因为 image 变成三通道了
        gt_image = viewpoint_cam.original_image.cuda()
        # :1表示取[0,1), ...表示后面所有维度都完整保留。它等价于：gt_image[:1, :, :]
        # .repeat(3, 1, 1)表示第0维复制3次, 第1维和第2维不变, 这样就把单通道的 gt_image 扩展成了三通道
        gt_edge =  gt_image[:1, ...].repeat(3, 1, 1)
        Ll1 = edge_aware_loss(image, gt_edge)

        if FUSED_SSIM_AVAILABLE:
            ssim_value = fused_ssim(
                image.unsqueeze(0),
                gt_edge.unsqueeze(0),
            )
        else:
            ssim_value = ssim(image, gt_edge)

        loss = opt.lambda_mse * ((1.0 - opt.lambda_dssim) * Ll1 + opt.lambda_dssim * (1.0 - ssim_value))

    return loss, Ll1

def training(dataset, opt, pipe, testing_iterations, saving_iterations,
             checkpoint_iterations, checkpoint, debug_from):

    if not SPARSE_ADAM_AVAILABLE and opt.optimizer_type == "sparse_adam":
        sys.exit(f"Trying to use sparse adam but it is not installed, please install the correct rasterizer using pip install [3dgs_accel].")

    # 1. 初始化训练对象：创建输出、曲线高斯模型、场景、优化器，并可选恢复 checkpoint。
    first_iter = 0
    tb_writer = prepare_output_and_logger(dataset)
    gaussians = GaussianCurveModel(dataset.sh_degree, dataset.n_gaussians, opt.optimizer_type, use_RGB=dataset.use_RGB)
    scene = Scene(dataset, gaussians)
    gaussians.training_setup(opt)
    if checkpoint:
        (model_params, first_iter) = torch.load(
            checkpoint,
            weights_only=False,
        )
        gaussians.restore(model_params, opt)

    bg_color = [1, 1, 1] if dataset.white_background else [0, 0, 0]
    background = torch.tensor(bg_color, dtype=torch.float32, device="cuda")
    bg = torch.rand((3), device="cuda") if opt.random_background else background
    iter_start = torch.cuda.Event(enable_timing = True)
    iter_end = torch.cuda.Event(enable_timing = True)

    use_sparse_adam = opt.optimizer_type == "sparse_adam" and SPARSE_ADAM_AVAILABLE 

    viewpoint_stack = scene.getTrainCameras().copy()
    viewpoint_indices = list(range(len(viewpoint_stack)))
    ema_loss_for_log = 0.0
    ema_normal_for_log = 0.0
    ema_product_for_log = 0.0
    curve_smo_for_log = 0.0
    curve_conn_for_log = 0.0
    normal_prior_error = torch.tensor(0.0).cuda()
    dot_products = torch.tensor(0.0).cuda()
    curve_smo = torch.tensor(0.0).cuda()
    curve_conn= torch.tensor(0.0).cuda()
    progress_bar = tqdm(range(first_iter, opt.iterations), desc="Training progress")
    first_iter += 1
    reset_timestep = 0

    for iteration in range(first_iter, opt.iterations + 1):
        # 2. 每轮训练前调度：更新学习率、提升 SH 阶数，并随机选一个训练视角。
        reset_timestep += 1
        iter_start.record()
        gaussians.update_learning_rate(iteration)

        # Every 1000 its we increase the levels of SH up to a maximum degree
        if iteration % 1000 == 0:
            gaussians.oneupSHdegree()

        # Pick a random Camera
        if not viewpoint_stack:
            viewpoint_stack = scene.getTrainCameras().copy()
            viewpoint_indices = list(range(len(viewpoint_stack)))
        rand_idx = randint(0, len(viewpoint_indices) - 1)
        viewpoint_cam = viewpoint_stack.pop(rand_idx)
        vind = viewpoint_indices.pop(rand_idx)
        # Render
        if (iteration - 1) == debug_from:
            pipe.debug = True

        # 3. 渲染当前 3D 曲线高斯：得到这一视角下的 2D 线条外观 image。
        render_pkg = render(viewpoint_cam, gaussians, pipe, bg, use_trained_exp=dataset.train_test_exp,
                            separate_sh=SPARSE_ADAM_AVAILABLE,
                            use_mask=iteration>=opt.densify_until_iter, mask_thr=opt.mask_threshold)
        # 旧代码注释
        # image, viewspace_point_tensor, visibility_filter, radii = render_pkg["render"], render_pkg["viewspace_points"], \
        #     render_pkg["visibility_filter"], render_pkg["radii"]
        image = render_pkg["render"]
        viewspace_point_tensor = render_pkg["viewspace_points"]
        visibility_filter = render_pkg["visibility_filter"]
        radii = render_pkg["radii"]
        # [1, H, W], 表示当前视角下每个像素被曲线高斯覆盖的程度
        rend_alpha = render_pkg["rend_alpha"]


        # 4. 图像监督 Loss：这里是把渲染出的线条外观和输入边缘图比较。
        
        # 旧代码
        # 如果数据集使用的是 PidiNet / DexiNed 边缘图，这里就是直接监督信号。
        # gt_image = viewpoint_cam.original_image.cuda()
        # Ll1 = edge_aware_loss(image, gt_image[:1, ...])
        
        # if FUSED_SSIM_AVAILABLE:
        #     ssim_value = fused_ssim(image.unsqueeze(0), gt_image[:1, ...].unsqueeze(0))
        # else:
        #     ssim_value = ssim(image, gt_image[:1, ...])

        # 新代码, 用新函数
        # loss: 包含 RGB、几何和后续正则项的总 loss. Ll1: 传给日志系统的基础图像/几何 loss
        loss, Ll1 = Loss_part(dataset, viewpoint_cam, image, rend_alpha, iteration, opt)


        # 5. 正则项：约束 mask、opacity、曲线平滑度、宽度和端点连接关系。
        if iteration>=opt.densify_until_iter:
            loss = loss + opt.lambda_mask * torch.mean((torch.sigmoid(gaussians._mask)))


        if visibility_filter.sum() > 0 and reset_timestep > 0:
            opacity = gaussians.get_opacity[visibility_filter]
            opa_loss = opt.opacity_loss_weight * torch.log(1 + opacity ** 2 / 0.5).mean()
            loss = loss + opa_loss

        if opt.lambda_curve_smo > 0 and visibility_filter.sum() > 0:
            rotation_mat = gaussians.get_rotation_matrix
            dir_global = rearrange(rotation_mat[..., 0], '(b m) c -> b m c', m=gaussians.n_gaussians)
            cos_sim = 1-F.cosine_similarity(dir_global[:, :-1, :], dir_global[:, 1:, :], dim=-1).abs()
            curve_smo = cos_sim.mean()
            loss = loss + opt.lambda_curve_smo * curve_smo

        if opt.lambda_width>0:
                width_thr = 0.005
                mask = gaussians.get_curve_width>=width_thr
                if mask.any():
                    lambda_width = (gaussians.get_curve_width[mask]-width_thr).mean()
                    loss = loss + opt.lambda_width * lambda_width

        if opt.lambda_points_conn > 0 and iteration > opt.conn_from_iter:
            curve_points = gaussians.get_curve_points
            start_points, end_points = curve_points[:,0], curve_points[:, -1] # N*3
            all_points = torch.cat([start_points, end_points], dim=0)

            # 原版用GPU做全量距离矩阵，显存爆炸
            # mask = torch.eye(len(start_points), dtype=torch.bool, device=start_points.device)
            # mask = torch.cat([torch.cat([mask, mask], dim=1), torch.cat([mask, mask], dim=1)], dim=0)
            # dist = torch.cdist(all_points, all_points, p=2)
            # dis_thr = 0.05
            # with torch.no_grad():
            #     valid_mask = (dist < dis_thr) & (~mask)
            # if valid_mask.any():
            #     curve_conn = dist[valid_mask] 
            #     curve_conn = curve_conn.mean()
            #     loss = loss + opt.lambda_points_conn * curve_conn

            # 假设现在有 N 条曲线，每条曲线有 2 个端点，所以端点数是：
            # M = 2N。“全量矩阵”就是把每个端点和每个端点都算一遍距离，得到一个 M x M 的矩阵。
            # 如果你有 140000 条曲线：
            # 端点数 M = 280000
            # 矩阵大小 = 280000 x 280000
            # 也就是约：
            # 78,400,000,000 个距离
            # float32 一个数 4 字节，单这个矩阵就要：
            # 78,400,000,000 * 4 ≈ 313 GB
            # CPU KD-tree 是什么
            # 当前版本没有算完整 M x M 距离矩阵，而是用 KD-tree 只找“距离小于阈值”的近邻端点。
            # 也就是说它不问：
            # 每个端点到所有端点距离是多少？
            # 而是问：
            # 每个端点附近 0.05 范围内有哪些端点？
            # 这省显存很多，但代价是每步要在 CPU 上建树和查询，所以 7000 后会慢。
            
            dis_thr = 0.05
            curve_conn = torch.tensor(0.0, device=all_points.device)
            # 我改的地方：先用 CPU KD-tree 找近邻端点对，再只在 GPU 上计算这些候选对的距离。
            # 这样不再构造 2N x 2N 的 torch.cdist 全量矩阵。
            pair_rows, pair_cols = _find_sparse_curve_endpoint_pairs(curve_points, dis_thr)
            if len(pair_rows) > 0:
                pair_rows = torch.from_numpy(pair_rows).to(all_points.device, dtype=torch.long)
                pair_cols = torch.from_numpy(pair_cols).to(all_points.device, dtype=torch.long)
                curve_conn = torch.linalg.vector_norm(all_points[pair_rows] - all_points[pair_cols], dim=-1).mean()
                loss = loss + opt.lambda_points_conn * curve_conn

        # 6. 反向传播：根据边缘图监督和正则项更新曲线高斯参数。
        loss.backward()
        iter_end.record()

        with torch.no_grad():
            # Progress bar
            ema_loss_for_log = 0.4 * loss.item() + 0.6 * ema_loss_for_log
            ema_normal_for_log = 0.4 * normal_prior_error.item() + 0.6 * ema_normal_for_log
            ema_product_for_log = 0.4 * dot_products.item() + 0.6 * ema_product_for_log
            curve_smo_for_log = 0.4 * curve_smo.item() + 0.6 * curve_smo_for_log
            curve_conn_for_log = 0.4 * curve_conn.item() + 0.6 * curve_conn_for_log

            if iteration % 10 == 0:
                loss_dict = {
                    "Curves": f"{gaussians.get_curve_points.shape[0]}",
                    "Gs": f"{len(gaussians.get_xyz)}",
                    "Loss": f"{ema_loss_for_log:.{5}f}",
                    "smo": f"{curve_smo_for_log:.{5}f}",
                    "conn": f"{curve_conn_for_log:.{5}f}",
                    "opa": f"{gaussians.get_opacity.mean().item():.{5}f}",
                }
                progress_bar.set_postfix(loss_dict)
                progress_bar.update(10)
            if iteration == opt.iterations:
                progress_bar.close()

            # Log and save
            if tb_writer is not None:
                tb_writer.add_scalar('train_loss_patches/curve_smo', curve_smo_for_log, iteration)
                tb_writer.add_scalar('train_loss_patches/curve_conn', curve_conn_for_log, iteration)


            training_report(tb_writer, iteration, Ll1, loss, l1_loss, iter_start.elapsed_time(iter_end),
                            testing_iterations, scene, render,
                            (pipe, background, 1., SPARSE_ADAM_AVAILABLE, None, dataset.train_test_exp),
                            dataset.train_test_exp)

            # 7. 结构调整：增密、剪枝、切分曲线，并把足够直的曲线转成显式线段结构。

            # --- 7a. 增密阶段（iteration < densify_until_iter，默认 7000 之前）---
            if iteration < opt.densify_until_iter:
                # 记录每个高斯在图像空间里的最大半径，用于后续判断是否需要增密或剪枝
                gaussians.max_radii2D[visibility_filter] = torch.max(gaussians.max_radii2D[visibility_filter], radii[visibility_filter])
                # 累积每个高斯的梯度信息，梯度大说明该区域拟合不够，需要增密
                gaussians.add_densification_stats(viewspace_point_tensor, visibility_filter)

                if iteration > opt.densify_from_iter and iteration % opt.densification_interval == 0:
                    # 每隔 densification_interval（默认2000） 步执行一次增密+剪枝：
                    # - 梯度大的高斯/曲线会被克隆或分裂，增加局部细节
                    # - opacity 太低的曲线会被剪掉，减少无效高斯
                    # - size_threshold: 7000 步后开始限制图像空间里过大的高斯
                    size_threshold = 20 if iteration > opt.opacity_reset_interval else None
                    gaussians.densify_and_prune(opt.densify_grad_threshold, opt.opacity_cull, scene.cameras_extent, size_threshold, radii)

            # --- 7b. 增密结束时的最终剪枝（iteration == densify_until_iter，默认 7000）---
            if iteration == opt.densify_until_iter:
                # 把 opacity 仍然很低（<= opacity_cull_second）的曲线全部删掉
                # 这是一次比增密阶段更激进的剪枝，清除训练前期没学到任何信息的曲线
                prune_mask = (gaussians.get_curve_opacity <= opt.opacity_cull_second).squeeze()
                gaussians.prune_curves(prune_mask)
                # 释放 GPU 碎片内存
                torch.cuda.empty_cache()
                # 冻结 opacity：把所有曲线的 opacity 强制拉到 >= 0.6，并停止优化 opacity
                # 之后 opacity 不再变化，只优化曲线形状、宽度、mask 等参数
                gaussians.fix_opacity()

            # --- 7c. 后期周期性剪枝（每 1000 步，500 offset，增密结束后）---
            if iteration % 1000 == 500 and iteration > opt.densify_until_iter:
                # 根据 opacity 和 mask 再次剪掉弱曲线
                gaussians.only_prune(opt.opacity_cull, opt.mask_threshold)
                # 把 mask 接近 0 的采样高斯从曲线上切分出去或修剪掉，使曲线更精简
                gaussians.mask_trim_split(opt.mask_threshold)

            # --- 7d. 曲线按曲率切分（每 1000 步，3000 步后）---
            if iteration % 1000 == 0 and iteration > 3000 and iteration != opt.iterations:
                # 如果一条曲线的局部曲率太大（相邻高斯方向夹角超过 threshold_angle）
                # 就把它从弯折处切断，分成两条更短的曲线
                # 这样曲线能更好地拟合复杂形状，而不是用一条大弧硬拟合
                gaussians.curve_split_curvature(opt.threshold_angle, opt.threshold_angle_skip)

            # --- 7e. 曲线拟合为线段 + 曲线合并（每 1000 步，增密结束后）---
            if (iteration % 1000 == 0 and iteration > opt.densify_until_iter) or iteration == opt.iterations:
                # 如果一条 Bezier 曲线已经足够直（控制点偏离直线小于 threshold_line）
                # 就把它转成显式线段（is_bezier=False），减少参数量、提升导出效率
                gaussians.fit_curve_to_line(opt.threshold_line, opt.threshold_max_line)
                # 把距离近、方向相似的曲线/线段合并成一条，减少重复的边
                gaussians.merge_curves(opt.distance_threshold, opt.similarity_threshold)

            # ---  7f. 保存当前状态（两处 saving_iterations 判断）---
            if (iteration in saving_iterations) and not dataset.simple:
                print("\n[ITER {}] Saving Gaussians".format(iteration))
                scene.save(iteration)
                gaussians.draw_curve(os.path.join(scene.model_path,
                                                           "point_cloud/iteration_{}".format(iteration)), iteration)

                gaussians.draw_ellipsoids(os.path.join(scene.model_path,
                                                           "point_cloud/iteration_{}".format(iteration)), iteration)

            if (iteration in saving_iterations) and not dataset.simple:
                print("\n[ITER {}] Saving Gaussians".format(iteration))
                scene.save(iteration)

            # Optimizer step
            if iteration < opt.iterations:
                gaussians.exposure_optimizer.step()
                gaussians.exposure_optimizer.zero_grad(set_to_none = True)
                if use_sparse_adam:
                    visible = radii > 0
                    gaussians.optimizer.step(visible, radii.shape[0])
                    gaussians.optimizer.zero_grad(set_to_none = True)
                else:
                    gaussians.optimizer.step()
                    gaussians.optimizer.zero_grad(set_to_none = True)

            if (iteration in checkpoint_iterations):
                print("\n[ITER {}] Saving Checkpoint".format(iteration))
                torch.save((gaussians.capture(), iteration), scene.model_path + "/chkpnt" + str(iteration) + ".pth")

        if hasattr(gaussians, 'prepare_scaling_rot'):
            gaussians.prepare_scaling_rot()
    
    # 8. 最终导出：从训练好的曲线/线段参数中提取 parametric edge 结果。
    extract_curves(gaussians, opt, scene, simple=dataset.simple)

def extract_curves(gaussians, opt, scene, simple=False):
     # meger_points:
    merged_bezier_curves = gaussians.get_curve_points[gaussians.is_bezier]
    merged_line_segments = gaussians.get_curve_points[~gaussians.is_bezier][:,[0,-1],:]
    merged_bezier_curves = rearrange(merged_bezier_curves, 'b m c -> b (m c)').detach().cpu().numpy()
    merged_line_segments = rearrange(merged_line_segments, 'b m c -> b (m c)').detach().cpu().numpy()

    if opt.merge_endpoints_flag:
        (
            merged_line_segments,
            merged_bezier_curves,
        ) = merge_endpoints(
            merged_line_segments,
            merged_bezier_curves,
            distance_threshold=0.015,
        )

    merged_edge_dict = {
        "lines_end_pts": (
            merged_line_segments.tolist() if len(merged_line_segments) > 0 else []
        ),
        "curves_ctl_pts": (
            merged_bezier_curves.tolist() if len(merged_bezier_curves) > 0 else []
        ),
    }
    if simple:
        # simple 模式只需要给 eval_replica.py 用的参数化边缘 JSON。
        # 不再调用 get_parametric_edge() 对每条 Bezier/线段重新采样，否则大场景会在训练结束后卡很久。
        return_edge_dict = merged_edge_dict
        # 额外导出一个给 3DGS_NOTE 用的标准高斯初始化 PLY，
        # 这样后面可以把 CurveGaussian 的几何结构和 COLMAP 原始点云合并训练。
        curve_init_ply_path = os.path.join(scene.model_path, "curve_3dgs_init.ply")
        save_curve_gaussians_for_3dgs_note(gaussians, curve_init_ply_path, sh_degree=3)
    else:
        from edge_extraction.extract_para_edge import get_parametric_edge
        # get_parametric_edge 把训练得到的“参数化边缘”（Bezier 曲线 + 直线段）
        # 整理成最终可导出的边缘点云，并在需要时做可见性筛选
        pred_edge_points, return_edge_dict = get_parametric_edge(opt.visible_checking, merged_edge_dict)
        edge_pcd = o3d.geometry.PointCloud()
        edge_pcd.points = o3d.utility.Vector3dVector(pred_edge_points)

        edge_ply_file_path = os.path.join(scene.model_path, "edge_points.ply")
        try:
            # 我改的地方：最终 edge_points.ply 也改成二进制 PLY，避免 ASCII 写超大文件失败。
            o3d.io.write_point_cloud(edge_ply_file_path, edge_pcd, write_ascii=False)
            print(f"Saved {edge_ply_file_path} for edge points visualization.")
        except IOError as e:
            print(f"Failed to save {edge_ply_file_path}: {e}")

    json_file_path = os.path.join(scene.model_path, "parametric_edges.json")
    try:
        with open(json_file_path, "w") as json_file:
            json.dump(return_edge_dict, json_file)
        print(f"Saved {json_file_path} for evaluation.")
    except IOError as e:
        print(f"Failed to save {json_file_path}: {e}")


def prepare_output_and_logger(args):    
    if not args.model_path:
        if os.getenv('OAR_JOB_ID'):
            unique_str=os.getenv('OAR_JOB_ID')
        else:
            unique_str = str(uuid.uuid4())
        if args.detector=='DexiNed':
            args.model_path = os.path.join("./output_DexiNed/", unique_str[0:10])
        elif args.detector=='PidiNet':
            args.model_path = os.path.join("./output_PidiNet/", unique_str[0:10])
        
    # Set up output folder
    print("Output folder: {}".format(args.model_path))
    os.makedirs(args.model_path, exist_ok = True)
    if not args.simple:
        with open(os.path.join(args.model_path, "cfg_args"), 'w') as cfg_log_f:
            cfg_log_f.write(str(Namespace(**vars(args))))

    # Create Tensorboard writer
    tb_writer = None
    if TENSORBOARD_FOUND and not args.simple:
        tb_writer = SummaryWriter(args.model_path)
    elif args.simple:
        print("Simple mode: only writing parametric_edges.json")
    else:
        print("Tensorboard not available: not logging progress")
    return tb_writer

def training_report(tb_writer, iteration, Ll1, loss, l1_loss, elapsed, testing_iterations,
                    scene : Scene, renderFunc, renderArgs, train_test_exp):
    if tb_writer:
        tb_writer.add_scalar('train_loss_patches/l1_loss', Ll1.item(), iteration)
        tb_writer.add_scalar('train_loss_patches/total_loss', loss.item(), iteration)
        tb_writer.add_scalar('iter_time', elapsed, iteration)
        tb_writer.add_scalar('total_points', scene.gaussians.get_xyz.shape[0], iteration)

    # Report test and samples of training set
    if iteration in testing_iterations:
        torch.cuda.empty_cache()
        validation_configs = ({'name': 'test', 'cameras' : scene.getTestCameras()}, 
                              {'name': 'train', 'cameras' : [scene.getTrainCameras()[idx % len(scene.getTrainCameras())] for idx in range(5, 30, 5)]})

        for config in validation_configs:
            if config['cameras'] and len(config['cameras']) > 0:
                l1_test = 0.0
                psnr_test = 0.0
                for idx, viewpoint in enumerate(config['cameras']):
                    render_pkg = renderFunc(viewpoint, scene.gaussians, *renderArgs)
                    image = torch.clamp(render_pkg["render"], 0.0, 1.0)
                    gt_image = torch.clamp(viewpoint.original_image.to("cuda"), 0.0, 1.0)
                    if train_test_exp:
                        image = image[..., image.shape[-1] // 2:]
                        gt_image = gt_image[..., gt_image.shape[-1] // 2:]
                    if tb_writer and (idx < 5):
                        tb_writer.add_images(config['name'] + "_view_{}/render".format(viewpoint.image_name), image[None], global_step=iteration)
                        if iteration == testing_iterations[0]:
                            tb_writer.add_images(config['name'] + "_view_{}/ground_truth".format(viewpoint.image_name), gt_image[None], global_step=iteration)
                        from utils.general_utils import colormap
                        depth = render_pkg["depth"]
                        norm = depth.max()
                        depth = depth / norm
                        depth = colormap(depth.cpu().numpy()[0], cmap='turbo')
                        tb_writer.add_images(config['name'] + "_view_{}/depth".format(viewpoint.image_name),
                                             depth[None], global_step=iteration)

                        rend_alpha = render_pkg['rend_alpha']
                        rend_dir = F.normalize(render_pkg["rend_dir"], dim=0)
                        rend_dir = rend_dir * 0.5 + 0.5
                        tb_writer.add_images(config['name'] + "_view_{}/rend_dir".format(viewpoint.image_name),
                                             rend_dir[None], global_step=iteration)
                        tb_writer.add_images(config['name'] + "_view_{}/rend_alpha".format(viewpoint.image_name),
                                             rend_alpha[None], global_step=iteration)

                    l1_test += l1_loss(image, gt_image).mean().double()
                    psnr_test += psnr(image, gt_image).mean().double()
                psnr_test /= len(config['cameras'])
                l1_test /= len(config['cameras'])          
                print("\n[ITER {}] Evaluating {}: L1 {} PSNR {}".format(iteration, config['name'], l1_test, psnr_test))
                if tb_writer:
                    tb_writer.add_scalar(config['name'] + '/loss_viewpoint - l1_loss', l1_test, iteration)
                    tb_writer.add_scalar(config['name'] + '/loss_viewpoint - psnr', psnr_test, iteration)


        torch.cuda.empty_cache()

if __name__ == "__main__":
    # Set up command line argument parser
    parser = ArgumentParser(description="Training script parameters", conflict_handler='resolve')
    lp = ModelParams(parser)
    op = OptimizationParams(parser)
    
    pp = PipelineParams(parser)
    parser.add_argument('--ip', type=str, default="127.0.0.1")
    parser.add_argument('--port', type=int, default=6011)
    parser.add_argument('--debug_from', type=int, default=-1)
    parser.add_argument('--detect_anomaly', action='store_true', default=False)
    parser.add_argument("--test_iterations", nargs="+", type=int, default=[3_000, 10_000])
    parser.add_argument("--save_iterations", nargs="+", type=int, default=[3_000, 10_000])
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--checkpoint_iterations", nargs="+", type=int, default=[10000])
    parser.add_argument("--start_checkpoint", type=str, default = None)
    args = parser.parse_args(sys.argv[1:])
    
    if 'ABC' in args.source_path:
        print("start training ABC")
        if lp.detector=='Pidinet':
            op = OptimizationParamsPidinet(parser)
    if 'Replica' in args.source_path:
        print("start training Replica")
        op = OptimizationParamsReplica(parser)

    args.save_iterations.append(args.iterations)
    print("Optimizing " + args.model_path)

    # Initialize system state (RNG)
    safe_state(args.quiet)

    torch.autograd.set_detect_anomaly(args.detect_anomaly)
    training(lp.extract(args), op.extract(args), pp.extract(args), 
            args.test_iterations, args.save_iterations,
            args.checkpoint_iterations, args.start_checkpoint, args.debug_from)

    # All done
    print("\nTraining complete.")
