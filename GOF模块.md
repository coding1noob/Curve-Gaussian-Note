
# 先尝试GOF方法提取平面

165服务器

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3  \
PYTHONPATH=.:submodules/diff-gaussian-rasterization:submodules/simple-knn \
python extract_mesh_gof.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_1 \
--iteration 30000 \
--data_device cpu \
--resolution 32 \
--max_gaussians 300 \
--max_points 4000 \
--tetra_backend scipy \
--binary_steps 2 \
--max_views 4 \
--output /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_1/test.ply
  
--data_device cpu
将相机图像等数据放在 CPU 内存中

--resolution 32
设置加载相机图像时的目标宽度约为 32 像素，并保持原始宽高比

--max_gaussians 300
最多使用 300 个 Gaussian，当前脚本不是随机选取，而是按照 opacity 从高到低选择

--max_points 4000
限制四面体采样点数量。
当前每个 Gaussian 通常生成：
- 8 个 oriented box corner；
- 1 个 Gaussian center；
合计约 9 个点。

--tetra_backend scipy
指定使用 SciPy 的 Delaunay 算法生成四面体

--max_views 4
最多保留前 4 个训练相机

进一步改参数
unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4  \
PYTHONPATH=.:submodules/diff-gaussian-rasterization:submodules/simple-knn \
python extract_mesh_gof.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_1 \
--iteration 30000 \
--data_device cpu \
--resolution 32 \
--max_gaussians 30000 \
--max_points 270000 \
--tetra_backend scipy \
--binary_steps 2 \
--max_views 200 \
--output /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_1/test.ply

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4  \
PYTHONPATH=.:submodules/diff-gaussian-rasterization:submodules/simple-knn \
python extract_mesh_gof.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_1 \
--iteration 30000 \
--data_device cpu \
--resolution 32 \
--max_gaussians 300000 \
--max_points 2700000 \
--tetra_backend scipy \
--binary_steps 2 \
--max_views 200 \
--output /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_1/test2.ply

# 效果不好，再用PGSR的方式来进行平面提取

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 \
PYTHONPATH=.:submodules/diff-gaussian-rasterization:submodules/simple-knn \
python extract_mesh_pgsr.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_1 \
--iteration 30000 \
--data_device cpu \
--resolution 2 \
--voxel_size 0.01 \
--sdf_trunc_scale 4 \
--max_depth 10 \
--alpha_threshold 0.1 \
--num_cluster 1 \
--use_depth_filter \
--mode joint \
--output /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_1/mesh_pgsr_joint.ply

效果比gof的好，但是网面全都没有表面提取出来

CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 \
PYTHONPATH=.:submodules/diff-gaussian-rasterization:submodules/simple-knn \
python extract_mesh_pgsr.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_1 \
--iteration 30000 \
--data_device cpu \
--resolution 1 \
--voxel_size 0.01 \
--sdf_trunc_scale 4 \
--max_depth 20 \
--alpha_threshold 0.03 \
--depth_normal_threshold -1 \
--num_cluster 0 \
--mode joint \
--output /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_1/mesh_pgsr_unfiltered.ply

--resolution 1：使用完整图像分辨率；
--alpha_threshold 0.03：保留 alpha 较低的墙面区域；
--max_depth 20：避免墙面因为深度超过 10 被裁掉；
--depth_normal_threshold -1：关闭四邻域深度跳变过滤；
不使用 --use_depth_filter；
--num_cluster 0：不删除小连通组件。


167服务器上进行测试：

1. 
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
PYTHONPATH=. \
/data1/conda_env/buaajhc/curveGS/bin/python extract_mesh_pgsr.py \
-s /data1/data/jhc/datasets/formal3_white \
-m /data1/data/jhc/output/3dgs_output/V109 \
--iteration 30000 \
--data_device cpu \
--resolution 1 \
--voxel_size 0.01 \
--sdf_trunc_scale 4 \
--max_depth 20 \
--alpha_threshold 0.03 \
--depth_normal_threshold -1 \
--num_cluster 0 \
--mode joint \
--output /data1/data/jhc/output/3dgs_output/V109/mesh_pgsr_unfiltered.ply


