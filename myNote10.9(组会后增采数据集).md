
1. 167上面的formal3_white
test4_test.py涂黑
**先测试**
python test_colmap_reader.py \
-s /home/gamma/storage_of_code/habitat-sim/camera_output/formal3_white/colmap \
-m output/test/formal3_white \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 5 \
--fill_y_threshold 0.1 \
--fill_z_threshold 0.1 \
--fill_grid_resX 200 \
--fill_grid_resY 50 \
--fill_grid_resZ 50 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 5
Simplyfill3 填充后总点数: 118431 points


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

[test] PSNR: 32.7019  SSIM: 0.9738  LPIPS: 0.0471 [09/10 19:59:13]

2. 1010-1排球网
涂黑了
**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/1010/1010-1 \
-m output/test/1010-1 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.1 \
--fill_z_threshold 0.3 \
--fill_grid_resX 200 \
--fill_grid_resY 50 \
--fill_grid_resZ 200 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3
Simplyfill3 填充后总点数: 252304 points

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/1010-1 \
-m /data1/data/jhc/output/curve_output/1010-1 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.1 \
--fill_z_threshold 0.3 \
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
/data1/data/jhc/output/curve_output/1010-1/curve_3dgs_init.ply \
/data1/data/jhc/datasets/1010-1 \
/data1/data/jhc/output/3dgs_output/1010-1 \
1

[test] PSNR: 20.0781  SSIM: 0.7268  LPIPS: 0.3017 [10/10 17:04:36]

3. 1010-2
涂黑了
**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/1010/1010-2 \
-m output/test/1010-2 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 0.8 \
--fill_y_threshold 0.1 \
--fill_z_threshold 0.8 \
--fill_grid_resX 200 \
--fill_grid_resY 50 \
--fill_grid_resZ 200 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3
Simplyfill3 填充后总点数: 735469 points

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

[test] PSNR: 17.2325  SSIM: 0.5731  LPIPS: 0.3176 [10/10 14:49:40]

4. 1010-3
涂黑了
**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/1010/1010-3 \
-m output/test/1010-3 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 0.5 \
--fill_y_threshold 0.5 \
--fill_z_threshold 0.5 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3
Simplyfill3 填充后总点数: 390080 points

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/1010-3 \
-m /data1/data/jhc/output/curve_output/1010-3 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.5 \
--fill_y_threshold 0.5 \
--fill_z_threshold 0.5 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
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
/data1/data/jhc/output/curve_output/1010-3/curve_3dgs_init.ply \
/data1/data/jhc/datasets/1010-3 \
/data1/data/jhc/output/3dgs_output/1010-3 \
2

[test] PSNR: 18.1400  SSIM: 0.5106  LPIPS: 0.3795 [10/10 14:10:19]

5. 1011-1

**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/1011/1011-1 \
-m output/test/1011-1 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 1 \
--fill_y_threshold 0.5 \
--fill_z_threshold 1 \
--fill_grid_resX 200 \
--fill_grid_resY 20 \
--fill_grid_resZ 100 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 10 \
--outlier_std_ratio 0.05 \
--camera_point_distance 5
Simplyfill3 填充后总点数: 179506 points

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python train.py \
-s /data1/data/jhc/datasets/1011-1 \
-m /data1/data/jhc/output/curve_output/1011-1 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 1 \
--fill_y_threshold 0.5 \
--fill_z_threshold 1 \
--fill_grid_resX 200 \
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

./nextStep.sh \
/data1/data/jhc/output/curve_output/1011-1/curve_3dgs_init.ply \
/data1/data/jhc/datasets/1011-1 \
/data1/data/jhc/output/3dgs_output/1011-1 \
0

[test] PSNR: 15.2342  SSIM: 0.4422  LPIPS: 0.4247 [11/10 23:26:35]

