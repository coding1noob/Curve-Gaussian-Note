# 

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_begin_5000_repeat1 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 5000 \
--curve_xyz_limit_max_generation 160 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_begin_5000_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_begin_5000_repeat1
-----

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_begin_5000_repeat2 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 5000 \
--curve_xyz_limit_max_generation 160 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_begin_5000_repeat2
-----

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_begin_5000_repeat2 \
--iteration 30000 \
--skip_train

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_begin_5000_repeat3 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 5000 \
--curve_xyz_limit_max_generation 160 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_begin_5000_repeat3 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_begin_5000_repeat3
---

SSIM : 0.8873736
PSNR : 28.7044888
LPIPS: 0.2775857

=====================

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_begin_3000_repeat1 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 3000 \
--curve_xyz_limit_max_generation 160 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_begin_3000_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_begin_3000_repeat1

----------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_begin_3000_repeat2 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 3000 \
--curve_xyz_limit_max_generation 160 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_begin_3000_repeat2 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_begin_3000_repeat2

----------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_begin_3000_repeat3 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 3000 \
--curve_xyz_limit_max_generation 160 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_begin_3000_repeat3 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_begin_3000_repeat3

SSIM : 0.8870512
PSNR : 28.6799749
LPIPS: 0.2781901


=====================

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_begin_8000_repeat1 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 8000 \
--curve_xyz_limit_max_generation 160 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_begin_8000_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_begin_8000_repeat1

----------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_begin_8000_repeat2 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 8000 \
--curve_xyz_limit_max_generation 160 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_begin_8000_repeat2 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_begin_8000_repeat2

----------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_begin_8000_repeat3 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 8000 \
--curve_xyz_limit_max_generation 160 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_begin_8000_repeat3 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_begin_8000_repeat3

SSIM : 0.8861606
PSNR : 28.6048851
LPIPS: 0.2780055

# 可选 限制 split 和 optimizer 更新

## split不限制

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_NoSplit_Limit_repeat1 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 0 \
--curve_xyz_limit_max_generation 160 \
--no_xyz_limit_split \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_NoSplit_Limit_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_NoSplit_Limit_repeat1

----------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_NoSplit_Limit_repeat2 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 0 \
--curve_xyz_limit_max_generation 160 \
--no_xyz_limit_split \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_NoSplit_Limit_repeat2 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_NoSplit_Limit_repeat2

----------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_NoSplit_Limit_repeat3 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 0 \
--curve_xyz_limit_max_generation 160 \
--no_xyz_limit_split \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_NoSplit_Limit_repeat3 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_NoSplit_Limit_repeat3

SSIM :    0.8914056	0.8868609	0.8869221
PSNR :   28.9420033	28.6048317	28.5936241
LPIPS:    0.2749818	0.2775299	0.2768871

SSIM  0.8883962
PSNR  28.7134864
LPIPS 0.2764663

----------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_NoSplit_Limit_repeat4 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 0 \
--curve_xyz_limit_max_generation 160 \
--no_xyz_limit_split \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_NoSplit_Limit_repeat4 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_NoSplit_Limit_repeat4

  SSIM :    0.8876894
  PSNR :   28.6517677
  LPIPS:    0.2772305

----------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_NoSplit_Limit_repeat5 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 0 \
--curve_xyz_limit_max_generation 160 \
--no_xyz_limit_split \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_NoSplit_Limit_repeat5 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_NoSplit_Limit_repeat5

  SSIM :    0.8870926
  PSNR :   28.4770145
  LPIPS:    0.2786077

## optimizer不限制

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_NoOptimizer_Limit_repeat1 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 0 \
--curve_xyz_limit_max_generation 160 \
--no_xyz_limit_optimizer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_NoOptimizer_Limit_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_NoOptimizer_Limit_repeat1

----------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_NoOptimizer_Limit_repeat2 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 0 \
--curve_xyz_limit_max_generation 160 \
--no_xyz_limit_optimizer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_NoOptimizer_Limit_repeat2 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_NoOptimizer_Limit_repeat2

----------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_NoOptimizer_Limit_repeat3 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 0 \
--curve_xyz_limit_max_generation 160 \
--no_xyz_limit_optimizer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_NoOptimizer_Limit_repeat3 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_NoOptimizer_Limit_repeat3

SSIM  0.8854984
PSNR  28.6393878
LPIPS 0.2779651

## split不限制也许有用，在这个基础上加 --curve_xyz_limit_begin


unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_NoSplit_Limit_begin5000_repeat1 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 5000 \
--curve_xyz_limit_max_generation 160 \
--no_xyz_limit_split \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_NoSplit_Limit_begin5000_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_NoSplit_Limit_begin5000_repeat1

----------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_NoSplit_Limit_begin5000_repeat2 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 5000 \
--curve_xyz_limit_max_generation 160 \
--no_xyz_limit_split \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_NoSplit_Limit_begin5000_repeat2 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_NoSplit_Limit_begin5000_repeat2

----------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_NoSplit_Limit_begin5000_repeat3 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 5000 \
--curve_xyz_limit_max_generation 160 \
--no_xyz_limit_split \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_NoSplit_Limit_begin5000_repeat3 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_NoSplit_Limit_begin5000_repeat3


