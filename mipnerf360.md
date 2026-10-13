
1. room

**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/mipnerf360/mipnerf360/room \
-m output/test/room \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3

2. bicycle

**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/mipnerf360/mipnerf360/bicycle \
-m output/test/bicycle \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3

3. stump

**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/mipnerf360/mipnerf360/stump \
-m output/test/stump \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3

4. bonsai

**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/mipnerf360/mipnerf360/bonsai \
-m output/test/bonsai \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 5

5. counter

**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/mipnerf360/mipnerf360/counter \
-m output/test/counter \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3

6. garden

**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/mipnerf360/mipnerf360/garden \
-m output/test/garden \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3

7. kitchen

**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/mipnerf360/mipnerf360/kitchen \
-m output/test/kitchen \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3

# 10.4晚执行

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/mipnerf360/bonsai \
-m /data1/data/jhc/output/curve_output/bonsai \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 5
--SGCR \
--final_opacity_cull 0.8

./nextStep.sh \
/data1/data/jhc/output/curve_output/bonsai/curve_3dgs_init.ply \
/data1/data/jhc/datasets/mipnerf360/bonsai \
/data1/data/jhc/output/3dgs_output/bonsai \
1

./nextStep_r1.sh \
/data1/data/jhc/output/curve_output/bonsai/curve_3dgs_init.ply \
/data1/data/jhc/datasets/mipnerf360/bonsai \
/data1/data/jhc/output/3dgs_output/bonsai \
1

project=stump
cd /data1/data/jhc/projects/Curve-Gaussian-Note
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/mipnerf360/"$project" \
-m /data1/data/jhc/output/curve_output/"$project" \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3
--SGCR \
--final_opacity_cull 0.8

./nextStep.sh \
/data1/data/jhc/output/curve_output/"$project"/curve_3dgs_init.ply \
/data1/data/jhc/datasets/mipnerf360/"$project" \
/data1/data/jhc/output/3dgs_output/"$project" \
1

---
data=stump
project=stump2
cd /data1/data/jhc/projects/Curve-Gaussian-Note
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/mipnerf360/"$data" \
-m /data1/data/jhc/output/curve_output/"$project" \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
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

./nextStep.sh \
/data1/data/jhc/output/curve_output/"$project"/curve_3dgs_init.ply \
/data1/data/jhc/datasets/mipnerf360/"$data" \
/data1/data/jhc/output/3dgs_output/"$project" \
1
[test] PSNR: 26.7902  SSIM: 0.7730  LPIPS: 0.2431 [06/10 20:43:44]
---


project=room
cd /data1/data/jhc/projects/Curve-Gaussian-Note
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/mipnerf360/"$project" \
-m /data1/data/jhc/output/curve_output/"$project" \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3
--SGCR \
--final_opacity_cull 0.8

./nextStep.sh \
/data1/data/jhc/output/curve_output/"$project"/curve_3dgs_init.ply \
/data1/data/jhc/datasets/mipnerf360/"$project" \
/data1/data/jhc/output/3dgs_output/"$project" \
1

project=kitchen
cd /data1/data/jhc/projects/Curve-Gaussian-Note
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/mipnerf360/"$project" \
-m /data1/data/jhc/output/curve_output/"$project" \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3
--SGCR \
--final_opacity_cull 0.8

./nextStep.sh \
/data1/data/jhc/output/curve_output/"$project"/curve_3dgs_init.ply \
/data1/data/jhc/datasets/mipnerf360/"$project" \
/data1/data/jhc/output/3dgs_output/"$project" \
1

-----

project=bicycle
cd /data1/data/jhc/projects/Curve-Gaussian-Note
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/mipnerf360/"$project" \
-m /data1/data/jhc/output/curve_output/"$project" \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3
--SGCR \
--final_opacity_cull 0.8

./nextStep.sh \
/data1/data/jhc/output/curve_output/"$project"/curve_3dgs_init.ply \
/data1/data/jhc/datasets/mipnerf360/"$project" \
/data1/data/jhc/output/3dgs_output/"$project" \
2

