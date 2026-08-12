
# 对比试验

## 3dgs

conda activate gs_pro6000

cd /data1/jhc/storage_of_code/gaussian-splatting

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_gs2_repeat1 \
--eval \
--disable_viewer \
--iterations 30000

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_gs2_repeat1 \
--iteration 7000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual_gs2_repeat1

cd /data1/jhc/storage_of_code/gs_pro6000
conda activate curveGS

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data1/jhc/storage_of_code/gaussian-splatting/output/virtual_gs2_repeat1 \
--iteration 7000 \
--skip_train

----------

conda activate gs_pro6000

cd /data1/jhc/storage_of_code/gaussian-splatting

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_gs2_repeat2 \
--eval \
--disable_viewer \
--iterations 30000

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_gs2_repeat2 \
--iteration 7000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual_gs2_repeat2

cd /data1/jhc/storage_of_code/gs_pro6000
conda activate curveGS

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data1/jhc/storage_of_code/gaussian-splatting/output/virtual_gs2_repeat2 \
--iteration 30000 \
--skip_train

------------

conda activate gs_pro6000

cd /data1/jhc/storage_of_code/gaussian-splatting

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_gs2_repeat3 \
--eval \
--disable_viewer \
--iterations 30000

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 TORCH_HOME=/data1/jhc/torch_cache python render.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_gs2_repeat3 \
--iteration 7000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual_gs2_repeat3

cd /data1/jhc/storage_of_code/gs_pro6000
conda activate curveGS

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data1/jhc/storage_of_code/gaussian-splatting/output/virtual_gs2_repeat3 \
--iteration 30000 \
--skip_train

## 指标总结

/virtual_gs2_repeat1                                                                   
Method: ours_7000                                                                                   
  SSIM :    0.8319307                                                                               
  PSNR :   28.5815334                                                                               
  LPIPS:    0.3046059                                                                               
                                                                                                    
Method: ours_30000                                                                                  
  SSIM :    0.9472296                                                                               
  PSNR :   32.5017242                                                                               
  LPIPS:    0.1026414

/virtual_gs2_repeat2
Method: ours_7000
  SSIM :    0.8312290
  PSNR :   28.6431999
  LPIPS:    0.3063112

Method: ours_30000
  SSIM :    0.9445400
  PSNR :   32.5761566
  LPIPS:    0.1045222

/virtual_gs2_repeat3                                                                                                                                                                         
 ours_7000                                                                                                                                                                                         
  SSIM :    0.8317725                                                                                                                                                                                     
  PSNR :   28.5898724                                                                                                                                                                                     
  LPIPS:    0.3050846                                                                                                                                                                                     
                                                                                                                                                                                                           ours_30000                                                                                                                                                                                        
  SSIM :    0.9458086                                                                                                                                                                                     
  PSNR :   33.0752296                                                                                                                                                                                     
  LPIPS:    
0.1041162

# 自己算法

## 先提取边缘图

跑
/home/gamma/storage_of_code/temp/test3.py

## 再做一个小测试

pcd_clean, _ = pcd_o3d.remove_radius_outlier(nb_points=30, radius=radius)      # nb_points=180
中的  nb_points 从 180 又改回为 30

python test_colmap_reader.py \
-s /home/gamma/storage_of_code/habitat-sim/camera_output/formal3/colmap \
-m output/test/test-virtual \
--detector PidiNet \
--eval \
--init_voxel_size 0.01 \
--method 0 \
--trajectory_root

然后下一小节传参数的时候，用 outlier_nb_points

## 开启curveGS训练

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_net2 \
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
--outlier_nb_points 30 \
--init_voxel_size 0.01

**注意，下一步需要转化为.bin**
colmap model_converter \
--input_path . \
--output_path . \
--output_type BIN


python edge_extraction/eval_replica.py \
--dataset_dir /data1/jhc/datasets/virtual_net2 \
--base_dir output/virtual_net2 \
--sample_resolution 0.002

## 开启gs训练


unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_curve_repeat1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_curve_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual_curve_repeat1



unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_curve_repeat2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_curve_repeat2 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual_curve_repeat2



unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_curve_repeat3 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_curve_repeat3 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual_curve_repeat3

# 8.12

## 修改 补点

在第一阶段筛选垂直补点的基础（只保留XY各自方向上  包围盒尺寸1/20 进行垂直补点）上进一步筛选
增加第二阶段，判断补点的矩形范围有没有已知点（fill_x_threshold为10的原因是，墙是沿着x方向延伸的）

python test_colmap_reader.py \
-s /home/gamma/storage_of_code/habitat-sim/camera_output/formal3/colmap \
-m output/test/test-virtual2 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 10 \
--fill_y_threshold 0.5 \
--fill_grid_resX 200 \
--fill_grid_resY 100 \
--fill_grid_resZ 50 \
--trajectory_root

同时测试一下其他数据集效果：
自行车:
python test_colmap_reader.py \
-s /home/gamma/rosbags/mipnerf360/bicycle \
-m output/test/test-bicycle_8.12 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 0.1 \
--fill_y_threshold 0.1 \
--trajectory_root \
--outlier_nb_points 180

DrJ:
python test_colmap_reader.py \
-s /home/gamma/rosbags/DrJohnson_Reconstruction_Inputs_Outputs/colmap \
-m output/test/test-DrJ2 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 0.1 \
--fill_y_threshold 0.1 \
--fill_grid_resX 200 \
--fill_grid_resY 125 \
--fill_grid_resZ 125 \
--trajectory_root

## 给curveGS训练















