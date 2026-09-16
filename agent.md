# CurveGS RGB Edge Supervision -> 3dgs_note Migration Guide

本文档记录 Curve-Gaussian 中已经完成的 RGB 边缘监督改动，并为后续修改 `/home/gamma/storage_of_code/gs_seldom/3dgs_note` 提供实施顺序、接口约定和验证标准。

目标不是把 CurveGS 的自定义 rasterizer 搬到 3dgs_note，而是让标准 3DGS 训练使用同一套数据语义：

1. 训练第 1 阶段：只有 COLMAP 高斯，训练 20000 次；RGB loss 只使用图像的非边缘区域，避免 COLMAP 高斯解释边缘结构。
2. 训练第 2 阶段：从第 20000 次 checkpoint 恢复，注入 CurveGS 导出的 `curve_3dgs_init_RGB.ply`，再训练 10000 次。
3. 第 2 阶段中，CurveGS 高斯负责边缘区域的初始化结构和颜色，COLMAP 高斯继续负责非边缘区域。
4. 最终总迭代数为 30000，但阶段切换发生在 checkpoint 恢复和模型参数注入时，而不是简单地在第 20000 次后继续使用原模型。

---

## 一、Curve-Gaussian 中已经完成的实现

### 1. 命令行开关

文件：`arguments/__init__.py`

已增加：

```python
self.use_RGB = False
```

开启方式：

```bash
--use_RGB
```

默认不传该参数时，必须保持原始 CurveGS 行为：白色曲线、原有 edge supervision、原有 `curve_3dgs_init.ply` 输出。

### 2. 输入数据

RGB 模式使用以下目录：

```text
<data_root>/images/
<data_root>/edge_PidiNet/
<data_root>/sparse/
```

含义：

- `images/`：原始 RGB 图像，用于颜色监督。
- `edge_PidiNet/`：边缘图，加载后通过 `convert("L")` 得到 `[1,H,W]` 的灰度 mask。
- `sparse/`：COLMAP 相机、位姿和初始点云。

不要把 `edge_PidiNet` 当作 RGB 真值。它只表示哪些像素属于边缘区域，以及每个像素的边缘置信度。

CurveGS 中的相机数据流：

```text
scene/dataset_readers.py
    -> CameraInfo.rgb_image_path
    -> CameraInfo.edge_image_path

utils/camera_utils.py
    -> original_rgb: [3,H,W]
    -> edge_mask:    [1,H,W]

scene/cameras.py
    -> camera.original_rgb
    -> camera.edge_mask
```

### 3. CurveGS 直接 RGB

文件：`scene/gaussian_curve_model.py`

训练颜色参数：

```python
self._logit_rgb
```

形状：

```text
[num_curves, n_gaussians, 3]
```

实际 RGB：

```python
@property
def get_rgb(self):
    return torch.sigmoid(self._logit_rgb).flatten(0, 1)
```

形状：

```text
[num_curves * n_gaussians, 3]
```

训练阶段不使用 SH。CurveGS renderer 直接把 `[N,3]` 的 RGB 传给自定义 `diff-cur-rasterization`。旧的 `_features_dc` 和 `_features_rest` 仅保留兼容性。

### 4. CurveGS RGB loss 语义

文件：`train.py` 的 `Loss_part()`

RGB 模式下：

```python
geometry_loss = torch.abs(rend_alpha - edge_mask).mean()

rgb_mask = edge_mask.expand_as(image)
rgb_error = torch.abs(image - gt_rgb)
rgb_loss = (
    (rgb_error * rgb_mask).sum()
    / rgb_mask.sum().clamp_min(1e-6)
)
```

颜色监督不是先生成并保存一张新的彩色边缘图，而是在 loss 中即时执行：

```text
original RGB image * edge mask
```

RGB warm-up：

```python
rgb_warmup = min(
    1.0,
    iteration / max(opt.rgb_warmup, 1),
)
```

### 5. CurveGS 导出文件

RGB 模式下最终生成：

```text
curve_3dgs_init.ply
curve_3dgs_init_RGB.ply
parametric_edges.json
```

