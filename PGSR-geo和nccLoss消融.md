# 165服务器 

1. factory2 高0.38
2. tennis1 低0.27
3. buaa_net 低0.04

5. 107-1-black 低0.1
6. 102-2 低0.04
8. net6v2 低0.18

./nextStep_noMultiLoss.sh \
/data2/jhc/output/curve_output/factory2/curve_3dgs_init.ply \
/data2/jhc/datasets/factory2 \
/data2/jhc/output/3dgs_output/factory2_noMultiLoss \
3
[test] PSNR: 25.5891  SSIM: 0.8248  LPIPS: 0.2548 [29/10 02:42:39]

./nextStep_noMultiLoss.sh \
/data2/jhc/output/curve_output/tennis1/curve_3dgs_init.ply \
/data2/jhc/datasets/tennis1 \
/data2/jhc/output/3dgs_output/tennis1_noMultiLoss \
3
[test] PSNR: 25.7356  SSIM: 0.8853  LPIPS: 0.1399 [29/10 05:33:14]

./nextStep_noMultiLoss.sh \
/data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
/data1/jhc/datasets/buaa_net \
/data2/jhc/output/3dgs_output/buaaNet_noMultiLoss \
3
[test] PSNR: 21.3448  SSIM: 0.5982  LPIPS: 0.3532 [29/10 07:34:10]

./nextStep_noMultiLoss.sh \
/data2/jhc/output/curve_output/107-1-black/curve_3dgs_init.ply \
/data1/jhc/datasets/107-1 \
/data2/jhc/output/3dgs_output/107-1_noMultiLoss \
3
[test] PSNR: 21.5605  SSIM: 0.6536  LPIPS: 0.2594 [29/10 08:43:05]

./nextStep_noMultiLoss.sh \
/data2/jhc/output/curve_output/102-2/curve_3dgs_init.ply \
/data1/jhc/datasets/102-2 \
/data2/jhc/output/3dgs_output/102-2_noMultiLoss \
3
[test] PSNR: 17.1018  SSIM: 0.5306  LPIPS: 0.3766 [29/10 09:47:42]

./nextStep_noMultiLoss.sh \
/data2/jhc/output/curve_output/net6v2/curve_3dgs_init.ply \
/data1/jhc/datasets/net6 \
/data2/jhc/output/3dgs_output/net6v2_noMultiLoss \
3
[test] PSNR: 18.9576  SSIM: 0.5569  LPIPS: 0.3412 [29/10 10:51:21]

## 10.29白天
7. net930-0 低0.1
1. sand_sun2 低0.05
2. sand_night3 高0.1
3. V109 高0.05
4. 1010-2 高0.05

./nextStep_noMultiLoss.sh \
/data2/jhc/output/curve_output/net930-0/curve_3dgs_init.ply \
/data1/jhc/datasets/net930-0 \
/data2/jhc/output/3dgs_output/net930-0_noMultiLoss \
2
[test] PSNR: 19.5683  SSIM: 0.4900  LPIPS: 0.3509 [29/10 13:19:45]

./nextStep_noMultiLoss.sh \
/data2/jhc/output/curve_output/sand_sun2/curve_3dgs_init.ply \
/data2/jhc/datasets/sand_sun2 \
/data2/jhc/output/3dgs_output/sand_sun2_noMultiLoss \
2
[test] PSNR: 19.0344  SSIM: 0.7202  LPIPS: 0.2565 [29/10 14:25:12]

./nextStep_noMultiLoss.sh \
/data2/jhc/output/curve_output/sand_night3_2/curve_3dgs_init.ply \
/data2/jhc/datasets/sand_night3 \
/data2/jhc/output/3dgs_output/sand_night3_2_noMultiLoss \
2
[test] PSNR: 30.2685  SSIM: 0.8786  LPIPS: 0.1416 [29/10 16:34:23]

