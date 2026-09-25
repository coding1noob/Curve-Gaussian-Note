
# mip-splatting 北航无人院网

60k结果：

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m /data1/jhc/storage_of_code/mip-splatting/output/buaa_net_only_mip \
--iteration 30000 \
--skip_train

[test] PSNR: 18.9432  SSIM: 0.5369  LPIPS: 0.4113 [24/09 21:47:08]

30k结果：

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m /data1/jhc/storage_of_code/mip-splatting/output/buaa_net_only_mip2 \
--eval

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m /data1/jhc/storage_of_code/mip-splatting/output/buaa_net_only_mip2 \
--iteration 30000 \
--skip_train

[test] PSNR: 18.8726  SSIM: 0.5375  LPIPS: 0.4117 [24/09 22:40:38]

# mip-splatting 体育场网

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/net6 \
-m /data1/jhc/storage_of_code/mip-splatting/output/net6_only_mip \
--eval

cd ../gs_pro6000
conda activate curveGS

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/net6 \
-m /data1/jhc/storage_of_code/mip-splatting/output/net6_only_mip \
--iteration 30000 \
--skip_train

[test] PSNR: 16.0262  SSIM: 0.4687  LPIPS: 0.4254 [25/09 09:10:33]

60k试试

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/net6 \
-m /data1/jhc/storage_of_code/mip-splatting/output/net6_only_mip2 \
--eval \
--iteration 60000

cd ../gs_pro6000
conda activate curveGS

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=4 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/net6 \
-m /data1/jhc/storage_of_code/mip-splatting/output/net6_only_mip2 \
--iteration 60000 \
--skip_train

[test] PSNR: 15.1672  SSIM: 0.4188  LPIPS: 0.4544 [25/09 11:20:16]










































