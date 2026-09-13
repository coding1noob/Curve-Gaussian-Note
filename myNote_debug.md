
# 先看 curve点云 

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_curve.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_initial \
--curve_ply /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply \
--eval \
--skip_train

# -m output/virtual8.12_curve_o_repeat1 转变而来

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_o \
--eval \
--disable_viewer \
--curve_opacity_fillter \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply \
--save_iterations 1 2000 5000 10000 20000

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_o \
--iteration 1 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_o \
--iteration 2000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_o \
--iteration 5000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_o \
--iteration 10000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_o \
--iteration 20000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_o \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python render_2.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_o \
--iteration 1 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/virtual_net2/edge_PidiNet

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python render_2.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_o \
--iteration 2000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/virtual_net2/edge_PidiNet

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python render_2.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_o \
--iteration 5000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/virtual_net2/edge_PidiNet

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python render_2.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_o \
--iteration 10000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/virtual_net2/edge_PidiNet

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python render_2.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_o \
--iteration 20000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/virtual_net2/edge_PidiNet

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python render_2.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_o \
--iteration 30000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/virtual_net2/edge_PidiNet

# 

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--save_iterations 1 2000 5000 10000 20000

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6 \
--iteration 1 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6 \
--iteration 2000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6 \
--iteration 5000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6 \
--iteration 10000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6 \
--iteration 20000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6 \
--iteration 30000 \
--skip_train

**渲染训练集**

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6 \
--iteration 30000

---------------------------------------------------------------------------------

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python render_2.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6 \
--iteration 1 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/virtual_net2/edge_PidiNet

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python render_2.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6 \
--iteration 2000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/virtual_net2/edge_PidiNet

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python render_2.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6 \
--iteration 5000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/virtual_net2/edge_PidiNet

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python render_2.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6 \
--iteration 10000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/virtual_net2/edge_PidiNet

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python render_2.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6 \
--iteration 20000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/virtual_net2/edge_PidiNet

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python render_2.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6 \
--iteration 30000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/virtual_net2/edge_PidiNet

# 分析位姿以及指定照片的周围位姿渲染结果

python analytic_pose.py \
--scene /home/gamma/storage_of_code/habitat-sim/camera_output/formal3/colmap \
--index 55

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
python render_random.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6 \
--iteration 30000 \
--test_index 7 \
--num_samples 30 \
--position_radius 0.5 \
--rotation_deg 10

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
python render_random.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6 \
--iteration 30000 \
--test_index 3 \
--num_samples 30 \
--position_radius 0.5 \
--rotation_deg 10

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
python render_random.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6 \
--iteration 30000 \
--test_index 8 \
--num_samples 30 \
--position_radius 0.5 \
--rotation_deg 10

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
python render_random.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6 \
--iteration 30000 \
--split train \
--image_name 000061.png \
--num_samples 30 \
--position_radius 0.5 \
--rotation_deg 10 \
--visible_sh \
--visible_depth

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
python render_random.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6 \
--iteration 30000 \
--split train \
--image_name 000051.png \
--num_samples 30 \
--position_radius 0.5 \
--rotation_deg 10 \
--visible_sh \
--visible_depth


# 使用原本的gaussian库进行渲染

PYTHONPATH=/data1/jhc/storage_of_code/gs_pro6000/submodules/diff-gaussian-rasterization:$PYTHONPATH \
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6_oriGS \
--iteration 30000 \
--skip_train