6. 1011-2
**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/1011/1011-2 \
-m output/test/1011-2 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 0.5 \
--fill_y_threshold 0.5 \
--fill_z_threshold 0.5 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 10 \
--outlier_std_ratio 0.05 \
--camera_point_distance 5
Simplyfill3 填充后总点数: 251999 points

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/1011-2 \
-m /data1/data/jhc/output/curve_output/1011-2 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.5 \
--fill_y_threshold 0.5 \
--fill_z_threshold 0.5 \
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
--camera_point_distance 5 \
--SGCR \
--final_opacity_cull 0.8
[SGCR] final prune: 32489 -> 5655 curves [11/10 21:03:58]

./nextStep.sh \
/data1/data/jhc/output/curve_output/1011-2/curve_3dgs_init.ply \
/data1/data/jhc/datasets/1011-2 \
/data1/data/jhc/output/3dgs_output/1011-2 \
1
[test] PSNR: 20.0777  SSIM: 0.5083  LPIPS: 0.4752 [11/10 22:43:41]

效果不好，查看一下
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python render_curve.py \
-s /data1/data/jhc/datasets/1011-2 \
-m /data1/data/jhc/output/3dgs_output/1011-2 \
--curve_ply /data1/data/jhc/output/curve_output/1011-2/curve_3dgs_init.ply \
--eval \
--skip_train

试试合并推后呢？
curve_source=/data1/data/jhc/output/curve_output/1011-2/curve_3dgs_init.ply
S=/data1/data/jhc/datasets/1011-2
M=/data1/data/jhc/output/3dgs_output/1011-2_2
device=1
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES="$device" \
python train.py \
-s "$S" \
-m "$M" \
--eval \
--disable_viewer \
--curvegs "$curve_source" \
--curvegs_inject_iteration 15000 \
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

[test] PSNR: 19.7326  SSIM: 0.4823  LPIPS: 0.4862 [12/10 00:21:38]

7. 
**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/1012/1012-1 \
-m output/test/1012-1 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.1 \
--fill_z_threshold 0.3 \
--fill_grid_resX 200 \
--fill_grid_resY 50 \
--fill_grid_resZ 200 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 10 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3
Simplyfill3 填充后总点数: 440865 points

正式训练
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/1012-1 \
-m /data1/data/jhc/output/curve_output/1012-1 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.1 \
--fill_z_threshold 0.3 \
--fill_grid_resX 200 \
--fill_grid_resY 50 \
--fill_grid_resZ 200 \
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
[SGCR] final prune: 41163 -> 6898 curves [12/10 15:12:28]

./nextStep.sh \
/data1/data/jhc/output/curve_output/1012-1/curve_3dgs_init.ply \
/data1/data/jhc/datasets/1012-1 \
/data1/data/jhc/output/3dgs_output/1012-1 \
1

[test] PSNR: 22.3165  SSIM: 0.8247  LPIPS: 0.2465 [12/10 16:24:23]

**虚拟网球网**

8.  2-2

**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/Blender/blender5 \
-m output/test/blender5 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.5 \
--fill_grid_resX 500 \
--fill_grid_resY 50 \
--fill_grid_resZ 50 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.01 \
--camera_point_distance 5
Simplyfill3 填充后总点数: 180284 points

PYTHON=/data1/conda_env/buaajhc/curveGS/bin/python
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
"$PYTHON" train.py \
-s /data1/data/jhc/datasets/blender5 \
-m /data1/data/jhc/output/curve_output/blender5 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.5 \
--fill_grid_resX 500 \
--fill_grid_resY 50 \
--fill_grid_resZ 50 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.01 \
--camera_point_distance 5 \
--SGCR \
--final_opacity_cull 0.5 \
--final_ratio_cull 2.0

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep.sh \
/data1/data/jhc/output/curve_output/blender5/curve_3dgs_init.ply \
/data1/data/jhc/datasets/blender5 \
/data1/data/jhc/output/3dgs_output/blender5 \
2
[test] PSNR: 24.1161  SSIM: 0.7573  LPIPS: 0.3878 [15/10 12:41:05]

PYTHON=/data1/conda_env/buaajhc/curveGS/bin/python
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python render_curve.py \
-s /data1/data/jhc/datasets/blender5 \
-m /data1/data/jhc/output/3dgs_output/blender5 \
--curve_ply /data1/data/jhc/output/curve_output/blender5/curve_3dgs_init.ply \
--eval \
--skip_train

