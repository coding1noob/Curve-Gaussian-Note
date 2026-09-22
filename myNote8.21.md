# 增添了 opacity mask外的惩罚，重新编译

cd submodules/diff-gaussian-rasterization
rm -rf build
pip uninstall diff-gaussian-rasterization -y
pip install . --no-build-isolation

# 开始训练

1. 

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask_repeat1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/buaa_net8.12_omask_repeat1

------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask_repeat2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask_repeat2 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/buaa_net8.12_omask_repeat2


CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask_repeat2 \
--iteration 20000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask_repeat2 \
--iteration 20000 \
--skip_train \
--colmap_only \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask_repeat2 \
--iteration 20000 \
--skip_train \
--curve_only \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet


------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask_repeat3 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask_repeat3 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/buaa_net8.12_omask_repeat3



2. 

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask2_repeat1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask2_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/buaa_net8.12_omask2_repeat1

------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask2_repeat2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask2_repeat2 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/buaa_net8.12_omask2_repeat2

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask2_repeat2 \
--iteration 20000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask2_repeat2 \
--iteration 20000 \
--skip_train \
--colmap_only \
--alpha \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask2_repeat2 \
--iteration 20000 \
--skip_train \
--curve_only \
--alpha \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask2_repeat3 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask2_repeat3 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/buaa_net8.12_omask2_repeat3

3. 测试：--outside_alpha_margin 0.0 看看能否让背景没有颜色

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask3_repeat1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask3_repeat1 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask3_repeat1

------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask3_repeat2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask3_repeat2 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask3_repeat2

------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask3_repeat3 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask3_repeat3 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask3_repeat3

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask3_repeat3 \
--iteration 20000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask3_repeat3 \
--iteration 20000 \
--skip_train \
--colmap_only \
--alpha \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask3_repeat3 \
--iteration 20000 \
--skip_train \
--curve_only \
--alpha \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

4. 把非边缘区域颜色泄露抑制到0

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask4_repeat1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 0.1

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask4_repeat1 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask4_repeat1

------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask4_repeat2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 0.1

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask4_repeat2 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask4_repeat2

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask4_repeat2 \
--iteration 20000 \
--skip_train \
--curve_only \
--alpha \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask4_repeat3 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 0.1

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask4_repeat3 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask4_repeat3


5. 加大剂量！把非边缘区域颜色泄露抑制到0

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask5_repeat1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask5_repeat1 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask5_repeat1

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask5_repeat1 \
--iteration 20000 \
--skip_train \
--curve_only \
--alpha \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask5_repeat1 \
--iteration 20000 \
--skip_train

-------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask5_repeat2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask5_repeat2 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask5_repeat2

-------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask5_repeat3 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask5_repeat3 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask5_repeat3

6. 用一用 RGB初始化的点云试试

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask5_RGB_repeat1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3_RGB/curve_3dgs_init_RGB.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask5_RGB_repeat1 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask5_RGB_repeat1

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask5_RGB_repeat1 \
--iteration 20000 \
--skip_train \
--curve_only \
--alpha \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

# 分析 curve 点初始化位置

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_curve.py \
-s /data1/jhc/datasets/buaa_net \
-m /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3 \
--curve_ply /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--eval \
--skip_train

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_curve.py \
-s /data1/jhc/datasets/buaa_net \
-m /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3_RGB \
--curve_ply /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3_RGB/curve_3dgs_init_RGB.ply \
--eval \
--skip_train

7. 增加置信度

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask6_repeat1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3_RGB/curve_3dgs_init_RGB.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--curve_confidence_edge_threshold 0.5 \
--curve_confidence_dilation_radius 0 \

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask6_repeat1 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask6_repeat1

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask6_repeat1 \
--iteration 20000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet


8. 增加 use_axis_direction_loss

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_axisDirection1_repeat1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--curve_confidence_edge_threshold 0.5 \
--curve_confidence_dilation_radius 0 \
--use_axis_direction_loss \
--lambda_axis_direction 0.005

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_axisDirection1_repeat1 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask7_axisDirection1_repeat1

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_axisDirection1_repeat1 \
--iteration 20000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

