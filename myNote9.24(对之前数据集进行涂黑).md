
# 修复环境

执行：

conda activate curveGS

cd /data1/jhc/storage_of_code/gs_pro6000/submodules/diff-gaussian-rasterization

which python
python -c "import sys, torch; print(sys.executable); print(torch.__version__);
print(torch.version.cuda)"
which nvcc
nvcc --version

  确认 python 是类似：

  /data1/jhc/miniconda3storage/curveGS/bin/python

  然后删除该扩展在源码目录中的旧构建产物：

rm -rf build
rm -f diff_gaussian_rasterization/_C*.so

  重新编译并安装：

python -m pip install -v --no-build-isolation -e .

  也可以只在源码目录中生成 .so：

  python setup.py build_ext --inplace

  推荐第一种 pip install -e .，因为它会使用当前环境的 PyTorch 编译配置。

  编译完成后验证：

cd /data1/jhc/storage_of_code/gs_pro6000

python - <<'PY'
import sys
import torch
import diff_gaussian_rasterization
from diff_gaussian_rasterization import _C

print("Python:", sys.executable)
print("PyTorch:", torch.__version__)
print("Torch CUDA:", torch.version.cuda)
print("Extension:", _C.__file__)
print("CUDA available:", torch.cuda.is_available())
PY

  Extension: 应该指向当前仓库，例如：

  /data1/jhc/storage_of_code/gs_pro6000/submodules/diff-gaussian-rasterization/
  diff_gaussian_rasterization/_C....so

  之后重新运行训练命令：

  CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 \
  /data1/jhc/miniconda3storage/curveGS/bin/python train.py ...

  如果编译时报 CUDA_HOME is not set，先设置 CUDA 路径，例如：

  export CUDA_HOME=/usr/local/cuda
  export PATH="$CUDA_HOME/bin:$PATH"
  export LD_LIBRARY_PATH="$CUDA_HOME/lib64:${LD_LIBRARY_PATH}"

  然后重新执行编译命令。

  注意：你当前目录下的扩展文件是：

  submodules/diff-gaussian-rasterization/diff_gaussian_rasterization/_C*.so

  重编译时应删除并重新生成这个文件，而不是只执行 pip install 却继续使用旧的 .so。另外，
  torch.version.cuda、nvcc --version 和实际驱动版本应兼容；如果当前环境中的 PyTorch 是 cuXXX，最好使
  用匹配的 CUDA toolkit 编译。

# 跑测试

python test_colmap_reader.py \
-s /home/gamma/storage_of_code/habitat-sim/camera_output/formal3_noSH/colmap \
-m output/test/formal3_noSH_delete \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 10 \
--fill_y_threshold 0.5 \
--fill_grid_resX 200 \
--fill_grid_resY 100 \
--fill_grid_resZ 50 \
--trajectory_root \
--init_voxel_size 0.01

先测试补点是否一样。上面这个补点数和 virtual_net2_noLight_SGCR_finalPrune_consistencyLoss(9.18组会前，无光，纹理地板，最终版) 一致

# 正式跑

1. 无光照复杂地面数据集 (仿照myNote9.18的 “5. 对真实光照的地面复杂纹理，进行不带SGCR的测试” )
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight_delete \
-m /data2/jhc/output/curve_output/virtual_net2_noLight_delete_SGCR \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 10 \
--fill_y_threshold 0.5 \
--fill_grid_resX 200 \
--fill_grid_resY 100 \
--fill_grid_resZ 50 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--SGCR

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight_delete \
-m /data2/jhc/output/3dgs_output/924/virtual_net2_noLight_delete \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_noLight_delete_SGCR/curve_3dgs_init.ply \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight_delete \
-m /data2/jhc/output/3dgs_output/924/virtual_net2_noLight_delete \
--iteration 30000 \
--skip_train

[test] PSNR: 28.5138  SSIM: 0.9408  LPIPS: 0.0742 [24/09 23:05:21]

二次实验

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/virtual_net2_noLight_delete \
-m /data2/jhc/output/3dgs_output/924/virtual_net2_noLight_delete2 \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_noLight_delete_SGCR/curve_3dgs_init.ply \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_noLight_delete \
-m /data2/jhc/output/3dgs_output/924/virtual_net2_noLight_delete2 \
--iteration 30000 \
--skip_train

[test] PSNR: 28.6052  SSIM: 0.9400  LPIPS: 0.0743 [25/09 10:41:50]

2. 有光照复杂地面数据集(对照 myNote9.18.md 中的 “8. 对真实光照的地面复杂纹理，带SGCR”)

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/virtual_net2_delete \
-m /data2/jhc/output/curve_output/virtual_net2_delete_SGCR \
--eval \
--iterations 30000 \
--fill_method simplefill3 \
--trajectory_root \
--fill_x_threshold 10 \
--fill_y_threshold 0.5 \
--fill_grid_resX 200 \
--fill_grid_resY 100 \
--fill_grid_resZ 50 \
--n_gaussians 3 \
--simple \
--lambda_points_conn 0 \
--init_voxel_size 0.01 \
--SGCR \
--final_opacity_cull 0.5

cd ../gs_pro6000

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2_delete \
-m /data2/jhc/output/3dgs_output/924/virtual_net2_delete \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_delete_SGCR/curve_3dgs_init.ply \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=2 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_delete \
-m /data2/jhc/output/3dgs_output/924/virtual_net2_delete \
--iteration 30000 \
--skip_train

[test] PSNR: 32.8799  SSIM: 0.9608  LPIPS: 0.0776 [25/09 11:36:11]

--------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/virtual_net2_delete \
-m /data2/jhc/output/3dgs_output/924/virtual_net2_delete2 \
--eval \
--disable_viewer \
--curvegs /data2/jhc/output/curve_output/virtual_net2_delete_SGCR/curve_3dgs_init.ply \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 19999 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 19999 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=5 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2_delete \
-m /data2/jhc/output/3dgs_output/924/virtual_net2_delete2 \
--iteration 30000 \
--skip_train

[test] PSNR: 33.0215  SSIM: 0.9616  LPIPS: 0.0760 [25/09 11:49:57]








































