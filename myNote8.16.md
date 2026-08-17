
# 融合 边缘图 和 RGB图

--image-folder 为输入RGB，--edge-folder 为输入黑白边缘图
--output-folder 为彩色边缘输出， --rgba-folder 为

python /home/gamma/storage_of_code/temp/test5.py \
--image-folder /path/to/images \
--edge-folder /path/to/edge_PidiNet \
--output-folder /path/to/edge_color \
--rgba-folder /path/to/edge_color_rgba


python /home/gamma/storage_of_code/temp/test5.py \
--image-folder /home/gamma/storage_of_code/habitat-sim/camera_output/formal3/colmap/images \
--edge-folder /home/gamma/storage_of_code/habitat-sim/camera_output/formal3/colmap/edge_PidiNet


# 测试
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 CUDA_LAUNCH_BLOCKING=1 python -u train.py -s \
/data1/jhc/datasets/virtual_net2 \
-m output/virtual_net2_8.12_test2 \
--eval \
--iterations 201 \
--checkpoint_iterations 200 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 10 \
--fill_y_threshold 0.5 \
--fill_grid_resX 200 \
--fill_grid_resY 100 \
--fill_grid_resZ 50 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--use_RGB

接着训练:
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 CUDA_LAUNCH_BLOCKING=1 python -u train.py -s \
/data1/jhc/datasets/virtual_net2 \
-m output/virtual_net2_8.12_test2 \
--eval \
--iterations 200 \
--start_checkpoint output/virtual_net2_8.12_test2/chkpnt100.pth \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 10 \
--fill_y_threshold 0.5 \
--fill_grid_resX 200 \
--fill_grid_resY 100 \
--fill_grid_resZ 50 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--use_RGB

# 删除冗余数据集

images/
edge_PidiNet/
curvegs_edge_mask/
baseline_non_edge_mask/
sparse/





