开始debug:
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
PYTHONPATH=. \
/data1/conda_env/buaajhc/curveGS/bin/python extract_mesh_pgsr.py \
  -s /data1/data/jhc/datasets/formal3_white \
  -m /data1/data/jhc/output/3dgs_output/V109 \
  --iteration 30000 \
  --data_device cpu \
  --resolution 1 \
  --voxel_size 0.01 \
  --sdf_trunc_scale 4 \
  --max_depth 20 \
  --alpha_threshold 0.03 \
  --depth_normal_threshold -1 \
  --num_cluster 0 \
  --max_views 1 \
  --mode joint \
  --output /tmp/pgsr_diagnostic.ply
输出：
valid_depth_pixels=8294400
depth_range=[2.95982, 14.3301]
depth_mean=10.1081
encoded_nonzero=8294400
vertices=0 triangles=0
PGSR 渲染和 TSDF 流程都成功执行了，但 TSDF 最终没有提取出三角面

增加了 --depth_pcd_output，可以把第一视角深度直接导出为点云：
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
PYTHONPATH=. \
/data1/conda_env/buaajhc/curveGS/bin/python \
extract_mesh_pgsr.py \
  -s /data1/data/jhc/datasets/formal3_white \
  -m /data1/data/jhc/output/3dgs_output/V109 \
  --iteration 30000 \
  --data_device cpu \
  --resolution 1 \
  --voxel_size 0.02 \
  --sdf_trunc_scale 8 \
  --max_depth 20 \
  --alpha_threshold 0.03 \
  --depth_normal_threshold -1 \
  --num_cluster 0 \
  --max_views 1 \
  --mode joint \
  --depth_pcd_output /tmp/pgsr_depth_first.ply \
  --raw_output /tmp/pgsr_raw.ply \
  --output /tmp/pgsr_diagnostic.ply

然后看结果：
/data1/conda_env/buaajhc/curveGS/bin/python - <<'PY'
import open3d as o3d
import numpy as np

pcd = o3d.io.read_point_cloud("/tmp/pgsr_depth_first.ply")
p = np.asarray(pcd.points)

print("points:", len(p))
if len(p):
    print("finite:", np.isfinite(p).all())
    print("min:", p.min(axis=0))
    print("max:", p.max(axis=0))
    print("mean:", p.mean(axis=0))
PY

全视角试试：
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
PYTHONPATH=. \
/data1/conda_env/buaajhc/curveGS/bin/python extract_mesh_pgsr.py \
  -s /data1/data/jhc/datasets/formal3_white \
  -m /data1/data/jhc/output/3dgs_output/V109 \
  --iteration 30000 \
  --data_device cpu \
  --resolution 2 \
  --voxel_size 0.01 \
  --sdf_trunc_scale 4 \
  --max_depth 20 \
  --alpha_threshold 0.1 \
  --depth_normal_threshold -1 \
  --num_cluster 0 \
  --max_views 0 \
  --use_depth_filter \
  --pose_mode pgsr \
  --mode joint \
  --raw_output /tmp/v109_raw_res2.ply \
  --output /tmp/v109_res2.ply

2. 
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
PYTHONPATH=. \
/data1/conda_env/buaajhc/curveGS/bin/python extract_mesh_pgsr.py \
-s /data1/data/jhc/datasets/net6 \
-m /data1/data/jhc/output/3dgs_output/net6v2_PGSR \
--iteration 30000 \
--data_device cpu \
--resolution 1 \

(/data1/conda_env/buaajhc/curveGS) buaajhc@user:/data1/data/jhc/projects/3dgs_note$ CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 \
PYTHONPATH=. \
/data1/conda_env/buaajhc/curveGS/bin/python extract_mesh_pgsr.py \
  -s /data1/data/jhc/datasets/net930-0 \
  -m /data1/data/jhc/output/3dgs_output/net930-0 \
  --iteration 30000 \
  --data_device cpu \
  --resolution 2 \
  --voxel_size 0.01 \
  --sdf_trunc_scale 8 \
  --max_depth 50 \
  --alpha_threshold 0.1 \
  --depth_normal_threshold -1 \
  --num_cluster 0 \
  --max_views 0 \
  --use_depth_filter \
  --mode joint \
  --raw_output /tmp/net930_raw_depth50.ply \
  --output /tmp/net930_depth50.ply
