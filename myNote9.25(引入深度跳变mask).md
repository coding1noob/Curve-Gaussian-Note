



--curve_pgsr_depth_normal_filter：布尔开关，默认关闭。开启后，对 CurveGS 的 PGSR 多视角损失应用 depth_normal_valid 过滤。
--curve_pgsr_ncc_min_valid_pixels：整数，默认 3。开启过滤时，一个 NCC patch 至少要有这么多个有效像素才参与 NCC。
--depth_normal_threshold 不是这次新增的参数；它此前已存在，用来控制 depth_normal_valid 的深度跳变阈值。

1. 

注：PGSR2和PGSR一样

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR2 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net6v2/curve_3dgs_init.ply \
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
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR2 \
--iteration 30000 \
--skip_train

[test] PSNR: 19.1120  SSIM: 0.5681  LPIPS: 0.3382 [25/09 22:39:54]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR2_depthMask1 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net6v2/curve_3dgs_init.ply \
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
--curve_pgsr_depth_normal_filter \
--curve_pgsr_ncc_min_valid_pixels 3 \
--depth_normal_threshold 0.01

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR2_depthMask1 \
--iteration 30000 \
--skip_train

[test] PSNR: 18.9986  SSIM: 0.5664  LPIPS: 0.3391 [25/09 22:39:54]

--------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR2_depthMask2 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net6v2/curve_3dgs_init.ply \
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
--curve_pgsr_depth_normal_filter \
--curve_pgsr_ncc_min_valid_pixels 3 \
--depth_normal_threshold 0.05

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR2_depthMask2 \
--iteration 30000 \
--skip_train

[test] PSNR: 19.1010  SSIM: 0.5683  LPIPS: 0.3378 [26/09 03:17:53]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR2_depthMask3 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net6v2/curve_3dgs_init.ply \
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
--curve_pgsr_depth_normal_filter \
--curve_pgsr_ncc_min_valid_pixels 3 \
--depth_normal_threshold 0.1

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR2_depthMask3 \
--iteration 30000 \
--skip_train

[test] PSNR: 19.1142  SSIM: 0.5696  LPIPS: 0.3375 [26/09 04:55:01]


2. 再使用20k合并看看结果

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR3 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net6v2/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
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
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR3 \
--iteration 30000 \
--skip_train

[test] PSNR: 18.6965  SSIM: 0.5333  LPIPS: 0.3944 [26/09 15:46:30]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR3_depthMask1 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net6v2/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
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
--curve_pgsr_depth_normal_filter \
--curve_pgsr_ncc_min_valid_pixels 3 \
--depth_normal_threshold 0.01

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR3_depthMask1 \
--iteration 30000 \
--skip_train

[test] PSNR: 18.7293  SSIM: 0.5346  LPIPS: 0.3957 [26/09 15:49:57]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR3_depthMask3 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net6v2/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
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
--curve_pgsr_depth_normal_filter \
--curve_pgsr_ncc_min_valid_pixels 3 \
--depth_normal_threshold 0.1

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR3_depthMask3 \
--iteration 30000 \
--skip_train

[test] PSNR: 18.7494  SSIM: 0.5348  LPIPS: 0.3936 [26/09 15:50:04]

3. 然后试试延长PGSR的Loss作用时间

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR4 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net6v2/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 1 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 1 \
--single_view_weight_end_iter 19999 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR4 \
--iteration 30000 \
--skip_train

[test] PSNR: 18.8076  SSIM: 0.5358  LPIPS: 0.3854 [27/09 11:28:17]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR4_depthMask1 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net6v2/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 1 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 1 \
--single_view_weight_end_iter 19999 \
--curve_PGSR \
--curve_pgsr_depth_normal_filter \
--curve_pgsr_ncc_min_valid_pixels 3 \
--depth_normal_threshold 0.01

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR4_depthMask1 \
--iteration 30000 \
--skip_train

[test] PSNR: 18.7374  SSIM: 0.5352  LPIPS: 0.3863 [26/09 20:43:22]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR4_depthMask2 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net6v2/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 1 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 1 \
--single_view_weight_end_iter 19999 \
--curve_PGSR \
--curve_pgsr_depth_normal_filter \
--curve_pgsr_ncc_min_valid_pixels 3 \
--depth_normal_threshold 0.05

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR4_depthMask2 \
--iteration 30000 \
--skip_train

[test] PSNR: 18.7781  SSIM: 0.5356  LPIPS: 0.3854 [26/09 22:10:47]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR4_depthMask3 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net6v2/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 1 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 1 \
--single_view_weight_end_iter 19999 \
--curve_PGSR \
--curve_pgsr_depth_normal_filter \
--curve_pgsr_ncc_min_valid_pixels 3 \
--depth_normal_threshold 0.1

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR4_depthMask3 \
--iteration 30000 \
--skip_train

[test] PSNR: 18.7901  SSIM: 0.5349  LPIPS: 0.3851 [26/09 23:37:25]

4. 3k到15k试一试？

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR5 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net6v2/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 3000 \
--multi_view_weight_end_iter 15000 \
--single_view_weight_from_iter 3000 \
--single_view_weight_end_iter 15000 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR5 \
--iteration 30000 \
--skip_train

[test] PSNR: 18.8038  SSIM: 0.5370  LPIPS: 0.3894 [27/09 13:26:20]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR5_depthMask1 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net6v2/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 3000 \
--multi_view_weight_end_iter 15000 \
--single_view_weight_from_iter 3000 \
--single_view_weight_end_iter 15000 \
--curve_PGSR \
--curve_pgsr_depth_normal_filter \
--curve_pgsr_ncc_min_valid_pixels 3 \
--depth_normal_threshold 0.01

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR5_depthMask1 \
--iteration 30000 \
--skip_train

[test] PSNR: 18.7885  SSIM: 0.5361  LPIPS: 0.3901 [27/09 14:40:19]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR5_depthMask2 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net6v2/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 3000 \
--multi_view_weight_end_iter 15000 \
--single_view_weight_from_iter 3000 \
--single_view_weight_end_iter 15000 \
--curve_PGSR \
--curve_pgsr_depth_normal_filter \
--curve_pgsr_ncc_min_valid_pixels 3 \
--depth_normal_threshold 0.05

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR5_depthMask2 \
--iteration 30000 \
--skip_train

[test] PSNR: 18.8048  SSIM: 0.5368  LPIPS: 0.3907 [27/09 13:35:14]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR6 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net6v2/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 15000 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 15000 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR6 \
--iteration 30000 \
--skip_train

[test] PSNR: 18.7638  SSIM: 0.5345  LPIPS: 0.3925 [27/09 15:00:52]

5. 算了还是3k合并吧，

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR6 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net6v2/curve_3dgs_init.ply \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 15000 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 15000 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR6 \
--iteration 30000 \
--skip_train

[test] PSNR: 19.1014  SSIM: 0.5679  LPIPS: 0.3374 [27/09 16:14:02]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR7 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net6v2/curve_3dgs_init.ply \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 3000 \
--multi_view_weight_end_iter 15000 \
--single_view_weight_from_iter 3000 \
--single_view_weight_end_iter 15000 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR7 \
--iteration 30000 \
--skip_train

[test] PSNR: 19.0976  SSIM: 0.5711  LPIPS: 0.3428 [27/09 16:17:35]