# 查看泛化能力

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
python render_random.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6 \
--iteration 20000 \
--split train \
--image_name 000051.png \
--num_samples 30 \
--position_radius 0.5 \
--rotation_deg 10 \
--visible_sh \
--visible_depth

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
python render_random.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6_repeat2 \
--iteration 10000 \
--split train \
--image_name 000051.png \
--num_samples 30 \
--position_radius 0.5 \
--rotation_deg 10 \
--visible_sh \
--visible_depth

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
python render_random.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6 \
--iteration 5000 \
--split train \
--image_name 000051.png \
--num_samples 30 \
--position_radius 0.5 \
--rotation_deg 10 \
--visible_sh \
--visible_depth

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
python render_random.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6 \
--iteration 2000 \
--split train \
--image_name 000051.png \
--num_samples 30 \
--position_radius 0.5 \
--rotation_deg 10 \
--visible_sh \
--visible_depth

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
python render_random.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6 \
--iteration 1 \
--split train \
--image_name 000051.png \
--num_samples 30 \
--position_radius 0.5 \
--rotation_deg 10 \
--visible_sh \
--visible_depth

# 手动清除点会不会变好？

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6_clean \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init_manual_clean.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--save_iterations 1 2000 5000 10000 20000

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6_clean \
--iteration 1 \
--skip_train

# 增加 Loss 消融去除

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6_No_outside_loss \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init_manual_clean.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--lambda_outside_loss 0.0 \
--save_iterations 1 2000 5000 10000 15000 20000

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
python render_random.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6_No_outside_loss \
--iteration 30000 \
--split train \
--image_name 000051.png \
--num_samples 30 \
--position_radius 0.5 \
--rotation_deg 10 \
--visible_sh \
--visible_depth

--------------------------------------------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6_No_outside_rgb \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init_manual_clean.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 0.0 \
--lambda_outside_loss 1.0 \
--save_iterations 1 2000 5000 10000 15000 20000

for iteration in 1 2000 5000 10000 15000 20000 30000; do
    echo "Rendering iteration ${iteration}"

    CUDA_DEVICE_ORDER=PCI_BUS_ID \
    CUDA_VISIBLE_DEVICES=2 \
    TORCH_HOME=/data1/jhc/torch_cache \
    python render_metrics.py \
        -s /data1/jhc/datasets/virtual_net2 \
        -m output/DEBUG_omask6_No_outside_rgb \
        --iteration "${iteration}" \
        --skip_train
done

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 \
python render_random.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6_No_outside_rgb \
--iteration 30000 \
--split train \
--image_name 000051.png \
--num_samples 30 \
--position_radius 0.5 \
--rotation_deg 10 \
--visible_sh \
--visible_depth

--------------------------------------------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6_No_outside \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init_manual_clean.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 0.0 \
--lambda_outside_loss 0.0 \
--save_iterations 1 2000 5000 10000 15000 20000

for iteration in 1 2000 5000 10000 15000 20000 30000; do
    echo "Rendering iteration ${iteration}"

    CUDA_DEVICE_ORDER=PCI_BUS_ID \
    CUDA_VISIBLE_DEVICES=5 \
    TORCH_HOME=/data1/jhc/torch_cache \
    python render_metrics.py \
        -s /data1/jhc/datasets/virtual_net2 \
        -m output/DEBUG_omask6_No_outside \
        --iteration "${iteration}" \
        --skip_train
done

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
python render_random.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/DEBUG_omask6_No_outside \
--iteration 30000 \
--split train \
--image_name 000051.png \
--num_samples 30 \
--position_radius 0.5 \
--rotation_deg 10 \
--visible_sh \
--visible_depth

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
python render_random.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data1/jhc/storage_of_code/gaussian-splatting/output/virtual_gs2_repeat3 \
--iteration 30000 \
--split train \
--image_name 000051.png \
--num_samples 30 \
--position_radius 0.5 \
--rotation_deg 10 \
--visible_sh \
--visible_depth

# 9.2
## 无光照
### 仅0阶

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2_noSH \
-m output/virtual_net2_noSH \
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

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/virtual_net2_noSH \
-m /data2/jhc/gs_pro6000/output/DEBUG_omask6_noSH \
--eval \
--disable_viewer \
--sh_degree 0 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noSH/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--save_iterations 1 2000 5000 10000 15000 20000

