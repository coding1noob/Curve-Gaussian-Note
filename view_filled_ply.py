"""Compare original and filled PLY clouds using the add_points_gui Open3D backend.

Original points are black; coordinates absent from the original are red.
Filled mode shows the union: all original points plus the added filled points.
Use --radius to restrict both views to a sphere, optionally with --center X Y Z.
Colors are display-only: neither input file is modified.
"""

import argparse
from pathlib import Path

import numpy as np


def load_points(path):
    from plyfile import PlyData

    path = Path(path).expanduser().resolve()
    if not path.is_file():
        raise ValueError(f"PLY file not found: {path}")
    ply = PlyData.read(str(path))
    if "vertex" not in ply:
        raise ValueError(f"No vertex element in {path}")
    vertices = ply["vertex"].data
    if not {"x", "y", "z"}.issubset(vertices.dtype.names or ()):
        raise ValueError(f"Missing vertex x/y/z properties in {path}")
    points = np.column_stack([vertices[axis] for axis in "xyz"]).astype(np.float64)
    if len(points) == 0 or not np.isfinite(points).all():
        raise ValueError(f"PLY must contain nonempty, finite coordinates: {path}")
    return points


def find_added_points(original, filled, tolerance):
    """Match by position, not row order: filtering may remove original rows.

    Without provenance in the PLY, new points coinciding with original positions
    (within tolerance) cannot be distinguished and are treated as original.
    """
    from scipy.spatial import cKDTree

    if not np.isfinite(tolerance) or tolerance < 0:
        raise ValueError("match_tolerance must be finite and non-negative")
    if len(original) == 0:
        return np.ones(len(filled), dtype=bool)
    distances, _ = cKDTree(original).query(filled, k=1)
    return distances > tolerance


def filter_display_radius(original, filled, added_mask, radius, center=None):
    """Clip both clouds with one sphere, preserving precomputed point labels."""
    if not np.isfinite(radius) or radius <= 0:
        raise ValueError("radius must be finite and positive")
    if center is None:
        center = (original.min(axis=0) + original.max(axis=0)) / 2.0
    center = np.asarray(center, dtype=np.float64)
    if center.shape != (3,) or not np.isfinite(center).all():
        raise ValueError("center must contain three finite coordinates")
    original_keep = np.linalg.norm(original - center, axis=1) <= radius
    filled_keep = np.linalg.norm(filled - center, axis=1) <= radius
    return original[original_keep], filled[filled_keep], added_mask[filled_keep], center


