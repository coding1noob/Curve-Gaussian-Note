
# 现实数据集

## 无人院

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net_simple \
--eval \
--iterations 30000 \
--fill_method simplefill \
--trajectory_root \
--fill_grid_resX 100 \
--fill_grid_resY 25 \
--fill_grid_resZ 50 \
--n_gaussians 3 \
--simple \
--init_voxel_size 0.01 \
--similarity_threshold 0.92 \
--distance_threshold 0.03 \
--opacity_cull 0.02 \
--opacity_cull_second 0.08 \
--mask_threshold 0.02

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
[test] PSNR: 21.4194  SSIM: 0.6009  LPIPS: 0.3520 [20/09 08:23:09]
[test] PSNR: 21.3511  SSIM: 0.6006  LPIPS: 0.3538 [20/09 02:41:25]

画图用：
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_1_pic \
--eval \
--disable_viewer \
--iterations 5000 \
--save_iterations 1 500 1000 1500 2000 3500 5000 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--curve_PGSR

for iter in 1 500 1000 1500 2000 3500 5000
do
	unset CUDA_VISIBLE_DEVICES
	CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_2.py \
	-s /data1/jhc/datasets/buaa_net \
	-m /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_1_pic \
	--iteration "$iter" \
	--curve_only \
	--skip_train
done

for iter in 1 500 1000 1500 2000 3500 5000
do
	unset CUDA_VISIBLE_DEVICES
	CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python render_2.py \
	-s /data1/jhc/datasets/buaa_net \
	-m /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_1_pic \
	--iteration "$iter" \
	--colmap_only \
	--skip_train
done


好像效果并不好
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
python final_cull.py \
--input /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--output /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init2.ply \
-s /data1/jhc/datasets/buaa_net \
--final_opacity_cull 0.5 \
--final_ratio_cull 5.0

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_curve.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_1_pic \
--curve_ply /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init2.ply \
--eval \
--skip_train

-------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
python final_cull.py \
--input /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--output /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init3.ply \
-s /data1/jhc/datasets/buaa_net \
--final_ratio_cull 2.0

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_curve.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_1_pic \
--curve_ply /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init3.ply \
--eval \
--skip_train

## net6(体育场角落)

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

## net930-0(工地防护网)

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

## 102-2

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

## 107-1(集装箱网)

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/107-1 \
-m /data1/data/jhc/output/curve_output/107-1-black \
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
--final_opacity_cull 0.5
[SGCR] final prune: 55819 -> 35940 curves [07/10 23:01:57]

./nextStep.sh \
/data1/data/jhc/output/curve_output/107-1-black/curve_3dgs_init.ply \
/data1/data/jhc/datasets/107-1 \
/data1/data/jhc/output/3dgs_output/107-1-black \
2

## 1010-2

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/1010-2 \
-m /data1/data/jhc/output/curve_output/1010-2 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.8 \
--fill_y_threshold 0.1 \
--fill_z_threshold 0.8 \
--fill_grid_resX 200 \
--fill_grid_resY 50 \
--fill_grid_resZ 200 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3 \
--SGCR \
--final_opacity_cull 0.8

./nextStep.sh \
/data1/data/jhc/output/curve_output/1010-2/curve_3dgs_init.ply \
/data1/data/jhc/datasets/1010-2 \
/data1/data/jhc/output/3dgs_output/1010-2 \
1


# 虚拟数据集


## V109

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/formal3_white \
-m /data1/data/jhc/output/curve_output/V109 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 5 \
--fill_y_threshold 0.1 \
--fill_z_threshold 0.1 \
--fill_grid_resX 200 \
--fill_grid_resY 50 \
--fill_grid_resZ 50 \
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

./nextStep.sh \
/data1/data/jhc/output/curve_output/V109/curve_3dgs_init.ply \
/data1/data/jhc/datasets/formal3_white \
/data1/data/jhc/output/3dgs_output/V109 \
2


## sand_night3

