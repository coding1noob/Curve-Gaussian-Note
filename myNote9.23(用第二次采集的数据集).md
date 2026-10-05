
# net6

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

## 改进render_normal.py

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

# net930

1. 
**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/930/net930-0 \
-m output/test/net930-0 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 1 \
--fill_y_threshold 0.2 \
--fill_grid_resX 300 \
--fill_grid_resY 20 \
--fill_grid_resZ 300 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3
Simplyfill3 填充后总点数: 499974 points

---

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net930-0 \
-m /data1/data/jhc/output/curve_output/net930-0 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 1 \
--fill_y_threshold 0.2 \
--fill_grid_resX 300 \
--fill_grid_resY 20 \
--fill_grid_resZ 300 \
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

cd ../3dgs_note/

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net930-0 \
-m /data1/data/jhc/output/3dgs_output/net930-0 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net930-0/curve_3dgs_init.ply \
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
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net930-0 \
-m /data1/data/jhc/output/3dgs_output/net930-0 \
--iteration 30000 \
--skip_train

2. 
**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/930/net930-1 \
-m output/test/net930-1 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 1 \
--fill_y_threshold 0.2 \
--fill_grid_resX 300 \
--fill_grid_resY 20 \
--fill_grid_resZ 300 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3
Simplyfill3 填充后总点数: 418994 points

---

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net930-1 \
-m /data1/data/jhc/output/curve_output/net930-1 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 1 \
--fill_y_threshold 0.2 \
--fill_grid_resX 300 \
--fill_grid_resY 20 \
--fill_grid_resZ 300 \
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

cd ../3dgs_note/

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net930-1 \
-m /data1/data/jhc/output/3dgs_output/net930-1 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net930-1/curve_3dgs_init.ply \
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
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net930-1 \
-m /data1/data/jhc/output/3dgs_output/net930-1 \
--iteration 30000 \
--skip_train

3. 
**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/930/net930-2 \
-m output/test/net930-2 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 1 \
--fill_y_threshold 0.2 \
--fill_grid_resX 300 \
--fill_grid_resY 20 \
--fill_grid_resZ 300 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3
Simplyfill3 填充后总点数: 557612 points

-----

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net930-2 \
-m /data1/data/jhc/output/curve_output/net930-2 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 1 \
--fill_y_threshold 0.2 \
--fill_grid_resX 300 \
--fill_grid_resY 20 \
--fill_grid_resZ 300 \
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

cd ../3dgs_note/

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net930-2 \
-m /data1/data/jhc/output/3dgs_output/net930-2 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net930-2/curve_3dgs_init.ply \
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
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net930-2 \
-m /data1/data/jhc/output/3dgs_output/net930-2 \
--iteration 30000 \
--skip_train

4. 
**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/930/net930-3 \
-m output/test/net930-3 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 3 \
--fill_y_threshold 0.2 \
--fill_grid_resX 300 \
--fill_grid_resY 20 \
--fill_grid_resZ 300 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3
Simplyfill3 填充后总点数: 698812 points

--------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net930-3 \
-m /data1/data/jhc/output/curve_output/net930-3 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 3 \
--fill_y_threshold 0.2 \
--fill_grid_resX 300 \
--fill_grid_resY 20 \
--fill_grid_resZ 300 \
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

cd ../3dgs_note/

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net930-3 \
-m /data1/data/jhc/output/3dgs_output/net930-3 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net930-3/curve_3dgs_init.ply \
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
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net930-3 \
-m /data1/data/jhc/output/3dgs_output/net930-3 \
--iteration 30000 \
--skip_train

5. 
**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/930/net930-4 \
-m output/test/net930-4 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 3 \
--fill_y_threshold 0.2 \
--fill_grid_resX 300 \
--fill_grid_resY 10 \
--fill_grid_resZ 300 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3
Simplyfill3 填充后总点数: 371046 points

----------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net930-4 \
-m /data1/data/jhc/output/curve_output/net930-4 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 3 \
--fill_y_threshold 0.2 \
--fill_grid_resX 300 \
--fill_grid_resY 10 \
--fill_grid_resZ 300 \
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

