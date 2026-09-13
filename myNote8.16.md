
# 融合 边缘图 和 RGB图

--image-folder 为输入RGB，--edge-folder 为输入黑白边缘图
--output-folder 为彩色边缘输出， --rgba-folder 为

python /home/gamma/storage_of_code/temp/test5.py \
--image-folder /path/to/images \
--edge-folder /path/to/edge_PidiNet \
--output-folder /path/to/edge_color \
--rgba-folder /path/to/edge_color_rgba


python /home/gamma/storage_of_code/temp/test5.py \
--image-folder /home/gamma/storage_of_code/habitat-sim/camera_output/formal3/colmap/images \
--edge-folder /home/gamma/storage_of_code/habitat-sim/camera_output/formal3/colmap/edge_PidiNet


# 测试
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 CUDA_LAUNCH_BLOCKING=1 python -u train.py -s \
/data1/jhc/datasets/virtual_net2 \
-m output/virtual_net2_8.12_test2 \
--eval \
--iterations 201 \
--checkpoint_iterations 200 \
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
--use_RGB

接着训练:
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 CUDA_LAUNCH_BLOCKING=1 python -u train.py -s \
/data1/jhc/datasets/virtual_net2 \
-m output/virtual_net2_8.12_test2 \
--eval \
--iterations 300 \
--start_checkpoint output/virtual_net2_8.12_test2/chkpnt200.pth \
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
--use_RGB

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 CUDA_LAUNCH_BLOCKING=1 python -u train.py -s \
/data1/jhc/datasets/virtual_net2 \
-m output/virtual_net2_8.12_test2 \
--eval \
--iterations 1000 \
--start_checkpoint output/virtual_net2_8.12_test2/chkpnt200.pth \
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
--use_RGB

# 删除冗余数据集

images/
edge_PidiNet/
curvegs_edge_mask/
baseline_non_edge_mask/
sparse/

# 正式测试

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python -u train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_net2_8.12_RGB1 \
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
--outlier_nb_points 30 \
--init_voxel_size 0.01 \
--use_RGB

可视化色彩方法:
python - <<'PY'
import numpy as np
from plyfile import PlyData, PlyElement

src = "output/virtual_net2_8.12_RGB1/curve_3dgs_init_RGB.ply"
dst = "output/virtual_net2_8.12_RGB1/curve_rgb_meshlab_preview.ply"

C0 = 0.28209479177387814
vertex = PlyData.read(src)["vertex"].data

xyz = np.stack([
    vertex["x"],
    vertex["y"],
    vertex["z"],
], axis=1).astype(np.float32)

f_dc = np.stack([
    vertex["f_dc_0"],
    vertex["f_dc_1"],
    vertex["f_dc_2"],
], axis=1)

rgb = np.clip(f_dc * C0 + 0.5, 0.0, 1.0)
rgb8 = np.round(rgb * 255.0).astype(np.uint8)

dtype = [
    ("x", "f4"),
    ("y", "f4"),
    ("z", "f4"),
    ("red", "u1"),
    ("green", "u1"),
    ("blue", "u1"),
]

preview = np.empty(xyz.shape[0], dtype=dtype)
preview["x"] = xyz[:, 0]
preview["y"] = xyz[:, 1]
preview["z"] = xyz[:, 2]
preview["red"] = rgb8[:, 0]
preview["green"] = rgb8[:, 1]
preview["blue"] = rgb8[:, 2]

PlyData(
    [PlyElement.describe(preview, "vertex")],
    text=False,
).write(dst)

print("Saved:", dst)
print("Points:", len(preview))
print("RGB min:", rgb8.min(axis=0))
print("RGB max:", rgb8.max(axis=0))
PY


# 正式进行有色彩的线条先验，高斯训练

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_curve_RGB_repeat1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12_RGB1/curve_3dgs_init_RGB.ply

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_curve_RGB_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual_curve_RGB_repeat1

# 然后进行带分割的进行训练

--edge_non_edge_loss需要和--curvegs_inject_iteration同步添加，用来“控制注入前的 COLMAP-only 阶段避开线条区域”

## 仿真环境

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_curve_ccmask_repeat1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12_RGB1/curve_3dgs_init_RGB.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_curve_ccmask_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/virtual_curve_ccmask_repeat1

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_curve_ccmask_repeat1 \
--iteration 20000 \
--skip_train

## 现实场景

### curveGS
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net_simple-3_RGB \
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
--outlier_nb_points 30 \
--init_voxel_size 0.01 \
--use_RGB

### gs训练

