"""Read and view a COLMAP point cloud, with state ready for future editing."""

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import numpy as np

# [依赖检查] 优雅地处理 Open3D 未安装的情况
try:
    import open3d as o3d
except ImportError as exc:
    o3d = None
    _OPEN3D_IMPORT_ERROR = exc

# 假设此文件与 scene 目录同级，或已配置好 PYTHONPATH
from scene.colmap_loader import (
    qvec2rotmat,
    read_extrinsics_binary,
    read_extrinsics_text,
    read_points3D_binary,
    read_points3D_text,
)


# ==============================================================================
# 1. 数据模型层 (Data Models)
# ==============================================================================

@dataclass
class PointCloudState:
    """内存中的点云状态容器，为未来的编辑功能预留结构。"""
    points: np.ndarray          # [N, 3] float32, 世界坐标
    colors: np.ndarray          # [N, 3] float32, 颜色 (范围 0.0 - 1.0)
    normals: np.ndarray         # [N, 3] float32, 法线 (当前初始化为0)
    point_ids: np.ndarray       # [N,] int64, 稳定的点 ID
    is_user_added: np.ndarray   # [N,] bool, 标记是否为用户手动添加的点
    dirty: bool = False         # bool, 标记数据是否被修改过（用于后续保存逻辑）

    @classmethod
    def from_colmap(cls, points, colors):
        """从 COLMAP 原始数据初始化，并统一颜色范围到 [0, 1]"""
        points = np.asarray(points, dtype=np.float32)
        colors = np.asarray(colors, dtype=np.float32)
        if colors.size and colors.max() > 1.0:
            colors = colors / 255.0
        return cls(
            points=points,
            colors=np.clip(colors, 0.0, 1.0),
            normals=np.zeros_like(points, dtype=np.float32),
            point_ids=np.arange(points.shape[0], dtype=np.int64),
            is_user_added=np.zeros(points.shape[0], dtype=bool),
        )

    def validate(self):
        """安全检查：确保所有数组形状匹配且数据有效 (无 NaN/Inf)"""
        count = self.points.shape[0]
        if self.points.shape != (count, 3):
            raise ValueError(f"points must have shape [N, 3], got {self.points.shape}")
        for name, values in (("colors", self.colors), ("normals", self.normals)):
            if values.shape != (count, 3):
                raise ValueError(f"{name} must have shape [N, 3], got {values.shape}")
        if self.point_ids.shape != (count,) or self.is_user_added.shape != (count,):
            raise ValueError("point metadata length does not match point count")
        if not np.isfinite(self.points).all() or not np.isfinite(self.colors).all():
            raise ValueError("point coordinates and colors must be finite")
        if np.any(self.colors < 0.0) or np.any(self.colors > 1.0):
            raise ValueError("colors must be in [0, 1]")


@dataclass
class LocatorState:
    """GUI 中红色定位球的状态机"""
    position: np.ndarray  # 当前中心位置 [3,]
    radius: float         # 当前半径
    step: float           # 每次按键移动的距离
    radius_step: float    # 每次按键缩放的距离
    image_name: str       # 关联的初始图像名
    image_id: int         # 关联的初始图像 ID

    def move(self, axis, direction):
        """沿指定轴 (0:X, 1:Y, 2:Z) 移动"""
        self.position[axis] += direction * self.step

    def resize(self, direction):
        """调整半径，确保最小不低于 radius_step * 0.1"""
        self.radius = max(self.radius + direction * self.radius_step, self.radius_step * 0.1)


# ==============================================================================
# 2. 数据加载层 (Data Loading)
# ==============================================================================

def load_first_camera_pose(source_path):
    """读取第一张图像的位姿，并计算其相机中心 (作为红球初始位置)"""
    sparse_dir = Path(source_path) / "sparse" / "0"
    binary_path = sparse_dir / "images.bin"
    text_path = sparse_dir / "images.txt"
    
    if binary_path.is_file():
        images = read_extrinsics_binary(str(binary_path))
    elif text_path.is_file():
        images = read_extrinsics_text(str(text_path))
    else:
        raise FileNotFoundError(f"Neither {binary_path} nor {text_path} exists.")
        
    if not images:
        raise ValueError(f"No registered image poses found in {sparse_dir}")
        
    # 按文件名排序，取第一张
    image = sorted(images.values(), key=lambda item: item.name)[0]
    
    # 核心数学：World-to-Camera 旋转矩阵，计算相机中心 C = -R^T * t
    rotation_world_to_camera = qvec2rotmat(image.qvec)
    camera_center = -rotation_world_to_camera.T @ np.asarray(image.tvec, dtype=np.float32)
    return image.name, int(image.id), camera_center.astype(np.float32)


