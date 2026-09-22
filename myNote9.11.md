
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

[test] PSNR: 30.7827  SSIM: 0.9682  LPIPS: 0.0470 [14/09 13:57:40]

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

-----------------------------------------------

# 解铃还须系铃人，在CurveGS端改进算法，指标提升成功

1. 开始用于nomask的尝试

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_onlyCurve_nomask_SGCR \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_white_simple_noLight_SGCR/curve_3dgs_init.ply \
--sh_degree 0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_onlyCurve_nomask_SGCR \
--iteration 30000 \
--skip_train

2. 地面复杂纹理无光照

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/curve_output/virtual_net2_noLight_SGCR \
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
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_onlyCurve_Mask_SGCR \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_noLight_SGCR/curve_3dgs_init.ply \
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
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_onlyCurve_Mask_SGCR \
--iteration 30000 \
--skip_train

效果不好，分析一下：

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python render_curve.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/curve_output/virtual_net2_noLight_SGCR \
--curve_ply /data2/jhc/output/curve_output/virtual_net2_noLight_SGCR/curve_3dgs_init.ply \
--eval \
--skip_test

3. 在2的基础上增加--final_opacity_cull 0.05

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/curve_output/virtual_net2_noLight_SGCR_finalPrune \
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

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python render_curve.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/curve_output/virtual_net2_noLight_SGCR_finalPrune \
--curve_ply /data2/jhc/output/curve_output/virtual_net2_noLight_SGCR_finalPrune/curve_3dgs_init.ply \
--eval \
--skip_test

效果有，但是网前杂点依旧消不掉

4. 增加 consistencyLoss

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/curve_output/virtual_net2_noLight_SGCR_finalPrune_consistencyLoss \
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

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python render_curve.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/curve_output/virtual_net2_noLight_SGCR_finalPrune_consistencyLoss \
--curve_ply /data2/jhc/output/curve_output/virtual_net2_noLight_SGCR_finalPrune_consistencyLoss/curve_3dgs_init.ply \
--eval \
--skip_test

------------------------------------------------------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_onlyCurve_Mask_SGCR2 \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_noLight_SGCR_finalPrune_consistencyLoss/curve_3dgs_init.ply \
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
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_onlyCurve_Mask_SGCR2 \
--iteration 30000 \
--skip_train

[test] PSNR: 26.4179  SSIM: 0.9052  LPIPS: 0.1205 [15/09 13:02:06]

网前杂点确实消掉了，但是最后指标还是很难提升

5. 不用 4. 的mask

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_nomask_SGCR2 \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_noLight_SGCR_finalPrune_consistencyLoss/curve_3dgs_init.ply \
--sh_degree 0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_nomask_SGCR2 \
--iteration 30000 \
--skip_train

[test] PSNR: 27.8711  SSIM: 0.9289  LPIPS: 0.0907 [15/09 14:16:49]

也是微弱提升吧

# 引入法线Loss（但不引入SGCR）

1. 给colmap点引入法线
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyColmap3_normal \
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
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--colmap_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyColmap3_normal \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyColmap3_normal \
--iteration 30000 \
--eval \
--skip_train

[test] PSNR: 30.6643  SSIM: 0.9659  LPIPS: 0.0513 [15/09 17:25:31]

2. 给colmap点单独引入法线

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_Onlynormal \
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
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--colmap_PGSR \
--multi_view_ncc_weight 0.0 \
--multi_view_geo_weight 0.0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_Onlynormal \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_Onlynormal \
--iteration 30000 \
--eval \
--skip_train

[test] PSNR: 30.4272  SSIM: 0.9650  LPIPS: 0.0542 [15/09 19:03:47]

3. 给curveGS点引入法线
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyCurve_normal \
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
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=3 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyCurve_normal \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=3 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_PGSRfull_onlyCurve_normal \
--iteration 30000 \
--eval \
--skip_train

[test] PSNR: 30.4404  SSIM: 0.9656  LPIPS: 0.0528 [15/09 19:04:10]

