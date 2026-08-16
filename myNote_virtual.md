
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

## 用新补点方法  给curveGS训练

**virtaul:**
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_net2_8.12 \
--eval \
--iterations 30000 \
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
--init_voxel_size 0.01

python edge_extraction/eval_replica.py \
--dataset_dir /data1/jhc/datasets/virtual_net2 \
--base_dir output/virtual_net2_8.12 \
--sample_resolution 0.002

**DrJ:**
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ_8.12 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 0.1 \
--fill_y_threshold 0.1 \
--fill_grid_resX 200 \
--fill_grid_resY 125 \
--fill_grid_resZ 125 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01

python edge_extraction/eval_replica.py \
--dataset_dir /data1/jhc/datasets/DrJ \
--base_dir output/DrJ_8.12 \
--sample_resolution 0.002

number of curves/lines: 923 96594

## 给gs训练

**virtaul:**
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_repeat1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual8.12_curve_repeat1

----------------------------------------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_repeat2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_repeat2 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual8.12_curve_repeat2

----------------------------------------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_repeat3 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_repeat3 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual8.12_curve_repeat3

----------------------------------------------------------------------------------------

**DrJ:**

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ8.12_onlyCurve_repeat1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ_8.12/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ8.12_onlyCurve_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ8.12_onlyCurve_repeat1

--------------------------------------------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ8.12_onlyCurve_repeat2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ_8.12/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ8.12_onlyCurve_repeat2 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ8.12_onlyCurve_repeat2

--------------------------------------------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ8.12_onlyCurve_repeat3 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ_8.12/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ8.12_onlyCurve_repeat3 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ8.12_onlyCurve_repeat3

最终结果：
SSIM: 0.8854900
PSNR: 28.6281920
LPIPS: 0.2778380

## 模块叠加（虚拟场景）（单个单个增加上去）

### 只增加不透明度改进 （reset 到 0.01？）

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_o_repeat1 \
--eval \
--disable_viewer \
--curve_opacity_fillter \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_o_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual8.12_curve_o_repeat1

### 只增加位置改进

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_xyz_repeat1 \
--eval \
--disable_viewer \
--curve_xyz_fillter \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_xyz_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual8.12_curve_xyz_repeat1

### 只增加mcmc

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_mcmc_repeat1 \
--eval \
--disable_viewer \
--mcmc \
--relocation \
--cap_max 5000000 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_mcmc_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual8.12_curve_mcmc_repeat1

### 只限制线高斯移动

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_xyzLimit_repeat1 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_xyzLimit_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual8.12_curve_xyzLimit_repeat1

### 只限制线高斯移动（5代）

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_xyzLimit_repeat1 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_xyzLimit_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual8.12_curve_xyzLimit_repeat1

-----------------------------------------

### 不限制保护继承范围

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_xyzLimit_no_max_repeat1 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_max_generation 3000 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_xyzLimit_no_max_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual8.12_curve_xyzLimit_no_max_repeat1

### 延迟启用方向限制(5000后开始)

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_xyzLimit_begin5000_repeat1 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_max_generation 3000 \
--curve_xyz_limit_begin 5000 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_xyzLimit_begin5000_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual8.12_curve_xyzLimit_begin5000_repeat1

8.14从这开始
### 只限制 split，不限制 optimizer

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_xyzLimit_onlySplit_repeat1 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_max_generation 3000 \
--no_xyz_limit_optimizer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_xyzLimit_onlySplit_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual8.12_curve_xyzLimit_onlySplit_repeat1

### 只限制 optimizer，不限制 split

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_xyzLimit_onlyOptim_repeat1 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_max_generation 3000 \
--no_xyz_limit_split \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_xyzLimit_onlyOptim_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual8.12_curve_xyzLimit_onlyOptim_repeat1

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_curve_xyzLimit_onlyOptim_repeat3 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual8.12_curve_xyzLimit_onlyOptim_repeat3

### 最终指令

./total_train.sh 2 1                                                                              
./total_train.sh 3 2   
./total_train.sh 4 3

## 模块叠加（真实场景）

### 再做一个小测试

python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/buaa_net \
-m output/test/buaa_net_simple-3_8.12 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 10 \
--fill_y_threshold 0.5 \
--fill_grid_resX 200 \
--fill_grid_resY 100 \
--fill_grid_resZ 50 \
--trajectory_root

### 开启curveGS训练

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net_simple-3 \
--eval \
--iterations 30000 \
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
--outlier_nb_points 30 \
--init_voxel_size 0.01

python edge_extraction/eval_replica.py \
--dataset_dir /data1/jhc/datasets/buaa_net \
--base_dir output/buaa_net_simple-3 \
--sample_resolution 0.002

number of curves/lines: 274 17232

### 给 gs 训练

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_curve_repeat1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_curve_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/buaa_net8.12_curve_repeat1

--------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_curve_repeat2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_curve_repeat2 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/buaa_net8.12_curve_repeat2

--------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_curve_repeat3 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_curve_repeat3 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/buaa_net8.12_curve_repeat3

# 手动删除点

1. 
python delete_point.py \
--input output/virtual_net2_8.12/curve_3dgs_init.ply \
--output output/virtual_net2_8.12/curve_3dgs_init_manual_clean.ply \
--boxes \
1 3 20 1.25 1.28 0.15 1 0 0 0 \
1 3 20 -0.07 1.37 -4.68 1 0 0 0 \
1 3 20 0.90 1.25 -0.13 1 0 0 0 \
1 3 2 3.81 1.48 -20.04 1 0 0 0 \
2 3 2 3.09 1.57 1.37 1 0 0 0 \
2 3 2 3.29 1.59 -3.19 1 0 0 0 \
2 3 2 3.14 1.57 -7.21 1 0 0 0 \
2 3 2 3.32 1.40 -14.50 1 0 0 0 \
2 3 3 3.03 1.32 7.75 1 0 0 0 \
2 4 3 2.23 1.80 -0.82 1 0 0 0 \
2 4 3 2.22 1.80 -5.35 1 0 0 0 \
2 4 3 2.27 1.80 3.69 1 0 0 0 

然后gs训练

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_curve_clean_repeat1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init_manual_clean.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_curve_clean_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual_curve_clean_repeat1



unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_curve_clean_repeat2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init_manual_clean.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_curve_clean_repeat2 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual_curve_clean_repeat2



unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_curve_clean_repeat3 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init_manual_clean.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_curve_clean_repeat3 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual_curve_clean_repeat3

2. 
python delete_point.py \
--input /home/gamma/storage_of_code/Curve-Gaussian/output/buaa_net_simple-3/curve_3dgs_init.ply \
--output /home/gamma/storage_of_code/Curve-Gaussian/output/buaa_net_simple-3/curve_3dgs_init_manual_clean.ply \
--boxes \
0.5 1.5 15 \
-0.420650 -1.278502 2.937510 \
0.107289 0.990806 0.082419 55.456095 \
1.5 3.5 15 \
-1.257110 -2.035127 3.930944 \
0.126510 0.985490 0.113157 55.768713
  
  
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_curve_clean_repeat1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init_manual_clean.ply \
--eval \
--disable_viewer

TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_curve_clean_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/buaa_net8.12_curve_clean_repeat1
  
  
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_curve_clean_repeat2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init_manual_clean.ply \
--eval \
--disable_viewer

TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_curve_clean_repeat2 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/buaa_net8.12_curve_clean_repeat2
  
  
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_curve_clean_repeat3 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init_manual_clean.ply \
--eval \
--disable_viewer

TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_curve_clean_repeat3 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/buaa_net8.12_curve_clean_repeat3




