9. 	2-3是2-2的增密版，变成环绕且两行
**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/Blender/blender6 \
-m output/test/blender6 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.5 \
--fill_grid_resX 500 \
--fill_grid_resY 100 \
--fill_grid_resZ 50 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 60 \
--outlier_nb_neighbors 15 \
--outlier_std_ratio 0.01 \
--camera_point_distance 3
Simplyfill3 填充后总点数: 588105 points

PYTHON=/data1/conda_env/buaajhc/curveGS/bin/python
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 \
"$PYTHON" train.py \
-s /data1/data/jhc/datasets/blender6 \
-m /data1/data/jhc/output/curve_output/blender6 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.3 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.5 \
--fill_grid_resX 500 \
--fill_grid_resY 100 \
--fill_grid_resZ 50 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 60 \
--outlier_nb_neighbors 15 \
--outlier_std_ratio 0.01 \
--camera_point_distance 3 \
--SGCR \
--final_opacity_cull 0.5 \
--final_ratio_cull 2.0

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep.sh \
/data1/data/jhc/output/curve_output/blender6/curve_3dgs_init.ply \
/data1/data/jhc/datasets/blender6 \
/data1/data/jhc/output/3dgs_output/blender6 \
1
[test] PSNR: 23.8835  SSIM: 0.7649  LPIPS: 0.4016 [15/10 21:30:15]

20. 足球场1试
**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/Blender/b_football \
-m output/test/b_football \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 1 \
--fill_y_threshold 0.5 \
--fill_z_threshold 1 \
--fill_grid_resX 300 \
--fill_grid_resY 50 \
--fill_grid_resZ 100 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.01 \
--camera_point_distance 5
Simplyfill3 填充后总点数: 371170 points

PYTHON=/data1/conda_env/buaajhc/curveGS/bin/python
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
"$PYTHON" train.py \
-s /data1/data/jhc/datasets/b_football \
-m /data1/data/jhc/output/curve_output/b_football \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 1 \
--fill_y_threshold 0.5 \
--fill_z_threshold 1 \
--fill_grid_resX 300 \
--fill_grid_resY 50 \
--fill_grid_resZ 100 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.01 \
--camera_point_distance 5 \
--SGCR \
--final_opacity_cull 0.5 \
--final_ratio_cull 2.0

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep.sh \
/data1/data/jhc/output/curve_output/b_football/curve_3dgs_init.ply \
/data1/data/jhc/datasets/b_football \
/data1/data/jhc/output/3dgs_output/b_football \
2

[test] PSNR: 12.3411  SSIM: 0.4000  LPIPS: 0.5579 [15/10 21:51:46]

21. 沙排1
**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/Blender/sand_volleyball1 \
-m output/test/sand_volleyball1 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 1 \
--fill_y_threshold 0.5 \
--fill_z_threshold 0.5 \
--fill_grid_resX 300 \
--fill_grid_resY 50 \
--fill_grid_resZ 100 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.01 \
--camera_point_distance 3
Simplyfill3 填充后总点数: 542201 points

PYTHON=/data1/conda_env/buaajhc/curveGS/bin/python
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 \
"$PYTHON" train.py \
-s /data1/data/jhc/datasets/sand_volleyball1 \
-m /data1/data/jhc/output/curve_output/sand_volleyball1 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 1 \
--fill_y_threshold 0.5 \
--fill_z_threshold 0.5 \
--fill_grid_resX 300 \
--fill_grid_resY 50 \
--fill_grid_resZ 100 \
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
--final_ratio_cull 2.0

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep.sh \
/data1/data/jhc/output/curve_output/sand_volleyball1/curve_3dgs_init.ply \
/data1/data/jhc/datasets/sand_volleyball1 \
/data1/data/jhc/output/3dgs_output/sand_volleyball1 \
0

[test] PSNR: 16.7614  SSIM: 0.5380  LPIPS: 0.5399 [16/10 06:12:12]

