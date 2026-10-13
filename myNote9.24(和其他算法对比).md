
# 北航无人院网
## AbsGS(167服务器)

source /opt/conda/etc/profile.d/conda.sh
conda activate /data1/conda_env/buaajhc/absGS
export PATH="$CONDA_PREFIX/bin:$PATH"
hash -r

1. 无人院

cd ../AbsGS
conda activate absGS

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python train.py \
-s /data1/data/jhc/datasets/buaa_net \
-m output/buaa_net_only_Abs \
--iteration 30000 \
--eval

cd ../3dgs_note
conda activate curveGS

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/buaa_net \
-m /data1/data/jhc/projects/AbsGS/output/buaa_net_only_Abs \
--iteration 30000 \
--skip_train

[test] PSNR: 20.6883  SSIM: 0.5631  LPIPS: 0.3731 [26/09 09:26:42]

2. 体育场

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python train.py \
-s /data1/data/jhc/datasets/net6 \
-m output/net6_only_Abs \
--iteration 30000 \
--eval

cd ../3dgs_note
conda activate curveGS

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/projects/AbsGS/output/net6_only_Abs \
--iteration 30000 \
--skip_train

[test] PSNR: 18.7902  SSIM: 0.5479  LPIPS: 0.3730 [26/09 09:28:07]

3. 

cd ../AbsGS
conda activate absGS	
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/jhc/torch_cache \
python train.py \
-s /data1/data/jhc/datasets/net927_1 \
-m output/net927_1 \
--iteration 30000 \
--eval

cd ../3dgs_note
conda activate curveGS
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net927_1 \
-m /data1/data/jhc/projects/AbsGS/output/net927_1 \
--iteration 30000 \
--skip_train

[test] PSNR: 18.8629  SSIM: 0.4822  LPIPS: 0.3470 [28/09 10:15:44]


# gaussian原版算法

conda create \
--prefix /data1/conda_env/buaajhc/gs \
--clone /data1/conda_env/buaajhc/mip

python -m pip uninstall diff-gaussian-rasterization

cd submodules/diff-gaussian-rasterization
python -m pip install -e . --no-build-isolation

## 1. 无人院

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python train.py \
-s /data1/data/jhc/datasets/buaa_net \
-m output/buaa_net \
--iteration 30000 \
--eval

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render.py \
-s /data1/data/jhc/datasets/buaa_net \
-m output/buaa_net \
--skip_train \
--iteration 30000

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python metrics.py \
-m output/buaa_net

## 2. net6

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python train.py \
-s /data1/data/jhc/datasets/net6 \
-m output/net6 \
--iteration 30000 \
--eval

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render.py \
-s /data1/data/jhc/datasets/net6 \
-m output/net6 \
--skip_train \
--iteration 30000

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python metrics.py \
-m output/net6

## 3. net928_1

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/jhc/torch_cache \
python train.py \
-s /data1/data/jhc/datasets/net928_1 \
-m output/net928_1 \
--iteration 30000 \
--eval \
--disable_view

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render.py \
-s /data1/data/jhc/datasets/net928_1 \
-m output/net928_1 \
--skip_train \
--iteration 30000

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python metrics.py \
-m output/net928_1

  SSIM :    0.6144162
  PSNR :   20.2024479
  LPIPS:    0.3043507

## 3. net928_1luan

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/jhc/torch_cache \
python train.py \
-s /data1/data/jhc/datasets/net928_1luan \
-m output/net928_1luan \
--iteration 30000 \
--eval \
--disable_view

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render.py \
-s /data1/data/jhc/datasets/net928_1luan \
-m output/net928_1luan \
--skip_train \
--iteration 30000

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python metrics.py \
-m output/net928_1luan

  SSIM :    0.6155263
  PSNR :   19.7000427
  LPIPS:    0.2926037



## 4. net928_1.2

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/jhc/torch_cache \
python train.py \
-s /data1/data/jhc/datasets/net928_1.2 \
-m output/net928_1.2 \
--iteration 30000 \
--eval \
--disable_view

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render.py \
-s /data1/data/jhc/datasets/net928_1.2 \
-m output/net928_1.2 \
--skip_train \
--iteration 30000

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python metrics.py \
-m output/net928_1.2

  SSIM :    0.5877501
  PSNR :   18.0396633
  LPIPS:    0.3354633