PYTHON=/data1/conda_env/buaajhc/curveGS/bin/python
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 \
"$PYTHON" train.py \
-s /data1/data/jhc/datasets/sand_night3 \
-m /data1/data/jhc/output/curve_output/sand_night3 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 3 \
--fill_y_threshold 3 \
--fill_z_threshold 0.5 \
--fill_grid_resX 150 \
--fill_grid_resY 150 \
--fill_grid_resZ 30 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.01 \
--camera_point_distance 3 \
--SGCR \
--final_opacity_cull 0.5 \
--final_ratio_cull 2.0 \
--final_distance_cull 3.0 \
--final_maxLength_percentile_cull 10

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep.sh \
/data1/data/jhc/output/curve_output/sand_night3/curve_3dgs_init.ply \
/data1/data/jhc/datasets/sand_night3 \
/data1/data/jhc/output/3dgs_output/sand_night3 \
0
[test] PSNR: 28.9817  SSIM: 0.8638  LPIPS: 0.1626 [19/10 09:19:52]


## sand_sun2

PYTHON=/data1/conda_env/buaajhc/curveGS/bin/python
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
"$PYTHON" train.py \
-s /data1/data/jhc/datasets/sand_sun2 \
-m /data1/data/jhc/output/curve_output/sand_sun2 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 3 \
--fill_y_threshold 3 \
--fill_z_threshold 0.2 \
--fill_grid_resX 150 \
--fill_grid_resY 100 \
--fill_grid_resZ 30 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.01 \
--camera_point_distance 2 \
--SGCR \
--final_opacity_cull 0.5 \
--final_ratio_cull 2.0 \
--final_distance_cull 2.0 \
--final_maxLength_percentile_cull 10

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep.sh \
/data1/data/jhc/output/curve_output/sand_sun2/curve_3dgs_init.ply \
/data1/data/jhc/datasets/sand_sun2 \
/data1/data/jhc/output/3dgs_output/sand_sun2 \
2
[test] PSNR: 19.0896  SSIM: 0.7232  LPIPS: 0.2578 [19/10 21:23:43]


## tennis1

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
python train.py \
-s /data2/jhc/datasets/tennis1 \
-m /data2/jhc/output/curve_output/tennis1 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 3 \
--fill_y_threshold 3 \
--fill_z_threshold 0.5 \
--fill_grid_resX 150 \
--fill_grid_resY 150 \
--fill_grid_resZ 30 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 3 \
--outlier_std_ratio 0.01 \
--camera_point_distance 5 \
--SGCR \
--final_opacity_cull 0.5 \
--final_ratio_cull 2.0 \
--final_distance_cull 5.0 \
--final_maxLength_percentile_cull 10
[SGCR] final prune: 72403 -> 21530 curves [20/10 12:40:44]
Saved /data2/jhc/output/curve_output/tennis1/curve_3dgs_init.ply for 3DGS_NOTE initialization. [20/10 12:40:45]
[final cull] curve_3dgs_init.ply: 64590 -> 57531 (distance=666, max-length-percentile=6393) [20/10 12:40:45]

./nextStep.sh \
/data2/jhc/output/curve_output/tennis1/curve_3dgs_init.ply \
/data2/jhc/datasets/tennis1 \
/data2/jhc/output/3dgs_output/tennis1 \
2


## factory2

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 \
python train.py \
-s /data2/jhc/datasets/factory2 \
-m /data2/jhc/output/curve_output/factory2 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 2 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 800 \
--fill_grid_resY 30 \
--fill_grid_resZ 30 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.01 \
--camera_point_distance 3 \
--SGCR \
--final_opacity_cull 0.5 \
--final_ratio_cull 2.0 \
--final_distance_cull 3.0 \
--final_maxLength_percentile_cull 10

./nextStep.sh \
/data2/jhc/output/curve_output/factory2/curve_3dgs_init.ply \
/data2/jhc/datasets/factory2 \
/data2/jhc/output/3dgs_output/factory2 \
4
[test] PSNR: 25.2005  SSIM: 0.8137  LPIPS: 0.2657 [23/10 03:17:13]

# mipnerf360

## bicycle

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

[test] PSNR: 25.2663  SSIM: 0.7612  LPIPS: 0.2277 [05/10 19:28:23]

## garden

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

[test] PSNR: 27.3893  SSIM: 0.8597  LPIPS: 0.1231 [05/10 22:14:26]

## stump 

cd /data1/data/jhc/projects/Curve-Gaussian-Note
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/mipnerf360/stump \
-m /data1/data/jhc/output/curve_output/stump \
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

# TnT

## Train

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

## M60

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

## Truck

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










































