#!/usr/bin/env python3
"""Delete PLY vertices inside one or more axis-aligned boxes.

The input PLY is treated as a 3D Gaussian PLY: all vertex properties are
preserved, and only the vertex rows inside the requested boxes are removed.
"""

# 使用说明：
# python delete_point.py \
# --input output/virtual_net2_8.12/curve_3dgs_init.ply \
# --output output/virtual_net2_8.12/curve_3dgs_init_manual_clean.ply \
# --boxes \
# 12.618 2.34032 9.14142 \
# -0.420650 -1.278502 2.937510 \
# 0.107289 0.990806 0.082419 55.456095


from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

import numpy as np
from plyfile import PlyData, PlyElement


REQUIRED_COORDINATES = ("x", "y", "z")
BOX_VALUE_COUNT = 10


Box = tuple[
    tuple[float, float, float],
    tuple[float, float, float],
    tuple[float, float, float],
    float,
]


def parse_boxes(values: Sequence[str]) -> list[Box]:
    """Parse repeated ``SX SY SZ CX CY CZ AX AY AZ ANGLE`` specifications."""
    if len(values) == 0 or len(values) % BOX_VALUE_COUNT != 0:
        raise argparse.ArgumentTypeError(
            "--boxes requires 10 values per box: "
            "SX SY SZ CX CY CZ AX AY AZ ANGLE"
        )

    try:
        numbers = [float(value) for value in values]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("all --boxes values must be numbers") from exc

    boxes: list[Box] = []
    for start in range(0, len(numbers), BOX_VALUE_COUNT):
        size = tuple(numbers[start : start + 3])
        center = tuple(numbers[start + 3 : start + 6])
        axis = tuple(numbers[start + 6 : start + 9])
        angle = numbers[start + 9]
        if any(length <= 0 for length in size):
            raise argparse.ArgumentTypeError(
                "box dimensions SX SY SZ must all be greater than zero"
            )
        if np.linalg.norm(axis) == 0:
            raise argparse.ArgumentTypeError("rotation axis AX AY AZ must not be zero")
        boxes.append((size, center, axis, angle))  # type: ignore[arg-type]
    return boxes


def rotation_matrix_axis_angle(
    axis: tuple[float, float, float], angle_degrees: float
) -> np.ndarray:
    """Return a rotation matrix from a CloudCompare axis and angle."""
    axis_array = np.asarray(axis, dtype=np.float64)
    axis_array /= np.linalg.norm(axis_array)
    x, y, z = axis_array
    angle = np.deg2rad(angle_degrees)
    cosine = np.cos(angle)
    sine = np.sin(angle)
    one_minus_cosine = 1.0 - cosine

    return np.array(
        [
            [
                cosine + x * x * one_minus_cosine,
                x * y * one_minus_cosine - z * sine,
                x * z * one_minus_cosine + y * sine,
            ],
            [
                y * x * one_minus_cosine + z * sine,
                cosine + y * y * one_minus_cosine,
                y * z * one_minus_cosine - x * sine,
            ],
            [
                z * x * one_minus_cosine - y * sine,
                z * y * one_minus_cosine + x * sine,
                cosine + z * z * one_minus_cosine,
            ],
        ],
        dtype=np.float64,
    )


def box_bounds(
    size: tuple[float, float, float],
    center: tuple[float, float, float],
) -> tuple[np.ndarray, np.ndarray]:
    """Return the lower and upper corners of an axis-aligned box."""
    half_size = np.asarray(size, dtype=np.float64) / 2.0
    center_array = np.asarray(center, dtype=np.float64)
    return center_array - half_size, center_array + half_size


def delete_points_in_boxes(
    input_path: Path,
    output_path: Path,
    boxes: Sequence[Box],
    strict: bool = False,
) -> tuple[int, int]:
    """Remove vertices inside any requested box and write a new PLY.

    Each box is specified as ``(size, center, axis, angle)``. The rotation
    uses CloudCompare's axis-angle format: ``(AX, AY, AZ, ANGLE)`` where the
    angle is in degrees. Bounds are inclusive by default; with ``strict=True``,
    points on box faces are retained. Returns the original vertex count and
    the number removed.
    """
    if not boxes:
        raise ValueError("at least one box is required")

    ply = PlyData.read(str(input_path))
    if "vertex" not in ply:
        raise ValueError(f"{input_path} does not contain a vertex element")

    vertex = ply["vertex"]
    missing = [name for name in REQUIRED_COORDINATES if name not in vertex.data.dtype.names]
    if missing:
        raise ValueError(f"PLY is missing coordinate fields: {', '.join(missing)}")

    xyz = np.column_stack([vertex.data[name] for name in REQUIRED_COORDINATES])
    remove = np.zeros(len(vertex.data), dtype=bool)
    for size, center, axis, angle in boxes:
        center_array = np.asarray(center, dtype=np.float64)
        half_size = np.asarray(size, dtype=np.float64) / 2.0
        rotation_matrix = rotation_matrix_axis_angle(axis, angle)
        # Transform global points into the box's local coordinate system.
        local_xyz = (xyz - center_array) @ rotation_matrix
        if strict:
            inside = np.all(
                (local_xyz > -half_size) & (local_xyz < half_size), axis=1
            )
        else:
            inside = np.all(
                (local_xyz >= -half_size) & (local_xyz <= half_size), axis=1
            )
        remove |= inside

    kept_data = vertex.data[~remove]

    # Preserve all Gaussian fields and the original PLY metadata.
    new_vertex = PlyElement.describe(kept_data, "vertex")
    output_ply = PlyData(
        [new_vertex],
        text=ply.text,
        byte_order=ply.byte_order,
        comments=ply.comments,
        obj_info=ply.obj_info,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_ply.write(str(output_path))
    return len(vertex.data), int(remove.sum())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Delete all PLY points inside one or more axis-aligned boxes."
    )
    parser.add_argument("--input", required=True, type=Path, help="Input PLY path")
    parser.add_argument("--output", required=True, type=Path, help="Output PLY path")
    parser.add_argument(
        "--boxes",
        required=True,
        nargs="+",
        metavar="VALUE",
        help=(
            "Repeated box values in groups of ten: "
            "SX SY SZ CX CY CZ AX AY AZ ANGLE; dimensions, global center, "
            "then CloudCompare axis-angle rotation"
        ),
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Use strict inequalities, leaving points exactly on box faces",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    boxes = parse_boxes(args.boxes)

    if args.input.resolve() == args.output.resolve():
        raise SystemExit("Input and output must be different files")

    original_count, removed_count = delete_points_in_boxes(
        args.input, args.output, boxes, strict=args.strict
    )

    print(f"Input:  {args.input}")
    print(f"Output: {args.output}")
    for index, (size, center, axis, angle) in enumerate(boxes, start=1):
        print(
            f"Box {index}: size=({size[0]:.9f}, {size[1]:.9f}, {size[2]:.9f}), "
            f"center=({center[0]:.9f}, {center[1]:.9f}, {center[2]:.9f}), "
            f"axis=({axis[0]:.6f}, {axis[1]:.6f}, {axis[2]:.6f}), "
            f"angle={angle:.6f} degrees"
        )
    print(f"Boxes:  {len(boxes)}")
    print(f"Points: {original_count} -> {original_count - removed_count}")
    print(f"Removed: {removed_count}")


if __name__ == "__main__":
    main()
