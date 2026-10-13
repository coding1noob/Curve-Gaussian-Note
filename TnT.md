
# Train

1. 

**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/TnT/Train \
-m output/test/Train \
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
Simplyfill3 填充后总点数: 533106 points

python test_colmap_reader.py \
-s /home/gamma/rosbags/TnT/Train \
-m output/test/Train \
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

---

开训
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/TnT/Train \
-m /data1/data/jhc/output/curve_output/Train \
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
/data1/data/jhc/output/curve_output/Train/curve_3dgs_init.ply \
/data1/data/jhc/datasets/TnT/Train \
/data1/data/jhc/output/3dgs_output/Train \
1

2. 微调整，线条变细，更捕捉细线
datasets=Train
project=Train2
cd /data1/jhc/storage_of_code/Curve-Gaussian-Note
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/TnT/"$datasets" \
-m /data2/jhc/output/curve_output/TnT/"$project" \
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
-s /data1/jhc/datasets/TnT/"$datasets" \
-m /data2/jhc/output/3dgs_output/TnT/"$project" \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/TnT/"$project"/curve_3dgs_init.ply \
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
-s /data1/jhc/datasets/TnT/"$datasets" \
-m /data2/jhc/output/3dgs_output/TnT/"$project" \
--iteration 30000 \
--skip_train
[test] PSNR: 20.2353  SSIM: 0.7007  LPIPS: 0.3155 [06/10 16:22:50]

3. 前面忘记加SGCR了，现在加
datasets=Train
project=Train3
cd /data1/jhc/storage_of_code/Curve-Gaussian-Note
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/TnT/"$datasets" \
-m /data2/jhc/output/curve_output/TnT/"$project" \
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
-s /data1/jhc/datasets/TnT/"$datasets" \
-m /data2/jhc/output/3dgs_output/TnT/"$project" \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/TnT/"$project"/curve_3dgs_init.ply \
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
-s /data1/jhc/datasets/TnT/"$datasets" \
-m /data2/jhc/output/3dgs_output/TnT/"$project" \
--iteration 30000 \
--skip_train

[test] PSNR: 20.2585  SSIM: 0.7012  LPIPS: 0.3141 [06/10 18:38:32]

4. 用test3_test.py跑出来的边缘图，涂黑，粗线

datasets=Train
project=Train4
cd /data1/jhc/storage_of_code/Curve-Gaussian-Note
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/TnT/"$datasets" \
-m /data2/jhc/output/curve_output/TnT/"$project" \
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
-s /data1/jhc/datasets/TnT/"$datasets" \
-m /data2/jhc/output/3dgs_output/TnT/"$project" \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/TnT/"$project"/curve_3dgs_init.ply \
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
-s /data1/jhc/datasets/TnT/"$datasets" \
-m /data2/jhc/output/3dgs_output/TnT/"$project" \
--iteration 30000 \
--skip_train
[test] PSNR: 19.9014  SSIM: 0.6925  LPIPS: 0.3248 [08/10 13:26:29]

# M60

**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/TnT/M60 \
-m output/test/M60 \
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
Simplyfill3 填充后总点数: 445212 points

开训
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/TnT/M60 \
-m /data1/data/jhc/output/curve_output/M60 \
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
/data1/data/jhc/output/curve_output/M60/curve_3dgs_init.ply \
/data1/data/jhc/datasets/TnT/M60 \
/data1/data/jhc/output/3dgs_output/M60 \
1

2. 微调整，线条变细，更捕捉细线
datasets=M60
project=M60-2
cd /data1/jhc/storage_of_code/Curve-Gaussian-Note
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/TnT/"$datasets" \
-m /data2/jhc/output/curve_output/TnT/"$project" \
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
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/TnT/"$datasets" \
-m /data2/jhc/output/3dgs_output/TnT/"$project" \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/TnT/"$project"/curve_3dgs_init.ply \
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
-s /data1/jhc/datasets/TnT/"$datasets" \
-m /data2/jhc/output/3dgs_output/TnT/"$project" \
--iteration 30000 \
--skip_train
[test] PSNR: 21.2242  SSIM: 0.7555  LPIPS: 0.3400 [06/10 16:21:50]