SSIM : 0.8879361
PSNR : 28.6730009
LPIPS: 0.2779015



# 增加 Loss

## 一次实验

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_Limit_Loss_repeat1 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 0 \
--curve_xyz_limit_max_generation 160 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply \
--lambda_aniso_opacity 0.005 \
--aniso_opacity_ratio_threshold 10 \
--aniso_opacity_min 0.08

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_Limit_Loss_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_Limit_Loss_repeat1

------------------------------------------------------------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_Limit_Loss_repeat2 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 0 \
--curve_xyz_limit_max_generation 160 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply \
--lambda_aniso_opacity 0.005 \
--aniso_opacity_ratio_threshold 10 \
--aniso_opacity_min 0.08

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_Limit_Loss_repeat2 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_Limit_Loss_repeat2

------------------------------------------------------------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_Limit_Loss_repeat3 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 0 \
--curve_xyz_limit_max_generation 160 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply \
--lambda_aniso_opacity 0.005 \
--aniso_opacity_ratio_threshold 10 \
--aniso_opacity_min 0.08

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_Limit_Loss_repeat3 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_Limit_Loss_repeat3


上面平均值：

SSIM : 0.8874808
PSNR : 28.6210524
LPIPS: 0.2771704


## 二次实验

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_Limit_Loss_repeat1 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 0 \
--curve_xyz_limit_max_generation 160 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply \
--lambda_aniso_opacity 0.01 \
--aniso_opacity_ratio_threshold 5 \
--aniso_opacity_min 0.1

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_Limit_Loss_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_Limit_Loss_repeat1

------------------------------------------------------------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_Limit_Loss_repeat2 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 0 \
--curve_xyz_limit_max_generation 160 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply \
--lambda_aniso_opacity 0.01 \
--aniso_opacity_ratio_threshold 5 \
--aniso_opacity_min 0.1

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_Limit_Loss_repeat2 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_Limit_Loss_repeat2

------------------------------------------------------------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_Limit_Loss_repeat3 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 0 \
--curve_xyz_limit_max_generation 160 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply \
--lambda_aniso_opacity 0.01 \
--aniso_opacity_ratio_threshold 5 \
--aniso_opacity_min 0.1

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_Limit_Loss_repeat3 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_Limit_Loss_repeat3


上面平均值（本地命名loss1）：

SSIM : 0.8879928
PSNR : 28.6425082
LPIPS: 0.2766834

## 三次实验

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_Limit_Loss2_repeat1 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 0 \
--curve_xyz_limit_max_generation 160 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply \
--lambda_aniso_opacity 0.01 \
--aniso_opacity_ratio_threshold 5 \
--aniso_opacity_min 0.3

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_Limit_Loss2_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_Limit_Loss2_repeat1

------------------------------------------------------------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_Limit_Loss2_repeat2 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 0 \
--curve_xyz_limit_max_generation 160 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply \
--lambda_aniso_opacity 0.01 \
--aniso_opacity_ratio_threshold 5 \
--aniso_opacity_min 0.3

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_Limit_Loss2_repeat2 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_Limit_Loss2_repeat2

------------------------------------------------------------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_Limit_Loss2_repeat3 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--curve_xyz_limit_begin 0 \
--curve_xyz_limit_max_generation 160 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply \
--lambda_aniso_opacity 0.05 \
--aniso_opacity_ratio_threshold 5 \
--aniso_opacity_min 0.3

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_Limit_Loss2_repeat3 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_Limit_Loss2_repeat3

SSIM : 0.8848361
PSNR : 28.4834544
LPIPS: 0.2791541


## 最后融合 no_xyz_limit_split 实验

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_Limit_noSplit_Loss_repeat1 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--no_xyz_limit_split \
--curve_xyz_limit_begin 0 \
--curve_xyz_limit_max_generation 160 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply \
--lambda_aniso_opacity 0.01 \
--aniso_opacity_ratio_threshold 5 \
--aniso_opacity_min 0.1

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_Limit_noSplit_Loss_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_Limit_noSplit_Loss_repeat1

------------------------------------------------------------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_Limit_noSplit_Loss_repeat2 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--no_xyz_limit_split \
--curve_xyz_limit_begin 0 \
--curve_xyz_limit_max_generation 160 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply \
--lambda_aniso_opacity 0.01 \
--aniso_opacity_ratio_threshold 5 \
--aniso_opacity_min 0.1

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_Limit_noSplit_Loss_repeat2 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_Limit_noSplit_Loss_repeat2

------------------------------------------------------------------------------------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_Limit_noSplit_Loss_repeat3 \
--eval \
--disable_viewer \
--curve_xyz_limit \
--no_xyz_limit_split \
--curve_xyz_limit_begin 0 \
--curve_xyz_limit_max_generation 160 \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/DrJ3/curve_3dgs_init.ply \
--lambda_aniso_opacity 0.01 \
--aniso_opacity_ratio_threshold 5 \
--aniso_opacity_min 0.1

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/DrJ \
-m output/DrJ3_xyzLimit_Limit_noSplit_Loss_repeat3 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/DrJ3_xyzLimit_Limit_noSplit_Loss_repeat3








