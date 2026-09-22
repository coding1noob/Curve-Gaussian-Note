
# 新增来自 2DGS 的 distortion depth

新增 --distortion_Loss 显式开关。只有同时满足以下条件时才计算 distortion：
--PGSR_depth
显式传入 --distortion_Loss
--curve_depth_distortion_weight > 0
iteration 位于配置窗口内
存在 CurveGS 点

当 multi_view_ncc_weight == 0 且 multi_view_geo_weight == 0 时：
不建立 nearest_id
不采样邻近相机
不渲染邻近视角
当 single_view_weight == 0 时，不创建 single-view normal 所需的 PGSR 渲染。

## 需要重新编译
cd /data1/jhc/storage_of_code/gs_pro6000/submodules/diff-plane-rasterization

python setup.py clean --all || true
rm -rf build
find . -name '*.so' -delete

pip install -e . --no-build-isolation --no-cache-dir

1. 地面复杂纹理无光照进行实验

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/918/Curve_mask_2DGS \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_ncc_weight 0.0 \
--multi_view_geo_weight 0.0 \
--single_view_weight 0.0 \
--distortion_Loss \
--curve_depth_distortion_weight 0.05 \
--curve_depth_distortion_from_iter 7000 \
--curve_depth_distortion_end_iter 20000

[ITER 30000] Evaluating test: L1 0.025754908887812726 PSNR 25.968473727886494

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/918/Curve_mask_2DGS2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_ncc_weight 0.0 \
--multi_view_geo_weight 0.0 \
--single_view_weight 0.0 \
--distortion_Loss \
--curve_depth_distortion_weight 0.1 \
--curve_depth_distortion_from_iter 7000 \
--curve_depth_distortion_end_iter 20000

[ITER 30000] Evaluating test: L1 0.025039797505507104 PSNR 25.949910677396336

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/918/Curve_mask_2DGS3 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_ncc_weight 0.0 \
--multi_view_geo_weight 0.0 \
--single_view_weight 0.0 \
--distortion_Loss \
--curve_depth_distortion_weight 0.01 \
--curve_depth_distortion_from_iter 7000 \
--curve_depth_distortion_end_iter 20000

[ITER 30000] Evaluating test: L1 0.025040574156894136 PSNR 26.00715475815993

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/918/Curve_mask_2DGS4 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_ncc_weight 0.0 \
--multi_view_geo_weight 0.0 \
--single_view_weight 0.0 \
--distortion_Loss \
--curve_depth_distortion_weight 0.1 \
--curve_depth_distortion_from_iter 7000 \
--curve_depth_distortion_end_iter 20000 \
--save_iterations 6999 \
--checkpoint_iterations 6999

[ITER 30000] Evaluating test: L1 0.02642198673521097 PSNR 25.790740233201248 [19/09 11:19:56]

# 新增效果不明显，试试提前到3k就合并之后的实验（不用新的SGCR模块，同时引入PGSR模块挨个试）

**对于地板有纹理，无光照，sh0情况**

1. 对colmap，PGSR全加！且使用终止到30k
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/918/Curve_mask_colmapPGSR_withNormal \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--single_view_weight_from_iter 7000 \
--colmap_PGSR \
--save_iterations 6999 \
--checkpoint_iterations 6999

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/918/Curve_mask_colmapPGSR_withNormal \
--iteration 30000 \
--skip_train

[test] PSNR: 27.1015  SSIM: 0.9229  LPIPS: 0.0926 [19/09 13:11:26]

2. 对colmap，PGSR全加，相当于只是提前了合并迭代数

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/918/Curve_mask_colmapPGSR_withNormal2_2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--colmap_PGSR \
--save_iterations 6999 \
--checkpoint_iterations 6999 \
--start_checkpoint /data2/jhc/output/3dgs_output/918/Curve_mask_colmapPGSR_withNormal/chkpnt6999.pth

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/918/Curve_mask_colmapPGSR_withNormal2_2 \
--iteration 30000 \
--skip_train

