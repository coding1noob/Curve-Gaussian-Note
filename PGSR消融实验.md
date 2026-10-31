# 165服务器 

1. factory2 中不正常

./nextStep_noPGSR.sh \
/data2/jhc/output/curve_output/factory2/curve_3dgs_init.ply \
/data2/jhc/datasets/factory2 \
/data2/jhc/output/3dgs_output/factory2_noPGSR \
4

[test] PSNR: 25.7676  SSIM: 0.8296  LPIPS: 0.2445 [24/10 02:36:46]

2. tennis1

./nextStep_noPGSR.sh \
/data2/jhc/output/curve_output/tennis1/curve_3dgs_init.ply \
/data2/jhc/datasets/tennis1 \
/data2/jhc/output/3dgs_output/tennis1_noPGSR \
4

[test] PSNR: 25.5350  SSIM: 0.8826  LPIPS: 0.1428 [24/10 03:43:18]

3. buaa_net

./nextStep_noPGSR.sh \
/data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
/data1/jhc/datasets/buaa_net \
/data2/jhc/output/3dgs_output/buaaNet_noPGSR \
4

[test] PSNR: 21.3855  SSIM: 0.5976  LPIPS: 0.3529 [24/10 04:31:58]

# 167服务器 

1. sand_sun2 略微不正常

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep_noPGSR.sh \
/data1/data/jhc/output/curve_output/sand_sun2/curve_3dgs_init.ply \
/data1/data/jhc/datasets/sand_sun2 \
/data1/data/jhc/output/3dgs_output/sand_sun2_noPGSR \
2

[test] PSNR: 19.1056  SSIM: 0.7251  LPIPS: 0.2516 [24/10 02:56:07]

2. sand_night3 很不正常

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep_noPGSR.sh \
/data1/data/jhc/output/curve_output/sand_night3/curve_3dgs_init.ply \
/data1/data/jhc/datasets/sand_night3 \
/data1/data/jhc/output/3dgs_output/sand_night3_noPGSR \
2

[test] PSNR: 29.9133  SSIM: 0.8719  LPIPS: 0.1455 [24/10 07:39:10]

重新做试验

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 \
python train.py \
-s /data2/jhc/datasets/sand_night3 \
-m /data2/jhc/output/curve_output/sand_night3_2 \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 3 \
--fill_y_threshold 3 \
--fill_z_threshold 0.5 \
--fill_grid_resX 150 \
--fill_grid_resY 150 \
--fill_grid_resZ 30 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 5 \
--outlier_std_ratio 0.01 \
--camera_point_distance 3 \
--SGCR \
--final_opacity_cull 0.5 \
--final_ratio_cull 2.0 \
--final_maxLength_percentile_cull 10

./nextStep.sh \
/data2/jhc/output/curve_output/sand_night3_2/curve_3dgs_init.ply \
/data2/jhc/datasets/sand_night3 \
/data2/jhc/output/3dgs_output/sand_night3_2 \
4
[test] PSNR: 30.1777  SSIM: 0.8838  LPIPS: 0.1436 [24/10 13:18:16]

./nextStep_noPGSR.sh \
/data2/jhc/output/curve_output/sand_night3_2/curve_3dgs_init.ply \
/data2/jhc/datasets/sand_night3 \
/data2/jhc/output/3dgs_output/sand_night3_2_noPGSR \
5
[test] PSNR: 29.8022  SSIM: 0.8743  LPIPS: 0.1449 [24/10 12:56:27]

3. V109

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep_noPGSR.sh \
/data1/data/jhc/output/curve_output/V109/curve_3dgs_init.ply \
/data1/data/jhc/datasets/formal3_white \
/data1/data/jhc/output/3dgs_output/V109_noPGSR \
2

[test] PSNR: 32.3363  SSIM: 0.9705  LPIPS: 0.0495 [24/10 10:08:42]

4. 1010-2

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep_noPGSR.sh \
/data1/data/jhc/output/curve_output/1010-2/curve_3dgs_init.ply \
/data1/data/jhc/datasets/1010-2 \
/data1/data/jhc/output/3dgs_output/1010-2_noPGSR \
2
[test] PSNR: 17.1188  SSIM: 0.5564  LPIPS: 0.3256 [24/10 11:26:59]

5. 107-1-black

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep_noPGSR.sh \
/data1/data/jhc/output/curve_output/107-1-black/curve_3dgs_init.ply \
/data1/data/jhc/datasets/107-1 \
/data1/data/jhc/output/3dgs_output/107-1_noPGSR \
1

[test] PSNR: 21.5493  SSIM: 0.6517  LPIPS: 0.2596 [24/10 03:35:49]

6. 102-2

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep_noPGSR.sh \
/data1/data/jhc/output/curve_output/102-2/curve_3dgs_init.ply \
/data1/data/jhc/datasets/102-2 \
/data1/data/jhc/output/3dgs_output/102-2_noPGSR \
1

[test] PSNR: 16.9759  SSIM: 0.5258  LPIPS: 0.3822 [24/10 07:29:35]

7. net930-0

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep_noPGSR.sh \
/data1/data/jhc/output/curve_output/net930-0/curve_3dgs_init.ply \
/data1/data/jhc/datasets/net930-0 \
/data1/data/jhc/output/3dgs_output/net930-0_noPGSR \
1

[test] PSNR: 19.5453  SSIM: 0.4889  LPIPS: 0.3534 [24/10 10:15:29]

8. net6v2

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep_noPGSR.sh \
/data1/data/jhc/output/curve_output/net6v2/curve_3dgs_init.ply \
/data1/data/jhc/datasets/net6 \
/data1/data/jhc/output/3dgs_output/net6v2_noPGSR \
1

[test] PSNR: 19.0284  SSIM: 0.5556  LPIPS: 0.3415 [24/10 11:11:43]






