4. 给curveGS点单独引入法线

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_Onlynormal2 \
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
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR \
--multi_view_ncc_weight 0.0 \
--multi_view_geo_weight 0.0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_Onlynormal2 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data2/jhc/datasets/formal3_white_notree_noLight \
-m /data2/jhc/output/3dgs_output/911/white_noLight_Mask_Onlynormal2 \
--iteration 30000 \
--eval \
--skip_train

[test] PSNR: 30.4181  SSIM: 0.9651  LPIPS: 0.0529 [15/09 19:04:30]

# 引入法线好像提升不大，再试试SGCR模块，用之前有光但是地板纹理少的数据集吧(915)

1. 

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/jhc/output/curve_output/virtual_net2_white_simple_SGCR \
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

cd /data1/jhc/storage_of_code/gs_pro6000

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/jhc/output/3dgs_output/915/white_simpe_Mask_SGCR \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_white_simple_SGCR/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/jhc/output/3dgs_output/915/white_simpe_Mask_SGCR \
--iteration 30000 \
--skip_train

[test] PSNR: 32.4417  SSIM: 0.9660  LPIPS: 0.0637 [16/09 14:17:54]

-------------------------------------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/jhc/output/3dgs_output/915/white_simpe_noMask_SGCR \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_white_simple_SGCR/curve_3dgs_init.ply \
--sh_degree 0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/jhc/output/3dgs_output/915/white_simpe_noMask_SGCR \
--iteration 30000 \
--skip_train

[test] PSNR: 32.0890  SSIM: 0.9722  LPIPS: 0.0533 [16/09 14:17:52]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/jhc/output/3dgs_output/915/white_simpe_noMask_SGCR2 \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_white_simple_SGCR/curve_3dgs_init.ply \
--sh_degree 0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/jhc/output/3dgs_output/915/white_simpe_noMask_SGCR2 \
--iteration 30000 \
--skip_train

[test] PSNR: 32.4553  SSIM: 0.9729  LPIPS: 0.0519 [16/09 15:42:00]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/jhc/output/3dgs_output/915/white_simpe_noMask_SGCR3 \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_white_simple_SGCR/curve_3dgs_init.ply \
--sh_degree 0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=3 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/jhc/output/3dgs_output/915/white_simpe_noMask_SGCR3 \
--iteration 30000 \
--skip_train

[test] PSNR: 32.5531  SSIM: 0.9728  LPIPS: 0.0521 [16/09 15:42:42]

# 不再用之前的 buaa_net_simple-3，用加了SGCR的，训 sh=0

1. 先训CurveGS	

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/curve_output/buaa_net_simple-4 \
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
--outlier_nb_points 30 \
--init_voxel_size 0.01 \
--SGCR \
--final_opacity_cull 0.5

2. 再训带Mask，			[test] PSNR: 21.0873  SSIM: 0.5730  LPIPS: 0.4056 [16/09 01:22:03]

cd /data1/jhc/storage_of_code/gs_pro6000

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/915/buaaNet_Mask_SGCR \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/buaa_net_simple-4/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/915/buaaNet_Mask_SGCR \
--iteration 30000 \
--skip_train

3. 不带Mask，			[test] PSNR: 20.9261  SSIM: 0.5909  LPIPS: 0.3787 [16/09 01:54:32]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/915/buaaNet_noMask_SGCR \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/buaa_net_simple-4/curve_3dgs_init.ply \
--sh_degree 0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/915/buaaNet_noMask_SGCR \
--iteration 30000 \
--skip_train

4. 带Mask 但只 对Curve 求法线Loss	[test] PSNR: 21.1029  SSIM: 0.5727  LPIPS: 0.4056 [16/09 02:53:23]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/915/buaaNet_noMask_SGCR_curveNormalLoss \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/buaa_net_simple-4/curve_3dgs_init.ply \
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
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR \
--multi_view_ncc_weight 0.0 \
--multi_view_geo_weight 0.0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/915/buaaNet_noMask_SGCR_curveNormalLoss \
--iteration 30000 \
--skip_train