第一次[ITER 30000] Evaluating test: L1 0.01869955752044916 PSNR 28.052235529972958 [19/09 14:13:12]
第二次[test] PSNR: 27.8088  SSIM: 0.9277  LPIPS: 0.0854 [19/09 15:32:17]
[test] PSNR: 27.7064  SSIM: 0.9269  LPIPS: 0.0859 [19/09 17:07:29]

3. 只对colmap加法线Loss

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/918/Curve_mask_colmap_OnlyNormal_2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--colmap_PGSR \
--save_iterations 6999 \
--checkpoint_iterations 6999 \
--multi_view_ncc_weight 0.0 \
--multi_view_geo_weight 0.0 \
--start_checkpoint /data2/jhc/output/3dgs_output/918/Curve_mask_colmapPGSR_withNormal/chkpnt6999.pth

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/918/Curve_mask_colmap_OnlyNormal_2 \
--iteration 30000 \
--skip_train

第一次 [ITER 30000] Evaluating test: L1 0.01951793165734181 PSNR 27.790057989267204 [19/09 14:08:15]
第二次 [test] PSNR: 28.0107  SSIM: 0.9283  LPIPS: 0.0845 [19/09 15:32:34]
第三那次 [test] PSNR: 27.8663  SSIM: 0.9282  LPIPS: 0.0852 [19/09 16:42:25]

3. 对cruveGS，PGSR全加，相当于只是提前了合并迭代数

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/918/Curve_mask_curvePGSR_withNormal \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR \
--save_iterations 6999 \
--checkpoint_iterations 6999 \
--start_checkpoint /data2/jhc/output/3dgs_output/918/Curve_mask_colmapPGSR_withNormal/chkpnt6999.pth

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/918/Curve_mask_curvePGSR_withNormal \
--iteration 30000 \
--skip_train

[test] PSNR: 28.3893  SSIM: 0.9384  LPIPS: 0.0789 [19/09 19:08:24]
[test] PSNR: 28.1524  SSIM: 0.9380  LPIPS: 0.0801 [19/09 20:28:57]

4. 只对curve加法线Loss，相当于只是提前了合并迭代数

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/918/Curve_mask_curve_OnlyNormal \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR \
--save_iterations 6999 \
--checkpoint_iterations 6999 \
--multi_view_ncc_weight 0.0 \
--multi_view_geo_weight 0.0 \
--start_checkpoint /data2/jhc/output/3dgs_output/918/Curve_mask_colmapPGSR_withNormal/chkpnt6999.pth

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/918/Curve_mask_curve_OnlyNormal \
--iteration 30000 \
--skip_train

[test] PSNR: 28.1041  SSIM: 0.9351  LPIPS: 0.0813 [19/09 19:28:31]
[test] PSNR: 28.2563  SSIM: 0.9356  LPIPS: 0.0808 [19/09 20:26:05]

5. 我草原来单独加都这么好，那我一起加了得了呗？

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/918/Curve_mask_AllPGSR_withNormal \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--colmap_PGSR \
--curve_PGSR \
--save_iterations 6999 \
--checkpoint_iterations 6999 \
--start_checkpoint /data2/jhc/output/3dgs_output/918/Curve_mask_colmapPGSR_withNormal/chkpnt6999.pth

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/918/Curve_mask_AllPGSR_withNormal \
--iteration 30000 \
--skip_train

[test] PSNR: 28.1205  SSIM: 0.9353  LPIPS: 0.0817 [19/09 22:07:38]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/918/Curve_mask_AllPGSR_withNormal_2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--colmap_PGSR \
--curve_PGSR \
--save_iterations 6999 \
--checkpoint_iterations 6999 \
--start_checkpoint /data2/jhc/output/3dgs_output/918/Curve_mask_colmapPGSR_withNormal/chkpnt6999.pth

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/918/Curve_mask_AllPGSR_withNormal_2 \
--iteration 30000 \
--skip_train

[test] PSNR: 28.0938  SSIM: 0.9355  LPIPS: 0.0817 [19/09 22:07:24]

**看来单独给curveGS加比较好？**

# sh3 冲！