Looking for config file in /data1/data/jhc/output/3dgs_output/net930-0/cfg_args
Config file found: /data1/data/jhc/output/3dgs_output/net930-0/cfg_args
Loading trained model at iteration 30000 [21/10 21:06:22]
------------LLFF HOLD------------- [21/10 21:06:24]
Reading camera 363/363 [21/10 21:06:24]
Loading Training Cameras [21/10 21:06:24]
Loading Test Cameras [21/10 21:10:59]
PGSR render + TSDF (joint): 100%|████████████████████████████████| 317/317 [00:52<00:00,  6.00it/s]
[Open3D WARNING] Write PLY failed: mesh has 0 vertices. [21/10 21:12:40]
[Open3D WARNING] Write PLY failed: mesh has 0 vertices. [21/10 21:12:40]
[PGSR] views=317 valid_depth_pixels=77622606 depth_range=[0.480718, 48.9665] depth_mean=3.45718 encoded_nonzero=77622606 vertices=0 triangles=0 output=/tmp/net930_depth50.ply [21/10 21:12:40]
--voxel_size 0.01 \
--sdf_trunc_scale 4 \
--max_depth 20 \
--alpha_threshold 0.03 \
--depth_normal_threshold -1 \
--num_cluster 0 \
--mode joint \
--output /data1/data/jhc/output/3dgs_output/net6v2_PGSR/mesh_pgsr_unfiltered.ply
也不成功


CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 \
PYTHONPATH=. \
/data1/conda_env/buaajhc/curveGS/bin/python extract_mesh_pgsr.py \
-s /data1/data/jhc/datasets/net930-0 \
-m /data1/data/jhc/output/3dgs_output/net930-0 \
--iteration 30000 \
--data_device cpu \
--resolution 1 \
--voxel_size 0.01 \
--sdf_trunc_scale 4 \
--max_depth 20 \
--alpha_threshold 0.03 \
--depth_normal_threshold -1 \
--num_cluster 0 \
--mode joint \
--output /data1/data/jhc/output/3dgs_output/net930-0/mesh_pgsr_unfiltered.ply
也不成功

# Oct23晚

先把新增脚本同步到两台服务器，在各自当前环境运行：
python diagnose_open3d_tsdf.py --cpu_threads 2
预期165通过；如果167也出现：
RGBD depth=[3, 3]
float-depth scale=1000 probe z=0.003
vertices=0 triangles=0 FAIL
就与本地复现一致。

试试在165低负载起步命令跑一跑167的结果

OMP_NUM_THREADS=4 OMP_THREAD_LIMIT=4 OMP_DYNAMIC=FALSE \
MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 NUMEXPR_NUM_THREADS=4 \
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=3 \
PYTHONPATH=. \
/usr/bin/time -v /data1/jhc/miniconda3storage/curveGS/bin/python extract_mesh_pgsr.py \
-s /data2/jhc/datasets/net930-0 \
-m /data2/jhc/output/3dgs_output/930-0 \
--iteration 30000 \
--data_device cpu \
--resolution 4 \
--voxel_size 0.05 \
--sdf_trunc_scale 4 \
--max_depth 20 \
--alpha_threshold 0.03 \
--depth_normal_threshold -1 \
--num_cluster 0 \
--max_views 4 \
--mode joint \
--output /data2/jhc/output/3dgs_output/930-0/mesh_pgsr_diag_res4_v4.ply

感觉可以放多相机了

OMP_NUM_THREADS=4 OMP_THREAD_LIMIT=4 OMP_DYNAMIC=FALSE \
MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 NUMEXPR_NUM_THREADS=4 \
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 \
PYTHONPATH=. \
/usr/bin/time -v /data1/jhc/miniconda3storage/curveGS/bin/python extract_mesh_pgsr.py \
-s /data2/jhc/datasets/net930-0 \
-m /data2/jhc/output/3dgs_output/930-0 \
--iteration 30000 \
--data_device cpu \
--resolution 4 \
--voxel_size 0.01 \
--sdf_trunc_scale 4 \
--max_depth 20 \
--alpha_threshold 0.03 \
--depth_normal_threshold -1 \
--num_cluster 0 \
--mode joint \
--output /data2/jhc/output/3dgs_output/930-0/mesh_pgsr2.ply

