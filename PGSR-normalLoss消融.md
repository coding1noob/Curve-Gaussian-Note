# 165服务器 

1. factory2
2. tennis1
3. buaa_net

./nextStep_noNormal.sh \
/data2/jhc/output/curve_output/factory2/curve_3dgs_init.ply \
/data2/jhc/datasets/factory2 \
/data2/jhc/output/3dgs_output/factory2_noNormal \
2

[test] PSNR: 24.9234  SSIM: 0.8116  LPIPS: 0.2679 [29/10 01:58:41]

./nextStep_noNormal.sh \
/data2/jhc/output/curve_output/tennis1/curve_3dgs_init.ply \
/data2/jhc/datasets/tennis1 \
/data2/jhc/output/3dgs_output/tennis1_noNormal \
2

[test] PSNR: 26.1561  SSIM: 0.8959  LPIPS: 0.1316 [29/10 04:48:53]

./nextStep_noNormal.sh \
/data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
/data1/jhc/datasets/buaa_net \
/data2/jhc/output/3dgs_output/buaaNet_noNormal \
2

[test] PSNR: 21.1346  SSIM: 0.6001  LPIPS: 0.3525 [29/10 07:28:30]

./nextStep_noNormal.sh \
/data2/jhc/output/curve_output/net6v2/curve_3dgs_init.ply \
/data1/jhc/datasets/net6 \
/data2/jhc/output/3dgs_output/net6v2_noNormal \
2

[test] PSNR: 19.1004  SSIM: 0.5658  LPIPS: 0.3362 [29/10 09:10:16]

## 930白天
7. net930-0
2. sand_night3
6. 102-2

./nextStep_noNormal.sh \
/data2/jhc/output/curve_output/net930-0/curve_3dgs_init.ply \
/data1/jhc/datasets/net930-0 \
/data2/jhc/output/3dgs_output/net930-0_noNormal \
3
[test] PSNR: 19.5711  SSIM: 0.4913  LPIPS: 0.3506 [29/10 14:46:48]

./nextStep_noNormal.sh \
/data2/jhc/output/curve_output/sand_night3_2/curve_3dgs_init.ply \
/data2/jhc/datasets/sand_night3 \
/data2/jhc/output/3dgs_output/sand_night3_2_noNormal \
3
[test] PSNR: 29.9864  SSIM: 0.8780  LPIPS: 0.1483 [29/10 17:08:16]

./nextStep_noNormal.sh \
/data2/jhc/output/curve_output/102-2/curve_3dgs_init.ply \
/data1/jhc/datasets/102-2 \
/data2/jhc/output/3dgs_output/102-2_noNormal \
3
[test] PSNR: 17.1524  SSIM: 0.5323  LPIPS: 0.3799 [29/10 19:58:36]

# 167服务器 

1. sand_sun2
2. sand_night3
3. V109
4. 1010-2 略微不对
5. 107-1-black
6. 102-2
7. net930-0
8. net6v2

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep_noNormal.sh \
/data1/data/jhc/output/curve_output/sand_sun2/curve_3dgs_init.ply \
/data1/data/jhc/datasets/sand_sun2 \
/data1/data/jhc/output/3dgs_output/sand_sun2_noNormal \
2

[test] PSNR: 19.0471  SSIM: 0.7261  LPIPS: 0.2570 [29/10 00:41:50]

./nextStep_noNormal.sh \
/data2/jhc/output/curve_output/sand_night3_2/curve_3dgs_init.ply \
/data2/jhc/datasets/sand_night3 \
/data2/jhc/output/3dgs_output/sand_night3_2_noNormal \
2

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep_noNormal.sh \
/data1/data/jhc/output/curve_output/V109/curve_3dgs_init.ply \
/data1/data/jhc/datasets/formal3_white \
/data1/data/jhc/output/3dgs_output/V109_noNormal \
2

[test] PSNR: 32.6283  SSIM: 0.9734  LPIPS: 0.0472 [29/10 01:30:24]

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep_noNormal.sh \
/data1/data/jhc/output/curve_output/1010-2/curve_3dgs_init.ply \
/data1/data/jhc/datasets/1010-2 \
/data1/data/jhc/output/3dgs_output/1010-2_noNormal \
2

[test] PSNR: 17.2775  SSIM: 0.5725  LPIPS: 0.3164 [29/10 05:31:20]

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep_noNormal.sh \
/data1/data/jhc/output/curve_output/107-1-black/curve_3dgs_init.ply \
/data1/data/jhc/datasets/107-1 \
/data1/data/jhc/output/3dgs_output/107-1_noNormal \
2

[test] PSNR: 21.5772  SSIM: 0.6572  LPIPS: 0.2648 [29/10 08:01:22]

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep_noNormal.sh \
/data1/data/jhc/output/curve_output/102-2/curve_3dgs_init.ply \
/data1/data/jhc/datasets/102-2 \
/data1/data/jhc/output/3dgs_output/102-2_noNormal \
2

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep_noNormal.sh \
/data1/data/jhc/output/curve_output/net930-0/curve_3dgs_init.ply \
/data1/data/jhc/datasets/net930-0 \
/data1/data/jhc/output/3dgs_output/net930-0_noNormal \
2

PATH=/data1/conda_env/buaajhc/curveGS/bin:$PATH \
./nextStep_noNormal.sh \
/data1/data/jhc/output/curve_output/net6v2/curve_3dgs_init.ply \
/data1/data/jhc/datasets/net6 \
/data1/data/jhc/output/3dgs_output/net6v2_noNormal \
20






