其中：

- `curve_3dgs_init.ply`：保留旧行为，使用中性灰 DC 颜色。
- `curve_3dgs_init_RGB.ply`：使用训练得到的直接 RGB。
- `f_dc_0/1/2`：`RGB2SH(rgb)`，只在导出时转换为标准 3DGS DC SH。
- `f_rest_0..44`：全零。
- `opacity`：写为 inverse sigmoid 后的 logit。
- `scale_0..2`：写为实际尺度取 `log` 后的值。
- `rot_0..3`：归一化四元数，顺序为 `w,x,y,z`。

标准 3DGS 读取后会执行：

```text
rgb = f_dc * C0 + 0.5
```

因此 `curve_3dgs_init_RGB.ply` 可以被 `3dgs_note --curvegs` 读取，且颜色会成为可训练的 `_features_dc`，不会被加载器丢弃。

---

## 二、3dgs_note 需要实现的目标训练流程

目标命令逻辑：

```text
Phase 1: COLMAP only, iterations 1..20000
Phase 2: restore checkpoint at 20000
         inject curve_3dgs_init_RGB.ply
         iterations 20001..30000
```

推荐最终命令形态可以是两次命令：

```bash
# Phase 1
python train.py \
    -s /data1/jhc/datasets/virtual_net2 \
    -m output/virtual_curve_two_stage \
    --eval \
    --disable_viewer \
    --iterations 20000 \
    --save_iterations 20000 \
    --checkpoint_iterations 20000 \
    --edge_non_edge_loss \
    --edge_folder edge_PidiNet

# Phase 2
python train.py \
    -s /data1/jhc/datasets/virtual_net2 \
    -m output/virtual_curve_two_stage \
    --start_checkpoint output/virtual_curve_two_stage/chkpnt20000.pth \
    --curvegs /absolute/path/curve_3dgs_init_RGB.ply \
    --iterations 30000 \
    --eval \
    --disable_viewer \
    --edge_non_edge_loss \
    --edge_folder edge_PidiNet
```

注意：上面是目标接口，不要假设这些参数已经存在。`3dgs_note` 需要先实现它们，或者采用项目已有的等价参数命名。

---

## 三、3dgs_note 的推荐修改顺序

### Step 1：增加 edge_PidiNet 的相机数据流

建议修改：

```text
3dgs_note/scene/dataset_readers.py
3dgs_note/utils/camera_utils.py
3dgs_note/scene/cameras.py
```

要求：

1. 保留现有 `camera.original_image` 语义，避免破坏标准 3DGS 代码。
2. 增加：

```python
camera.original_rgb  # [3,H,W]
camera.edge_mask     # [1,H,W]
```

3. 路径按照当前 CurveGS 的规则构造：

```python
rgb_path = os.path.join(images_folder, image_name)
edge_path = rgb_path.replace("images", "edge_PidiNet")
edge_path = edge_path.replace(".jpg", ".png").replace(".JPG", ".png")
```

4. 使用和原图相同的 resolution 缩放。
5. edge 图必须 `convert("L")`，不要把三通道 edge 图直接当 RGB 目标。
6. 在缺失文件时立即抛出带具体路径的 `FileNotFoundError`。

建议新增模型参数：

```python
self.edge_folder = "edge_PidiNet"
self.use_edge_loss = False
```

不要让默认训练自动依赖 edge_PidiNet；只有显式启用时才读取额外目录。

### Step 2：实现非边缘区域 RGB loss

3dgs_note 的标准渲染输出通常为：

```python
rendered_image  # [3,H,W]
```

定义非边缘权重：

```python
non_edge_mask = (1.0 - camera.edge_mask).clamp(0.0, 1.0)
non_edge_mask = non_edge_mask.expand_as(rendered_image)
```

建议使用归一化的 masked L1：

```python
rgb_error = torch.abs(rendered_image - camera.original_rgb)
non_edge_rgb_loss = (
    (rgb_error * non_edge_mask).sum()
    / non_edge_mask.sum().clamp_min(1e-6)
)
```

