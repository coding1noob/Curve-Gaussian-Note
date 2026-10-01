# COLMAP 点云 GUI

## 当前实现

项目新增了 [add_points_gui.py](add_points_gui.py)，用于读取 COLMAP 点云并通过 Open3D 可视化。当前版本是只读查看器，尚未实现鼠标或键盘手动增点。

脚本直接读取：

```text
<source_path>/sparse/0/points3D.bin
```

如果 `points3D.bin` 不存在，则回退读取：

```text
<source_path>/sparse/0/points3D.txt
```

当前使用底层 `scene.colmap_loader` 读取点云，不调用训练侧的 `readColmapSceneInfo`。因此不会依赖 `images`、边缘图或深度图，也不会因为 GUI 启动而强制在源数据目录生成 `points3D.ply`。

## 启动方式

在 `curveGS` 环境中启动：

```bash
conda run --no-capture-output -n curveGS \
python add_points_gui.py \
-s /path/to/colmap_dataset
```

例如：

```bash
python add_points_gui.py \
-s /data1/data/jhc/datasets/net927_1 \
--display_voxel_size 0.01 \
--point_size 2
```

无图形界面或只想验证 COLMAP 点云读取时：

```bash
python add_points_gui.py \
-s /path/to/colmap_dataset \
--no-gui
```

查看完整参数：

```bash
python add_points_gui.py --help
```

## 命令行参数

### 与 `test_colmap_reader.py` 对齐的参数

- `-s`, `--source_path`：必需参数，COLMAP 数据集根目录，应包含 `sparse/0`。
- `--images`：保留该参数以兼容测试脚本，当前点云查看器不会读取图像。
- `--depths`：保留该参数以兼容测试脚本，当前不会读取深度图。
- `--eval`：保留该参数以兼容测试脚本，当前不使用相机划分。
- `--train_test_exp`：保留该参数以兼容测试脚本，当前不参与点云查看。
- `--detector`：接受 `PidiNet` 或 `DexiNed`，当前不会读取边缘图。
- `--llffhold`：保留该参数以兼容测试脚本，当前不使用相机划分。
- `--init_voxel_size`：对加载到内存中的点云状态执行体素降采样，`0` 表示关闭。

### GUI 和输出参数

- `--display_voxel_size`：只对显示副本执行体素降采样，不改变内存中的点云状态；`0` 表示关闭。
- `--point_size`：Open3D 显示的点大小，默认 `2.0`。
- `--window_width`：窗口宽度，默认 `1280`。
- `--window_height`：窗口高度，默认 `800`。
- `--background R G B`：背景颜色，三个分量范围为 `[0, 1]`，默认是 `0.05 0.05 0.05`。
- `--no-gui`：只读取、校验并打印点数，不创建窗口。
- `--output PATH`：显式导出当前点云为 PLY；不指定时不会写出编辑文件。
- `--locator_step`：定位球每次键盘移动的世界坐标距离，默认 `0.05`。
- `--locator_radius`：定位球初始半径，默认 `0.15`。
- `--locator_radius_step`：每次按 `I/J` 改变的半径，默认 `0.02`。

示例：

```bash
python add_points_gui.py \
-s /data1/data/jhc/datasets/net927_1 \
--display_voxel_size 0.02 \
--point_size 3 \
--background 0 0 0
```

导出 PLY：

```bash
python add_points_gui.py \
-s /data1/data/jhc/datasets/net927_1 \
--no-gui \
--output /tmp/net927_1_points.ply
```

`--output` 是显式操作，脚本不会默认覆盖 COLMAP 原始文件或源目录中的 `points3D.ply`。

## 窗口操作

当前 Open3D 窗口显示一个以第一张 COLMAP 图像相机中心为初始位置的亮红色、高不透明度定位球。球使用红色 `RGBA=(1, 0, 0, 0.8)` 材质，并带有轻微红色自发光，便于在点云中识别。第一张图像按图像文件名排序后选择，COLMAP 的 `qvec` 和 `tvec` 表示 world-to-camera 变换，脚本用：

```text
R = qvec2rotmat(qvec)
C = -R.T @ tvec
```

计算相机中心 `C`。定位球是辅助几何，不会写入 `--output` 导出的点云。

键盘快捷键：

- `W` / `S`：定位球沿世界坐标 `X` 轴正向 / 负向移动。
- `A` / `D`：定位球沿世界坐标 `Y` 轴负向 / 正向移动。
- `Q` / `E`：定位球沿世界坐标 `Z` 轴负向 / 正向移动。
- `I` / `J`：增大 / 减小定位球半径。
- `B`：保存当前定位球，在当前位置固定复制一个同半径、亮红色半透明锚点；之后移动或缩放活动定位球不会改变已保存锚点。
- `R`：重置相机视角。
- `Esc`：退出窗口。

