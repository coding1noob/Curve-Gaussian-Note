# 曲线思路

输入多视角图像
    -> 预先提取 edge_PidiNet / edge_DexiNed 边缘图
    -> 初始化 3D Bezier 曲线
    -> 沿 Bezier 曲线采样细长高斯椭球
    -> 从当前相机视角渲染成 2D 线条图
    -> 和真实边缘图做 edge-aware loss + SSIM loss
    -> 反向传播优化曲线控制点、高斯位置/宽度/方向/透明度等
    -> 训练后期剪枝、切分、合并，并把足够直的 Bezier 曲线转成线段
    -> 最终导出 3D 参数化边缘：Bezier curves + line segments

# 训练

1. 读 COLMAP 初始点云
   scene/dataset_readers.py
        ↓
2. 每个初始点初始化一条 Bezier 曲线
   scene/gaussian_curve_model.py -> initialize_bezier_curves()
        ↓
3. Bezier 控制点作为可训练参数
   self._curve_points = nn.Parameter(...)
        ↓
4. 沿每条曲线采样 n_gaussians 个高斯中心
   get_curve_gaussians(self.sample_t)
        ↓
5. 根据曲线切线和宽度构造细长高斯椭球
   prepare_scaling_rot()
   得到 _xyz / _rotation / _scaling / _opacity / _mask
        ↓
6. render() 把这些高斯送入 CUDA rasterizer
   gaussian_renderer/__init__.py
        ↓
7. rasterizer 输出 2D 渲染图 image
   render_pkg["render"]
        ↓
8. image 和输入边缘图 gt_image 比较
   edge_aware_loss + SSIM loss
        ↓
9. loss.backward()
   梯度从渲染图传回高斯参数，再传回 Bezier 控制点等可训练参数
        ↓
10. optimizer.step()
   更新 _curve_points / _width / _opacity / _mask 等参数
        ↓
11. prepare_scaling_rot()
   用更新后的曲线重新计算高斯中心、方向、尺度


# 训练后

输出的图像不含高斯椭球渲染，而是通过优化后的曲线直接输出图像

# 细节
7000 iteration 时触发的事情

1. 增密阶段结束，触发一次大规模剪枝

在 train.py：

``` 
if iteration == opt.densify_until_iter:
    prune_mask = (gaussians.get_curve_opacity <= opt.opacity_cull_second).squeeze()
    gaussians.prune_curves(prune_mask)
    torch.cuda.empty_cache()
    gaussians.fix_opacity()
```

这一步把 opacity 太低的曲线全部剪掉，然后 fix_opacity() 把 opacity 冻结，不再让 opacity 参与后续优化，同时把 opacity 的学习率设为 0

2. 曲线端点连接正则项开始生效

在 train.py：

```
if opt.lambda_points_conn > 0 and iteration > opt.conn_from_iter:
    ...
    pair_rows, pair_cols = _find_sparse_curve_endpoint_pairs(curve_points, dis_thr)
    ...
    curve_conn = torch.linalg.vector_norm(...)
    loss = loss + opt.lambda_points_conn * curve_conn
```

conn_from_iter=7000，也就是说 7000 之后每次迭代都要额外计算曲线端点之间的近邻对，并把连接距离加进 loss 里。这个 KD-tree 近邻计算在曲线数量很多时开销不小。

3. 每 1000 步触发结构调整

7000 之后每隔 1000 步触发：

```
if iteration % 1000 == 500 and iteration > opt.densify_until_iter:
    gaussians.only_prune(...)
    gaussians.mask_trim_split(...)

if iteration % 1000 == 0 and iteration > 3000 and iteration != opt.iterations:
    gaussians.curve_split_curvature(...)

if (iteration % 1000 == 0 and iteration > opt.densify_until_iter) or ...:
    gaussians.fit_curve_to_line(...)
    gaussians.merge_curves(...)

```

这些操作包括：

- 曲线按曲率切分
- 把足够直的曲线转成线段
- 曲线合并

这些都是比较重的操作，每次都要重新计算高斯中心和方向（prepare_scaling_rot()），有时候还会改变曲线数量

# 训练打印

进度条里每个数字的含义：

Loss = 1.88010
综合图像损失，由两部分加权求和：

L1 边缘感知损失（edge_aware_loss）：渲染出的线条图和 GT 边缘图的逐像素差
SSIM 结构相似度损失（1 - ssim_value） 数值越小说明渲染结果越接近目标边缘图。
curve_smo = 0.00139
曲线平滑度损失（smoothness）。计算同一条曲线上相邻高斯的切线方向之间的夹角，夹角越大说明曲线越"折"。这个值很小（0.001级别）说明曲线整体已经比较平滑。对应 opt.lambda_curve_smo 权重控制。

