17.9693
0.5302
0.2919


CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/103-2 \
-m /data1/data/jhc/output/3dgs_output/103-2 \
--iteration 30000 \
--skip_train \
--opacity_filter 0.5

[test] PSNR: 15.7596  SSIM: 0.4655  LPIPS: 0.3990 [04/10 00:43:55]

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/103-2 \
-m /data1/data/jhc/output/3dgs_output/103-2 \
--iteration 30000 \
--skip_train \
--opacity_filter 0.1

[test] PSNR: 17.5334  SSIM: 0.5144  LPIPS: 0.3140 [04/10 00:54:58]