## 5. net928_2

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python train.py \
-s /data1/data/jhc/datasets/net928_2 \
-m output/net928_2 \
--iteration 30000 \
--eval \
--disable_view

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render.py \
-s /data1/data/jhc/datasets/net928_2 \
-m output/net928_2 \
--skip_train \
--iteration 30000

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python metrics.py \
-m output/net928_2

  SSIM :    0.6607236
  PSNR :   20.7408257
  LPIPS:    0.2821249

## 5. net929

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python train.py \
-s /data1/data/jhc/datasets/net929 \
-m output/net929 \
--iteration 30000 \
--eval \
--disable_view

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render.py \
-s /data1/data/jhc/datasets/net929 \
-m output/net929 \
--skip_train \
--iteration 30000

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python metrics.py \
-m output/net929

## 6. net930

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python train.py \
-s /data1/data/jhc/datasets/net930 \
-m output/net930 \
--iteration 30000 \
--eval \
--disable_view

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render.py \
-s /data1/data/jhc/datasets/net930 \
-m output/net930 \
--skip_train \
--iteration 30000

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python metrics.py \
-m output/net930

  SSIM :    0.4907007
  PSNR :   19.6599312
  LPIPS:    0.3845825

for CAM in net930-1 net930-2 net930-3 net930-4 net930-5
do
	CUDA_DEVICE_ORDER=PCI_BUS_ID \
	CUDA_VISIBLE_DEVICES=2 \
	TORCH_HOME=/data1/jhc/torch_cache \
	python train.py \
	-s /data1/data/jhc/datasets/"$CAM" \
	-m output/"$CAM" \
	--iteration 30000 \
	--eval \
	--disable_view

	CUDA_DEVICE_ORDER=PCI_BUS_ID \
	CUDA_VISIBLE_DEVICES=2 \
	TORCH_HOME=/data1/data/jhc/torch_cache \
	python render.py \
	-s /data1/data/jhc/datasets/"$CAM" \
	-m output/"$CAM" \
	--skip_train \
	--iteration 30000

	CUDA_DEVICE_ORDER=PCI_BUS_ID \
	CUDA_VISIBLE_DEVICES=2 \
	TORCH_HOME=/data1/data/jhc/torch_cache \
	python metrics.py \
	-m output/"$CAM"
done

## 7. CUC

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES="$device" \
TORCH_HOME=/data1/jhc/torch_cache \
python train.py \
-s "$S" \
-m "$M" \
--iteration 30000 \
--eval \
--disable_view

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES="$device" \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render.py \
-s "$S" \
-m "$M" \
--skip_train \
--iteration 30000

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES="$device" \
TORCH_HOME=/data1/data/jhc/torch_cache \
python metrics.py \
-m "$M"

上面保存为run_exp.sh

./run_exp.sh \
/data1/data/jhc/datasets/cuc1 \
/data1/data/jhc/output/curve_output/cuc1 \
0

./run_exp.sh \
/data1/data/jhc/datasets/cuc2 \
/data1/data/jhc/projects/gaussian-splatting/output/cuc2 \
0

./run_exp.sh \
/data1/data/jhc/datasets/cuc3 \
/data1/data/jhc/output/curve_output/cuc3 \
2

## 8. 10月2号数据集

./run_exp.sh \
/data1/data/jhc/datasets/102-1 \
/data1/data/jhc/projects/gaussian-splatting/output/102-1 \
0

./run_exp.sh \
/data1/data/jhc/datasets/102-2 \
/data1/data/jhc/projects/gaussian-splatting/output/102-2 \
1

## 9. 10月3号数据集

./run_exp.sh \
/data1/data/jhc/datasets/103-1 \
/data1/data/jhc/projects/gaussian-splatting/output/103-1 \
0