curve_conn = 0.03297
端点连接损失（connectivity）。把距离近的不同曲线端点之间的距离加入 loss，鼓励端点"接上"，避免线条断开悬空。iteration > conn_from_iter（即 7000 之后）才开始生效，所以你在 7000 前看不到这个项。

opacity = 0.64392
当前所有曲线的平均 opacity 值。fix_opacity() 在第 7000 步把 opacity 强制拉到 ≥ 0.6 并冻结，所以 7000 步之后这个值基本稳定在 0.6 以上，不再下降。如果接近 1.0 说明大多数曲线都是"实"的；0.64 说明曲线整体偏弱，还有部分曲线被 mask 遮住。

# 输出解耦

<model_path>/
  cfg_args
  cameras.json
  input.ply
  input_filled.ply
  exposure.json
  point_cloud/
    iteration_3000/
      point_cloud.ply
      curve_step3000.ply
      ellipsoids_step3000.ply
    iteration_10000/
      point_cloud.ply
      curve_step10000.ply
      ellipsoids_step10000.ply
  chkpnt10000.pth
  edge_points.ply
  parametric_edges.json
  events.out.tfevents...   # 如果 tensorboard 可用

  # 调参日志

--threshold_angle
当前默认 20，每 1000 iter 会按曲率把曲线切开。网状结构边缘检测有噪声，20 度太容易把一根线切成多段。
看相邻两个高斯方向的夹角，超过就切

--threshold_angle_skip
看隔一个高斯的方向夹角，超过也切

--threshold_line / --threshold_max_line
这两个控制“足够直的曲线转成线段”。转成线段后，后续线段合并更容易。
建议：
--threshold_line 0.003 --threshold_max_line 0.01

--n_gaussians
你现在是 6，对长线条可能偏少。建议试 8 或 12。如果显存够，先试 12

--similarity_threshold 0.92
控制曲线/线段合并时的方向相似度门槛。值越高，要求方向越一致才合并；值越低，更容易合并。

--distance_threshold
当前默认 0.02，控制后期曲线/线段合并距离。太小会导致断开的相邻线段合不回去。

--opacity_cull 0.02
训练后期周期性剪枝用的 opacity 阈值。opacity 低于这个值的曲线更容易被删。

--opacity_cull_second 0.08
在 densify_until_iter 那一刻的强剪枝阈值，默认发生在 7000 iter。低于这个 opacity 的曲线会被删。

--mask_threshold 0.02
控制 mask 剪枝/修剪。mask 低于阈值的曲线采样点会被认为不可靠，后期会被剪掉或切掉。

# 修改添加RGB

1. 
先修改submodules/diff-cur-rasterization/cuda_rasterizer/config.h，里面把光栅器单通道改为三通道

完成后可以用下面的命令确认差异，但不要安装：
git diff -- submodules/diff-cur-rasterization/cuda_rasterizer/config.h

2. 

第二步修改 CurveGS 内部 RGB 缓冲区大小。
打开 submodules/diff-cur-rasterization/cuda_rasterizer/rasterizer_impl.cu

obtain(chunk, geom.rgb, P, 128);
改成：
obtain(chunk, geom.rgb, P * NUM_CHANNELS, 128);

3. 
然后修改 Python renderer，gaussian_renderer/__init__.py 中有关 colors_precomp 的逻辑,
colors_precomp 可以理解为：已经由 Python 计算好的、每个高斯的直接颜色。
它是每个高斯传给光栅化器的颜色输入，形状通常是：[P, 3]. 修改完其变为:
不使用 SH, 每个高斯使用三个通道, 每个高斯 RGB 可以训练

接着修改同一文件的 rasterizer 调用

4. 
修改 train.py, 让 让当前灰度边缘监督适配三通道渲染输出 

完成这一步后，底层三通道兼容链路就基本接通了。下一步我们会重新编译 diff-cur-rasterization，先验证“不传 --use_RGB”时三通道白线能正常完成前向和反向，再开始加入可训练 RGB 参数

5. 
重新编译

python -m pip install \
--force-reinstall \
--no-deps \
--no-build-isolation \
./submodules/diff-cur-rasterization

然后试运行:

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2 CUDA_LAUNCH_BLOCKING=1 python train.py \
-s /data1/jhc/datasets/virtual_net2 \
-m output/virtual_net2_8.12_test \
--eval \
--iterations 2 \
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
--quiet

