
# 在167服务器上配置环境

## 先挂梯子

ssh -NfR 7897:localhost:7897 buaajhc@10.132.26.167

ssh buaajhc@10.132.26.167

git config --global http.proxy http://127.0.0.1:7897
git config --global https.proxy http://127.0.0.1:7897

export http_proxy=http://127.0.0.1:7897
export https_proxy=http://127.0.0.1:7897
export HTTP_PROXY=http://127.0.0.1:7897
export HTTPS_PROXY=http://127.0.0.1:7897

上面只对 Git 的 HTTP/HTTPS 传输生效，不会代理 SSH 的 22 端口。所以 curl 能通，不代表 SSH clone 能通。

你需要

vim ~/.ssh/config

然后写入：

Host github.com
    HostName ssh.github.com
    User git
    Port 443
    ProxyCommand nc -X connect -x 127.0.0.1:7897 %h %p
      
然后测试：
ssh -T git@github.com

## 配conda环境

/opt/conda/bin/conda create --prefix "/data1/conda_env/$USER/curveGS" python=3.10 -y

source /opt/conda/etc/profile.d/conda.sh

export CONDA_ENVS_PATH="/data1/conda_env/$USER"

conda activate curveGS

## 安装 CUDA，torch等等

export CUDA_HOME=/usr/local/cuda-12.8
export PATH="$CUDA_HOME/bin:$PATH"
export LD_LIBRARY_PATH="$CUDA_HOME/lib64:${LD_LIBRARY_PATH:-}"

which nvcc
nvcc --version

(下面命令可以通过：
which python
python -m pip --version
查看下载到哪里)
python -m pip install --no-cache-dir \
filelock typing-extensions sympy networkx jinja2 fsspec numpy pillow mpmath MarkupSafe \
nvidia-cuda-nvrtc==13.0.88 nvidia-cuda-runtime==13.0.96 nvidia-cuda-cupti==13.0.85 \
nvidia-cudnn-cu13==9.15.1.9 nvidia-cublas==13.1.0.3 nvidia-cufft==12.0.0.61 \
nvidia-curand==10.4.0.35 nvidia-cusolver==12.0.4.66 nvidia-cusparse==12.6.3.3 \
nvidia-cusparselt-cu13==0.8.0 nvidia-nccl-cu13==2.28.9 nvidia-nvshmem-cu13==3.4.5 \
nvidia-nvtx==13.0.85 nvidia-nvjitlink==13.0.88 nvidia-cufile==1.15.1.6 \
cuda-bindings==13.0.3 cuda-pathfinder==1.5.6 triton==3.6.0 \
-i https://pypi.tuna.tsinghua.edu.cn/simple

python -m pip install torch torchvision torchaudio --index-url https://mirrors.nju.edu.cn/pytorch/whl/cu128

验证
python -c "import torch, torchvision, numpy; print('torch', torch.__version__);print('torchvision', torchvision.__version__); print('numpy', numpy.__version__); print('cuda', torch.cuda.is_available())"

## 高斯泼溅训练的包

同环境中安装：
python -m pip install ./submodules/diff-gaussian-rasterization --no-build-isolation
python -m pip install ./submodules/diff-plane-rasterization --no-build-isolation

## 重登服务器可能出现未export的情况

source /opt/conda/etc/profile.d/conda.sh
conda deactivate
conda activate /data1/conda_env/buaajhc/curveGS

# 165服务器

## 跑baseline

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/net1 \
-m /data2/jhc/output/3dgs_output/921/net1_gs \
--eval \
--disable_viewer

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/net2 \
-m /data2/jhc/output/3dgs_output/921/net2_gs \
--eval \
--disable_viewer

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/net3 \
-m /data2/jhc/output/3dgs_output/921/net3_gs \
--eval \
--disable_viewer

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=6 python train.py \
-s /data1/jhc/datasets/net4 \
-m /data2/jhc/output/3dgs_output/921/net4_gs \
--eval \
--disable_viewer

cd ../gs_pro6000
conda activate curveGS

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/net1 \
-m /data2/jhc/output/3dgs_output/921/net1_gs \
--iteration 30000 \
--skip_train
[test] PSNR: 17.3923  SSIM: 0.5211  LPIPS: 0.3793 [22/09 09:45:15]

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/net2 \
-m /data2/jhc/output/3dgs_output/921/net2_gs \
--iteration 30000 \
--skip_train
[test] PSNR: 17.8613  SSIM: 0.5644  LPIPS: 0.3908 [22/09 09:45:52]

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/net3 \
-m /data2/jhc/output/3dgs_output/921/net3_gs \
--iteration 30000 \
--skip_train
[test] PSNR: 18.2511  SSIM: 0.7757  LPIPS: 0.2815 [22/09 09:46:20]

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES=6 \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s /data1/jhc/datasets/net4 \
-m /data2/jhc/output/3dgs_output/921/net4_gs \
--iteration 30000 \
--skip_train
[test] PSNR: 14.9327  SSIM: 0.3514  LPIPS: 0.4804 [22/09 09:47:30]

