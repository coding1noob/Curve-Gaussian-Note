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
