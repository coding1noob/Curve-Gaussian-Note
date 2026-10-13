0. buaa_net
165
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python mask_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_1 \
--iteration 30000 \
--threshold 0.9 \
--device cuda

**gs**
167
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/buaa_net \
-m /data1/data/jhc/projects/gaussian-splatting/output/buaa_net \
--iteration 30000 \
--threshold 0.9 \
--device cuda

**mip**
167
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/buaa_net \
-m /data1/data/jhc/projects/mip-splatting/output/buaa_net \
--iteration 30000 \
--threshold 0.9 \
--device cuda \
--layout mip_splatting \
--scale_factor -1

**AbsGS**
167
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/buaa_net \
-m /data1/data/jhc/projects/AbsGS/output/buaa_net_only_Abs \
--iteration 30000 \
--threshold 0.9 \
--device cuda

**IndoorGS**
165
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python mask_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m /data1/jhc/storage_of_code/IndoorGS-note/output/buaa_net2 \
--iteration 30000 \
--threshold 0.9 \
--device cuda

**anaGS**
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=3 \
TORCH_HOME=/data1/jhc/torch_cache \
python mask_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m /data1/jhc/storage_of_code/Analytic-Splatting/outputs/buaa_net \
--iteration 30000 \
--threshold 0.9 \
--device cuda

1. net6

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR \
--iteration 30000 \
--threshold 0.9 \
--device cuda
Masked metrics: PSNR=14.046098461857548 SSIM=0.3815522823068831 LPIPS=0.37709343488569613

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/projects/gaussian-splatting/output/net6 \
--iteration 30000 \
--threshold 0.9 \
--device cuda
Masked metrics: PSNR=13.705130965621382 SSIM=0.3719784473931348 LPIPS=0.41354541535730716

**mip**
mv /data1/data/jhc/projects/mip-splatting/output/net6/test/ours_30000/test_preds_-1 /data1/data/jhc/projects/mip-splatting/output/net6/test/ours_30000/renders
mv /data1/data/jhc/projects/mip-splatting/output/net6/test/ours_30000/gt_-1 /data1/data/jhc/projects/mip-splatting/output/net6/test/ours_30000/gt
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/projects/mip-splatting/output/net6 \
--iteration 30000 \
--threshold 0.9 \
--device cuda

**AbsGS**
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/projects/AbsGS/output/net6_only_Abs \
--iteration 30000 \
--threshold 0.9 \
--device cuda

**indoorGS**
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/indoorGS_output/net6 \
--iteration 30000 \
--threshold 0.9 \
--device cuda

**anaGS**
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=3 \
TORCH_HOME=/data1/jhc/torch_cache \
python mask_metrics.py \
-s /data1/jhc/datasets/net6 \
-m /data1/jhc/storage_of_code/Analytic-Splatting/output/net6 \
--iteration 30000 \
--threshold 0.9 \
--device cuda

2. net930

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/net930-0 \
-m /data1/data/jhc/output/3dgs_output/net930-black-0 \
--iteration 30000 \
--threshold 0.9 \
--device cuda
PSNR=15.332342521004055 SSIM=0.40908588290862413 LPIPS=0.3512553381531135

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/net930-0 \
-m /data1/data/jhc/projects/gaussian-splatting/output/net930 \
--iteration 30000 \
--threshold 0.9 \
--device cuda
Masked metrics: PSNR=14.833494227865469 SSIM=0.38894463605854823 LPIPS=0.4076375443002452

**mip**

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/net930-0 \
-m /data1/data/jhc/projects/mip-splatting/output/net930-0 \
--iteration 30000 \
--threshold 0.9 \
--device cuda \
--layout mip_splatting \
--scale_factor -1

**indoorGS**
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/net930-0 \
-m /data1/data/jhc/output/indoorGS_output/net930-0-IndoorGS \
--iteration 30000 \
--threshold 0.9 \
--device cuda

**AbsGS**
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/net930-0 \
-m /data1/data/jhc/projects/AbsGS/output/net930-0 \
--iteration 30000 \
--threshold 0.9 \
--device cuda