## 跑自己代码

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/net1 \
-m /data2/jhc/output/curve_output/net1 \
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

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/net2 \
-m /data2/jhc/output/curve_output/net2 \
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

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=5 python train.py \
-s /data1/jhc/datasets/net3 \
-m /data2/jhc/output/curve_output/net3 \
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

**这里开始用167服务器的**

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python train.py \
-s /data1/data/jhc/datasets/net4 \
-m /data1/data/jhc/output/curve_output/net4 \
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

-----------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python train.py \
-s /data1/data/jhc/datasets/net1 \
-m /data1/data/jhc/output/3dgs_output/net1 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net1/curve_3dgs_init.ply \
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
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net1 \
-m /data1/data/jhc/output/3dgs_output/net1 \
--iteration 30000 \
--skip_train

[test] PSNR: 17.3369  SSIM: 0.4919  LPIPS: 0.4010 [22/09 13:13:04]

-----------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python train.py \
-s /data1/data/jhc/datasets/net2 \
-m /data1/data/jhc/output/3dgs_output/net2 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net2/curve_3dgs_init.ply \
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
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net2 \
-m /data1/data/jhc/output/3dgs_output/net2 \
--iteration 30000 \
--skip_train

[test] PSNR: 17.2134  SSIM: 0.5327  LPIPS: 0.4146 [22/09 14:17:45]

-----------------------------------

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 python train.py \
-s /data1/data/jhc/datasets/net3 \
-m /data1/data/jhc/output/3dgs_output/net3 \
--eval \
--disable_viewer \
--curvegs /data1/data/jhc/output/curve_output/net3/curve_3dgs_init.ply \
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
CUDA_VISIBLE_DEVICES=0 \
TORCH_HOME=/data1/data/jhc/torch_cache \
python render_metrics.py \
-s /data1/data/jhc/datasets/net3 \
-m /data1/data/jhc/output/3dgs_output/net3 \
--iteration 30000 \
--skip_train

[test] PSNR: 17.9404  SSIM: 0.7556  LPIPS: 0.3084 [22/09 13:14:51]

## 调调参数再试试

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=4 python train.py \
-s /data1/jhc/datasets/net1 \
-m /data2/jhc/output/curve_output/net1 \
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

上面和下面等价：

python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/net1 \
-m output/test/net1 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 10 \
--fill_y_threshold 0.5 \
--fill_grid_resX 200 \
--fill_grid_resY 100 \
--fill_grid_resZ 50 \
--trajectory_root

但是 --outlier_nb_points 30，--outlier_nb_neighbors 30，--outlier_std_ratio 2.0 默认参数 其实还是需要调节的
outlier_nb_points：半径离群点过滤的最小邻居数。
outlier_nb_neighbors：统计离群点过滤使用的邻居数，默认 30。
outlier_std_ratio：统计离群点过滤的标准差倍数，默认 2.0。

python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/net1 \
-m output/test/net1 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 10 \
--fill_y_threshold 0.5 \
--fill_grid_resX 200 \
--fill_grid_resY 100 \
--fill_grid_resZ 50 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 10

python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/net2 \
-m output/test/net2 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 10 \
--fill_y_threshold 0.5 \
--fill_grid_resX 200 \
--fill_grid_resY 100 \
--fill_grid_resZ 50 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 10

python test_colmap_reader.py \
-s /home/gamma/rosbags/COLMAP/net4 \
-m output/test/net4 \
--eval \
--init_voxel_size 0.01 \
--method 3 \
--fill_x_threshold 10 \
--fill_y_threshold 0.5 \
--fill_grid_resX 200 \
--fill_grid_resY 100 \
--fill_grid_resZ 50 \
--trajectory_root \
--init_voxel_size 0.01 \
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 10

**测试完毕**

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python train.py \
-s /data1/data/jhc/datasets/net1 \
-m /data1/data/jhc/output/curve_output/net1v2 \
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
--outlier_nb_points 5 \
--outlier_nb_neighbors 30 \
--outlier_std_ratio 0.05 \
--camera_point_distance 10 \
--SGCR \
--final_opacity_cull 0.5






