./nextStep_noMultiLoss.sh \
/data2/jhc/output/curve_output/V109/curve_3dgs_init.ply \
/data2/jhc/datasets/formal3_white \
/data2/jhc/output/3dgs_output/V109 \
2
[test] PSNR: 32.7538  SSIM: 0.9722  LPIPS: 0.0492 [29/10 18:14:29]

./nextStep_noMultiLoss.sh \
/data2/jhc/output/curve_output/1010-2/curve_3dgs_init.ply \
/data2/jhc/datasets/1010-2 \
/data2/jhc/output/3dgs_output/1010-2 \
2
[test] PSNR: 17.2782  SSIM: 0.5658  LPIPS: 0.3171 [29/10 20:44:47]

# 167服务器 

1. sand_sun2
2. sand_night3
3. V109
4. 1010-2
5. 107-1-black
6. 102-2
7. net930-0
8. net6v2

./run_nerf.sh mipnerf360/bicycle 0

./run_nerf.sh mipnerf360/stump 0

./run_nerf.sh mipnerf360/garden 0

cd ../Curve-Gaussian-Note && conda activate curveGS

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep_noMultiLoss.sh \
/data1/data/jhc/output/curve_output/sand_sun2/curve_3dgs_init.ply \
/data1/data/jhc/datasets/sand_sun2 \
/data1/data/jhc/output/3dgs_output/sand_sun2_noMultiLoss \
0

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep_noMultiLoss.sh \
/data2/jhc/output/curve_output/sand_night3_2/curve_3dgs_init.ply \
/data2/jhc/datasets/sand_night3 \
/data2/jhc/output/3dgs_output/sand_night3_2_noMultiLoss \
0

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep_noMultiLoss.sh \
/data1/data/jhc/output/curve_output/V109/curve_3dgs_init.ply \
/data1/data/jhc/datasets/formal3_white \
/data1/data/jhc/output/3dgs_output/V109_noMultiLoss \
0

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep_noMultiLoss.sh \
/data1/data/jhc/output/curve_output/1010-2/curve_3dgs_init.ply \
/data1/data/jhc/datasets/1010-2 \
/data1/data/jhc/output/3dgs_output/1010-2_noMultiLoss \
0

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep_noMultiLoss.sh \
/data1/data/jhc/output/curve_output/107-1-black/curve_3dgs_init.ply \
/data1/data/jhc/datasets/107-1 \
/data1/data/jhc/output/3dgs_output/107-1_noMultiLoss \
20

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep_noMultiLoss.sh \
/data1/data/jhc/output/curve_output/102-2/curve_3dgs_init.ply \
/data1/data/jhc/datasets/102-2 \
/data1/data/jhc/output/3dgs_output/102-2_noMultiLoss \
20

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep_noMultiLoss.sh \
/data1/data/jhc/output/curve_output/net930-0/curve_3dgs_init.ply \
/data1/data/jhc/datasets/net930-0 \
/data1/data/jhc/output/3dgs_output/net930-0_noMultiLoss \
20

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep_noMultiLoss.sh \
/data1/data/jhc/output/curve_output/net6v2/curve_3dgs_init.ply \
/data1/data/jhc/datasets/net6 \
/data1/data/jhc/output/3dgs_output/net6v2_noMultiLoss \
20

## mipnerf360

./nextStep_noMultiLoss.sh \
/data2/jhc/output/curve_output/mipnerf360/bicycle/curve_3dgs_init.ply \
/data1/jhc/datasets/mipnerf360/bicycle \
/data2/jhc/output/3dgs_output/bicycle_noMultiLoss \
2
[test] PSNR: 25.1740  SSIM: 0.7581  LPIPS: 0.2250 [30/10 02:58:03]

./nextStep_noMultiLoss.sh \
/data2/jhc/output/curve_output/mipnerf360/garden_nofilter/curve_3dgs_init.ply \
/data1/jhc/datasets/mipnerf360/garden \
/data2/jhc/output/3dgs_output/garden_noMultiLoss \
2
[test] PSNR: 27.4602  SSIM: 0.8581  LPIPS: 0.1228 [30/10 05:12:46]

