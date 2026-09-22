运行 PGSR 分支前还需要编译 CUDA 扩展：
cd submodules/diff-plane-rasterization
pip install -v -e . --no-build-isolation

同时记得加
#include <cstdint>


1. 
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--save_iterations 15000 20000 22500 25000

2. 
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--save_iterations 18000 20000 25000 \
--checkpoint_iterations 18000 20000 25000

3. 发现限制 相邻相机 太小了，改宽限制条件

默认条件是：
  最大视角夹角：30°
  最小距离：0.01
  最大距离：1.5
  最多邻机：8
变成：
--multi_view_max_angle 45 \
--multi_view_max_dis 3.0 \
--multi_view_min_dis 0.01 \
--multi_view_num 8

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR2_2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_max_angle 45 \
--multi_view_max_dis 3.0 \
--multi_view_min_dis 0.01 \
--multi_view_num 8 \
--start_checkpoint /data2/jhc/3dgs_output/virtual_net2_PGSR2/chkpnt18000.pth

4. 忘记加--curvegs_inject_iteration 20000了，同时修改权重

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR2_3 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_max_angle 45 \
--multi_view_max_dis 3.0 \
--multi_view_min_dis 0.01 \
--multi_view_num 8 \
--multi_view_geo_weight 0.01 \
--multi_view_ncc_weight 0.03 \
--start_checkpoint /data2/jhc/3dgs_output/virtual_net2_PGSR2/chkpnt18000.pth

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python render_2.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR2_3 \
--iteration 30000 \
--geoLoss \
--nccLoss \
--curve_only \
--PGSR_depth \
--d_mask_classify \
--skip_test

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_2.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR2_3 \
--iteration 30000 \
--curve_only \
--PGSR_depth


确实权重降低了指标上升了:
[ITER 30000] Evaluating test: L1 0.020141685883013103 PSNR 28.61430549621582 [06/09 23:09:50]

5. 只加 geoloss

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR2_4 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_max_angle 45 \
--multi_view_max_dis 3.0 \
--multi_view_min_dis 0.01 \
--multi_view_num 8 \
--multi_view_geo_weight 0.01 \
--multi_view_ncc_weight 0.0 \
--start_checkpoint /data2/jhc/3dgs_output/virtual_net2_PGSR2/chkpnt18000.pth

6. 只加 nccloss

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR2_5 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_max_angle 45 \
--multi_view_max_dis 3.0 \
--multi_view_min_dis 0.01 \
--multi_view_num 8 \
--multi_view_geo_weight 0.0 \
--multi_view_ncc_weight 0.03 \
--start_checkpoint /data2/jhc/3dgs_output/virtual_net2_PGSR2/chkpnt18000.pth

7. 延后进场时间

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR2_6 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_max_angle 45 \
--multi_view_max_dis 3.0 \
--multi_view_min_dis 0.01 \
--multi_view_num 8 \
--multi_view_geo_weight 0.0 \
--multi_view_ncc_weight 0.03 \
--multi_view_weight_from_iter 22000 \
--start_checkpoint /data2/jhc/3dgs_output/virtual_net2_PGSR2/chkpnt18000.pth

8. 正常情况

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR2_ori \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--start_checkpoint /data2/jhc/3dgs_output/virtual_net2_PGSR2/chkpnt18000.pth

5到8依次来看，正常情况(不加)最好，延迟次之，nccloss再次，geoloss最差

9. 代替 2. ，只不过再是随机了，而前3个邻近相机都用

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR3 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_max_angle 45 \
--multi_view_max_dis 3.0 \
--multi_view_min_dis 0.01 \
--save_iterations 19000 20000 25000 \
--checkpoint_iterations 19000 20000 25000 \
--multi_view_pixel_noise_th 3

[ITER 30000] Evaluating test: L1 0.02088314681672133 PSNR 28.345067097590523 [08/09 01:35:52]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python render_2.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR3 \
--iteration 30000 \
--iteration 30000 \
--geoLoss \
--nccLoss \
--curve_only \
--PGSR_depth \
--d_mask_classify


--- 周二 ---
10. 超级扩大（不随机）

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR3_1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_max_angle 80 \
--multi_view_max_dis 6.0 \
--multi_view_min_dis 0.01 \
--start_checkpoint /data2/jhc/3dgs_output/virtual_net2_PGSR3/chkpnt19000.pth