cd ../3dgs_note/

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net930-4 \
-m /data1/data/jhc/output/3dgs_output/net930-4 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net930-4/curve_3dgs_init.ply \
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
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net930-4 \
-m /data1/data/jhc/output/3dgs_output/net930-4 \
--iteration 30000 \
--skip_train

6. 
**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/930/net930-5 \
-m output/test/net930-5 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 3 \
--fill_y_threshold 0.2 \
--fill_z_threshold 1 \
--fill_grid_resX 300 \
--fill_grid_resY 10 \
--fill_grid_resZ 300 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3
Simplyfill3 填充后总点数: 410644 points

----------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net930-5 \
-m /data1/data/jhc/output/curve_output/net930-5 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 3 \
--fill_y_threshold 0.2 \
--fill_z_threshold 1 \
--fill_grid_resX 300 \
--fill_grid_resY 10 \
--fill_grid_resZ 300 \
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

cd ../3dgs_note/

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net930-5 \
-m /data1/data/jhc/output/3dgs_output/net930-5 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net930-5/curve_3dgs_init.ply \
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
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net930-5 \
-m /data1/data/jhc/output/3dgs_output/net930-5 \
--iteration 30000 \
--skip_train

7. 对于上面1~6重新启用black过的边缘图进行训练

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net930-0 \
-m /data1/data/jhc/output/3dgs_output/net930-black-0 \
--iteration 30000 \
--skip_train

------

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net930-3 \
-m /data1/data/jhc/output/3dgs_output/net930-black-3 \
--iteration 30000 \
--skip_train

------

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net930-1 \
-m /data1/data/jhc/output/3dgs_output/net930-black-1 \
--iteration 30000 \
--skip_train

------

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net930-2 \
-m /data1/data/jhc/output/3dgs_output/net930-black-2 \
--iteration 30000 \
--skip_train

------

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net930-4 \
-m /data1/data/jhc/output/3dgs_output/net930-black-4 \
--iteration 30000 \
--skip_train

------

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net930-5 \
-m /data1/data/jhc/output/3dgs_output/net930-black-5 \
--iteration 30000 \
--skip_train

# CUC数据集

1. cuc1

**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/CUC/cuc1 \
-m output/test/cuc1 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 0.5 \
--fill_y_threshold 0.2 \
--fill_z_threshold 1 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 10 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3

----------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python train.py \
-s /data1/data/jhc/datasets/cuc1 \
-m /data1/data/jhc/output/curve_output/cuc1 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.5 \
--fill_y_threshold 0.2 \
--fill_z_threshold 1 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 10 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3 \
--SGCR \
--final_opacity_cull 0.8

cd ../3dgs_note/

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/cuc1 \
-m /data1/data/jhc/output/3dgs_output/cuc1 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/cuc1/curve_3dgs_init.ply \
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
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/cuc1 \
-m /data1/data/jhc/output/3dgs_output/cuc1 \
--iteration 30000 \
--skip_train

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python render_curve.py \
-s /data1/data/jhc/datasets/cuc1 \
-m /data1/data/jhc/output/3dgs_output/cuc1 \
--curve_ply /data1/data/jhc/output/curve_output/cuc1/curve_3dgs_init.ply \
--eval \
--skip_train

**cuc1 参数细调**

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/cuc1 \
-m /data1/data/jhc/output/3dgs_output/cuc1-2 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/cuc1/curve_3dgs_init.ply \
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
-s /data1/data/jhc/datasets/cuc1 \
-m /data1/data/jhc/output/3dgs_output/cuc1-2 \
--iteration 30000 \
--skip_train

2. cuc2

**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/CUC/cuc2 \
-m output/test/cuc2 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 1 \
--fill_y_threshold 0.2 \
--fill_z_threshold 1 \
--fill_grid_resX 100 \
--fill_grid_resY 20 \
--fill_grid_resZ 100 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 10 \
--outlier_std_ratio 0.05 \
--camera_point_distance 5

