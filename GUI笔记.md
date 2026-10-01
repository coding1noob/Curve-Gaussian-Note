
python add_points_gui.py \
-s /home/gamma/rosbags/COLMAP/930/net930-0




python add_points_gui.py \
-s /home/gamma/rosbags/COLMAP/930/net930-0 \
--locator_step 0.1 \
--locator_radius 0.3 \
--locator_radius_step 0.03

--triangle_grid_step 0.05：控制表面点的密度（0.05 表示每 5 厘米一个点，可根据场景尺度调整，越小越密）
--triangle_thickness_samples 3：控制厚度方向的层数。最大厚度即为球的直径，如果只想补一个无限薄的平面，可以设为 1

手动补点尝试：

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
























