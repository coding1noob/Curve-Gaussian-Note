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

import torch
import math
from diff_cur_rasterization import GaussianRasterizationSettings, GaussianRasterizer
from scene.gaussian_curve_model import GaussianCurveModel
from utils.sh_utils import eval_sh

def render(viewpoint_camera, pc : GaussianCurveModel, pipe, bg_color : torch.Tensor, scaling_modifier = 1.0,
           separate_sh = False, override_color = None,
           use_trained_exp=False, use_mask=False, mask_thr=0.01):
    """
    Render the scene. 
    
    Background tensor (bg_color) must be on GPU!
    """
 
    # Create zero tensor. We will use it to make pytorch return gradients of the 2D (screen-space) means
    screenspace_points = torch.zeros_like(pc.get_xyz, dtype=pc.get_xyz.dtype, requires_grad=True, device="cuda") + 0
    try:
        screenspace_points.retain_grad()
    except:
        pass

    # Set up rasterization configuration
    tanfovx = math.tan(viewpoint_camera.FoVx * 0.5)
    tanfovy = math.tan(viewpoint_camera.FoVy * 0.5)

    raster_settings = GaussianRasterizationSettings(
        image_height=int(viewpoint_camera.image_height),
        image_width=int(viewpoint_camera.image_width),
        tanfovx=tanfovx,
        tanfovy=tanfovy,
        bg=bg_color,
        scale_modifier=scaling_modifier,
        viewmatrix=viewpoint_camera.world_view_transform,
        projmatrix=viewpoint_camera.full_proj_transform,
        sh_degree=pc.active_sh_degree,
        campos=viewpoint_camera.camera_center,
        prefiltered=False,
        debug=pipe.debug,
        antialiasing=pipe.antialiasing,
        render_geo=pipe.render_geo,
    )

    rasterizer = GaussianRasterizer(raster_settings=raster_settings)

    means3D = pc.get_xyz
    means2D = screenspace_points
    opacity = pc.get_opacity

    # If precomputed 3d covariance is provided, use it. If not, then it will be computed from
    # scaling / rotation by the rasterizer.
    scales = None
    rotations = None
    cov3D_precomp = None

    if pipe.compute_cov3D_python:
        cov3D_precomp = pc.get_covariance(scaling_modifier)
    else:
        scales = pc.get_scaling
        rotations = pc.get_rotation
    if use_mask:
        # mask = torch.sigmoid(pc._mask)
        mask = ((torch.sigmoid(pc._mask) > mask_thr).float() - torch.sigmoid(pc._mask)).detach() + torch.sigmoid(pc._mask)
        scales = pc.get_scaling * mask.view(-1, 1)
        opacity = pc.get_opacity * mask.view(-1, 1)

    # 注释掉源代码, 修改 curveGS 能适配RGB作监督

    # # 球谐系数初始化，由观察方向计算颜色
    # shs = None
    # # Python 已经算好每个高斯的颜色初始化，直接传给 CUDA
    # colors_precomp = None
    # # 上面 二者只能使用一个
    # # override_color 为此函数传入参数。None：使用模型自己的颜色或 SH，非 None：使用调用者提供的颜色
    # # 目前 CurveGS 最后会覆盖它，所以这个功能实际上失效了
    # if override_color is None:
    #     # 判断是否在 Python 中把 SH 转换成 RGB
    #     if pipe.convert_SHs_python:
    #         # 在python中求值

    #         # 取得模型的 SH 特征并调整形状，标准 3DGS 中，pc.get_features 通常是：
    #         # [高斯数量, 每个颜色通道的 SH 系数数量, 3（表示RGB）]
    #         # transpose(1, 2) 后变成：[P, 3, K]
    #         shs_view = pc.get_features.transpose(1, 2).view(-1, 3, (pc.max_sh_degree+1)**2)
    #         # 计算从相机中心指向每个高斯中心的方向，因为 SH 颜色具有视角相关性，所以必须知道观察方向
    #         dir_pp = (pc.get_xyz - viewpoint_camera.camera_center.repeat(pc.get_features.shape[0], 1))
    #         # 归一化成单位向量
    #         dir_pp_normalized = dir_pp/dir_pp.norm(dim=1, keepdim=True)
    #         # 最后调用 eval_sh() 计算颜色
    #         # 根据以下内容计算每个高斯在当前观察方向下的颜色：
    #         # 当前启用的 SH 阶数；
    #         # 每个高斯的 SH 系数；
    #         # 相机到高斯的观察方向
    #         sh2rgb = eval_sh(pc.active_sh_degree, shs_view, dir_pp_normalized)
    #         # 标准 3DGS 的 SH 表示以 0.5 为颜色中心，因此下一行要加 0.5
    #         colors_precomp = torch.clamp_min(sh2rgb + 0.5, 0.0)
    #     else:
    #         # 不在 Python 中求值，把 SH 系数传给 CUDA
            
    #         # 是否将 SH 的 DC 分量和高阶分量分开传递。这一般是某些稀疏优化器或新版 rasterizer 的接口
    #         if separate_sh:
    #             dc, shs = pc.get_features_dc, pc.get_features_rest
    #         else:
    #             shs = pc.get_features
    # else:
    #     # override_color存在, 则使用外部覆盖颜色
    #     colors_precomp = override_color
    # # 上面其实curveGS都没生效, 下面两行才是真正运行的地方
    # shs = None
    # colors_precomp = torch.ones(means3D.shape[0], 1).cuda()

    # 修改后:
    shs = None
    if override_color is None:
    # 兼容原始 CurveGS：所有高斯暂时渲染为白色
        colors_precomp = torch.ones(
            (means3D.shape[0], 3), device=means3D.device, dtype=means3D.dtype
        )
    else:
        colors_precomp = override_color

        # 如果 colors_precomp 仅有一个维度, 不是[P,3], 比如[3], 即所有高斯共享一个RGB颜色, 则扩展
        if colors_precomp.ndim == 1:
            # unsqueeze(0) 在第 0 维增加一个维度：[3] -> [1, 3]
            # expand(means3D.shape[0], -1) 把这一个颜色扩展给所有高斯。
            # 如果有 P=100 个高斯：[1, 3] -> [100, 3]
            colors_precomp = colors_precomp.unsqueeze(0).expand(means3D.shape[0], -1)

        if colors_precomp.shape != (means3D.shape[0], 3):
            raise ValueError(
                "override_color must have shape [3] or "
                f"[{means3D.shape[0]}, 3], got {tuple(colors_precomp.shape)}"
            )
        
        colors_precomp = colors_precomp.to(
            device=means3D.device,
            dtype=means3D.dtype,
        ).contiguous()
                


    global_normal = pc.get_main_axis(viewpoint_camera)
    local_normal = global_normal @ viewpoint_camera.world_view_transform[:3, :3]
    # pts_in_cam = means3D @ viewpoint_camera.world_view_transform[:3, :3] + viewpoint_camera.world_view_transform[3, :3]
    # depth_z = pts_in_cam[:, 2]
    input_all_map = torch.zeros((means3D.shape[0], 4)).cuda().float()
    input_all_map[:, :3] = local_normal
    input_all_map[:, 3] = 1.0



    # 去掉传入不存在的 dc= 参数
    # if separate_sh:
    #     rendered_image, radii, depth_image, out_all_map = rasterizer(
    #         means3D = means3D,
    #         means2D = means2D,
    #         dc = dc,
    #         shs = shs,
    #         colors_precomp = colors_precomp,
    #         opacities = opacity,
    #         scales = scales,
    #         rotations = rotations,
    #         all_map=input_all_map,
    #         cov3D_precomp = cov3D_precomp)
    # else:
    #     rendered_image, radii, depth_image, out_all_map = rasterizer(
    #         means3D = means3D,
    #         means2D = means2D,
    #         shs = shs,
    #         colors_precomp = colors_precomp,
    #         opacities = opacity,
    #         scales = scales,
    #         rotations = rotations,
    #         all_map=input_all_map,
    #         cov3D_precomp = cov3D_precomp)

    # 修改后:
    rendered_image, radii, depth_image, out_all_map = rasterizer(
        means3D=means3D,
        means2D=means2D,
        shs=None,
        colors_precomp=colors_precomp,
        opacities=opacity,
        scales=scales,
        rotations=rotations,
        all_map=input_all_map,
        cov3D_precomp=cov3D_precomp,
    )



        
    # Apply exposure to rendered image (training only)
    if use_trained_exp:
        exposure = pc.get_exposure_from_name(viewpoint_camera.image_name)
        rendered_image = torch.matmul(rendered_image.permute(1, 2, 0), exposure[:3, :3]).permute(2, 0, 1) + exposure[:3, 3,   None, None]

    # Those Gaussians that were frustum culled or had a radius of 0 were not visible.
    # They will be excluded from value updates used in the splitting criteria.
    rendered_image = rendered_image.clamp(0, 1)
    rendered_alpha = out_all_map[3:4, ]
    rendered_dir = out_all_map[0:3]

    # transform normal from view space to world space
    rendered_dir = (rendered_dir.permute(1, 2, 0) @ (viewpoint_camera.world_view_transform[:3, :3].T)).permute(2, 0,
                                                                                                                 1)

    out = {
        "render": rendered_image,
        "viewspace_points": screenspace_points,
        "visibility_filter" : (radii > 0).nonzero(),
        "radii": radii,
        "depth" : depth_image,
        "rend_dir": rendered_dir,
        "rend_alpha": rendered_alpha
        }
    
    return out