def load_colmap_points(source_path):
    """读取 COLMAP 3D 点云数据"""
    sparse_dir = Path(source_path) / "sparse" / "0"
    if not sparse_dir.is_dir():
        raise FileNotFoundError(f"COLMAP model directory not found: {sparse_dir}")
        
    binary_path = sparse_dir / "points3D.bin"
    text_path = sparse_dir / "points3D.txt"
    
    if binary_path.is_file():
        points, colors, _ = read_points3D_binary(str(binary_path))
    elif text_path.is_file():
        points, colors, _ = read_points3D_text(str(text_path))
    else:
        raise FileNotFoundError(f"Neither {binary_path} nor {text_path} exists.")
        
    return PointCloudState.from_colmap(points, colors)


def voxel_downsample(points, colors, voxel_size):
    """使用 Open3D 进行体素降采样 (返回新的 numpy 数组)"""
    if voxel_size <= 0 or len(points) == 0:
        return points, colors
    if o3d is None:
        raise RuntimeError("Open3D is required for voxel downsampling.") from _OPEN3D_IMPORT_ERROR
        
    cloud = o3d.geometry.PointCloud()
    cloud.points = o3d.utility.Vector3dVector(points)
    cloud.colors = o3d.utility.Vector3dVector(colors)
    downsampled = cloud.voxel_down_sample(voxel_size)
    return np.asarray(downsampled.points), np.asarray(downsampled.colors)


# ==============================================================================
# 3. GUI 渲染与交互层 (GUI & Interaction)
# ==============================================================================