for iteration in 1 2000 5000 10000 15000 20000 30000; do
    echo "Rendering iteration ${iteration}"

    CUDA_DEVICE_ORDER=PCI_BUS_ID \
    CUDA_VISIBLE_DEVICES=2 \
    TORCH_HOME=/data1/jhc/torch_cache \
    python render_metrics.py \
	-s /data1/jhc/datasets/virtual_net2_noSH \
	-m /data2/jhc/gs_pro6000/output/DEBUG_omask6_noSH \
        --iteration "${iteration}" \
        --skip_train
done

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 \
python render_random.py \
-s /data1/jhc/datasets/virtual_net2_noSH \
-m /data2/jhc/gs_pro6000/output/DEBUG_omask6_noSH \
--iteration 30000 \
--split train \
--image_name 000051.png \
--num_samples 30 \
--position_radius 0.5 \
--rotation_deg 10 \
--visible_sh \
--visible_depth

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 \
python render_random.py \
-s /data1/jhc/datasets/virtual_net2_noSH \
-m /data2/jhc/gs_pro6000/output/DEBUG_omask6_noSH \
--iteration 30000 \
--split train \
--image_name 000061.png \
--num_samples 30 \
--position_radius 0.5 \
--rotation_deg 10 \
--visible_sh \
--visible_depth

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 \
python render_random.py \
-s /data1/jhc/datasets/virtual_net2_noSH \
-m /data2/jhc/gs_pro6000/output/DEBUG_omask6_noSH \
--iteration 30000 \
--image_name 000056.png \
--num_samples 30 \
--position_radius 0.5 \
--rotation_deg 10 \
--visible_sh \
--visible_depth

### 原生GS训一版没有SH的

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/gs_pro6000/output/DEBUG_omask6_noSH_oriGS \
--eval \
--disable_viewer \
--sh_degree 0 \
--save_iterations 1 2000 5000 10000 15000 20000

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/gs_pro6000/output/DEBUG_omask6_noSH_oriGS \
--iteration 30000 \
--skip_train

### 保留SH 3阶

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/gs_pro6000/output/DEBUG_omask6_noLight \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--save_iterations 1 2000 5000 10000 15000 20000

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/gs_pro6000/output/DEBUG_omask6_noLight \
--iteration 30000 \
--skip_train


### 换成纯色地板

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data2/jhc/datasets/formal3_white \
-m /data2/curve_output/virtual_net2_white \
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

3阶SH

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data2/jhc/datasets/formal3_white \
-m /data2/jhc/gs_pro6000/output/DEBUG_omask6_white \
--eval \
--disable_viewer \
--curvegs /data2/curve_output/virtual_net2_white/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--save_iterations 1 2000 5000 10000 15000 20000


CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white \
-m /data2/jhc/gs_pro6000/output/DEBUG_omask6_white \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python render_2.py \
-s /data2/jhc/datasets/formal3_white \
-m /data2/jhc/gs_pro6000/output/DEBUG_omask6_white \
--iteration 1 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data2/jhc/datasets/formal3_white/edge_PidiNet

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python render_2.py \
-s /data2/jhc/datasets/formal3_white \
-m /data2/jhc/gs_pro6000/output/DEBUG_omask6_white \
--iteration 1 \
--skip_train \
--colmap_only \
--edge_folder /data2/jhc/datasets/formal3_white/edge_PidiNet

### 纯色地板的基础上继续删东西

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/curve_output/virtual_net2_white_simple \
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

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/curve_output/virtual_net2_white_simple \
--eval \
--disable_viewer \
--curvegs /data2/curve_output/virtual_net2_white_simple/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--save_iterations 1 2000 5000 10000 15000 20000

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/curve_output/virtual_net2_white_simple \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/curve_output/virtual_net2_white_simple \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python render_2.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/curve_output/virtual_net2_white_simple \
--iteration 1 \
--skip_train \
--colmap_only \
--edge_folder /data2/jhc/datasets/formal3_white/edge_PidiNet







