
# 整体pipeline
## 先提取边缘图

跑
/home/gamma/storage_of_code/temp/test3.py

## 再做一个小测试

pcd_clean, _ = pcd_o3d.remove_radius_outlier(nb_points=30, radius=radius)      # nb_points=180
中的  nb_points 从30改为180


python test_colmap_reader.py \
-s /home/gamma/rosbags/mipnerf360/bicycle \
-m output/test/test-bicycle \
--detector PidiNet \
--eval \
--init_voxel_size 0.01 \
--method 0 \
--trajectory_root

## 开启curveGS训练

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/mipnerf360/bicycle \
-m output/bicycle \
--eval \
--iterations 30000 \
--fill_method simplefill \
--trajectory_root \
--fill_grid_resX 100 \
--fill_grid_resY 100 \
--fill_grid_resZ 100 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--outlier_nb_points 180

python edge_extraction/eval_replica.py \
--dataset_dir /data1/jhc/datasets/mipnerf360/bicycle \
--base_dir output/bicycle \
--sample_resolution 0.002





# 对比试验

## 3dgs

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/mipnerf360/bicycle \
-m output/bicycle_repeat1 \
--eval \
--disable_viewer \
--iterations 30000

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render.py \
-s /data1/jhc/datasets/mipnerf360/bicycle \
-m output/bicycle_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/bicycle_repeat1

-----------------------------------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/mipnerf360/bicycle \
-m output/bicycle_repeat2 \
--eval \
--disable_viewer \
--iterations 30000

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render.py \
-s /data1/jhc/datasets/mipnerf360/bicycle \
-m output/bicycle_repeat2 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/bicycle_repeat2

-----------------------------------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/mipnerf360/bicycle \
-m output/bicycle_repeat3 \
--eval \
--disable_viewer \
--iterations 30000

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render.py \
-s /data1/jhc/datasets/mipnerf360/bicycle \
-m output/bicycle_repeat3 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/bicycle_repeat3