6. 
arguments/__init__.py 增加传入参数 --use_RGB

然后他在 train.py 中：
lp = ModelParams(parser)
负责注册参数；在 train.py 中：
training(lp.extract(args), ...)
lp.extract(args) 会创建传入 training() 的 dataset 对象。由于 use_RGB 是 ModelParams 的成员，所以后续在训练函数中可以直接读取

7. 
改数据读取层
scene/dataset_readers.py 中的 CameraInfo 类
以及
readColmapSceneInfo 函数 中的 readColmapCameras 函数(也在 scene/dataset_readers.py 里面)

然后检查:
python - <<'PY'
from scene.dataset_readers import readColmapSceneInfo

scene_info = readColmapSceneInfo(
    "/home/gamma/storage_of_code/habitat-sim/camera_output/formal3/colmap",
    "images",
    "",
    False,
    False,
    detector="PidiNet",
)

cam = scene_info.train_cameras[0]
print("RGB:", cam.rgb_image_path)
print("edge:", cam.edge_image_path)
print("same RGB path:", cam.rgb_image_path == cam.image_path)
print("RGB exists:", __import__("os").path.exists(cam.rgb_image_path))
print("edge exists:", __import__("os").path.exists(cam.edge_image_path))
PY

8. 

在 scene/cameras.py 中的 Camera类 构造函数需要加入
original_rgb
edge_mask
即加入Camera类, 才能给之后的训练调用

然后在 utils/camera_utils.py 中 loadCam 函数

**整条调用链:**
train.py
  ↓
ModelParams / 命令行参数
  ↓
training(dataset, ...)
  ↓
Scene(dataset, gaussians)
  ↓
dataset_readers.py
  ↓
CameraInfo
  ↓
camera_utils.py::loadCam()
  ↓
cameras.py::Camera
  ↓
scene.getTrainCameras()
  ↓
viewpoint_cam
  ↓
train.py 读取监督数据

9. 
给 GaussianCurveModel 增加“每个高斯的基础 RGB 参数”

scene/gaussian_curve_model.py
中 GaussianCurveModel 类里面添加
开启参数 self.use_RGB 用于传递参数, self._logit_rgb (形状是[N, M, 3], 含义是
N：曲线数量
M：每条曲线的采样高斯数量
3：RGB 三个通道)

同时模仿
@property
def get_xyz(self)
创建获取rgb属性的函数

然后在 create_from_pcd 函数中

上面的改动都会通过
gaussians = GaussianCurveModel(dataset.sh_degree, dataset.n_gaussians, opt.optimizer_type, use_RGB=dataset.use_RGB)
和train.py连接

10. 
把 _logit_rgb 加入 GaussianCurveModel.training_setup() 的优化器参数组

scene/gaussian_curve_model.py 中 training_setup 函数
加入
l = [
        {'params': [self._features_dc], 'lr': training_args.feature_lr, "name": "f_dc"},
    ]
这样的参数表, 用 l.append 添加

添加时需要添加其对应的学习率 training_args.rgb_lr, 所以需要初始化学习率变量

arguments/__init__.py 中 OptimizationParams 类,
在其中加入：
self.rgb_lr = 0.01

11. 
改 train.py, 增加 loss 权重

先在 arguments/__init__.py 增加权重

然后再在 train.py 中修改 (此处新增了 Loss_part 函数)

12. 
让曲线分裂时同步复制 RGB 参数

修改 scene/gaussian_curve_model.py 里面的 densify_and_split_curve 函数
(此函数和 train.py 的调用链:
train.py 中的 densify_and_prune -> densify_and_split_curve )

完成后，曲线分裂产生的新曲线就会继承原曲线的 RGB

13. 
让曲线合并时同步生成 RGB 参数

修改 scene/gaussian_curve_model.py merge_curves 函数


补充说明 densification_postfix 函数的作用

以曲线分裂为例：
densify_and_prune()
    找出哪些曲线需要分裂
        ↓
densify_and_split_curve()
    用 De Casteljau 算法计算左右两条新曲线
    准备新曲线的 opacity、width、mask、RGB 等参数
        ↓
densification_postfix()
    把新曲线和新参数正式加入模型及 optimizer
        ↓
prune_curves()
    删除原来的父曲线

合并时也是类似的：
merge_curves()
    找出需要合并的曲线
    拟合出合并后的新曲线
        ↓
prune_curves()
    删除参与合并的旧曲线
        ↓
densification_postfix()
    把合并后的新曲线正式加入模型