如果项目同时使用 DSSIM/SSIM，不要直接把单通道 mask 传入要求 `[3,H,W]` 的实现。应明确选择：

- 先实现 masked L1，验证流程正确后再增加 masked SSIM；或
- 对 mask 做三通道扩展，再确认 SSIM 的 reduction 不会把非边缘区域重新平均进去。

### Step 3：Phase 1 只初始化和训练 COLMAP 高斯

Phase 1 不得加载 `--curvegs`。

训练模型必须只来自标准 COLMAP point cloud：

```python
gaussians.create_from_pcd(scene_info.point_cloud, cameras_extent)
```

Phase 1 的目标：

- 只让 COLMAP 高斯解释非边缘区域的 RGB。
- 非边缘 masked RGB loss 是主要图像监督。
- 不应让后续 curvegs 点提前参与训练。
- 正常的 opacity、scale、rotation、SH 和 densification 行为按 3dgs_note 原有逻辑处理。

建议在训练日志中明确打印：

```text
[Phase 1] COLMAP only
[Phase 1] non-edge mask supervision enabled
```

Phase 1 结束时必须保存：

```text
point_cloud/iteration_20000/point_cloud.ply
chkpnt20000.pth
```

`chkpnt20000.pth` 必须包含：

- 当前高斯参数；
- optimizer state；
- 当前 iteration；
- active SH degree；
- densification 相关状态；
- 当前 phase 标识或已注入 curvegs 标识。

### Step 4：实现 CurveGS PLY 的延迟注入

当前 `3dgs_note` 的 `--curvegs` 行为是在 `Scene.__init__()` 初始化模型时立即把 CurveGS 和 COLMAP 拼接。这不满足“两万次后再注入”的目标。

不要简单地在 Phase 1 也传入 `--curvegs`，否则 CurveGS 点会从第 1 次迭代开始训练。

推荐新增独立方法，例如：

```python
def append_curvegs_from_ply(
    self,
    curvegs_path,
    train_cameras,
    cameras_extent,
    curve_opacity_filter=False,
    curve_xyz_filter=False,
    curve_xyz_limit=None,
):
    """Read curvegs PLY and append its tensors after Phase 1."""
```

实现原则：

1. 复用现有 `_load_curvegs_ply_for_init()`，避免复制 PLY schema 解析逻辑。
2. 只读取 CurveGS 点的：

```text
xyz
features_dc
features_rest
opacity
scaling
rotation
```

3. 将它们 append 到当前 COLMAP 高斯，而不是重新创建 COLMAP 高斯。
4. 同步扩展：

```text
_xyz
_features_dc
_features_rest
_opacity
_scaling
_rotation
max_radii2D
xyz_gradient_accum
denom
```

5. 更新 CurveGS 标记：

```python
curvegs_original_mask
curvegs_generation
```

6. 如果 optimizer 已经存在，必须同时把新参数加入 optimizer，并为新参数初始化 Adam state；不能只修改 Tensor 而忘记 optimizer。
7. 如果 3dgs_note 使用 fused/sparse Adam，必须遵循项目已有的参数替换和 optimizer state 管理方式。
8. 注入后检查所有张量的第 0 维相同。

推荐注入后打印：

```text
[Phase 2] CurveGaussian points appended: N_curve
[Phase 2] COLMAP points retained: N_colmap
[Phase 2] Total points: N_total
```

### Step 5：恢复 checkpoint 后切换到 Phase 2

训练入口需要支持以下逻辑：

```python
if start_checkpoint is None:
    # Phase 1
    create COLMAP-only model
else:
    # load COLMAP-only checkpoint
    restore checkpoint
    assert current_iteration == 20000
    append_curvegs_from_ply(curvegs_path)
```

推荐把“恢复 checkpoint”和“注入 curvegs”分成两个明确步骤：

```python
gaussians.restore(model_params, opt)
gaussians.append_curvegs_from_ply(curvegs_path, ...)
```

不要在 `restore()` 内隐式读取外部 curvegs 文件，因为这样会让 checkpoint 的可复现性和参数来源不清晰。

