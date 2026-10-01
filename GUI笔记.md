
python add_points_gui.py \
-s /home/gamma/rosbags/COLMAP/930/net930-0




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


