167 重新配置环境

conda create -p /data1/conda_env/buaajhc/curveGS_o3d019 \
  --clone /data1/conda_env/buaajhc/curveGS

conda activate /data1/conda_env/buaajhc/curveGS_o3d019

python -m pip install --no-deps "open3d==0.19.0" -i https://pypi.tuna.tsinghua.edu.cn/simple/

python -m pip install "PyYAML>=5.4.1" \
  -i https://pypi.tuna.tsinghua.edu.cn/simple/
  
python -m pip install addict pyquaternion \
  -i https://pypi.tuna.tsinghua.edu.cn/simple/

python -c 'import open3d; print(open3d.__version__, open3d.__file__)'

python diagnose_open3d_tsdf.py --cpu_threads 2

成功之后试试：

OMP_NUM_THREADS=4 OMP_THREAD_LIMIT=4 OMP_DYNAMIC=FALSE \
MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 NUMEXPR_NUM_THREADS=4 \
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
PYTHONPATH=. \
python extract_mesh_pgsr.py \
-s /data1/data/jhc/datasets/net930-0 \
-m /data1/data/jhc/output/3dgs_output/net930-0 \
--iteration 30000 \
--data_device cpu \
--resolution 4 \
--voxel_size 0.05 \
--sdf_trunc_scale 4 \
--max_depth 20 \
--alpha_threshold 0.03 \
--depth_normal_threshold -1 \
--num_cluster 0 \
--max_views 4 \
--mode joint \
--output /data1/data/jhc/output/3dgs_output/net930-0/mesh_pgsr_diag_res4_v4.ply

[PGSR] views=4 valid_depth_pixels=2181471 depth_range=[0.812915, 19.9999] depth_mean=6.34166 encoded_nonzero=2181471 vertices=191733 triangles=149665 output=/data1/data/jhc/output/3dgs_output/net930-0/mesh_pgsr_diag_res4_v4.ply [24/10 01:03:53]
成功了！说明真是open3d版本的问题，需要 open3d==0.19.0 才行

试试全图片：
OMP_NUM_THREADS=4 OMP_THREAD_LIMIT=4 OMP_DYNAMIC=FALSE \
MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 NUMEXPR_NUM_THREADS=4 \
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
PYTHONPATH=. \
python extract_mesh_pgsr.py \
-s /data1/data/jhc/datasets/net930-0 \
-m /data1/data/jhc/output/3dgs_output/net930-0 \
--iteration 30000 \
--data_device cpu \
--resolution 4 \
--voxel_size 0.05 \
--sdf_trunc_scale 4 \
--max_depth 20 \
--alpha_threshold 0.03 \
--depth_normal_threshold -1 \
--num_cluster 0 \
--mode joint \
--output /data1/data/jhc/output/3dgs_output/net930-0/mesh_pgsr_diag_res4.ply
[PGSR] views=317 valid_depth_pixels=168266596 depth_range=[0.480694, 20] depth_mean=6.35794 encoded_nonzero=168266596 vertices=1747812 triangles=1745612 output=/data1/data/jhc/output/3dgs_output/net930-0/mesh_pgsr_diag_res4.curveGS_o3d019ply [24/10 01:09:56]

有提取平面，但是网上的没法提取：

当前精度偏粗。 resolution=4 把原图降到了920×614；voxel_size=0.05 是用于低负载验证的设置。细线在图像中可能只剩很少像素，在体素中也可能无法被充分表达。
新增了一个值得优先测试的参数
Open3D默认使用 depth_sampling_stride=4 来采样深度、激活体素块。我已在 extract_mesh_pgsr.py:309 开放：
--depth_sampling_stride 1

OMP_NUM_THREADS=4 OMP_THREAD_LIMIT=4 OMP_DYNAMIC=FALSE \
MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 NUMEXPR_NUM_THREADS=4 \
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
PYTHONPATH=. \
python extract_mesh_pgsr.py \
-s /data1/data/jhc/datasets/net930-0 \
-m /data1/data/jhc/output/3dgs_output/net930-0 \
--iteration 30000 \
--data_device cpu \
--resolution 2 \
--voxel_size 0.01 \
--sdf_trunc_scale 4 \
--depth_sampling_stride 1 \
--max_depth 20 \
--alpha_threshold 0.03 \
--depth_normal_threshold -1 \
--num_cluster 0 \
--mode joint \
--output /data1/data/jhc/output/3dgs_output/net930-0/mesh_pgsr_diag_res2.ply
卡死了