def run_viewer(points, colors, locator, args):
    """初始化并运行 Open3D 可视化窗口"""
    if o3d is None:
        raise RuntimeError("Open3D is required for the GUI.") from _OPEN3D_IMPORT_ERROR

    # [1] 初始化 Open3D 应用程序和窗口
    app = o3d.visualization.gui.Application.instance
    app.initialize()
    window = app.create_window("COLMAP Point Cloud", args.window_width, args.window_height)
    scene_widget = o3d.visualization.gui.SceneWidget()
    scene_widget.scene = o3d.visualization.rendering.Open3DScene(window.renderer)
    window.add_child(scene_widget)

    # [2] 配置点云材质并添加到场景
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)
    if len(colors) == len(points):
        point_cloud.colors = o3d.utility.Vector3dVector(colors)

    point_material = o3d.visualization.rendering.MaterialRecord()
    point_material.shader = "defaultUnlit"  # 无光照着色，保持原始颜色
    point_material.point_size = args.point_size
    scene_widget.scene.set_background(np.asarray((*args.background, 1.0), dtype=np.float32))
    scene_widget.scene.add_geometry("colmap_points", point_cloud, point_material)

    # [3] 辅助函数：生成定位球 (红球) 和 锚点球 (保存的固定红球)
    def make_locator_mesh():
        mesh = o3d.geometry.TriangleMesh.create_sphere(radius=float(locator.radius), resolution=24)
        mesh.compute_vertex_normals()
        mesh.translate(locator.position.astype(np.float64))
        return mesh

    def make_anchor_mesh(position, radius):
        mesh = o3d.geometry.TriangleMesh.create_sphere(radius=float(radius), resolution=20)
        mesh.compute_vertex_normals()
        mesh.translate(np.asarray(position, dtype=np.float64))
        return mesh
    
    # 👇 【新增】生成黄色坐标系十字 (LineSet)
    def make_axes_lines(position, radius):
        length = radius * 1.5  # 轴长设为半径的1.5倍，确保伸出红球外部，清晰可见
        origin = np.asarray(position, dtype=np.float64)
        points = [
            origin,
            origin + np.array([length, 0.0, 0.0], dtype=np.float64), # X轴末端
            origin + np.array([0.0, length, 0.0], dtype=np.float64), # Y轴末端
            origin + np.array([0.0, 0.0, length], dtype=np.float64)  # Z轴末端
        ]
        lines = [[0, 1], [0, 2], [0, 3]]
        # 纯黄色 [R, G, B]，如果需要经典RGB，可改为 [[1,0,0], [0,1,0], [0,0,1]]
        colors = [[1.0, 1.0, 0.0] for _ in range(3)] 
        
        line_set = o3d.geometry.LineSet()
        line_set.points = o3d.utility.Vector3dVector(points)
        line_set.lines = o3d.utility.Vector2iVector(lines)
        line_set.colors = o3d.utility.Vector3dVector(colors)
        return line_set

    locator_material = o3d.visualization.rendering.MaterialRecord()
    locator_material.shader = "defaultLitTransparency"
    locator_material.base_color = (1.0, 0.0, 0.0, 0.8)      # 红色，80% 不透明度
    locator_material.emissive_color = (0.2, 0.0, 0.0, 1.0)  # 轻微自发光，防止在暗处看不见
    locator_material.has_alpha = True
    scene_widget.scene.add_geometry("locator_sphere", make_locator_mesh(), locator_material)
    
    # 👇 【修改】1. 定义坐标轴材质 (必须项)
    axes_material = o3d.visualization.rendering.MaterialRecord()
    axes_material.shader = "defaultUnlit"  # 使用无光照着色，确保线条颜色不受场景光照影响
    axes_material.base_color = [1.0, 1.0, 1.0, 1.0] # 白色基底，让 LineSet 自身的顶点颜色(黄色)生效
    
    # 👇 【修改】2. 传入 axes_material 作为第四个参数
    scene_widget.scene.add_geometry("locator_axes", make_axes_lines(locator.position, locator.radius), axes_material)

    anchors = []  # 存储已保存的锚点: (name, position, radius)

    # [4] 设置初始相机视角，对准定位球
    bounds = point_cloud.get_axis_aligned_bounding_box()
    if len(points) == 0:
        bounds = o3d.geometry.AxisAlignedBoundingBox(locator.position - locator.radius, locator.position + locator.radius)
    scene_widget.setup_camera(60.0, bounds, locator.position.reshape(3, 1))

    # [5] 交互逻辑：保存锚点
    # [5] 交互逻辑：保存锚点 & 每3次生成三角形
    def add_anchor():
        anchor_id = len(anchors)
        name = "anchor_{:04d}".format(anchor_id)
        anchor_material = o3d.visualization.rendering.MaterialRecord()
        anchor_material.shader = "defaultLitTransparency"
        anchor_material.base_color = (1.0, 0.0, 0.0, 0.8)
        anchor_material.emissive_color = (0.2, 0.0, 0.0, 1.0)
        anchor_material.has_alpha = True
        scene_widget.scene.add_geometry(name, make_anchor_mesh(locator.position, locator.radius), anchor_material)
        
        # 1. 记录当前锚点
        anchors.append((name, locator.position.copy(), locator.radius))
        print(f"Saved {name}: position={np.array2string(locator.position, precision=5)}, radius={locator.radius}")
        
        # 2. 👇 核心新增：检查是否攒够了 3 个锚点
        if len(anchors) % 3 == 0:
            # 获取最近的 3 个锚点
            recent = anchors[-3:]
            p0, r0 = recent[0][1], recent[0][2]
            p1, r1 = recent[1][1], recent[1][2]
            p2, r2 = recent[2][1], recent[2][2]
            
            # --- A. 可视化黄线三角形 ---
            tri_idx = len(anchors) // 3 - 1
            tri_name = f"triangle_{tri_idx:04d}"
            
            line_set = o3d.geometry.LineSet()
            line_set.points = o3d.utility.Vector3dVector([p0, p1, p2])
            line_set.lines = o3d.utility.Vector2iVector([[0, 1], [1, 2], [2, 0]])
            line_set.colors = o3d.utility.Vector3dVector([[1.0, 1.0, 0.0] for _ in range(3)]) # 纯黄色
            
            # 复用之前定义的 axes_material (defaultUnlit，确保黄色高亮)
            scene_widget.scene.add_geometry(tri_name, line_set, axes_material)
            print(f"  -> Formed and visualized {tri_name} with yellow lines.")
            
            # --- B. 保存到 .txt 文件 ---
            txt_path = os.path.join(args.source_path, "saved_triangles.txt")
            
            # 如果是第一个三角形，写入表头方便阅读
            if len(anchors) == 3:
                with open(txt_path, "w") as f:
                    f.write("# p0_x p0_y p0_z  p1_x p1_y p1_z  p2_x p2_y p2_z  radius_of_p0\n")
            
            # 格式化数据并追加写入 (保留6位小数)
            line_to_write = f"{p0[0]:.6f} {p0[1]:.6f} {p0[2]:.6f}  {p1[0]:.6f} {p1[1]:.6f} {p1[2]:.6f}  {p2[0]:.6f} {p2[1]:.6f} {p2[2]:.6f}  {r0:.6f}\n"
            
            with open(txt_path, "a") as f:
                f.write(line_to_write)
            print(f"  -> Appended triangle data to: {txt_path}")

    # [6] 交互逻辑：键盘事件监听 (核心修改点)
    def on_key(event):
        if event.type != event.DOWN:
            return scene_widget.IGNORED
        key = event.key
        
        if key == o3d.visualization.gui.KeyName.ESCAPE:
            app.quit()
            return scene_widget.CONSUMED
            
        # 移动逻辑
        if key == o3d.visualization.gui.KeyName.W: locator.move(0, 1)
        elif key == o3d.visualization.gui.KeyName.S: locator.move(0, -1)
        elif key == o3d.visualization.gui.KeyName.A: locator.move(1, -1)
        elif key == o3d.visualization.gui.KeyName.D: locator.move(1, 1)
        elif key == o3d.visualization.gui.KeyName.Q: locator.move(2, -1)
        elif key == o3d.visualization.gui.KeyName.E: locator.move(2, 1)
        # 缩放逻辑
        elif key == o3d.visualization.gui.KeyName.I: locator.resize(1)
        elif key == o3d.visualization.gui.KeyName.J: locator.resize(-1)
        # 视角重置
        elif key == o3d.visualization.gui.KeyName.R:
            scene_widget.setup_camera(60.0, bounds, locator.position.reshape(3, 1))
            window.post_redraw()
            return scene_widget.CONSUMED
        # 保存锚点
        elif key == o3d.visualization.gui.KeyName.B:
            add_anchor()
            return scene_widget.CONSUMED
        else:
            return scene_widget.IGNORED
            
        scene_widget.scene.remove_geometry("locator_sphere")
        scene_widget.scene.remove_geometry("locator_axes") # 移除旧的
        
        scene_widget.scene.add_geometry("locator_sphere", make_locator_mesh(), locator_material)
        
        # 👇 【修改】重新添加时，同样必须传入 axes_material
        scene_widget.scene.add_geometry("locator_axes", make_axes_lines(locator.position, locator.radius), axes_material)
        
        scene_widget.force_redraw()
        window.post_redraw()

        print(f"locator position=[{locator.position[0]:.4f}, {locator.position[1]:.4f}, {locator.position[2]:.4f}], radius={locator.radius:.4f}")
        return scene_widget.CONSUMED

    scene_widget.set_on_key(on_key)
    window.set_on_close(lambda: True)
    
    print("Controls: W/S=X +/-; A/D=Y -/+; Q/E=Z -/+; I/J=radius +/-; B=save anchor; R=reset view; Esc=exit")
    app.run()


