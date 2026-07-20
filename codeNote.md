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