OMP_NUM_THREADS=4 OMP_THREAD_LIMIT=4 OMP_DYNAMIC=FALSE \
MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 NUMEXPR_NUM_THREADS=4 \
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
PYTHONPATH=. \
python extract_mesh_pgsr.py \
-s /data1/data/jhc/datasets/net930-0 \
-m /data1/data/jhc/output/3dgs_output/net930-0 \
--iteration 30000 \
--data_device cpu \
--resolution 4 \
--voxel_size 0.01 \
--sdf_trunc_scale 4 \
--depth_sampling_stride 1 \
--max_depth 20 \
--alpha_threshold 0.03 \
--depth_normal_threshold -1 \
--num_cluster 0 \
--mode joint \
--output /data1/data/jhc/output/3dgs_output/net930-0/mesh_pgsr_diag_res4_2.ply
卡死了

OMP_NUM_THREADS=4 OMP_THREAD_LIMIT=4 OMP_DYNAMIC=FALSE \
MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 NUMEXPR_NUM_THREADS=4 \
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 \
PYTHONPATH=. \
python extract_mesh_pgsr.py \
-s /data1/data/jhc/datasets/net930-0 \
-m /data1/data/jhc/output/3dgs_output/net930-0 \
--iteration 30000 \
--data_device cpu \
--resolution 4 \
--voxel_size 0.05 \
--sdf_trunc_scale 4 \
--depth_sampling_stride 1 \
--max_depth 20 \
--alpha_threshold 0.03 \
--depth_normal_threshold -1 \
--num_cluster 0 \
--mode joint \
--output /data1/data/jhc/output/3dgs_output/net930-0/mesh_pgsr_diag_res4_2.ply
[PGSR] voxel_size=0.05 sdf_trunc=0.2 depth_sampling_stride=1 [24/10 20:09:20]
PGSR render + TSDF (joint): 100%|████████████████████████████████| 317/317 [00:38<00:00,  8.33it/s]
[PGSR] views=317 valid_depth_pixels=168266596 depth_range=[0.480694, 20] depth_mean=6.35794 encoded_nonzero=168266596 vertices=1755194 triangles=1752750 output=/data1/data/jhc/output/3dgs_output/net930-0/mesh_pgsr_diag_res4_2.ply [24/10 20:10:02]
还是没网

先定位丢在哪一步：

OMP_NUM_THREADS=4 OMP_THREAD_LIMIT=4 OMP_DYNAMIC=FALSE \
MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 NUMEXPR_NUM_THREADS=4 \
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 PYTHONPATH=. \
/data1/conda_env/buaajhc/curveGS_o3d019/bin/python extract_mesh_pgsr.py \
-s /data1/data/jhc/datasets/net930-0 \
-m /data1/data/jhc/output/3dgs_output/net930-0 \
--iteration 30000 --data_device cpu --resolution 2 \
--max_depth 20 --alpha_threshold 0.03 --depth_normal_threshold -1 \
--mode joint --max_views 4 --diagnostic_views 4 --diagnostic_only \
--diagnostic_dir /data1/data/jhc/output/3dgs_output/net930-0/diag_joint_r2_n4 \
--memory_log_interval 1

网线的深度好像都渲染出来了，继续排查

MODE=joint
OMP_NUM_THREADS=4 OMP_THREAD_LIMIT=4 OMP_DYNAMIC=FALSE \
MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 NUMEXPR_NUM_THREADS=4 \
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 PYTHONPATH=. \
/data1/conda_env/buaajhc/curveGS_o3d019/bin/python extract_mesh_pgsr.py \
  -s /data1/data/jhc/datasets/net930-0 \
  -m /data1/data/jhc/output/3dgs_output/net930-0 \
  --iteration 30000 --data_device cpu --resolution 2 \
  --view_names DSC_5421.JPG DSC_5422.JPG DSC_5423.JPG DSC_5424.JPG \
  --max_views 4 --diagnostic_views 4 --diagnostic_only \
  --max_depth 20 --alpha_threshold 0.03 --depth_normal_threshold -1 \
  --mode "$MODE" --memory_log_interval 1 \
  --diagnostic_dir "/data1/data/jhc/output/3dgs_output/net930-0/diag_${MODE}_adjacent_r2"