1. 试试新改进

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_ccmask2_repeat1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3_RGB/curve_3dgs_init_RGB.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_ccmask2_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/buaa_net8.12_ccmask2_repeat1

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_ccmask2_repeat1 \
--iteration 20000 \
--skip_train

-----------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_ccmask2_repeat2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3_RGB/curve_3dgs_init_RGB.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_ccmask2_repeat2 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/buaa_net8.12_ccmask2_repeat2

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_ccmask2_repeat2 \
--iteration 20000 \
--skip_train

-----------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_ccmask2_repeat3 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3_RGB/curve_3dgs_init_RGB.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_ccmask2_repeat3 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/buaa_net8.12_ccmask2_repeat3

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_ccmask2_repeat3 \
--iteration 20000 \
--skip_train

2. 只用RGB重试老算法，并比较20000结果

CurveGaussian init points :  141081 [19/08 13:07:33]
COLMAP init points        :  78958 [19/08 13:07:33]
Total points at init      :  220039 [19/08 13:07:33]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_RGBcurve_repeat1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3_RGB/curve_3dgs_init_RGB.ply \
--save_iterations 20000

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_RGBcurve_repeat1 \
--iteration 20000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_RGBcurve_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/buaa_net8.12_RGBcurve_repeat1

------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_RGBcurve_repeat2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3_RGB/curve_3dgs_init_RGB.ply \
--save_iterations 20000

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_RGBcurve_repeat2 \
--iteration 20000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_RGBcurve_repeat2 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/buaa_net8.12_RGBcurve_repeat2

------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_RGBcurve_repeat3 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3_RGB/curve_3dgs_init_RGB.ply \
--save_iterations 20000

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_RGBcurve_repeat3 \
--iteration 20000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_RGBcurve_repeat3 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/buaa_net8.12_RGBcurve_repeat3

3. 不用RGB试一试？

CurveGaussian init points :  52518 [19/08 15:46:35]
COLMAP init points        :  78958 [19/08 15:46:35]
Total points at init      :  131476 [19/08 15:46:35]

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_ccmask2_noRGB_repeat1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_ccmask2_noRGB_repeat1 \
--iteration 20000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_ccmask2_noRGB_repeat1 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/buaa_net8.12_ccmask2_noRGB_repeat1

---

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_ccmask2_noRGB_repeat2 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_ccmask2_noRGB_repeat2 \
--iteration 20000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_ccmask2_noRGB_repeat2 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/buaa_net8.12_ccmask2_noRGB_repeat2

---

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_ccmask2_noRGB_repeat3 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--save_iterations 20000

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_ccmask2_noRGB_repeat3 \
--iteration 20000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 TORCH_HOME=/data1/jhc/torch_cache python render_metrics.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_ccmask2_noRGB_repeat3 \
--iteration 30000 \
--skip_train

TORCH_HOME=/data1/jhc/torch_cache python metrics.py -m output/buaa_net8.12_ccmask2_noRGB_repeat3

4. 增添打印 .csv

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 python train.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_ccmask2_noRGB_repeat1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/buaa_net_simple-3/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--iterations 20000

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_ccmask2_noRGB_repeat1 \
--iteration 20000 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_ccmask2_noRGB_repeat1 \
--iteration 20000 \
--skip_train \
--colmap_only \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_2.py \
-s /data1/jhc/datasets/buaa_net \
-m output/buaa_net8.12_ccmask2_noRGB_repeat1 \
--iteration 20000 \
--skip_train \
--curve_only \
--edge_folder /data1/jhc/datasets/buaa_net/edge_PidiNet

然后就会输出：
test/ours_20000/joint/renders
test/ours_20000/colmap_only/renders
test/ours_20000/curve_only/renders

5. 

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_ccmask2_noRGB_repeat1 \
--eval \
--disable_viewer \
--curvegs /data1/jhc/storage_of_code/Curve-Gaussian-Note/output/virtual_net2_8.12/curve_3dgs_init.ply \
--curvegs_inject_iteration 20000 \
--edge_non_edge_loss \
--iterations 20000

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_2.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_ccmask2_noRGB_repeat1 \
--iteration 20001 \
--skip_train

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_2.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_ccmask2_noRGB_repeat1 \
--iteration 20001 \
--skip_train \
--colmap_only \
--edge_folder /data1/jhc/datasets/virtual_net2/edge_PidiNet

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python render_2.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual8.12_ccmask2_noRGB_repeat1 \
--iteration 20001 \
--skip_train \
--curve_only \
--edge_folder /data1/jhc/datasets/virtual_net2/edge_PidiNet







