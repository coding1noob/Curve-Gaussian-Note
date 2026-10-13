
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

8. 虚拟网球网

**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/Blender/blender1 \
-m output/test/blender1 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 1 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 200 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 0 \
--outlier_nb_neighbors 0 \
--outlier_std_ratio 0 \
--camera_point_distance 5
Simplyfill3 填充后总点数: 444611 points

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/blender1 \
-m /data1/data/jhc/output/curve_output/blender1 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 1 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 200 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 0 \
--outlier_nb_neighbors 0 \
--outlier_std_ratio 0 \
--camera_point_distance 5 \
--SGCR \
--final_opacity_cull 0.8
[SGCR] final prune: 118046 -> 88276 curves [12/10 23:18:49]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python render_curve.py \
-s /data1/data/jhc/datasets/blender1 \
-m /data1/data/jhc/output/3dgs_output/blender1 \
--curve_ply /data1/data/jhc/output/curve_output/blender1/curve_3dgs_init.ply \
--eval \
--skip_train
效果不错，继续

./nextStep.sh \
/data1/data/jhc/output/curve_output/blender1/curve_3dgs_init.ply \
/data1/data/jhc/datasets/blender1 \
/data1/data/jhc/output/curve_output/blender1 \
1
[test] PSNR: 18.5575  SSIM: 0.6689  LPIPS: 0.3657 [13/10 03:07:31]

9. 虚拟网球网2
**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/Blender/blender2 \
-m output/test/blender2 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 1 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 200 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 0 \
--outlier_nb_neighbors 0 \
--outlier_std_ratio 0 \
--camera_point_distance 5
Simplyfill3 填充后总点数: 435337 points

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/blender2 \
-m /data1/data/jhc/output/curve_output/blender2 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 1 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 200 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 0 \
--outlier_nb_neighbors 0 \
--outlier_std_ratio 0 \
--camera_point_distance 5 \
--SGCR \
--final_opacity_cull 0.8

[SGCR] final prune: 123119 -> 88694 curves [13/10 05:22:02]

./nextStep.sh \
/data1/data/jhc/output/curve_output/blender2/curve_3dgs_init.ply \
/data1/data/jhc/datasets/blender2 \
/data1/data/jhc/output/curve_output/blender2 \
1
[test] PSNR: 18.8825  SSIM: 0.6752  LPIPS: 0.3449 [13/10 08:20:54]


10. 

**先测试**
python test_colmap_reader.py \
-s /home/gamma/rosbags/Blender/blender3 \
-m output/test/blender3 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 1 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 300 \
--fill_grid_resY 20 \
--fill_grid_resZ 75 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 10 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3
Simplyfill3 填充后总点数: 133590 points

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/blender3 \
-m /data1/data/jhc/output/curve_output/blender3 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 1 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 300 \
--fill_grid_resY 20 \
--fill_grid_resZ 75 \
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
[SGCR] final prune: 30200 -> 6732 curves [13/10 19:50:29]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python render_curve.py \
-s /data1/data/jhc/datasets/blender3 \
-m /data1/data/jhc/output/3dgs_output/blender3 \
--curve_ply /data1/data/jhc/output/curve_output/blender3/curve_3dgs_init.ply \
--eval \
--skip_train

./nextStep.sh \
/data1/data/jhc/output/curve_output/blender3/curve_3dgs_init.ply \
/data1/data/jhc/datasets/blender3 \
/data1/data/jhc/output/3dgs_output/blender3 \
1
[test] PSNR: 26.4420  SSIM: 0.8565  LPIPS: 0.2556 [13/10 20:34:12]