MODE=curve_only
OMP_NUM_THREADS=4 OMP_THREAD_LIMIT=4 OMP_DYNAMIC=FALSE \
MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 NUMEXPR_NUM_THREADS=4 \
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 PYTHONPATH=. \
/data1/conda_env/buaajhc/curveGS_o3d019/bin/python extract_mesh_pgsr.py \
  -s /data1/data/jhc/datasets/net930-0 \
  -m /data1/data/jhc/output/3dgs_output/net930-0 \
  --iteration 30000 --data_device cpu --resolution 2 \
  --view_names DSC_5421.JPG DSC_5422.JPG DSC_5423.JPG DSC_5424.JPG \
  --max_views 4 --diagnostic_views 4 --diagnostic_only \
  --max_depth 20 --alpha_threshold 0.03 --depth_normal_threshold -1 \
  --mode "$MODE" --memory_log_interval 1 \
  --diagnostic_dir "/data1/data/jhc/output/3dgs_output/net930-0/diag_${MODE}_adjacent_r2"


python extract_mesh_pgsr.py \
  -s /data1/data/jhc/datasets/net930-0 \
  -m /data1/data/jhc/output/3dgs_output/net930-0 \
  --iteration 30000 --data_device cpu --resolution 2 \
  --view_names DSC_5421.JPG DSC_5422.JPG DSC_5423.JPG DSC_5424.JPG \
  --max_views 4 --mode curve_only \
  --voxel_size 0.05 --sdf_trunc_scale 4 \
  --depth_sampling_stride 1 \
  --max_depth 20 --alpha_threshold 0.03 \
  --depth_normal_threshold -1 --num_cluster 0 \
  --memory_log_interval 1 \
  --output /data1/data/jhc/output/3dgs_output/net930-0/mesh_curve_adjacent4_v005.ply



OMP_NUM_THREADS=4 OMP_THREAD_LIMIT=4 OMP_DYNAMIC=FALSE \
MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 NUMEXPR_NUM_THREADS=4 \
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 PYTHONPATH=. \
/data1/conda_env/buaajhc/curveGS_o3d019/bin/python extract_mesh_pgsr.py \
  -s /data1/data/jhc/datasets/net930-0 \
  -m /data1/data/jhc/output/3dgs_output/net930-0 \
  --iteration 30000 --data_device cpu --resolution 2 \
  --view_names DSC_5421.JPG DSC_5422.JPG DSC_5423.JPG DSC_5424.JPG \
  --max_views 4 --mode joint_curve \
  --voxel_size 0.05 --sdf_trunc_scale 4 \
  --depth_sampling_stride 1 \
  --max_depth 20 --alpha_threshold 0.03 \
  --depth_normal_threshold -1 --num_cluster 0 \
  --memory_log_interval 1 \
  --output /data1/data/jhc/output/3dgs_output/net930-0/mesh_hybrid_adjacent4_v005.ply
  
**最终**
930-0
OMP_NUM_THREADS=4 OMP_THREAD_LIMIT=4 OMP_DYNAMIC=FALSE \
MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 NUMEXPR_NUM_THREADS=4 \
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 PYTHONPATH=. \
/data1/conda_env/buaajhc/curveGS_o3d019/bin/python extract_mesh_pgsr.py \
-s /data1/data/jhc/datasets/net930-0 \
-m /data1/data/jhc/output/3dgs_output/net930-0 \
--iteration 30000 --data_device cpu --resolution 2 \
--mode joint_curve \
--voxel_size 0.05 --sdf_trunc_scale 4 \
--depth_sampling_stride 1 \
--max_depth 20 --alpha_threshold 0.03 \
--depth_normal_threshold -1 --num_cluster 0 \
--memory_log_interval 1 \
--max_views 0 \
--output /data1/data/jhc/output/3dgs_output/net930-0/mesh_hybrid_alltrain_r2_v005.ply

