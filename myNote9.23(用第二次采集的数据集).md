
**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/net52 \
-m output/test/net52v1 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 1 \
--fill_y_threshold 0.5 \
--fill_grid_resX 300 \
--fill_grid_resY 50 \
--fill_grid_resZ 100 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3

python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/net6 \
-m output/test/net6v2 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 1 \
--fill_y_threshold 0.5 \
--fill_grid_resX 300 \
--fill_grid_resY 50 \
--fill_grid_resZ 100 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3

真正进行实验

0. 跑baseline

cd ../gaussian-splatting
conda activate gs_pro6000

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/net52 \
-m /data2/jhc/output/3dgs_output/921/net52_gs \
--eval \
--disable_viewer

cd ../gs_pro6000
conda activate curveGS

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/net52 \
-m /data2/jhc/output/3dgs_output/921/net52_gs \
--iteration 30000 \
--skip_train
[test] PSNR: 19.7918  SSIM: 0.6525  LPIPS: 0.3443 [23/09 17:27:42]

----------------------------------------------------------------------

cd ../gaussian-splatting
conda activate gs_pro6000

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/net6 \
-m /data2/jhc/output/3dgs_output/921/net6_gs \
--eval \
--disable_viewer

cd ../gs_pro6000
conda activate curveGS

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/net6 \
-m /data2/jhc/output/3dgs_output/921/net6_gs \
--iteration 30000 \
--skip_train
[test] PSNR: 19.1494  SSIM: 0.5757  LPIPS: 0.3582 [23/09 14:06:52]

网没补齐！冲！

2. net6

完了网都没补上，再改进：

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/curve_output/net6v2 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 1 \
--fill_y_threshold 0.5 \
--fill_grid_resX 300 \
--fill_grid_resY 50 \
--fill_grid_resZ 100 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3 \
--SGCR \
--final_opacity_cull 0.8

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_noPGSR \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net6v2/curve_3dgs_init.ply \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_noPGSR \
--iteration 30000 \
--skip_train

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python render_curve.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_noPGSR \
--curve_ply /data1/data/jhc/output/curve_output/net6v2/curve_3dgs_init.ply \
--eval \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_PGSR.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_noPGSR \
--iteration 30000 \
--eval \
--skip_train

[test] PSNR: 18.9222  SSIM: 0.5540  LPIPS: 0.3431 [23/09 15:46:53]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python render_2.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_noPGSR \
--iteration 30000 \
--curve_only \
--skip_train

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python render_2.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_noPGSR \
--iteration 30000 \
--colmap_only \
--skip_train

再试试PGSR呢？

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR \
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
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_PGSR.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR \
--iteration 30000 \
--eval \
--skip_train

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python render_2.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR \
--iteration 30000 \
--curve_only \
--skip_train

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python render_2.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR \
--iteration 30000 \
--colmap_only \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_PGSR.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR \
--iteration 30000 \
--eval \
--skip_train

[test] PSNR: 19.1395  SSIM: 0.5693  LPIPS: 0.3370 [23/09 16:58:27]

# 改进render_normal

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_normal.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_noPGSR \
--iteration 30000 \
--depth_normal_threshold -1 \
--skip_train \
--curve_only

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_normal.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_noPGSR \
--iteration 30000 \
--depth_normal_threshold 0.1 \
--skip_train \
--curve_only

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_normal.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_noPGSR \
--iteration 30000 \
--depth_normal_threshold 0.05 \
--skip_train \
--curve_only

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_normal.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_noPGSR \
--iteration 30000 \
--depth_normal_threshold 0.01 \
--skip_train \
--curve_only


CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_normal.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR \
--iteration 30000 \
--depth_normal_threshold -1 \
--skip_train \
--curve_only

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_normal.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR \
--iteration 30000 \
--depth_normal_threshold 0.1 \
--skip_train \
--curve_only

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_normal.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR \
--iteration 30000 \
--depth_normal_threshold 0.01 \
--skip_train \
--curve_only





