22. 沙排2
**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/Blender/sand_volleyball2 \
-m output/test/sand_volleyball2 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 5 \
--fill_y_threshold 5 \
--fill_z_threshold 0.1 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 50 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.01 \
--camera_point_distance 5
Simplyfill3 填充后总点数: 428228 points

PYTHON=/data1/conda_env/buaajhc/curveGS/bin/python
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 \
"$PYTHON" train.py \
-s /data1/data/jhc/datasets/sand_volleyball2 \
-m /data1/data/jhc/output/curve_output/sand_volleyball2 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 5 \
--fill_y_threshold 5 \
--fill_z_threshold 0.1 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 50 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.01 \
--camera_point_distance 5 \
--SGCR \
--final_opacity_cull 0.5 \
--final_ratio_cull 2.0

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep.sh \
/data1/data/jhc/output/curve_output/sand_volleyball2/curve_3dgs_init.ply \
/data1/data/jhc/datasets/sand_volleyball2 \
/data1/data/jhc/output/3dgs_output/sand_volleyball2 \
1
[test] PSNR: 17.5061  SSIM: 0.5250  LPIPS: 0.5152 [16/10 06:16:20]


23. 沙排3-2,在2的基础上增加相机
**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/Blender/sand_volleyball3-2 \
-m output/test/sand_volleyball3-2 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 5 \
--fill_y_threshold 5 \
--fill_z_threshold 0.1 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 50 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.01 \
--camera_point_distance 3
Simplyfill3 填充后总点数: 431738 points

PYTHON=/data1/conda_env/buaajhc/curveGS/bin/python
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 \
"$PYTHON" train.py \
-s /data1/data/jhc/datasets/sand_volleyball3-2 \
-m /data1/data/jhc/output/curve_output/sand_volleyball3-2 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 5 \
--fill_y_threshold 5 \
--fill_z_threshold 0.1 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 50 \
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
--final_ratio_cull 2.0

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep.sh \
/data1/data/jhc/output/curve_output/sand_volleyball3-2/curve_3dgs_init.ply \
/data1/data/jhc/datasets/sand_volleyball3-2 \
/data1/data/jhc/output/3dgs_output/sand_volleyball3-2 \
0
[ITER 7000] Evaluating test: L1 0.0871631983527035 PSNR 17.254363761757904 [16/10 13:40:32]
[ITER 7000] Evaluating train: L1 0.09321244582533837 PSNR 16.66059722900391 [16/10 13:40:32]

 [test] PSNR: 17.2458  SSIM: 0.5084  LPIPS: 0.5662 [16/10 14:30:06]
 
24. 
**先测试**
python test_colmap_reader.py \
-s /home/gamma/storage_of_code/habitat-sim/camera_output/soccer2/colmap \
-m output/test/soccer2 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 2 \
--fill_y_threshold 0.1 \
--fill_z_threshold 2 \
--fill_grid_resX 300 \
--fill_grid_resY 25 \
--fill_grid_resZ 100 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.01 \
--camera_point_distance 5
Simplyfill3 填充后总点数: 312055 points

PYTHON=/data1/conda_env/buaajhc/curveGS/bin/python
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 \
"$PYTHON" train.py \
-s /data1/data/jhc/datasets/soccer2 \
-m /data1/data/jhc/output/curve_output/soccer2 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 2 \
--fill_y_threshold 0.1 \
--fill_z_threshold 2 \
--fill_grid_resX 300 \
--fill_grid_resY 25 \
--fill_grid_resZ 100 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.01 \
--camera_point_distance 5 \
--SGCR \
--final_opacity_cull 0.5 \
--final_ratio_cull 2.0

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep.sh \
/data1/data/jhc/output/curve_output/soccer2/curve_3dgs_init.ply \
/data1/data/jhc/datasets/soccer2 \
/data1/data/jhc/output/3dgs_output/soccer2 \
1

[test] PSNR: 26.0925  SSIM: 0.9246  LPIPS: 0.1249 [17/10 13:22:44]