165上，buaa_net
OMP_NUM_THREADS=4 OMP_THREAD_LIMIT=4 OMP_DYNAMIC=FALSE \
MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 NUMEXPR_NUM_THREADS=4 \
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 PYTHONPATH=. \
python extract_mesh_pgsr.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_1 \
--iteration 30000 --data_device cpu --resolution 2 \
--mode joint_curve \
--voxel_size 0.05 \
--sdf_trunc_scale 4 \
--depth_sampling_stride 1 \
--max_depth 20 \
--alpha_threshold 0.03 \
--depth_normal_threshold -1 \
--num_cluster 0 \
--memory_log_interval 1 \
--output /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_1/buaa_net_mesh.ply
也非常好

总结：
初始命令只使用 joint，把普通高斯和 CurveGS 高斯放进同一个深度和 TSDF。现在使用 joint_curve，把两类高斯分别提取，再合并 mesh，从而避免 joint 分支的背景深度把 CurveGS 网片冲掉。

1. 原始代码中：
num_cluster=1
会调用 _post_process_mesh()，只保留最大的连通组件。线网通常是细碎、断裂、多个小组件，很容易被这个步骤删掉。
当前 joint_curve 中：
- scene 分支可以使用 --num_cluster。
- curve 分支强制保留所有组件。
- 最终合并结果也不再执行最大连通域筛选。

2. 新增 depth_sampling_stride
初始代码创建 TSDF 时没有传这个参数，因此使用 Open3D 默认采样步长，当前等效为4。
现在代码在 extract_mesh_pgsr.py:390-395 中传入：
depth_sampling_stride=int(depth_sampling_stride)
当前使用：
--depth_sampling_stride 1
它的作用是：
- 4：用较稀疏的深度采样激活 TSDF block。
- 1：用每个深度像素参与 block 激活。
细线只占少量像素时，stride=4 可能导致对应体素块没有被激活；stride=1 更容易让线网区域进入 TSDF。

3. 相机加载和内存管理被改进
现在 Scene 支持：
- train_camera_limit
- train_camera_names
- load_test_cameras=False
提取 mesh 时只加载训练相机，不再同时加载测试相机，避免不必要的内存消耗。

4. --mode joint_curve
这是最关键的模式变化。
joint_curve = joint + curve_only 独立提取后合并
其中 curve_only 只使用 CurveGS 高斯：
selected = gaussians.curvegs_original_mask.bool()
初始命令使用的是：
--mode joint
joint 模式下，线网高斯和墙面、植被、地面等普通高斯共同参与 plane depth 计算，线材的深度可能被其他高斯影响。当前模式单独提取 CurveGS，使线网深度更加集中。

再仔细调一调参数试试：

调大--alpha_threshold 从0.03到0.2，发现杂点没有变少
OMP_NUM_THREADS=4 OMP_THREAD_LIMIT=4 OMP_DYNAMIC=FALSE \
MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 NUMEXPR_NUM_THREADS=4 \
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 PYTHONPATH=. \
python extract_mesh_pgsr.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_1 \
--iteration 30000 --data_device cpu --resolution 2 \
--mode joint_curve \
--voxel_size 0.05 \
--sdf_trunc_scale 4 \
--depth_sampling_stride 1 \
--max_depth 20 \
--alpha_threshold 0.2 \
--depth_normal_threshold -1 \
--num_cluster 0 \
--memory_log_interval 1 \
--output /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_1/mesh1/mesh.ply

再调小--voxel_size，确实细节变好，但是网也断了，而且meshlab很卡，mesh_scene.ply很卡，有1.4G
OMP_NUM_THREADS=4 OMP_THREAD_LIMIT=4 OMP_DYNAMIC=FALSE \
MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 NUMEXPR_NUM_THREADS=4 \
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 PYTHONPATH=. \
python extract_mesh_pgsr.py \
-s /data1/jhc/datasets/buaa_net \
-m /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_1 \
--iteration 30000 --data_device cpu --resolution 2 \
--mode joint_curve \
--voxel_size 0.01 \
--sdf_trunc_scale 4 \
--depth_sampling_stride 1 \
--max_depth 20 \
--alpha_threshold 0.2 \
--depth_normal_threshold -1 \
--num_cluster 0 \
--memory_log_interval 1 \
--output /data2/jhc/output/3dgs_output/918_sh3/buaaNet_curvePGSR_withNormal_1/mesh2/mesh.ply