**anaGS**
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=3 \
TORCH_HOME=/data1/jhc/torch_cache \
python mask_metrics.py \
-s /data1/jhc/datasets/net930-0 \
-m /data1/jhc/storage_of_code/Analytic-Splatting/output/net930-0 \
--iteration 30000 \
--threshold 0.9 \
--device cuda

3. cuc2

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/cuc2 \
-m /data1/data/jhc/output/3dgs_output/cuc2 \
--iteration 30000 \
--threshold 0.9 \
--device cuda

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/cuc2 \
-m /data1/data/jhc/projects/gaussian-splatting/output/cuc2 \
--iteration 30000 \
--threshold 0.9 \
--device cuda

**mip**

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/cuc2 \
-m /data1/data/jhc/projects/mip-splatting/output/cuc2 \
--iteration 30000 \
--threshold 0.9 \
--device cuda \
--layout mip_splatting \
--scale_factor -1

4. cuc3

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/cuc3 \
-m /data1/data/jhc/output/3dgs_output/cuc3 \
--iteration 30000 \
--threshold 0.9 \
--device cuda

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/cuc3 \
-m /data1/data/jhc/projects/gaussian-splatting/output/cuc3 \
--iteration 30000 \
--threshold 0.9 \
--device cuda


5. 102-2

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/102-2 \
-m /data1/data/jhc/output/3dgs_output/102-2 \
--iteration 30000 \
--threshold 0.9 \
--device cuda

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/102-2 \
-m /data1/data/jhc/projects/gaussian-splatting/output/102-2 \
--iteration 30000 \
--threshold 0.9 \
--device cuda

**AbsGS**
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/102-2 \
-m /data1/data/jhc/projects/AbsGS/output/102-2 \
--iteration 30000 \
--threshold 0.9 \
--device cuda

**mip**

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/102-2 \
-m /data1/data/jhc/projects/mip-splatting/output/102-2 \
--iteration 30000 \
--threshold 0.9 \
--device cuda \
--layout mip_splatting \
--scale_factor -1

**indoorGS**
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/102-2 \
-m /data1/data/jhc/output/indoorGS_output/102-2 \
--iteration 30000 \
--threshold 0.9 \
--device cuda

9. 107-1

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/107-1 \
-m /data1/data/jhc/output/3dgs_output/107-1 \
--iteration 30000 \
--threshold 0.9 \
--device cuda

**gs**
167
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/107-1 \
-m /data1/data/jhc/projects/gaussian-splatting/output/107-1 \
--iteration 30000 \
--threshold 0.9 \
--device cuda
Masked metrics: PSNR=16.28478533881051 SSIM=0.49030434765986036 LPIPS=0.2711176723241806

**mip**
167
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/107-1 \
-m /data1/data/jhc/projects/mip-splatting/output/107-1 \
--iteration 30000 \
--threshold 0.9 \
--device cuda \
--layout mip_splatting \
--scale_factor -1
Masked metrics: PSNR=16.397681508745467 SSIM=0.49980046493666513 LPIPS=0.2436084630233901

**AbsGS**
167
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python mask_metrics.py \
-s /data1/data/jhc/datasets/107-1 \
-m /data1/data/jhc/projects/AbsGS/output/107-1 \
--iteration 30000 \
--threshold 0.9 \
--device cuda
Masked metrics: PSNR=14.759965964726039 SSIM=0.43055825574057444 LPIPS=0.28089796751737595

**IndoorGS**
165
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=3 \
TORCH_HOME=/data1/jhc/torch_cache \
python mask_metrics.py \
-s /data1/jhc/datasets/107/107-1 \
-m /data1/jhc/storage_of_code/IndoorGS-note/output/107-1 \
--iteration 30000 \
--threshold 0.9 \
--device cuda

**anaGS**
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=3 \
TORCH_HOME=/data1/jhc/torch_cache \
python mask_metrics.py \
-s /data1/jhc/datasets/107/107-1 \
-m /data1/jhc/storage_of_code/Analytic-Splatting/output/107-1 \
--iteration 30000 \
--threshold 0.9 \
--device cuda






































