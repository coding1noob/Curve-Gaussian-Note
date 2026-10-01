
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

## 

for CAM in front_left_camera front_right_camera left_camera right_camera
do
  CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
  env -u DISPLAY \
  MPLCONFIGDIR=/tmp/cmrnext-mpl \
  /data1/jhc/miniconda3storage/cmrnext/bin/python \
  evaluate_flow_calibration.py \
    --weights \
      weights/cmrnext-calib-LEnc-iter1.tar \
      weights/cmrnext-calib-LEnc-iter5.tar \
      weights/cmrnext-calib-LEnc-iter6.tar \
    --data_folder "$DATA_ROOT" \
    --dataset pandaset \
    --pandaset_sequences "$SEQ" \
    --num_worker 0 \
    --cam "$CAM" \
    --viz_save_dir "$OUTPUT_ROOT/$CAM"
done

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