[ITER 30000] Evaluating test: L1 0.027997244149446487 PSNR 26.165190916794998 [08/09 10:20:54]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python render_2.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR3_1 \
--iteration 30000 \
--geoLoss \
--nccLoss \
--curve_only \
--PGSR_depth \
--d_mask_classify

11. 好卡，还是只算一个邻近相机的吧（不随机），只不过multi_view_max_angle啥的还是超级扩大

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR3_2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_max_angle 80 \
--multi_view_max_dis 6.0 \
--multi_view_min_dis 0.01 \
--multi_view_num 1 \
--start_checkpoint /data2/jhc/3dgs_output/virtual_net2_PGSR3/chkpnt19000.pth

[ITER 30000] Evaluating test: L1 0.0226068591269163 PSNR 27.431512099045975 [08/09 10:17:35]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python render_2.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR3_2 \
--iteration 30000 \
--geoLoss \
--nccLoss \
--curve_only \
--PGSR_depth \
--d_mask_classify

12. 确实11.和10.区别不大，那就只算一个的吧，但是随机，并且 --multi_view_pixel_noise_th 更大胆一点

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR3_3 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_max_angle 80 \
--multi_view_max_dis 6.0 \
--multi_view_min_dis 0.01 \
--multi_view_num 1 \
--start_checkpoint /data2/jhc/3dgs_output/virtual_net2_PGSR3/chkpnt19000.pth \
--multi_view_pixel_noise_th 10

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python render_2.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR3_3 \
--iteration 30000 \
--geoLoss \
--nccLoss \
--curve_only \
--PGSR_depth \
--d_mask_classify

13. 把 --curvegs_inject_iteration 和  --multi_view_weight_from_iter 都提前

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR3_4 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply \
--curvegs_inject_iteration 10000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_max_angle 80 \
--multi_view_max_dis 6.0 \
--multi_view_min_dis 0.01 \
--multi_view_num 1 \
--multi_view_weight_from_iter 11000 \
--multi_view_pixel_noise_th 10 \
--save_iterations 5000 8000 10000 15000 \
--checkpoint_iterations 5000 8000 15000

[ITER 30000] Evaluating test: L1 0.02011410304560111 PSNR 28.221371430617115 [08/09 14:13:54]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python render_2.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR3_4 \
--iteration 30000 \
--geoLoss \
--nccLoss \
--curve_only \
--PGSR_depth \
--d_mask_classify

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR3_4 \
--iteration 30000 \
--skip_train

14. 只提前 --curvegs_inject_iteration 但不加 --PGSR_depth

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR3_5 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply \
--curvegs_inject_iteration 10000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--start_checkpoint /data2/jhc/3dgs_output/virtual_net2_PGSR3_4/chkpnt8000.pth

-------------------------------------------------------------------------------------------

20. 开始用 简化的场景, 并且是没有sh

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR4 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--sh_degree 0 \
--save_iterations 8000 15000 19999 \
--checkpoint_iterations 8000 15000 19999

[ITER 30000] Evaluating test: L1 0.026400151232687328 PSNR 25.48656933124249 [08/09 13:52:54]

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/virtual_net2_PGSR4 \
--iteration 30000 \
--skip_train

21. 简化场景且不加 PGSR_depth

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR4_noPGSR \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--sh_degree 0 \
--start_checkpoint /data2/jhc/3dgs_output/virtual_net2_PGSR4/chkpnt19999.pth

[ITER 30000] Evaluating test: L1 0.02320560784294055 PSNR 26.343692926260143 [08/09 14:27:50]

22. 简化场景且只加 geoloss

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR4_onlyGeoloss \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--sh_degree 0 \
--multi_view_ncc_weight 0.0 \
--start_checkpoint /data2/jhc/3dgs_output/virtual_net2_PGSR4/chkpnt19999.pth

------------LLFF HOLD------------- [08/09 17:08:41]
[ITER 30000] Evaluating test: L1 0.025198041174847346 PSNR 25.75601885868953 [08/09 18:04:50]

23. 简化场景且只加 nccloss

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/3dgs_output/virtual_net2_PGSR4_onlyNccloss \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--sh_degree 0 \
--multi_view_geo_weight 0.0 \
--start_checkpoint /data2/jhc/3dgs_output/virtual_net2_PGSR4/chkpnt19999.pth

------------LLFF HOLD------------- [08/09 15:44:28]
[ITER 30000] Evaluating test: L1 0.025535003425410163 PSNR 25.66809756939228 [08/09 16:39:57]