./run_exp.sh \
/data1/data/jhc/datasets/103-2 \
/data1/data/jhc/projects/gaussian-splatting/output/103-2 \
1

## 10. mipnerf360数据集大规模测试


./run_exp.sh \
/data1/data/jhc/datasets/mipnerf360/bonsai \
/data1/data/jhc/projects/gaussian-splatting/output/bonsai \
2

  SSIM :    0.9476455                                                                               
  PSNR :   32.4628716
  LPIPS:    0.1795119

----------------------------

./run_exp.sh \
/data1/data/jhc/datasets/mipnerf360/stump \
/data1/data/jhc/projects/gaussian-splatting/output/stump \
2

  SSIM :    0.7669106
  PSNR :   26.6454926
  LPIPS:    0.2434780
  
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python full_metrics.py \
--renders_dir /data1/data/jhc/projects/gaussian-splatting/output/stump/test/ours_30000/renders \
--gt_dir /data1/data/jhc/projects/gaussian-splatting/output/stump/test/ours_30000/gt \
--show_metrics

----------------------------

./run_exp.sh \
/data1/data/jhc/datasets/mipnerf360/room \
/data1/data/jhc/projects/gaussian-splatting/output/room \
1

  SSIM :    0.9276738
  PSNR :   31.7914257
  LPIPS:    0.1958769

./run_exp.sh \
/data1/data/jhc/datasets/mipnerf360/kitchen \
/data1/data/jhc/projects/gaussian-splatting/output/kitchen \
2

  SSIM :    0.9325972
  PSNR :   31.6367474
  LPIPS:    0.1158317


./run_exp.sh \
/data1/data/jhc/datasets/mipnerf360/bicycle \
/data1/data/jhc/projects/gaussian-splatting/output/bicycle \
1
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python full_metrics.py \
--renders_dir /data1/data/jhc/projects/gaussian-splatting/output/bicycle/test/ours_30000/renders \
--gt_dir /data1/data/jhc/projects/gaussian-splatting/output/bicycle/test/ours_30000/gt \
--show_metrics

./run_exp.sh \
/data1/data/jhc/datasets/mipnerf360/counter \
/data1/data/jhc/projects/gaussian-splatting/output/counter \
1

./run_exp.sh \
/data1/data/jhc/datasets/mipnerf360/garden \
/data1/data/jhc/projects/gaussian-splatting/output/garden \
1
CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python full_metrics.py \
--renders_dir /data1/data/jhc/projects/gaussian-splatting/output/garden/test/ours_30000/renders \
--gt_dir /data1/data/jhc/projects/gaussian-splatting/output/garden/test/ours_30000/gt \
--show_metrics


## 11. TnT

./run_exp.sh \
/data1/data/jhc/datasets/TnT/M60 \
/data1/data/jhc/projects/gaussian-splatting/output/M60 \
1

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python full_metrics.py \
--renders_dir /data1/data/jhc/projects/gaussian-splatting/output/Train/test/ours_30000/renders \
--gt_dir /data1/data/jhc/projects/gaussian-splatting/output/Train/test/ours_30000/gt \
--show_metrics

./run_exp.sh \
/data1/data/jhc/datasets/TnT/Train \
/data1/data/jhc/projects/gaussian-splatting/output/Train \
2

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python full_metrics.py \
--renders_dir /data1/data/jhc/projects/gaussian-splatting/output/M60/test/ours_30000/renders \
--gt_dir /data1/data/jhc/projects/gaussian-splatting/output/M60/test/ours_30000/gt \
--show_metrics

## 12. 106

./run_exp.sh \
/data1/data/jhc/datasets/106 \
/data1/data/jhc/projects/gaussian-splatting/output/106 \
1

## 13. 107

./run_exp.sh \
/data1/data/jhc/datasets/107-1 \
/data1/data/jhc/projects/gaussian-splatting/output/107-1 \
1

./run_exp.sh \
/data1/data/jhc/datasets/107-2 \
/data1/data/jhc/projects/gaussian-splatting/output/107-2 \
0

./run_exp.sh \
/data1/data/jhc/datasets/107-3 \
/data1/data/jhc/projects/gaussian-splatting/output/107-3 \
2