project=counter
cd /data1/data/jhc/projects/Curve-Gaussian-Note
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/mipnerf360/"$project" \
-m /data1/data/jhc/output/curve_output/"$project" \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3
--SGCR \
--final_opacity_cull 0.8

./nextStep.sh \
/data1/data/jhc/output/curve_output/"$project"/curve_3dgs_init.ply \
/data1/data/jhc/datasets/mipnerf360/"$project" \
/data1/data/jhc/output/3dgs_output/"$project" \
2

project=garden
cd /data1/data/jhc/projects/Curve-Gaussian-Note
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/mipnerf360/"$project" \
-m /data1/data/jhc/output/curve_output/"$project" \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3
--SGCR \
--final_opacity_cull 0.8

./nextStep.sh \
/data1/data/jhc/output/curve_output/"$project"/curve_3dgs_init.ply \
/data1/data/jhc/datasets/mipnerf360/"$project" \
/data1/data/jhc/output/3dgs_output/"$project" \
2

# bicycle特调

1. 
project=bicycle
cd /data1/data/jhc/projects/Curve-Gaussian-Note
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/mipnerf360/"$project" \
-m /data2/jhc/output/curve_output/mipnerf360/"$project" \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3
--SGCR \
--final_opacity_cull 0.8

cd ../gs_pro6000

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/mipnerf360/"$project" \
-m /data2/jhc/output/3dgs_output/mipnerf360/"$project" \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/mipnerf360/"$project"/curve_3dgs_init.ply \
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
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/mipnerf360/"$project" \
-m /data2/jhc/output/3dgs_output/mipnerf360/"$project" \
--iteration 30000 \
--skip_train

[test] PSNR: 25.2663  SSIM: 0.7612  LPIPS: 0.2277 [05/10 19:28:23]

2. 这个应该是细线？
datasets=bicycle
project=bicycle2
cd /data1/jhc/storage_of_code/Curve-Gaussian-Note
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/mipnerf360/"$datasets" \
-m /data2/jhc/output/curve_output/mipnerf360/"$project" \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
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

cd ../gs_pro6000

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/mipnerf360/"$datasets" \
-m /data2/jhc/output/3dgs_output/mipnerf360/"$project" \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/mipnerf360/"$project"/curve_3dgs_init.ply \
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
CUDA_VISIBLE_DEVICES=3 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/mipnerf360/"$datasets" \
-m /data2/jhc/output/3dgs_output/mipnerf360/"$project" \
--iteration 30000 \
--skip_train
[test] PSNR: 25.0684  SSIM: 0.7595  LPIPS: 0.2282 [06/10 19:16:13]

3. 再用edge_PidiNet(未涂黑,原分辨率)跑一次，只不过记得加换行
datasets=bicycle
project=bicycle3
cd /data1/jhc/storage_of_code/Curve-Gaussian-Note
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/mipnerf360/"$datasets" \
-m /data2/jhc/output/curve_output/mipnerf360/"$project" \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
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

cd ../gs_pro6000

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/mipnerf360/"$datasets" \
-m /data2/jhc/output/3dgs_output/mipnerf360/"$project" \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/mipnerf360/"$project"/curve_3dgs_init.ply \
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
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/mipnerf360/"$datasets" \
-m /data2/jhc/output/3dgs_output/mipnerf360/"$project" \
--iteration 30000 \
--skip_train

[test] PSNR: 25.0419  SSIM: 0.7598  LPIPS: 0.2276 [06/10 23:44:47]

# garden 特调

1. 
project=garden
cd /data1/data/jhc/projects/Curve-Gaussian-Note
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/mipnerf360/"$project" \
-m /data2/jhc/output/curve_output/mipnerf360/"$project" \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3
--SGCR \
--final_opacity_cull 0.8

cd ../gs_pro6000

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/mipnerf360/"$project" \
-m /data2/jhc/output/3dgs_output/mipnerf360/"$project" \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/mipnerf360/"$project"/curve_3dgs_init.ply \
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
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/mipnerf360/"$project" \
-m /data2/jhc/output/3dgs_output/mipnerf360/"$project" \
--iteration 30000 \
--skip_train