3. 前面忘记加SGCR了，现在加

datasets=M60
project=M60-3
cd /data1/jhc/storage_of_code/Curve-Gaussian-Note
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/TnT/"$datasets" \
-m /data2/jhc/output/curve_output/TnT/"$project" \
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
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/TnT/"$datasets" \
-m /data2/jhc/output/3dgs_output/TnT/"$project" \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/TnT/"$project"/curve_3dgs_init.ply \
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
-s /data1/jhc/datasets/TnT/"$datasets" \
-m /data2/jhc/output/3dgs_output/TnT/"$project" \
--iteration 30000 \
--skip_train

[test] PSNR: 21.1866  SSIM: 0.7550  LPIPS: 0.3406 [06/10 18:42:33]

# 卡车

1. 
**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/TnT/Truck \
-m output/test/Truck \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 0.1 \
--fill_y_threshold 0.1 \
--fill_z_threshold 0.1 \
--fill_grid_resX 300 \
--fill_grid_resY 300 \
--fill_grid_resZ 300 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05
Simplyfill3 填充后总点数: 451267 points

开训
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/TnT/Truck \
-m /data1/data/jhc/output/curve_output/Truck \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.1 \
--fill_y_threshold 0.1 \
--fill_z_threshold 0.1 \
--fill_grid_resX 300 \
--fill_grid_resY 300 \
--fill_grid_resZ 300 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--SGCR \
--final_opacity_cull 0.8

./nextStep.sh \
/data1/data/jhc/output/curve_output/Truck/curve_3dgs_init.ply \
/data1/data/jhc/datasets/TnT/Truck \
/data1/data/jhc/output/3dgs_output/Truck \
1

指标：
PSNR：	21.8062
SSIM：	0.7448
LPIPS：	0.3002

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python render_curve.py \
-s /data1/data/jhc/datasets/TnT/Truck \
-m /data1/data/jhc/output/3dgs_output/Truck \
--curve_ply /data1/data/jhc/output/curve_output/Truck/curve_3dgs_init.ply \
--eval \
--skip_train

2. 用test3_test.py跑出来的边缘图，涂黑，粗线
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/TnT/Truck \
-m /data1/data/jhc/output/curve_output/Truck3 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.1 \
--fill_y_threshold 0.1 \
--fill_z_threshold 0.1 \
--fill_grid_resX 300 \
--fill_grid_resY 300 \
--fill_grid_resZ 300 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--SGCR \
--final_opacity_cull 0.8

./nextStep.sh \
/data1/data/jhc/output/curve_output/Truck3/curve_3dgs_init.ply \
/data1/data/jhc/datasets/TnT/Truck \
/data1/data/jhc/output/3dgs_output/Truck3 \
2

[test] PSNR: 21.8427  SSIM: 0.7471  LPIPS: 0.2992 [08/10 14:36:17]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python render_curve.py \
-s /data1/data/jhc/datasets/TnT/Truck \
-m /data1/data/jhc/output/3dgs_output/Truck3 \
--curve_ply /data1/data/jhc/output/curve_output/Truck3/curve_3dgs_init.ply \
--eval \
--skip_train

3. 在2的基础上不用滤波

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/TnT/Truck \
-m /data1/data/jhc/output/curve_output/Truck4 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.1 \
--fill_y_threshold 0.1 \
--fill_z_threshold 0.1 \
--fill_grid_resX 300 \
--fill_grid_resY 300 \
--fill_grid_resZ 300 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 0 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--SGCR \
--final_opacity_cull 0.8

./nextStep.sh \
/data1/data/jhc/output/curve_output/Truck4/curve_3dgs_init.ply \
/data1/data/jhc/datasets/TnT/Truck \
/data1/data/jhc/output/3dgs_output/Truck4 \
2

[test] PSNR: 21.8491  SSIM: 0.7473  LPIPS: 0.2991 [08/10 16:32:43]