## 14. 106-2

./run_exp.sh \
/data1/data/jhc/datasets/106-2 \
/data1/data/jhc/projects/gaussian-splatting/output/106-2 \
2

## 15. TnT中的卡车

./run_exp.sh \
/data1/data/jhc/datasets/TnT/Truck \
/data1/data/jhc/projects/gaussian-splatting/output/Truck \
2

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=1 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python full_metrics.py \
--renders_dir /data1/data/jhc/projects/gaussian-splatting/output/Truck/test/ours_30000/renders \
--gt_dir /data1/data/jhc/projects/gaussian-splatting/output/Truck/test/ours_30000/gt \
--show_metrics

## 16. V109

./run_exp.sh \
/data1/data/jhc/datasets/formal3_white \
/data1/data/jhc/projects/gaussian-splatting/output/V109 \
1

  SSIM :    0.9541044
  PSNR :   32.1090508
  LPIPS:    0.0714128

## 17. 1010数据集

1010-1排球网
./run_exp.sh \
/data1/data/jhc/datasets/1010-1 \
/data1/data/jhc/projects/gaussian-splatting/output/1010-1 \
1
  SSIM :    0.7439128                                                                               
  PSNR :   20.3705215                                                                               
  LPIPS:    0.2953990

./run_exp.sh \
/data1/data/jhc/datasets/1010-2 \
/data1/data/jhc/projects/gaussian-splatting/output/1010-2 \
2
  SSIM :    0.5698621
  PSNR :   17.2433777
  LPIPS:    0.3616252

./run_exp.sh \
/data1/data/jhc/datasets/1010-3 \
/data1/data/jhc/projects/gaussian-splatting/output/1010-3 \
1
  SSIM :    0.5193532
  PSNR :   18.0786610
  LPIPS:    0.3831007

## 18. 1011数据集

./run_exp.sh \
/data1/data/jhc/datasets/1011-1 \
/data1/data/jhc/projects/gaussian-splatting/output/1011-1 \
1
  SSIM :    0.4671374
  PSNR :   15.4333019
  LPIPS:    0.4456077


./run_exp.sh \
/data1/data/jhc/datasets/1011-2 \
/data1/data/jhc/projects/gaussian-splatting/output/1011-2 \
0
  SSIM :    0.5095098
  PSNR :   20.0685024
  LPIPS:    0.4674730

## 19. 1012数据集

./run_exp.sh \
/data1/data/jhc/datasets/1012-1 \
/data1/data/jhc/projects/gaussian-splatting/output/1012-1 \
0
  SSIM :    0.8260823
  PSNR :   22.4153175
  LPIPS:    0.2452799


./run_exp.sh \
/data1/data/jhc/datasets/1012-2 \
/data1/data/jhc/projects/gaussian-splatting/output/1012-2 \
0
  SSIM :    0.8122016
  PSNR :   22.1968346
  LPIPS:    0.2479148


./run_exp.sh \
/data1/data/jhc/datasets/1012-3 \
/data1/data/jhc/projects/gaussian-splatting/output/1012-3 \
0
  SSIM :    0.7990289
  PSNR :   22.0679607
  LPIPS:    0.2854997

## 20. tennis 

./run_exp.sh \
/data1/data/jhc/datasets/blender1 \
/data1/data/jhc/projects/gaussian-splatting/output/blender1 \
0
  SSIM :    0.8042303
  PSNR :   24.0941963
  LPIPS:    0.2792440

./run_exp.sh \
/data1/data/jhc/datasets/blender2 \
/data1/data/jhc/projects/gaussian-splatting/output/blender2 \
1
  SSIM :    0.8071084
  PSNR :   24.4168015
  LPIPS:    0.2692851

./run_exp.sh \
/data1/data/jhc/datasets/blender3 \
/data1/data/jhc/projects/gaussian-splatting/output/blender3 \
1
  SSIM :    0.8599075
  PSNR :   26.6004353
  LPIPS:    0.2496433
  
  
  
  
  
  
  
  
  
  
  



