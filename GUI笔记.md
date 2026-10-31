
    print("=================================================================")
    print("Controls:")
    print("  Move:    W/S (X), A/D (Y), Q/E (Z)  [Press repeatedly]")
    print("  Resize:  I (larger), J (smaller)")
    print("  Step:    O (increase step), K (decrease step)  <-- NEW!")
    print("  Action:  B (save anchor), R (reset view), Esc (exit)")
    print(f"Initial Step: {locator.step:.4f} | Initial Radius: {locator.radius:.4f}")
    print("=================================================================")

1. 

python add_points_gui.py \
-s /home/gamma/rosbags/COLMAP/930/net930-0 \
--locator_step 0.1 \
--locator_radius 0.3 \
--locator_radius_step 0.03

--triangle_grid_step 0.05：控制表面点的密度（0.05 表示每 5 厘米一个点，可根据场景尺度调整，越小越密）
--triangle_thickness_samples 3：控制厚度方向的层数。最大厚度即为球的直径，如果只想补一个无限薄的平面，可以设为 1

手动补点测试：

python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/930/net930-0 \
-m output/test/net930-0_manualFill \
--eval \
--method 4 \
--init_voxel_size 0.01 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3 \
--triangle_grid_step 0.05 \
--triangle_thickness_samples 3

正式启动：

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net930-0 \
-m /data1/data/jhc/output/curve_output/net930-0_manual \
--eval \
--iterations 30000 \
--fill_method manualfill \
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

2. 

python add_points_gui.py \
-s /home/gamma/rosbags/COLMAP/930/net930-1 \
--locator_step 0.1 \
--locator_radius 0.3 \
--locator_radius_step 0.03

测试：
python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/930/net930-1 \
-m output/test/net930-1_manualFill \
--eval \
--method 4 \
--init_voxel_size 0.01 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3 \
--triangle_grid_step 0.05 \
--triangle_thickness_samples 3

正式启动：

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net930-1 \
-m /data1/data/jhc/output/curve_output/net930-1_manual \
--eval \
--iterations 30000 \
--fill_method manualfill \
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
手动三角填充后总点数: 44317 points

3. 

python add_points_gui.py \
-s /home/gamma/rosbags/COLMAP/103/103-2 \
--locator_step 0.1 \
--locator_radius 0.3 \
--locator_radius_step 0.03

测试：
python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/103/103-2 \
-m output/test/103-2_manualFill \
--eval \
--method 4 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 3 \
--triangle_grid_step 0.05 \
--triangle_thickness_samples 3

正式启动：

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/103-2 \
-m /data1/data/jhc/output/curve_output/103-2_manual \
--eval \
--iterations 30000 \
--fill_method manualfill \
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

4. buaa4_simple

python add_points_gui.py \
-s /home/gamma/rosbags/COLMAP/buaa4_simple \
--locator_step 0.1 \
--locator_radius 0.3 \
--locator_radius_step 0.03

测试：
python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/buaa4_simple \
-m output/test/buaa4_simple_manualFill \
--eval \
--method 4 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--triangle_grid_step 0.05 \
--triangle_thickness_samples 5 \
--triangle_grid_step 0.03

正式启动：

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/buaa4_simple \
-m /data2/jhc/output/curve_output/buaa4_simple_manual \
--eval \
--iterations 30000 \
--fill_method manualfill \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--SGCR \
--final_opacity_cull 0.5 \
--triangle_thickness_samples 5 \
--triangle_grid_step 0.03

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
python train.py \
-s /data1/jhc/datasets/buaa4_simple \
-m /data2/jhc/output/3dgs_output/buaa4_simple_manual \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/buaa4_simple_manual/curve_3dgs_init.ply \
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
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render.py \
-s /data1/jhc/datasets/buaa4_simple \
-m /data2/jhc/output/3dgs_output/buaa4_simple_manual \
--iteration 30000 \
--skip_train

python /home/gamma/storage_of_code/gs_seldom/3dgrut/threedgrut/export/scripts/ply_to_usd.py \
/home/gamma/storage_of_code/gs_seldom/3dgs_output/buaa4_simple_manual/point_cloud.ply

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python render_curve.py \
-s /data1/jhc/datasets/buaa4_simple \
-m /data2/jhc/output/3dgs_output/buaa4_simple_manual \
--curve_ply /data2/jhc/output/curve_output/buaa4_simple_manual/curve_3dgs_init.ply \
--eval \
--skip_train

5. buaa4_simple2

python add_points_gui.py \
-s /home/gamma/rosbags/COLMAP/buaa4_simple2 \
--locator_step 0.1 \
--locator_radius 0.3 \
--locator_radius_step 0.03

python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/buaa4_simple2 \
-m output/test/buaa4_simple2_manualFill \
--eval \
--method 4 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--triangle_grid_step 0.05 \
--triangle_thickness_samples 7 \
--triangle_grid_step 0.03
手动三角填充后总点数: 224045 points

正式启动：
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/buaa4_simple2 \
-m /data2/jhc/output/curve_output/buaa4_simple2_manual \
--eval \
--iterations 30000 \
--fill_method manualfill \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--SGCR \
--final_opacity_cull 0.5 \
--triangle_thickness_samples 7 \
--triangle_grid_step 0.03

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python render_curve.py \
-s /data1/jhc/datasets/buaa4_simple2 \
-m /data2/jhc/output/3dgs_output/buaa4_simple2_manual \
--curve_ply /data2/jhc/output/curve_output/buaa4_simple2_manual/curve_3dgs_init.ply \
--eval \
--skip_train
























# 截图写论文


python /home/gamma/storage_of_code/Curve-Gaussian_Note/view_filled_ply.py \
/home/gamma/storage_of_code/Curve-Gaussian_Note/output/test/buaa_net_Oct29 \
--point_size 4 \
--added_point_size 12 \
--radius 6 \
--center 0 0 0

python /home/gamma/storage_of_code/Curve-Gaussian_Note/view_filled_ply.py \
/home/gamma/storage_of_code/Curve-Gaussian_Note/output/test/net930-0 \
--point_size 4 \
--added_point_size 12 \
--radius 6 \
--center 0 0 0


python test_colmap_reader.py \
-s /home/gamma/storage_of_code/habitat-sim/camera_output/factory2/colmap \
-m output/test/factory2-pic \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 2 \
--fill_y_threshold 0.3 \
--fill_z_threshold 0.3 \
--fill_grid_resX 400 \
--fill_grid_resY 15 \
--fill_grid_resZ 15 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.01 \
--camera_point_distance 3

python /home/gamma/storage_of_code/Curve-Gaussian_Note/view_filled_ply.py \
/home/gamma/storage_of_code/Curve-Gaussian_Note/output/test/factory2-pic \
--point_size 4 \
--added_point_size 12