def run_viewer(original, filled, added_mask, args):
    display_points = np.concatenate((original, filled[added_mask]), axis=0)
    if len(display_points) == 0:
        print("No visible points remain. Increase --radius or change --center; no window opened.")
        return

    import open3d as o3d

    gui = o3d.visualization.gui
    rendering = o3d.visualization.rendering
    app = gui.Application.instance
    app.initialize()
    window = app.create_window("PLY comparison - black: original / red: added",
                               args.window_width, args.window_height)
    widget = gui.SceneWidget()
    widget.scene = rendering.Open3DScene(window.renderer)
    widget.scene.set_background(np.array([1, 1, 1, 1], dtype=np.float32))
    # Keep point colors independent of illumination and tone mapping.
    widget.scene.view.set_color_grading(rendering.ColorGrading(
        rendering.ColorGrading.Quality.MEDIUM,
        rendering.ColorGrading.ToneMapping.LINEAR,
    ))
    window.add_child(widget)

    clouds = []

    def add_cloud(name, points, color, size):
        if len(points) == 0:
            return
        cloud = o3d.geometry.PointCloud()
        cloud.points = o3d.utility.Vector3dVector(points)
        cloud.paint_uniform_color(color)
        material = rendering.MaterialRecord()
        material.shader = "defaultUnlit"
        material.point_size = size
        # Avoid reduced point sets while moving the camera.
        widget.scene.add_geometry(name, cloud, material, False)
        clouds.append(cloud)

    add_cloud("input", original, [0, 0, 0], args.point_size)
    # Reuse all original points in both views; do not render matched rows twice.
    add_cloud("added", filled[added_mask], [1, 0, 0], args.added_point_size)
    present = {"input"} if len(original) else set()
    if np.any(added_mask):
        present.add("added")

    lower = display_points.min(axis=0)
    upper = display_points.max(axis=0)
    if np.max(upper - lower) == 0:
        lower, upper = lower - 0.5, upper + 0.5
    bounds = o3d.geometry.AxisAlignedBoundingBox(lower, upper)

    def reset_view():
        widget.setup_camera(60.0, bounds, bounds.get_center())
        widget.force_redraw()

    toolbar = gui.Horiz(12, gui.Margins(8, 4, 8, 4))
    input_button = gui.Button("Original (input.ply)")
    filled_button = gui.Button("Filled + Original")
    reset_button = gui.Button("Reset view [R]")
    status = gui.Label("")
    for control in (input_button, filled_button, reset_button, status):
        toolbar.add_child(control)
    window.add_child(toolbar)

    def show_view(view):
        # Visibility changes preserve the camera for direct before/after comparison.
        for name in present:
            widget.scene.show_geometry(name, name == "input" or view == "filled")
        if view == "input":
            status.text = f"Original: {len(original):,} black points"
        else:
            status.text = (f"Merged: {len(original):,} black + "
                           f"{np.count_nonzero(added_mask):,} red")
        widget.force_redraw()
        window.post_redraw()

    input_button.set_on_clicked(lambda: show_view("input"))
    filled_button.set_on_clicked(lambda: show_view("filled"))
    reset_button.set_on_clicked(reset_view)

    def on_layout(context):
        rect = window.content_rect
        height = toolbar.calc_preferred_size(context, gui.Widget.Constraints()).height
        toolbar.frame = gui.Rect(rect.x, rect.y, rect.width, height)
        widget.frame = gui.Rect(rect.x, rect.y + height, rect.width,
                               max(1, rect.height - height))

    def on_key(event):
        if event.type == gui.KeyEvent.DOWN:
            if event.key == gui.KeyName.R:
                reset_view()
                return gui.Widget.EventCallbackResult.CONSUMED
            if event.key == gui.KeyName.ESCAPE:
                app.quit()
                return gui.Widget.EventCallbackResult.CONSUMED
        return gui.Widget.EventCallbackResult.IGNORED

    window.set_on_layout(on_layout)
    widget.set_on_key(on_key)
    reset_view()
    show_view(args.view)
    print("Mouse: drag to rotate, wheel to zoom, Ctrl+drag to pan.")
    print("Toolbar: original / original + filled (same camera). R: reset view. Esc: exit.")
    app.run()


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "directory", nargs="?", type=Path,
        default=Path(__file__).resolve().parent / "output/test/buaa_net_Oct29",
        help="Directory containing input.ply and input_filled.ply.",
    )
    parser.add_argument("--input", type=Path, help="Override original PLY path.")
    parser.add_argument("--filled", type=Path, help="Override filled PLY path.")
    parser.add_argument("--view", choices=("input", "filled"), default="filled",
                        help="input: original only; filled: original + added filled points.")
    parser.add_argument("--point_size", type=float, default=2.0,
                        help="Black point size in pixels (default: 2).")
    parser.add_argument("--added_point_size", type=float, default=3.0,
                        help="Red point size in pixels (default: 3).")
    parser.add_argument("--match_tolerance", type=float, default=1e-6,
                        help="Original-position matching distance in scene units (default: 1e-6).")
    parser.add_argument("--radius", type=float,
                        help="Show points at distance <= radius from center, in scene units. "
                             "Omit to disable clipping; applies to both clouds.")
    parser.add_argument("--center", nargs=3, type=float, metavar=("X", "Y", "Z"),
                        help="Sphere center; requires --radius. Default: original bounding-box center.")
    parser.add_argument("--window_width", type=int, default=1440)
    parser.add_argument("--window_height", type=int, default=900)
    parser.add_argument("--no-gui", action="store_true",
                        help="Validate PLYs and report counts without opening a window.")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    for name in ("point_size", "added_point_size"):
        if not np.isfinite(getattr(args, name)) or getattr(args, name) <= 0:
            parser.error(f"{name} must be finite and positive")
    if args.window_width < 640 or args.window_height < 240:
        parser.error("Window must be at least 640 x 240")
    if args.radius is not None and (not np.isfinite(args.radius) or args.radius <= 0):
        parser.error("radius must be finite and positive")
    if args.center is not None:
        if args.radius is None:
            parser.error("--center requires --radius")
        if not np.isfinite(args.center).all():
            parser.error("center must contain three finite coordinates")
    directory = args.directory.expanduser()
    original_path = args.input or directory / "input.ply"
    filled_path = args.filled or directory / "input_filled.ply"
    try:
        original = load_points(original_path)
        filled = load_points(filled_path)
        added_mask = find_added_points(original, filled, args.match_tolerance)
        print(f"Original: {original_path} ({len(original):,} points)")
        print(f"Filled:   {filled_path} ({len(filled):,} points)")
        if args.radius is not None:
            # Classify before clipping so boundary points do not get relabeled as added.
            original, filled, added_mask, center = filter_display_radius(
                original, filled, added_mask, args.radius, args.center)
            print(f"Radius filter: center={center.tolist()}, radius={args.radius:g}")
            print(f"Within radius: {len(original):,} original / {len(filled):,} filled points")
        print(f"Merged display (original + filled): {len(original):,} black / "
              f"{np.count_nonzero(added_mask):,} red (added)")
        print(f"Position matching tolerance: {args.match_tolerance:g}; files are not modified.")
        if not args.no_gui:
            run_viewer(original, filled, added_mask, args)
    except ImportError as exc:
        parser.exit(1, f"Missing dependency: {exc}. Use the add_points_gui environment "
                       "or install: pip install numpy scipy plyfile open3d\n")
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