1. 先试一版无光照复杂地形的

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/918_sh3/Curve_mask_curvePGSR_withNormal1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR \
--save_iterations 6999 \
--checkpoint_iterations 6999

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/918_sh3/Curve_mask_curvePGSR_withNormal1 \
--iteration 30000 \
--skip_train

[test] PSNR: 28.3412  SSIM: 0.9369  LPIPS: 0.0797 [19/09 23:48:52]
[test] PSNR: 28.2694  SSIM: 0.9364  LPIPS: 0.0798 [19/09 23:48:52]

2. 在上面基础上加用SGCR模块

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/918_sh3/Curve_mask_curvePGSR_withNormal_SGCR1 \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_noLight_SGCR_finalPrune_consistencyLoss/curve_3dgs_init.ply \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/918_sh3/Curve_mask_curvePGSR_withNormal_SGCR1 \
--iteration 30000 \
--skip_train

[test] PSNR: 28.3699  SSIM: 0.9370  LPIPS: 0.0788 [20/09 03:04:09]
[test] PSNR: 28.5141  SSIM: 0.9368  LPIPS: 0.0787 [20/09 04:50:34]

3. 有SGCR跑buaa_net数据集（但其实这里用的SGCR不全面）

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_SGCR1 \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/buaa_net_simple-4/curve_3dgs_init.ply \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_SGCR1 \
--iteration 30000 \
--skip_train

[test] PSNR: 21.2721  SSIM: 0.5988  LPIPS: 0.3552 [20/09 06:07:00]
[test] PSNR: 21.3366  SSIM: 0.5993  LPIPS: 0.3544 [20/09 07:17:06]

4. 无SGCR跑buaa_net数据集

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_1 \
--iteration 30000 \
--skip_train

[test] PSNR: 21.4194  SSIM: 0.6009  LPIPS: 0.3520 [20/09 08:23:09]
[test] PSNR: 21.3511  SSIM: 0.6006  LPIPS: 0.3538 [20/09 02:41:25]

5. 对真实光照的地面复杂纹理，进行不带SGCR的测试

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/output/3dgs_output/918_sh3/virtualNet2_curvePGSR_withNormal_1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/output/3dgs_output/918_sh3/virtualNet2_curvePGSR_withNormal_1 \
--iteration 30000 \
--skip_train

[test] PSNR: 33.3059  SSIM: 0.9633  LPIPS: 0.0760 [20/09 03:41:19]
[test] PSNR: 33.2456  SSIM: 0.9626  LPIPS: 0.0770 [20/09 04:41:30]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/output/3dgs_output/918_sh3/virtualNet2_curvePGSR_withNormal_3 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/output/3dgs_output/918_sh3/virtualNet2_curvePGSR_withNormal_3 \
--iteration 30000 \
--skip_train

[test] PSNR: 33.0196  SSIM: 0.9622  LPIPS: 0.0779 [21/09 11:45:03]

6. 不复杂纹理的地面，使用baseline进行测试

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/jhc/output/gs_pro6000_output/output/formal3_white_simple \
--eval \
--disable_viewer

cd ../gs_pro6000
conda activate curveGS

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/jhc/output/gs_pro6000_output/output/formal3_white_simple \
--iteration 30000 \
--skip_train

7. 不复杂纹理的地面，进行不带SGCR的测试

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/jhc/output/3dgs_output/918_sh3/virtualNet2_Simple_curvePGSR_withNormal_1 \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_white_simple/curve_3dgs_init.ply \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=3 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/jhc/output/3dgs_output/918_sh3/virtualNet2_Simple_curvePGSR_withNormal_1 \
--iteration 30000 \
--skip_train

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/jhc/output/3dgs_output/918_sh3/virtualNet2_Simple_curvePGSR_withNormal_2 \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_white_simple/curve_3dgs_init.ply \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/jhc/output/3dgs_output/918_sh3/virtualNet2_Simple_curvePGSR_withNormal_2 \
--iteration 30000 \
--skip_train

8. 对真实光照的地面复杂纹理，带SGCR

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/output/curve_output/virtual_net2_SGCR \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 10 \
--fill_y_threshold 0.5 \
--fill_grid_resX 200 \
--fill_grid_resY 100 \
--fill_grid_resZ 50 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--SGCR \
--final_opacity_cull 0.5