Phase 2 的 iteration 语义：

- checkpoint 中保存的 iteration 是 `20000`；
- 恢复后训练循环从 `20001` 开始；
- `--iterations 30000` 表示总迭代上限，不是再训练 30000 次。

如果项目现有命令把 `--iterations` 理解为“恢复后再训练 N 次”，必须统一语义并在日志中打印清楚。

### Step 6：Phase 2 的区域监督语义

Phase 2 中建议分区域处理：

```text
非边缘区域：COLMAP 高斯继续提供主要监督
边缘区域：CurveGS 初始化高斯提供结构和颜色
```

最初的实现可以使用一个全局 masked RGB loss：

```python
non_edge_mask = (1.0 - edge_mask).clamp(0.0, 1.0)
edge_mask = edge_mask.clamp(0.0, 1.0)

non_edge_loss = masked_l1(
    rendered_image,
    original_rgb,
    non_edge_mask,
)

edge_loss = masked_l1(
    rendered_image,
    original_rgb,
    edge_mask,
)

loss = lambda_non_edge * non_edge_loss + lambda_edge * edge_loss
```

但必须明确：标准 3DGS 的渲染图是所有高斯的合成结果，普通 RGB loss 本身不能直接区分某个像素是由 COLMAP 高斯还是 CurveGS 高斯产生的。如果需求是“COLMAP 点只接受非边缘监督”，仅使用整张渲染图的 `non_edge_mask` 还不够严格，它只是在像素层屏蔽边缘 loss。

严格实现“COLMAP 高斯不学习边缘”需要至少一种方案：

1. 使用 CurveGS/非 CurveGS 参数分组，并针对 COLMAP 高斯计算单独的渲染或贡献；
2. 在渲染器输出每个点的贡献/分组 alpha，再对 COLMAP 贡献施加 non-edge 约束；
3. 第一阶段只使用非边缘 mask loss，第二阶段冻结或降低 COLMAP 参数在边缘相关 loss 中的梯度；
4. 先使用像素级 masked loss 作为 MVP，并在实验中验证是否足够。

推荐先实现方案 4 验证完整训练链，再根据实验结果增加分组贡献控制。不要在文档或实验结论中把像素 mask loss 宣称为“严格的每个 COLMAP 点只接受非边缘梯度”。

### Step 7：颜色和 SH 约定

CurveGS 导出的 `curve_3dgs_init_RGB.ply`：

```text
f_dc = RGB2SH(trained_rgb)
f_rest = 0
```

3dgs_note 加载后：

- `f_dc` 成为可训练的基础颜色；
- `f_rest` 初始全零；
- 如果 `sh_degree=3`，后续可以学习高阶 SH；
- 如果希望颜色始终是视角无关的基础 RGB，使用 `--sh_degree 0` 或冻结高阶 SH。

建议第一次集成测试使用：

```bash
--sh_degree 3
```

因为这与 PLY 的 45 个 `f_rest_*` 属性一致，且是标准 3DGS 常用配置。

### Step 8：Densification 和 optimizer 注意事项

这是延迟注入最容易出错的部分。

注入 CurveGS 点后必须检查：

```python
assert gaussians.get_xyz.shape[0] == gaussians.get_features.shape[0]
assert gaussians.get_xyz.shape[0] == gaussians.get_opacity.shape[0]
assert gaussians.get_xyz.shape[0] == gaussians.get_scaling.shape[0]
assert gaussians.get_xyz.shape[0] == gaussians.get_rotation.shape[0]
```

如果 3dgs_note 对 CurveGS 点使用 `curvegs_original_mask`，必须保证：

```text
mask 长度 == 注入后的总高斯数
前 N_curve 或后 N_curve 的位置约定始终一致
```

如果点被 prune/densify：

- 同步更新 `curvegs_original_mask`；
- 同步更新 `curvegs_generation`；
- 同步更新 optimizer state；
- 不要假设 CurveGS 点永远位于固定索引，除非项目明确禁止对其 prune。