----------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python train.py \
-s /data1/data/jhc/datasets/cuc2 \
-m /data1/data/jhc/output/curve_output/cuc2 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 1 \
--fill_y_threshold 0.2 \
--fill_z_threshold 1 \
--fill_grid_resX 100 \
--fill_grid_resY 20 \
--fill_grid_resZ 100 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 10 \
--outlier_std_ratio 0.05 \
--camera_point_distance 5 \
--SGCR \
--final_opacity_cull 0.8

cd ../3dgs_note/

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python train.py \
-s /data1/data/jhc/datasets/cuc2 \
-m /data1/data/jhc/output/3dgs_output/cuc2 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/cuc2/curve_3dgs_init.ply \
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
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/cuc2 \
-m /data1/data/jhc/output/3dgs_output/cuc2 \
--iteration 30000 \
--skip_train

3. cuc3

**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/CUC/cuc3 \
-m output/test/cuc3 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 0.2 \
--fill_y_threshold 0.2 \
--fill_z_threshold 0.2 \
--fill_grid_resX 100 \
--fill_grid_resY 20 \
--fill_grid_resZ 100 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 10 \
--outlier_std_ratio 0.05 \
--camera_point_distance 5

----------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/cuc3 \
-m /data1/data/jhc/output/curve_output/cuc3 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.2 \
--fill_y_threshold 0.2 \
--fill_z_threshold 0.2 \
--fill_grid_resX 100 \
--fill_grid_resY 20 \
--fill_grid_resZ 100 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 10 \
--outlier_std_ratio 0.05 \
--camera_point_distance 5 \
--SGCR \
--final_opacity_cull 0.8

cd ../3dgs_note/

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/cuc3 \
-m /data1/data/jhc/output/3dgs_output/cuc3 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/cuc3/curve_3dgs_init.ply \
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
-s /data1/data/jhc/datasets/cuc3 \
-m /data1/data/jhc/output/3dgs_output/cuc3 \
--iteration 30000 \
--skip_train

# 10.2

1. 
**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/102/102-1 \
-m output/test/102-1 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 3 \
--fill_y_threshold 0.2 \
--fill_z_threshold 1 \
--fill_grid_resX 300 \
--fill_grid_resY 10 \
--fill_grid_resZ 300 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3
Simplyfill3 填充后总点数: 693240 points

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python train.py \
-s /data1/data/jhc/datasets/102-1 \
-m /data1/data/jhc/output/curve_output/102-1 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 3 \
--fill_y_threshold 0.2 \
--fill_z_threshold 1 \
--fill_grid_resX 300 \
--fill_grid_resY 10 \
--fill_grid_resZ 300 \
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

cd ../3dgs_note/

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python train.py \
-s /data1/data/jhc/datasets/102-1 \
-m /data1/data/jhc/output/3dgs_output/102-1 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/102-1/curve_3dgs_init.ply \
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
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/102-1 \
-m /data1/data/jhc/output/3dgs_output/102-1 \
--iteration 30000 \
--skip_train

2. 
python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/102/102-2 \
-m output/test/102-2 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 3 \
--fill_y_threshold 0.2 \
--fill_z_threshold 1 \
--fill_grid_resX 300 \
--fill_grid_resY 10 \
--fill_grid_resZ 300 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 5
Simplyfill3 填充后总点数: 432857 points

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/102-2 \
-m /data1/data/jhc/output/curve_output/102-2 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 3 \
--fill_y_threshold 0.2 \
--fill_z_threshold 1 \
--fill_grid_resX 300 \
--fill_grid_resY 10 \
--fill_grid_resZ 300 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 5 \
--SGCR \
--final_opacity_cull 0.8

cd ../3dgs_note/

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/102-2 \
-m /data1/data/jhc/output/3dgs_output/102-2 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/102-2/curve_3dgs_init.ply \
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
-s /data1/data/jhc/datasets/102-2 \
-m /data1/data/jhc/output/3dgs_output/102-2 \
--iteration 30000 \
--skip_train