[test] PSNR: 27.2799  SSIM: 0.8544  LPIPS: 0.1287 [05/10 21:03:52]

--------------------

2. 
**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/mipnerf360/mipnerf360/garden \
-m output/test/garden \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 300 \
--fill_grid_resY 300 \
--fill_grid_resZ 300 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 0 \
--outlier_nb_neighbors 0 \
--outlier_std_ratio 0
Simplyfill3 填充后总点数: 379218 points

正式跑
S=garden
M=garden_nofilter
cd /data1/data/jhc/projects/Curve-Gaussian-Note
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/mipnerf360/"$S" \
-m /data2/jhc/output/curve_output/mipnerf360/"$M" \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 300 \
--fill_grid_resY 300 \
--fill_grid_resZ 300 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 0 \
--outlier_nb_neighbors 0 \
--outlier_std_ratio 0
--SGCR \
--final_opacity_cull 0.8

cd ../gs_pro6000

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/mipnerf360/"$S" \
-m /data2/jhc/output/3dgs_output/mipnerf360/"$M" \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/mipnerf360/"$M"/curve_3dgs_init.ply \
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
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/mipnerf360/"$S" \
-m /data2/jhc/output/3dgs_output/mipnerf360/"$M" \
--iteration 30000 \
--skip_train

[test] PSNR: 27.3893  SSIM: 0.8597  LPIPS: 0.1231 [05/10 22:14:26]

3. 尝试全PGSR

project=garden
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/mipnerf360/"$project" \
-m /data2/jhc/output/3dgs_output/mipnerf360/garden_fullPGSR \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/mipnerf360/"$project"/curve_3dgs_init.ply \
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
--curve_PGSR \
--colmap_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/mipnerf360/"$project" \
-m /data2/jhc/output/3dgs_output/mipnerf360/garden_fullPGSR \
--iteration 30000 \
--skip_train

[test] PSNR: 26.7792  SSIM: 0.8501  LPIPS: 0.1320 [05/10 22:29:03]

4. 试试细线1

S=garden
M=garden_thinLine1
cd /data1/data/jhc/projects/Curve-Gaussian-Note
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/mipnerf360/"$S" \
-m /data2/jhc/output/curve_output/mipnerf360/"$M" \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 300 \
--fill_grid_resY 300 \
--fill_grid_resZ 300 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 0 \
--outlier_nb_neighbors 0 \
--outlier_std_ratio 0

cd ../gs_pro6000

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/mipnerf360/"$S" \
-m /data2/jhc/output/3dgs_output/mipnerf360/"$M" \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/mipnerf360/"$M"/curve_3dgs_init.ply \
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
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/mipnerf360/"$S" \
-m /data2/jhc/output/3dgs_output/mipnerf360/"$M" \
--iteration 30000 \
--skip_train
[test] PSNR: 26.3456  SSIM: 0.8512  LPIPS: 0.1285 [06/10 22:10:55]

5. 试试细线2

S=garden
M=garden_thinLine2
cd /data1/data/jhc/projects/Curve-Gaussian-Note
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/mipnerf360/"$S" \
-m /data2/jhc/output/curve_output/mipnerf360/"$M" \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 300 \
--fill_grid_resY 300 \
--fill_grid_resZ 300 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 0 \
--outlier_nb_neighbors 0 \
--outlier_std_ratio 0 \
--SGCR \
--final_opacity_cull 0.8

cd ../gs_pro6000

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/mipnerf360/"$S" \
-m /data2/jhc/output/3dgs_output/mipnerf360/"$M" \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/mipnerf360/"$M"/curve_3dgs_init.ply \
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
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/mipnerf360/"$S" \
-m /data2/jhc/output/3dgs_output/mipnerf360/"$M" \
--iteration 30000 \
--skip_train
[test] PSNR: 26.4833  SSIM: 0.8526  LPIPS: 0.1274 [06/10 21:50:44]






