建议 Phase 2 的第一版先关闭或限制 CurveGS 点的 densification/pruning，确认注入、颜色和训练稳定后，再开放完整结构变化。

---

## 四、建议的参数设计

建议在 `3dgs_note/arguments/__init__.py` 增加：

```python
self.edge_folder = "edge_PidiNet"
self.use_edge_loss = False
self.lambda_non_edge = 1.0
self.lambda_edge = 1.0
self.phase1_iterations = 20000
self.curvegs_inject_iteration = 20000
self.curvegs = ""
```

也可以不增加 `phase1_iterations`，直接使用“两次命令 + checkpoint”的方式，逻辑更清晰。

推荐优先采用两次命令，而不是一次命令内自动切换：

- Phase 1 命令不传 `--curvegs`；
- Phase 2 命令传 `--start_checkpoint` 和 `--curvegs`；
- 这样更容易检查 checkpoint、点数和输出文件。

---

## 五、验证清单

### A. 数据读取

```text
[ ] images/ 和 edge_PidiNet/ 文件名一一对应
[ ] edge mask 被加载为 [1,H,W]
[ ] RGB 被加载为 [3,H,W]
[ ] 分辨率缩放后二者尺寸一致
[ ] 缺失 edge 文件会显示准确路径
```

### B. Phase 1

```text
[ ] 不传 --curvegs 时只初始化 COLMAP 点
[ ] 日志显示 COLMAP-only
[ ] 使用 non-edge mask RGB loss
[ ] 训练到 20000 次
[ ] 生成 chkpnt20000.pth
[ ] 生成 point_cloud/iteration_20000/point_cloud.ply
[ ] checkpoint 中没有任何 CurveGS 点
```

### C. Phase 2 注入

```text
[ ] 从 chkpnt20000.pth 恢复
[ ] 读取 curve_3dgs_init_RGB.ply
[ ] 注入数量等于 PLY vertex 数量
[ ] COLMAP 点数量保持不变
[ ] 总点数 = COLMAP 点数 + CurveGS 点数
[ ] f_dc 颜色没有被覆盖
[ ] opacity/scale/rotation 形状正确
[ ] optimizer 包含新增点参数
[ ] 从 20001 继续，而不是从 1 或 30001 开始
```

### D. Phase 2 训练

```text
[ ] 训练到 30000 次
[ ] 不出现 optimizer state shape 错误
[ ] 不出现 CUDA invalid gradient 错误
[ ] 不出现 NaN/Inf loss
[ ] 训练中 non-edge loss 有效
[ ] 曲线区域颜色与 curve_3dgs_init_RGB.ply 初值一致或合理变化
[ ] 生成 iteration_30000/point_cloud.ply
```

### E. 颜色验证

使用 3dgs_note 加载最终 PLY 后，检查：

```python
rgb = SH2RGB(features_dc)
```

验证：

```text
[ ] CurveGS 点的 rgb 均值与导入 PLY 的 rgb 接近
[ ] f_rest 初始为零
[ ] CurveGS 点没有被当成 COLMAP 点覆盖
[ ] 标准渲染可以正常显示
```

---

## 六、常见错误

### 1. 把 `--curvegs` 同时传给 Phase 1

错误结果：CurveGS 点从第 1 次就加入，无法验证“20000 次后注入”。

正确做法：Phase 1 不传 `--curvegs`。

### 2. 只修改 `_xyz`，没有加入 optimizer

错误结果：曲线点存在但不更新，或者后续 optimizer state 报 shape 错误。

正确做法：所有可训练参数和 optimizer 状态同步扩展。

### 3. 把 `edge_PidiNet` 当成彩色 ground truth

错误结果：RGB 通道语义错误，颜色监督退化为灰度监督。

正确做法：

```text
images -> original_rgb
edge_PidiNet -> edge_mask
```

### 4. 忘记标准 3DGS 的参数化格式

PLY 中必须保持：

```text
opacity = logit(opacity_probability)
scale = log(metric_scale)
rotation = normalized quaternion
f_dc = RGB2SH(rgb)
```

### 5. 训练结束后渲染不存在的 iteration