cd ../gs_pro6000

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/output/3dgs_output/918_sh3/virtualNet2_curvePGSR_withNormal_SGCR1 \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_SGCR/curve_3dgs_init.ply \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/output/3dgs_output/918_sh3/virtualNet2_curvePGSR_withNormal_SGCR1 \
--iteration 30000 \
--skip_train

[test] PSNR: 33.1605  SSIM: 0.9607  LPIPS: 0.0799 [20/09 18:58:51]
[test] PSNR: 33.1605  SSIM: 0.9604  LPIPS: 0.0794 [20/09 20:31:30]

9. 不复杂纹理的地面，带SGCR

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/jhc/output/3dgs_output/918_sh3/virtualNet2_Simple_curvePGSR_withNormal_SGCR1 \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_white_simple_SGCR/curve_3dgs_init.ply \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/jhc/output/3dgs_output/918_sh3/virtualNet2_Simple_curvePGSR_withNormal_SGCR1 \
--iteration 30000 \
--skip_train

[test] PSNR: 33.4993  SSIM: 0.9788  LPIPS: 0.0427 [20/09 16:56:31]
[test] PSNR: 33.1778  SSIM: 0.9782  LPIPS: 0.0430 [20/09 18:19:53]

**这下面是跑别的弄错了，实际上跑成了和上面一样的**

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/jhc/output/3dgs_output/918_sh3/virtualNet2_Simple_curvePGSR_withNormal_1 \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_white_simple_SGCR/curve_3dgs_init.ply \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/jhc/output/3dgs_output/918_sh3/virtualNet2_Simple_curvePGSR_withNormal_1 \
--iteration 30000 \
--skip_train

[test] PSNR: 34.1259  SSIM: 0.9792  LPIPS: 0.0422 [20/09 05:38:44]
[test] PSNR: 33.6223  SSIM: 0.9788  LPIPS: 0.0429 [20/09 06:38:35]


10. 对第八点(对真实光照的地面复杂纹理，带SGCR)重新测试，看看curveGS的代码是否能回到以前

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/output/curve_output/virtual_net2_noSGCR \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 10 \
--fill_y_threshold 0.5 \
--fill_grid_resX 200 \
--fill_grid_resY 100 \
--fill_grid_resZ 50 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01

cd ../gs_pro6000

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/output/3dgs_output/918_sh3/virtualNet2_curvePGSR_withNormal_noSGCR1 \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_noSGCR/curve_3dgs_init.ply \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/output/3dgs_output/918_sh3/virtualNet2_curvePGSR_withNormal_noSGCR1 \
--iteration 30000 \
--skip_train

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/output/3dgs_output/918_sh3/virtualNet2_curvePGSR_withNormal_noSGCR2 \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_noSGCR/curve_3dgs_init.ply \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/output/3dgs_output/918_sh3/virtualNet2_curvePGSR_withNormal_noSGCR2 \
--iteration 30000 \
--skip_train

[test] PSNR: 32.5358  SSIM: 0.9596  LPIPS: 0.0803 [21/09 01:24:19]
[test] PSNR: 33.2828  SSIM: 0.9604  LPIPS: 0.0800 [21/09 00:23:58]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/output/3dgs_output/918_sh3/virtualNet2_curvePGSR_withNormal_noSGCR3 \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_noSGCR/curve_3dgs_init.ply \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=3 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/output/3dgs_output/918_sh3/virtualNet2_curvePGSR_withNormal_noSGCR3 \
--iteration 30000 \
--skip_train

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/output/3dgs_output/918_sh3/virtualNet2_curvePGSR_withNormal_noSGCR4 \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_noSGCR/curve_3dgs_init.ply \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/output/3dgs_output/918_sh3/virtualNet2_curvePGSR_withNormal_noSGCR4 \
--iteration 30000 \
--skip_train

[test] PSNR: 32.8605  SSIM: 0.9603  LPIPS: 0.0794 [21/09 09:22:15]
[test] PSNR: 32.8752  SSIM: 0.9599  LPIPS: 0.0801 [21/09 09:22:28]














