---------------------------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_axisDirection1_repeat2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--curve_confidence_edge_threshold 0.5 \
--curve_confidence_dilation_radius 0 \
--use_axis_direction_loss \
--lambda_axis_direction 0.01

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_axisDirection1_repeat2 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask7_axisDirection1_repeat2

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_axisDirection1_repeat2 \
--iteration 20000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

---------------------------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_axisDirection1_repeat3 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--curve_confidence_edge_threshold 0.5 \
--curve_confidence_dilation_radius 0 \
--use_axis_direction_loss \
--lambda_axis_direction 0.05

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_axisDirection1_repeat3 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask7_axisDirection1_repeat3

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_axisDirection1_repeat3 \
--iteration 20000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

---------------------------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_axisDirection1_repeat4 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--curve_confidence_edge_threshold 0.5 \
--curve_confidence_dilation_radius 0 \
--use_axis_direction_loss \
--lambda_axis_direction 0.1

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_axisDirection1_repeat4 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask7_axisDirection1_repeat4

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_axisDirection1_repeat4 \
--iteration 20000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

9. 在虚拟数据集上试试

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_omask6_repeat4 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_omask6_repeat4 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual8.12_omask6_repeat4

10. 增加 长轴Loss

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_ratioLoss1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--curve_confidence_edge_threshold 0.5 \
--curve_confidence_dilation_radius 0 \
--use_ratio_shape_loss \
--lambda_ratio_shape 0.0005

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_ratioLoss1 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask7_ratioLoss1 \

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_ratioLoss1 \
--iteration 20000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

-----------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_ratioLoss2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--curve_confidence_edge_threshold 0.5 \
--curve_confidence_dilation_radius 0 \
--use_ratio_shape_loss \
--lambda_ratio_shape 0.005

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_ratioLoss2 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask7_ratioLoss2 \

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_ratioLoss2 \
--iteration 20000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_ratioLoss3 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--curve_confidence_edge_threshold 0.5 \
--curve_confidence_dilation_radius 0 \
--use_ratio_shape_loss \
--lambda_ratio_shape 0.01

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_ratioLoss3 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask7_ratioLoss3 \

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_ratioLoss3 \
--iteration 20000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_ratioLoss4 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--curve_confidence_edge_threshold 0.5 \
--curve_confidence_dilation_radius 0 \
--use_ratio_shape_loss \
--lambda_ratio_shape 0.05

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_ratioLoss4 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask7_ratioLoss4 \

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_ratioLoss4 \
--iteration 20000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_ratioLoss5 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--curve_confidence_edge_threshold 0.5 \
--curve_confidence_dilation_radius 0 \
--use_ratio_shape_loss \
--lambda_ratio_shape 0.1

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_ratioLoss5 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask7_ratioLoss5 \

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_ratioLoss5 \
--iteration 20000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

11. 走之前的补充

**一致性补充实验**

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_axisDirection1_repeat5 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--curve_confidence_edge_threshold 0.5 \
--curve_confidence_dilation_radius 0 \
--use_axis_direction_loss \
--lambda_axis_direction 0.5

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_axisDirection1_repeat5 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask7_axisDirection1_repeat5

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_axisDirection1_repeat5 \
--iteration 20000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_axisDirection1_repeat6 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--curve_confidence_edge_threshold 0.5 \
--curve_confidence_dilation_radius 0 \
--use_axis_direction_loss \
--lambda_axis_direction 1.0

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_axisDirection1_repeat6 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask7_axisDirection1_repeat6

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_axisDirection1_repeat6 \
--iteration 20000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_axisDirection1_repeat7 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--curve_confidence_edge_threshold 0.5 \
--curve_confidence_dilation_radius 0 \
--use_axis_direction_loss \
--lambda_axis_direction 2.0

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_axisDirection1_repeat7 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask7_axisDirection1_repeat7

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_axisDirection1_repeat7 \
--iteration 20000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