如果训练在 30000 次保存 PLY，render 时必须指定：

```bash
--iteration 30000
```

并且训练命令必须包含：

```bash
--save_iterations 30000
```

### 6. 磁盘空间或挂载状态异常

训练前检查：

```bash
df -hT .
touch output/test_write.tmp
```

如果出现 `Read-only file system`，先更换可写输出目录或处理服务器存储，不能靠修改 Python loss 绕过。

---

## 七、最终实施原则

1. 先完成 edge_PidiNet 数据读取和 masked RGB loss。
2. 再单独验证 COLMAP-only 的 20000 次训练与 checkpoint。
3. 再实现延迟 CurveGS PLY 注入。
4. 再验证注入后的点数、颜色、optimizer 和一次前向反向。
5. 最后跑完整的 20000 + 10000 两阶段训练。
6. 任何阶段出现问题时，先保留对应输出目录和日志，不要直接覆盖之前的 checkpoint。

最重要的接口边界：

```text
Curve-Gaussian:
    edge_PidiNet + images
    -> edge geometry supervision + masked RGB supervision
    -> curve_3dgs_init_RGB.ply

3dgs_note:
    Phase 1: COLMAP-only + non-edge supervision
    Phase 2: restore checkpoint + append curve_3dgs_init_RGB.ply
              + continue standard 3DGS training
```

## 八、CurveGaussian 分裂后的统计量同步

### 1. 已确认的错误

在 `n_gaussians=3`、训练到约第 4000 次迭代时，如果曲线分裂流程报错：

```text
IndexError: The shape of the mask [850815] at index 0 does not match
 the shape of the indexed tensor [455883, 1]
```

错误调用链通常是：

```text
curve_split_curvature()
-> densify_and_split_curve()
-> densification_postfix()
-> prune_curves()
```

### 2. 根因

`densification_postfix()` 添加了新曲线，却只重置了 `denom` 和 `max_radii2D`，没有同步重置 `xyz_gradient_accum`。因此新增曲线后：

- `prune_curves()` 按最新曲线数量生成了 per-Gaussian mask；
- `xyz_gradient_accum` 仍然保留旧的 Gaussian 数量；
- 用新 mask 索引旧统计量时触发维度不匹配。

所有 per-Gaussian 状态都必须遵循：

```text
num_gaussians = num_curves * n_gaussians
```

### 3. 修复要求

文件：`scene/gaussian_curve_model.py`

在 `densification_postfix()` 完成新曲线拼接后，同时重置以下三个统计量：

```python
self.xyz_gradient_accum = torch.zeros(
    (self.get_curve_points.shape[0] * self.n_gaussians, 1),
    device="cuda",
)
self.denom = torch.zeros(
    (self.get_curve_points.shape[0] * self.n_gaussians, 1),
    device="cuda",
)
self.max_radii2D = torch.zeros(
    (self.get_curve_points.shape[0] * self.n_gaussians),
    device="cuda",
)
```

`prune_curves()` 中的 `valid_points_mask` 也必须按曲线维度展开：

```python
valid_points_mask = valid_curves_mask.unsqueeze(1) \\
    .repeat(1, self.n_gaussians).flatten()
```

### 4. 副本同步与验证

训练命令实际使用哪个源码目录，就必须修改哪个目录。例如命令若从：

```text
/data1/jhc/storage_of_code/Curve-Gaussian-Note/
```

启动，则必须将上述修复同步到该目录的 `scene/gaussian_curve_model.py`；只修改：

```text
/home/gamma/storage_of_code/Curve-Gaussian/
```

不会影响正在运行的副本。

修改后至少执行：

```bash
python -m py_compile scene/gaussian_curve_model.py
```

并在下一次分裂、合并和剪枝前检查：

```python
assert self.xyz_gradient_accum.shape[0] == self.get_xyz.shape[0]
assert self.denom.shape[0] == self.get_xyz.shape[0]
assert self.max_radii2D.shape[0] == self.get_xyz.shape[0]
```

每次拓扑操作后都应保持这些断言成立。