# 10.3

1. 
**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/103/103-1 \
-m output/test/103-1 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 3 \
--fill_y_threshold 0.2 \
--fill_z_threshold 1 \
--fill_grid_resX 300 \
--fill_grid_resY 10 \
--fill_grid_resZ 300 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3
Simplyfill3 填充后总点数: 699232 points

**编辑文件nextStep.sh：**
	#!/bin/bash
	curve_source="$1"
	S="$2"
	M="$3"
	device="$4"

	echo "===== 配置 ====="
	echo "曲线先验: $curve_source"
	echo "数据集S: $S"
	echo "输出目录M: $M"
	echo "GPU device: $device"
	echo "================="

	cd ../3dgs_note/

	unset CUDA_VISIBLE_DEVICES
	CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES="$device" \
	python train.py \
	-s "$S" \
	-m "$M" \
	--eval \
	--disable_viewer \
	--curvegs "$curve_source" \
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
	CUDA_VISIBLE_DEVICES="$device" \
	TORCH_HOME=/data1/data/jhc/torch_cache \
	python render_metrics.py \
	-s "$S" \
	-m "$M" \
	--iteration 30000 \
	--skip_train

然后使用：

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python train.py \
-s /data1/data/jhc/datasets/103-1 \
-m /data1/data/jhc/output/curve_output/103-1 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 3 \
--fill_y_threshold 0.2 \
--fill_z_threshold 1 \
--fill_grid_resX 300 \
--fill_grid_resY 10 \
--fill_grid_resZ 300 \
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

./nextStep.sh \
/data1/data/jhc/output/curve_output/103-1/curve_3dgs_init.ply \
/data1/data/jhc/datasets/103-1 \
/data1/data/jhc/output/3dgs_output/103-1 \
0

2. 103-2
**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/103/103-2 \
-m output/test/103-2 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 3 \
--fill_y_threshold 0.2 \
--fill_z_threshold 1 \
--fill_grid_resX 300 \
--fill_grid_resY 10 \
--fill_grid_resZ 300 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3
Simplyfill3 填充后总点数: 625975 points

然后使用：

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/103-2 \
-m /data1/data/jhc/output/curve_output/103-2 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 3 \
--fill_y_threshold 0.2 \
--fill_z_threshold 1 \
--fill_grid_resX 300 \
--fill_grid_resY 10 \
--fill_grid_resZ 300 \
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

./nextStep.sh \
/data1/data/jhc/output/curve_output/103-2/curve_3dgs_init.ply \
/data1/data/jhc/datasets/103-2 \
/data1/data/jhc/output/3dgs_output/103-2 \
1

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python render_curve.py \
-s /data1/data/jhc/datasets/103-2 \
-m /data1/data/jhc/output/3dgs_output/103-2 \
--curve_ply /data1/data/jhc/output/curve_output/103-2/curve_3dgs_init.ply \
--eval \
--skip_train

3. 103-2 微改参数

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python train.py \
-s /data1/data/jhc/datasets/103-2 \
-m /data1/data/jhc/output/3dgs_output/103-2-1 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/103-2/curve_3dgs_init.ply \
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
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/103-2 \
-m /data1/data/jhc/output/3dgs_output/103-2-1 \
--iteration 30000 \
--skip_train

4. 103-2 不改参数（重复实验）

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python train.py \
-s /data1/data/jhc/datasets/103-2 \
-m /data1/data/jhc/output/3dgs_output/103-2-2 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/103-2/curve_3dgs_init.ply \
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
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/103-2 \
-m /data1/data/jhc/output/3dgs_output/103-2-2 \
--iteration 30000 \
--skip_train

5. 103-2 手工补点

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/103-2 \
-m /data1/data/jhc/output/3dgs_output/103-2_manual \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/103-2_manual/curve_3dgs_init.ply \
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
-s /data1/data/jhc/datasets/103-2 \
-m /data1/data/jhc/output/3dgs_output/103-2_manual \
--iteration 30000 \
--skip_train
