./nextStep_noMultiLoss.sh \
/data2/jhc/output/curve_output/stump2/curve_3dgs_init.ply \
/data1/jhc/datasets/mipnerf360/stump \
/data2/jhc/output/3dgs_output/stump_noMultiLoss \
2
[test] PSNR: 26.5597  SSIM: 0.7633  LPIPS: 0.2433 [30/10 06:42:32]

./nextStep_noNormal.sh \
/data2/jhc/output/curve_output/mipnerf360/bicycle/curve_3dgs_init.ply \
/data1/jhc/datasets/mipnerf360/bicycle \
/data2/jhc/output/3dgs_output/bicycle_noNormal \
2
[test] PSNR: 25.2408  SSIM: 0.7604  LPIPS: 0.2271 [30/10 09:06:44]

./nextStep_noNormal.sh \
/data2/jhc/output/curve_output/mipnerf360/garden_nofilter/curve_3dgs_init.ply \
/data1/jhc/datasets/mipnerf360/garden \
/data2/jhc/output/3dgs_output/garden_noNormal \
2
[test] PSNR: 27.4264  SSIM: 0.8596  LPIPS: 0.1230 [30/10 11:22:43]

./nextStep_noNormal.sh \
/data2/jhc/output/curve_output/stump2/curve_3dgs_init.ply \
/data1/jhc/datasets/mipnerf360/stump \
/data2/jhc/output/3dgs_output/stump_noNormal \
2
[test] PSNR: 26.6883  SSIM: 0.7716  LPIPS: 0.2434 [30/10 13:01:36]

## TnT

./nextStep_noMultiLoss.sh \
/data2/jhc/output/curve_output/TnT/Truck/curve_3dgs_init.ply \
/data1/jhc/datasets/TnT/Truck \
/data2/jhc/output/3dgs_output/Truck_noMultiLoss \
2
[test] PSNR: 21.8243  SSIM: 0.7460  LPIPS: 0.2945 [31/10 02:21:27]

./nextStep_noMultiLoss.sh \
/data2/jhc/output/curve_output/TnT/M60-2/curve_3dgs_init.ply \
/data1/jhc/datasets/TnT/M60 \
/data2/jhc/output/3dgs_output/M60-2_noMultiLoss \
2
[test] PSNR: 20.9642  SSIM: 0.7520  LPIPS: 0.3427 [31/10 03:32:09]

./nextStep_noMultiLoss.sh \
/data2/jhc/output/curve_output/TnT/Train3/curve_3dgs_init.ply \
/data1/jhc/datasets/TnT/Train \
/data2/jhc/output/3dgs_output/Train3_noMultiLoss \
2
[test] PSNR: 20.1698  SSIM: 0.6988  LPIPS: 0.3122 [31/10 04:37:56]

./nextStep_noNormal.sh \
/data2/jhc/output/curve_output/TnT/Truck/curve_3dgs_init.ply \
/data1/jhc/datasets/TnT/Truck \
/data2/jhc/output/3dgs_output/Truck_noNormal \
2
[test] PSNR: 21.8427  SSIM: 0.7458  LPIPS: 0.2987 [31/10 06:30:22]

./nextStep_noNormal.sh \
/data2/jhc/output/curve_output/TnT/M60-2/curve_3dgs_init.ply \
/data1/jhc/datasets/TnT/M60 \
/data2/jhc/output/3dgs_output/M60-2_noNormal \
2
[test] PSNR: 21.0208  SSIM: 0.7532  LPIPS: 0.3432 [31/10 08:04:53]

./nextStep_noNormal.sh \
/data2/jhc/output/curve_output/TnT/Train3/curve_3dgs_init.ply \
/data1/jhc/datasets/TnT/Train \
/data2/jhc/output/3dgs_output/Train3_noNormal \
2
[test] PSNR: 20.2939  SSIM: 0.7000  LPIPS: 0.3159 [31/10 09:34:23]