24. 试试现实数据集，只加PGSR，当然记得要加 --multi_view_num 1

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/3dgs_output/buaa_net8.12_onlyPGSR \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--PGSR_depth \
--multi_view_max_angle 45 \
--multi_view_max_dis 4.0 \
--multi_view_min_dis 0.01 \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000

[ITER 30000] Evaluating test: L1 0.05452958802724707 PSNR 21.181381094044653 [08/09 18:53:25]

25. 虚拟场景也只用PGSR

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/virtual_net2_onlyPGSR \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--PGSR_depth \
--sh_degree 0 \
--save_iterations 8000 15000 19999 \
--checkpoint_iterations 8000 15000 19999

------------LLFF HOLD------------- [09/09 13:52:12]
[ITER 30000] Evaluating test: L1 0.020084474235773087 PSNR 27.399567090548004 [09/09 14:53:42]

26. 补充一下不加任何的sh_0实验

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/virtual_net2_onlyCurve \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--save_iterations 8000 15000 19999

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/virtual_net2_onlyCurve \
--iteration 30000 \
--eval \
--skip_train

# 9.10晚上

1. 先试PGSR在sh_0，延后至20000再开始，并且仅保留geoLoss的表现

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/jhc/output/PGSR_output/virtual_net2_white_simple_PGSR_onlyGeoLoss_begin20k \
--eval \
--curvegs /data2/jhc/output/curve_output/virtual_net2_white_simple/curve_3dgs_init.ply \
--sh_degree 0 \
--single_view_weight 0.0 \
--multi_view_ncc_weight 0.0 \
--multi_view_weight_from_iter 20000

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data2/jhc/datasets/formal3_white_simple \
-m /data2/jhc/output/PGSR_output/virtual_net2_white_simple_PGSR_onlyGeoLoss_begin20k \
--iteration 30000 \
--skip_train

26. 保留其余重新跑一下

2. 先跑不分割的（因为26没分割），然后加PGSR

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_nomask_PGSRfull \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--PGSR_depth \
--multi_view_num 1

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_nomask_PGSRfull \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_nomask_PGSRfull \
--iteration 30000 \
--eval \
--skip_train

3. 再在上面基础上只保留NCC和只保留GEO

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_nomask_PGSR_onlyNCC \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_geo_weight 0.0 \
--save_iterations 20000 25000

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_nomask_PGSR_onlyNCC \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_nomask_PGSR_onlyNCC \
--iteration 30000 \
--eval \
--skip_train

----------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_nomask_PGSR_onlyGEO \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_ncc_weight 0.0 \
--save_iterations 20000 25000

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_nomask_PGSR_onlyGEO \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_nomask_PGSR_onlyGEO \
--iteration 30000 \
--eval \
--skip_train

4. 再跑一个增加范围的(全保留)

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_nomask_PGSRfull_addRange \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_max_angle 45 \
--multi_view_max_dis 4.5 \
--multi_view_min_dis 0.01

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_nomask_PGSRfull_addRange \
--iteration 30000 \
--skip_train

5. 再跑一个增加数量的(全保留)

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_nomask_PGSRfull_addNum \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--PGSR_depth \
--multi_view_num 3

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_nomask_PGSRfull_addNum \
--iteration 30000 \
--skip_train

6. 再跑一个分割的，加PGSR的

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask_PGSRfull \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--PGSR_depth \
--multi_view_num 1 \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask_PGSRfull \
--iteration 30000 \
--skip_train

7. 再跑一个分割，PGSR只保留GEO的

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask_PGSR_onlyGEO \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--PGSR_depth \
--multi_view_num 1 \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--multi_view_ncc_weight 0.0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask_PGSR_onlyGEO \
--iteration 30000 \
--skip_train

8. 再跑一个只分割，但是不用PGSR的

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0 \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask \
--iteration 30000 \
--skip_train

[test] PSNR: 26.1045  SSIM: 0.9013  LPIPS: 0.1237 [11/09 11:22:00]

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_mask \
--iteration 30000 \
--eval \
--skip_train

9. 只融合curveGS但不mask

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_nomask \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_noLight/curve_3dgs_init.ply \
--sh_degree 0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_nomask \
--iteration 30000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_PGSR.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/Curve_nomask \
--iteration 30000 \
--eval \
--skip_train


10. 复杂地面nolight场景，跑baseline

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/orin_gs \
--eval \
--disable_viewer \
--sh_degree 0

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight \
-m /data2/jhc/output/3dgs_output/910/orin_gs \
--iteration 30000 \
--skip_train