**长轴比补充实验**

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_ratioLoss6 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--curve_confidence_edge_threshold 0.5 \
--curve_confidence_dilation_radius 0 \
--use_ratio_shape_loss \
--lambda_ratio_shape 0.5

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_ratioLoss6 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask7_ratioLoss6 \

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_ratioLoss6 \
--iteration 20000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_ratioLoss7 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--curve_confidence_edge_threshold 0.5 \
--curve_confidence_dilation_radius 0 \
--use_ratio_shape_loss \
--lambda_ratio_shape 1.0

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_ratioLoss7 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask7_ratioLoss7 \

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_ratioLoss7 \
--iteration 20000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_ratioLoss8 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--curve_confidence_edge_threshold 0.5 \
--curve_confidence_dilation_radius 0 \
--use_ratio_shape_loss \
--lambda_ratio_shape 2.0

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_ratioLoss8 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask7_ratioLoss8 \

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_ratioLoss8 \
--iteration 20000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

**新增的实验** --curve_confidence_reset

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_confidenceReset1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--curve_confidence_edge_threshold 0.5 \
--curve_confidence_dilation_radius 0 \
--curve_confidence_reset

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_confidenceReset1 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask7_confidenceReset1

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_confidenceReset1 \
--iteration 20000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

------------------------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_confidenceReset2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--curve_confidence_edge_threshold 0.5 \
--curve_confidence_dilation_radius 0 \
--curve_confidence_reset

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_confidenceReset2 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask7_confidenceReset2

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_confidenceReset2 \
--iteration 20000 \
--skip_train \
--curve_only \
--confidence \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

------------------------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_confidenceReset3 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000 \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--curve_confidence_edge_threshold 0.5 \
--curve_confidence_dilation_radius 0 \
--curve_confidence_reset

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_confidenceReset3 \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python metrics.py \
-m output/buaa_net8.12_omask7_confidenceReset3




CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask7_confidenceReset1 \
--iteration 30000 \
--skip_train


12. 分析.ply

summary.json	总汇总文件，最重要。里面有总点数、CurveGS 点数、KNN 参数、各指标的均值/分位数，以及 curve_confidence 和 opacity / anisotropy / direction consistency 的相关性。
curve_points_metrics.csv	点级明细表，最大那个文件。每一行对应一个 CurveGS 点，包含它的 xyz、generation、curve_confidence、实际 opacity、长中短轴尺度、长轴方向、邻域方向一致性等。
confidence_bins.csv	按 confidence 分箱后的统计。比如 [0,0.2)、[0.2,0.4)、[0.8,1.0] 每一组里的平均 opacity、平均 anisotropy、方向一致性等，用来看高 confidence 点是否真的更像稳定边缘点。
confidence_hist.png	curve_confidence 分布直方图。看 confidence 是集中在高分、低分，还是大多数在中间。
opacity_hist.png	CurveGS 点真实不透明度分布，注意这里已经是 sigmoid(opacity_logit) 后的实际 opacity。
anisotropy_longest_shortest_hist.png	最长轴 / 最短轴 分布。值越大，说明高斯越扁/越细，但它不能区分“线状”还是“片状”。
line_ratio_longest_middle_hist.png	最长轴 / 中间轴 分布。这个更接近“是否真的线状”。值越大，说明最长轴明显比另外两个轴长，更像线。
axis_neighbor_consistency_hist.png	每个点的主轴方向和 KNN 邻居主轴方向的一致性。值是 abs(cos)，接近 1 表示邻域方向平行或反平行，接近 0 表示方向乱。
axis_to_neighbor_vector_alignment_hist.png	每个点的主轴方向是否沿着邻居连线方向。接近 1 表示长轴沿着局部点云走向，接近 0 表示垂直。
confidence_vs_opacity.png	散点图：confidence 和 opacity 的关系。用来看高 confidence 点是不是也更不透明。
confidence_vs_anisotropy.png	散点图：confidence 和 最长轴/最短轴 的关系。用来看高 confidence 点是否更细。
confidence_vs_axis_consistency.png	散点图：confidence 和邻域主轴一致性的关系。用来看高 confidence 点是否方向更稳定。

python analytic_ply.py /home/gamma/storage_of_code/gs_seldom/3dgs_output/buaa_net_output/'长轴比增大 约束实验'/buaa_net8.12_omask7_ratioLoss8_权重2.0/iteration_20000/point_cloud.ply


13. 


CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask5_repeat1 \
--iteration 30000 \
--skip_train \
--curve_only \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_omask5_repeat1 \
--iteration 30000 \
--skip_train \
--colmap_only \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet





