# ==============================================================================
# 4. 命令行与主控制流 (CLI & Main)
# ==============================================================================

def build_parser():
    parser = argparse.ArgumentParser(description="Read a COLMAP point cloud and display it with Open3D.")
    parser.add_argument("-s", "--source_path", required=True, help="COLMAP dataset root containing sparse/0/points3D.bin.")
    # --- 以下参数为兼容旧脚本保留，当前逻辑中不使用 ---
    parser.add_argument("--images", default="images", help="Accepted for parity; not used.")
    parser.add_argument("--depths", default="", help="Accepted for parity; not used.")
    parser.add_argument("--eval", action="store_true", help="Accepted for parity; not used.")
    parser.add_argument("--train_test_exp", action="store_true", help="Accepted for parity; not used.")
    parser.add_argument("--detector", default="PidiNet", choices=["PidiNet", "DexiNed"], help="Accepted for parity; not used.")
    parser.add_argument("--llffhold", type=int, default=8, help="Accepted for parity; not used.")
    # ------------------------------------------------
    parser.add_argument("--init_voxel_size", type=float, default=0.0, help="Voxel downsampling for the point cloud state; 0 disables it.")
    parser.add_argument("--display_voxel_size", type=float, default=0.0, help="Additional voxel downsampling for display only; 0 disables it.")
    parser.add_argument("--point_size", type=float, default=2.0, help="Open3D point size in pixels.")
    parser.add_argument("--window_width", type=int, default=1280)
    parser.add_argument("--window_height", type=int, default=800)
    parser.add_argument("--background", nargs=3, type=float, default=(0.05, 0.05, 0.05), metavar=("R", "G", "B"), help="Open3D background color [0, 1].")
    parser.add_argument("--no-gui", action="store_true", help="Load and validate points without opening a window.")
    parser.add_argument("--output", default=None, help="Optional output PLY path; no file is written by default.")
    parser.add_argument("--locator_step", type=float, default=0.05, help="World-coordinate movement per key press.")
    parser.add_argument("--locator_radius", type=float, default=0.15, help="Initial radius of the red locator sphere.")
    parser.add_argument("--locator_radius_step", type=float, default=0.02, help="Radius change per I/J key press.")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    source_path = os.path.abspath(os.path.expanduser(args.source_path))
    
    if not os.path.isdir(source_path):
        raise SystemExit(f"Source directory does not exist: {source_path}")
    if args.init_voxel_size < 0 or args.display_voxel_size < 0:
        raise SystemExit("voxel sizes must be non-negative")
    if args.locator_step <= 0 or args.locator_radius <= 0 or args.locator_radius_step <= 0:
        raise SystemExit("locator step, radius, and radius step must be positive")

    # 1. 加载并验证点云
    state = load_colmap_points(source_path)
    state.validate()
    print(f"Loaded {len(state.points)} COLMAP points")
    
    # 2. 获取第一张相机位姿，初始化定位球
    image_name, image_id, camera_center = load_first_camera_pose(source_path)
    locator = LocatorState(
        position=camera_center,
        radius=float(args.locator_radius),
        step=float(args.locator_step),
        radius_step=float(args.locator_radius_step),
        image_name=image_name,
        image_id=image_id,
    )

    # 3. (可选) 对内存中的真实状态进行降采样
    if args.init_voxel_size > 0:
        state.points, state.colors = voxel_downsample(state.points, state.colors, args.init_voxel_size)
        state.normals = np.zeros_like(state.points, dtype=np.float32)
        state.point_ids = np.arange(len(state.points), dtype=np.int64)
        state.is_user_added = np.zeros(len(state.points), dtype=bool)
        print(f"State voxel downsample: {len(state.points)} points")

    # 4. (可选) 导出为 PLY 文件
    if args.output:
        if o3d is None:
            raise RuntimeError("Open3D is required to write PLY output.") from _OPEN3D_IMPORT_ERROR
        output_path = os.path.abspath(os.path.expanduser(args.output))
        output_cloud = o3d.geometry.PointCloud()
        output_cloud.points = o3d.utility.Vector3dVector(state.points)
        output_cloud.colors = o3d.utility.Vector3dVector(state.colors)
        if not o3d.io.write_point_cloud(output_path, output_cloud):
            raise RuntimeError(f"Failed to write point cloud: {output_path}")
        print(f"Wrote point cloud: {output_path}")

    # 5. 退出或启动 GUI
    if args.no_gui:
        return 0

    # 仅为显示创建降采样副本，不污染 state
    display_points, display_colors = voxel_downsample(state.points, state.colors, args.display_voxel_size)
    print(f"Displaying {len(display_points)} points; press Esc to close")
    run_viewer(display_points, display_colors, locator, args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())