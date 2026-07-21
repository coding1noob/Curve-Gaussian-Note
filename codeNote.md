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