25. sandnight2
python test_colmap_reader.py \
-s /home/gamma/storage_of_code/habitat-sim/camera_output/sand_night2/colmap \
-m output/test/sand_night2 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 3 \
--fill_y_threshold 3 \
--fill_z_threshold 0.5 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.01 \
--camera_point_distance 5
Simplyfill3 填充后总点数: 784106 points

PYTHON=/data1/conda_env/buaajhc/curveGS/bin/python
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 \
"$PYTHON" train.py \
-s /data1/data/jhc/datasets/sand_night2 \
-m /data1/data/jhc/output/curve_output/sand_night2 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 3 \
--fill_y_threshold 3 \
--fill_z_threshold 0.5 \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.01 \
--camera_point_distance 5 \
--SGCR \
--final_opacity_cull 0.5 \
--final_ratio_cull 2.0

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep.sh \
/data1/data/jhc/output/curve_output/sand_night2/curve_3dgs_init.ply \
/data1/data/jhc/datasets/sand_night2 \
/data1/data/jhc/output/3dgs_output/sand_night2 \
1

[test] PSNR: 22.8622  SSIM: 0.6466  LPIPS: 0.3301 [18/10 02:17:08]

效果不好看看情况
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python render_curve.py \
-s /data1/data/jhc/datasets/sand_night2 \
-m /data1/data/jhc/output/3dgs_output/sand_night2 \
--curve_ply /data1/data/jhc/output/curve_output/sand_night2/curve_3dgs_init.ply \
--eval \
--skip_train

**增加一点删除阈值**

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python final_cull.py \
--input /data1/data/jhc/output/curve_output/sand_night2/curve_3dgs_init.ply \
--output /data1/data/jhc/output/curve_output/sand_night2/curve_3dgs_init2.ply \
--final_opacity_cull 0.8 \
--final_ratio_cull 5.0

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python render_curve.py \
-s /data1/data/jhc/datasets/sand_night2 \
-m /data1/data/jhc/output/3dgs_output/sand_night2 \
--curve_ply /data1/data/jhc/output/curve_output/sand_night2/curve_3dgs_init2.ply \
--eval \
--skip_train

**长度过大或者过小的被删除**

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python final_cull.py \
--input /data1/data/jhc/output/curve_output/sand_night2/curve_3dgs_init.ply \
--output /data1/data/jhc/output/curve_output/sand_night2/curve_3dgs_init3.ply \
--final_opacity_cull 0.8 \
--final_ratio_cull 5.0 \
--final_maxLength_cull
Gaussians: 663690 -> 243484 (removed 420206)
Removed by opacity:    87333
Removed by ratio:      357962
Removed by max length:  12204

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python render_curve.py \
-s /data1/data/jhc/datasets/sand_night2 \
-m /data1/data/jhc/output/3dgs_output/sand_night2 \
--curve_ply /data1/data/jhc/output/curve_output/sand_night2/curve_3dgs_init3.ply \
--eval \
--skip_train

**距离严格大于阈值的高斯被删除，等于阈值的高斯保留**
滤除5m以外的
conda run -n curveGS python final_cull.py \
--input /data1/data/jhc/output/curve_output/sand_night2/curve_3dgs_init.ply \
--output /data1/data/jhc/output/curve_output/sand_night2/curve_3dgs_init4.ply \
-s /data1/data/jhc/datasets/sand_night2 \
--final_opacity_cull 0.8 \
--final_ratio_cull 5.0 \
--final_distance_cull 5.0
Gaussians: 663690 -> 215376 (removed 448314)
Removed by opacity:    87333
Removed by ratio:      357962
Removed by max length:  0
Removed by distance:    78651
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python render_curve.py \
-s /data1/data/jhc/datasets/sand_night2 \
-m /data1/data/jhc/output/3dgs_output/sand_night2 \
--curve_ply /data1/data/jhc/output/curve_output/sand_night2/curve_3dgs_init4.ply \
--eval \
--skip_train

