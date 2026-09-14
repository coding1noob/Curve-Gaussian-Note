
空场景，纯色地板，无光照

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/curve_output/virtual_net2_white_simple_noLight \
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

1. 仅curveGS点

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_onlyCurve_nomask \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_white_simple_noLight/curve_3dgs_init.ply \
--sh_degree 0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_onlyCurve_nomask \
--iteration 30000 \
--skip_train

[test] PSNR: 31.0673  SSIM: 0.9720  LPIPS: 0.0364 [11/09 21:51:32]

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_onlyCurve_nomask \
--iteration 30000 \
--eval \
--skip_train

2. 融合curveGS点(非边缘监督) + PGSR

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_nomask_PGSRfull \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_white_simple_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--PGSR_depth \
--multi_view_num 1

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_nomask_PGSRfull \
--iteration 30000 \
--skip_train

[test] PSNR: 29.9695  SSIM: 0.9674  LPIPS: 0.0414 [11/09 21:54:27]

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_nomask_PGSRfull \
--iteration 30000 \
--eval \
--skip_train

3. 融合curveGS点(非边缘监督) + 仅geoLoss的PGSR

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_nomask_PGSR_onlyGEO \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_white_simple_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_ncc_weight 0.0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_nomask_PGSR_onlyGEO \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_nomask_PGSR_onlyGEO \
--iteration 30000 \
--eval \
--skip_train

[test] PSNR: 30.6588  SSIM: 0.9698  LPIPS: 0.0422 [12/09 10:06:20]


-------------------------------------

4. 仅curveGS点（边缘mask）

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_onlyCurve_Mask \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_white_simple_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_onlyCurve_Mask \
--iteration 30000 \
--skip_train

[test] PSNR: 30.4240  SSIM: 0.9647  LPIPS: 0.0531 [11/09 22:35:16]

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_onlyCurve_Mask \
--iteration 30000 \
--eval \
--skip_train

只渲染CurveGS/colmap点
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python render_2.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_onlyCurve_Mask \
--iteration 30000 \
--curve_only \
--skip_train

5. curveGS点（边缘mask）+ PGSR 

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_white_simple_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull \
--iteration 30000 \
--eval \
--skip_train

[test] PSNR: 29.0247  SSIM: 0.9583  LPIPS: 0.0608 [11/09 23:49:31]

只渲染CurveGS/colmap点
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python render_2.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull \
--iteration 30000 \
--colmap_only


6. curveGS点（边缘mask）+ 仅geoLoss的PGSR

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSR_onlyGEO \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_white_simple_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_ncc_weight 0.0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSR_onlyGEO \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=3 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSR_onlyGEO \
--iteration 30000 \
--eval \
--skip_train

[test] PSNR: 29.6280  SSIM: 0.9608  LPIPS: 0.0579 [12/09 00:51:42]


7. 提前 --curvegs_inject_iteration 和 --multi_view_weight_from_iter

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSR_onlyGEO_start5k \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_white_simple_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 5000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_ncc_weight 0.0 \
--multi_view_weight_from_iter 8000

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSR_onlyGEO_start5k \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSR_onlyGEO_start5k \
--iteration 30000 \
--eval \
--skip_train

[test] PSNR: 30.7834  SSIM: 0.9706  LPIPS: 0.0395 [12/09 14:00:47]

---------------------------------------------------------------------------

1. 只对colmap点进行PGSR

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyColmap \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_white_simple_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--colmap_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyColmap \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyColmap \
--iteration 30000 \
--eval \
--skip_train

只渲染CurveGS/colmap点
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python render_2.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyColmap \
--iteration 30000 \
--curve_only

2. 

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyColmap2 \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_white_simple_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--colmap_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyColmap2 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyColmap2 \
--iteration 30000 \
--eval \
--skip_train

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python render_2.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyColmap2 \
--iteration 30000 \
--curve_only

[test] PSNR: 28.8425  SSIM: 0.9572  LPIPS: 0.0594 [13/09 01:48:11]


3. 

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyColmap3 \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_white_simple_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
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
--colmap_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyColmap3 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyColmap3 \
--iteration 30000 \
--eval \
--skip_train

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python render_2.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyColmap3 \
--iteration 30000 \
--curve_only

[test] PSNR: 30.4723  SSIM: 0.9669  LPIPS: 0.0498 [13/09 12:50:30]

4. 先手动去除杂点试试

python delete_point.py \
--input output/virtual_net2_white_simple_noLight/curve_3dgs_init.ply \
--output output/virtual_net2_white_simple_noLight/curve_3dgs_init_manual_clean.ply \
--boxes \
3 3 5 3.133 1.596 -5.760 1 0 0 0

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyColmap4 \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_white_simple_noLight/curve_3dgs_init_manual_clean.ply \
--sh_degree 0 \
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
--colmap_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyColmap4 \
--iteration 30000 \
--skip_train

[test] PSNR: 30.7732  SSIM: 0.9676  LPIPS: 0.0490 [13/09 17:40:27]

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyColmap4 \
--iteration 30000 \
--eval \
--skip_train

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_2.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyColmap4 \
--iteration 30000 \
--curve_only

5. 试试新改好的curveGS，再冲一次

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/curve_output/virtual_net2_white_simple_noLight_SGCR \
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
--SGCR

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyColmap5 \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_white_simple_noLight_SGCR/curve_3dgs_init.ply \
--sh_degree 0 \
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
--colmap_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyColmap5 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyColmap5 \
--iteration 30000 \
--eval \
--skip_train

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_2.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyColmap5 \
--iteration 30000 \
--curve_only