`Q` 已经用于 Z 轴移动，因此不再作为退出键。鼠标旋转、平移和缩放使用 Open3D 默认交互方式。每次移动或调整半径后，终端会打印当前定位坐标和球半径；按 `B` 后会打印新增锚点编号、坐标和半径。锚点目前只保存在当前可视化会话中，尚未写入 PLY 或独立工程文件。

## 内部点云状态

脚本定义了 `PointCloudState`，将点数据与 Open3D 的显示对象分离，为后续编辑功能预留状态结构。当前状态包括：

- `points`：`[N, 3]` 的 `float32` 世界坐标；
- `colors`：`[N, 3]` 的 `float32` 颜色，统一为 `[0, 1]`；
- `normals`：`[N, 3]` 的法线，当前 COLMAP 点读取后初始化为零；
- `point_ids`：当前状态中的稳定整数 ID；
- `is_user_added`：标记是否为用户新增点，当前全部为 `False`；
- `dirty`：预留的编辑状态标记，当前读取后为 `False`。

读取后会检查点坐标、颜色是否有限，数组是否为 `[N, 3]`，以及颜色是否在 `[0, 1]` 范围内。

颜色转换遵循项目现有约定：COLMAP 二进制读取器返回 `0..255` 的 RGB，GUI 内部转换成 `0..1` 的浮点颜色。

## `pcl_viewer` 评估

当前没有把 `pcl_viewer` 或 PCL 加入项目依赖。原因如下：

- 仓库没有现成的 PCL 依赖或 Python/C++ 桥接；
- `pcl_viewer` 更适合临时查看 PLY/PCD 文件，不适合作为 Python 训练项目中的状态管理组件；
- 即使接入 PCLVisualizer，鼠标点击仍然只提供屏幕坐标，不能自动确定新增点的三维深度；
- PCL 窗口中的点编辑结果还需要额外同步回 Python、保存并转换为训练侧点云格式。

因此，当前脚本使用 Open3D。PCL 工具仍然可以作为外部程序查看导出的 PLY，但不属于 `add_points_gui.py` 的运行时依赖。

## 已完成的验证

已在本地 `curveGS` 环境中验证：

- `python add_points_gui.py --help` 可以正常显示参数；
- Python 语法检查通过；
- `points3D.bin` 读取成功；
- 示例数据读取到 `52459` 个 COLMAP 点；
- 缺少 `points3D.bin` 时可以回退到 `points3D.txt`；
- 缺少 `sparse/0` 时会报告明确错误；
- `--init_voxel_size` 可以对状态点云降采样；
- `--display_voxel_size` 和显式 PLY 导出路径可以执行；
- 无 GUI 模式可以用于无显示环境下的读取检查。

## 当前限制

当前版本只显示点云和定位辅助球，不执行以下操作：

- 鼠标点击新增三维点；
- 删除或移动已有点；
- 撤销和重做；
- 修改 COLMAP 的 `points3D.bin`、`images.bin` 或 `cameras.bin`；
- 保存点 ID、重投影误差和 track 观测关系；
- 直接把普通点云转换成已训练的 Gaussian 参数。

`read_points3D_binary` 的当前接口返回坐标、RGB 和误差数组，但 GUI 第一版只将坐标和 RGB 放入显示状态。未来如果需要保留 COLMAP point ID、误差或 track，应切换到能够保留完整元数据的读取接口，并使用独立的编辑工程文件保存。

## 后续手动加点设计

下一阶段建议继续使用 Open3D，而不是先引入 `pcl_viewer`。手动加点必须先定义屏幕点击对应的三维深度策略，不能把二维鼠标位置直接当成唯一的三维坐标。

推荐按以下顺序实现：

1. **已有点吸附**：鼠标选择最近的已有点，支持选中、标记和删除。
2. **工作平面求交**：用户指定一个平面，鼠标射线与平面求交后生成新点。
3. **局部几何求交**：使用附近点、法线或局部平面估计点击位置的深度。
4. **编辑状态管理**：实现新增、删除、移动、撤销和重做。
5. **显式保存**：PLY 用于与 Open3D、CloudCompare 或 PCL 互操作；NPZ/JSON 保存 point ID、来源、是否用户新增等编辑元数据。
6. **训练适配**：将编辑后的点云转换为项目的 `BasicPointCloud`，再交给 `GaussianCurveModel.create_from_pcd` 初始化，而不是把普通点云 PLY 当成训练完成的 Gaussian PLY。

编辑结果不应默认覆盖 COLMAP 源数据。建议保存到用户明确指定的新路径，并保留原始 `.bin` 文件不变。