滤除3m以外的
conda run -n curveGS python final_cull.py \
--input /data1/data/jhc/output/curve_output/sand_night2/curve_3dgs_init.ply \
--output /data1/data/jhc/output/curve_output/sand_night2/curve_3dgs_init5.ply \
-s /data1/data/jhc/datasets/sand_night2 \
--final_opacity_cull 0.8 \
--final_ratio_cull 5.0 \
--final_distance_cull 3.0
Gaussians: 663690 -> 65560 (removed 598130)
Removed by opacity:    87333
Removed by ratio:      357962
Removed by max length:  0
Removed by distance:    457633
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python render_curve.py \
-s /data1/data/jhc/datasets/sand_night2 \
-m /data1/data/jhc/output/3dgs_output/sand_night2 \
--curve_ply /data1/data/jhc/output/curve_output/sand_night2/curve_3dgs_init5.ply \
--eval \
--skip_train

**太短，10%最短的删除**
conda run -n curveGS python final_cull.py \
--input /data1/data/jhc/output/curve_output/sand_night2/curve_3dgs_init.ply \
--output /data1/data/jhc/output/curve_output/sand_night2/curve_3dgs_init6.ply \
-s /data1/data/jhc/datasets/sand_night2 \
--final_opacity_cull 0.5 \
--final_ratio_cull 2.0 \
--final_distance_cull 3.0 \
--final_maxLength_percentile_cull 10
Gaussians: 663690 -> 185431 (removed 478259)
Removed by opacity:    0
Removed by ratio:      196
Removed by max length:  0
Removed by distance:    457633
Removed by max-length percentile: 20604
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python render_curve.py \
-s /data1/data/jhc/datasets/sand_night2 \
-m /data1/data/jhc/output/3dgs_output/sand_night2 \
--curve_ply /data1/data/jhc/output/curve_output/sand_night2/curve_3dgs_init6.ply \
--eval \
--skip_train

28. sand_night3

python test_colmap_reader.py \
-s /home/gamma/storage_of_code/habitat-sim/camera_output/sand_night3/colmap \
-m output/test/sand_night3 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 3 \
--fill_y_threshold 3 \
--fill_z_threshold 0.5 \
--fill_grid_resX 150 \
--fill_grid_resY 150 \
--fill_grid_resZ 30 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.01 \
--camera_point_distance 3
Simplyfill3 填充后总点数: 304666 points

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


30. soccer4
**先测试**
python test_colmap_reader.py \
-s /home/gamma/storage_of_code/habitat-sim/camera_output/soccer4 \
-m output/test/soccer4 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 2 \
--fill_y_threshold 0.1 \
--fill_z_threshold 2 \
--fill_grid_resX 150 \
--fill_grid_resY 50 \
--fill_grid_resZ 50 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.01 \
--camera_point_distance 5
Simplyfill3 填充后总点数: 308880 points

165上跑
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
python train.py \
-s /data2/jhc/datasets/soccer4 \
-m /data2/jhc/output/curve_output/soccer4 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 2 \
--fill_y_threshold 0.1 \
--fill_z_threshold 2 \
--fill_grid_resX 150 \
--fill_grid_resY 50 \
--fill_grid_resZ 50 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.01 \
--camera_point_distance 5 \
--SGCR \
--final_opacity_cull 0.5 \
--final_ratio_cull 2.0 \
--final_distance_cull 5.0 \
--final_maxLength_percentile_cull 10

./nextStep.sh \
/data2/jhc/output/curve_output/soccer4/curve_3dgs_init.ply \
/data2/jhc/datasets/soccer4 \
/data2/jhc/output/3dgs_output/soccer4 \
2

167上跑

PYTHON=/data1/conda_env/buaajhc/curveGS/bin/python
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 \
"$PYTHON" train.py \
-s /data1/data/jhc/datasets/soccer4 \
-m /data1/data/jhc/output/curve_output/soccer4 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 2 \
--fill_y_threshold 0.1 \
--fill_z_threshold 2 \
--fill_grid_resX 150 \
--fill_grid_resY 50 \
--fill_grid_resZ 50 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.01 \
--camera_point_distance 5 \
--SGCR \
--final_opacity_cull 0.5 \
--final_ratio_cull 2.0 \
--final_distance_cull 5.0 \
--final_maxLength_percentile_cull 10

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep.sh \
/data1/data/jhc/output/curve_output/soccer4/curve_3dgs_init.ply \
/data1/data/jhc/datasets/soccer4 \
/data1/data/jhc/output/3dgs_output/soccer4 \
1