5. 带Mask 但只 对colmap 求法线Loss	[test] PSNR: 21.0243  SSIM: 0.5710  LPIPS: 0.4088 [16/09 03:53:15]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/915/buaaNet_noMask_SGCR_colmapNormalLoss \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/buaa_net_simple-4/curve_3dgs_init.ply \
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
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--colmap_PGSR \
--multi_view_ncc_weight 0.0 \
--multi_view_geo_weight 0.0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/915/buaaNet_noMask_SGCR_colmapNormalLoss \
--iteration 30000 \
--skip_train

6. 训一版baseline的sh=0		做对比

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/GS_output/buaaNet_sh0 \
--eval \
--disable_viewer \
--sh_degree 0

cd /data1/jhc/storage_of_code/gs_pro6000

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/GS_output/buaaNet_sh0 \
--iteration 30000 \
--skip_train

[test] PSNR: 21.0403  SSIM: 0.5844  LPIPS: 0.4088 [16/09 15:16:39]

7. 训一版不带Mask，没有SGCR的sh=0	和	训一版有Mask的	做对比

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/915/buaaNet_noMask_noSGCR \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--sh_degree 0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/915/buaaNet_noMask_noSGCR \
--iteration 30000 \
--skip_train

[test] PSNR: 21.0413  SSIM: 0.5917  LPIPS: 0.3764 [16/09 15:08:17]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/915/buaaNet_Mask_noSGCR \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/915/buaaNet_Mask_noSGCR \
--iteration 30000 \
--skip_train

[test] PSNR: 21.1204  SSIM: 0.5729  LPIPS: 0.4069 [16/09 15:45:50]

# 对地面复杂纹理无光照进行法线Loss实验（无SGCR）

1. 只对colmap点加入法线Loss

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask_colmapOnlynormal \
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
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--colmap_PGSR \
--multi_view_ncc_weight 0.0 \
--multi_view_geo_weight 0.0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask_colmapOnlynormal \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask_colmapOnlynormal \
--iteration 30000 \
--eval \
--skip_train

[test] PSNR: 26.2969  SSIM: 0.9004  LPIPS: 0.1239 [17/09 12:07:41]

2. 只对 curve点 单独加法线Loss

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask_curveOnlynormal \
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
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR \
--multi_view_ncc_weight 0.0 \
--multi_view_geo_weight 0.0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask_curveOnlynormal \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask_curveOnlynormal \
--iteration 30000 \
--eval \
--skip_train

[test] PSNR: 25.7811  SSIM: 0.8974  LPIPS: 0.1277 [17/09 12:51:19]

3. 对colmap点加入法线Loss以及另两个Loss

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask_colmapPGSR_withNormal \
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
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--colmap_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask_colmapPGSR_withNormal \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask_colmapPGSR_withNormal \
--iteration 30000 \
--eval \
--skip_train

4. 对curve点加入法线Loss以及另两个Loss

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask_curvePGSR_withNormal \
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
-m /data2/jhc/output/3dgs_output/910/Curve_mask_curvePGSR_withNormal \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask_curvePGSR_withNormal \
--iteration 30000 \
--eval \
--skip_train

# 补做融合迭代数次数的消融实验

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 15000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask2 \
--iteration 30000 \
--skip_train

[test] PSNR: 26.5236  SSIM: 0.9063  LPIPS: 0.1156 [18/09 18:33:55]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask3 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 10000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask3 \
--iteration 30000 \
--skip_train

[test] PSNR: 27.2424  SSIM: 0.9224  LPIPS: 0.0943 [18/09 19:27:43]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask4 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 5000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask4 \
--iteration 30000 \
--skip_train

[test] PSNR: 27.6700  SSIM: 0.9263  LPIPS: 0.0858 [18/09 18:13:20]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask5 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 1 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask5 \
--iteration 30000 \
--skip_train

[test] PSNR: 27.7096  SSIM: 0.9302  LPIPS: 0.0861 [18/09 18:54:00]