31. sand_sun2

python test_colmap_reader.py \
-s /home/gamma/storage_of_code/habitat-sim/camera_output/sand_sun2/colmap \
-m output/test/sand_sun2 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 3 \
--fill_y_threshold 3 \
--fill_z_threshold 0.2 \
--fill_grid_resX 150 \
--fill_grid_resY 100 \
--fill_grid_resZ 30 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.01 \
--camera_point_distance 2
Simplyfill3 填充后总点数: 142714 points

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


32. 165上跑tennis1
**先测试**
python test_colmap_reader.py \
-s /home/gamma/storage_of_code/habitat-sim/camera_output/tennis1/colmap \
-m output/test/tennis1 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 3 \
--fill_y_threshold 3 \
--fill_z_threshold 0.5 \
--fill_grid_resX 150 \
--fill_grid_resY 150 \
--fill_grid_resZ 30 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 3 \
--outlier_std_ratio 0.01 \
--camera_point_distance 5
Simplyfill3 填充后总点数: 190405 points

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

[test] PSNR: 25.9999  SSIM: 0.8948  LPIPS: 0.1316 [20/10 14:12:45]

33. factory数据集
**先测试**
python test_colmap_reader.py \
-s /home/gamma/storage_of_code/habitat-sim/camera_output/factory/colmap \
-m output/test/factory \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 2 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 800 \
--fill_grid_resY 30 \
--fill_grid_resZ 30 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.01 \
--camera_point_distance 3
Simplyfill3 填充后总点数: 248057 points





PYTHON=/data1/conda_env/buaajhc/curveGS/bin/python
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 \
"$PYTHON" train.py \
-s /data1/data/jhc/datasets/factory \
-m /data1/data/jhc/output/curve_output/factory \
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

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep.sh \
/data1/data/jhc/output/curve_output/factory/curve_3dgs_init.ply \
/data1/data/jhc/datasets/factory \
/data1/data/jhc/output/3dgs_output/factory \
0

cd ../gaussian-splatting/
conda activate gs

./run_exp.sh \
/data1/data/jhc/datasets/factory \
/data1/jhc/storage_of_code/gaussian-splatting/output/factory \
0


34. factory2数据集(165跑)
**先测试**
python test_colmap_reader.py \
-s /home/gamma/storage_of_code/habitat-sim/camera_output/factory2/colmap \
-m output/test/factory2 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 2 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 800 \
--fill_grid_resY 30 \
--fill_grid_resZ 30 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.01 \
--camera_point_distance 3
Simplyfill3 填充后总点数: 142126 points


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

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep.sh \
/data2/jhc/output/curve_output/factory2/curve_3dgs_init.ply \
/data2/jhc/datasets/factory2 \
/data2/jhc/output/3dgs_output/factory2 \
4

[test] PSNR: 25.2005  SSIM: 0.8137  LPIPS: 0.2657 [23/10 03:17:13]

**noblack跑一次**

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
python train.py \
-s /data2/jhc/datasets/factory2_noblack \
-m /data2/jhc/output/curve_output/factory2_noblack \
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

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep.sh \
/data2/jhc/output/curve_output/factory2_noblack/curve_3dgs_init.ply \
/data2/jhc/datasets/factory2_noblack \
/data2/jhc/output/3dgs_output/factory2_noblack \
2

[test] PSNR: 22.4632  SSIM: 0.7637  LPIPS: 0.3005 [23/10 12:06:53]



python ply_to_usd.py \
/home/gamma/storage_of_code/gs_seldom/3dgs_output/net/Net6/ours/iteration_30000/point_cloud.ply


35. buaa_net

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/918_sh3/buaaNet_pic_Oct30 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_PGSR.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/918_sh3/buaaNet_pic_Oct30 \
--iteration 30000 \
--eval

















