#!/usr/bin/env python3
"""Cull exported Curve-Gaussian 3DGS PLY files without retraining.

The exported ``opacity`` and ``scale_*`` properties use the standard 3DGS
logit/log-scale representation.  Omitted thresholds disable their respective
filters, so an origin PLY can also be copied without changing its rows.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

import numpy as np
from plyfile import PlyData, PlyElement


ORIGIN_NAME = "curve_3dgs_init(origin).ply"
RGB_ORIGIN_NAME = "curve_3dgs_init_RGB(origin).ply"
DEFAULT_FINAL_NAME = "curve_3dgs_init.ply"
RGB_DEFAULT_FINAL_NAME = "curve_3dgs_init_RGB.ply"


def _validate_thresholds(
    opacity_threshold: Optional[float], ratio_threshold: Optional[float]
) -> None:
    if opacity_threshold is not None:
        if not np.isfinite(opacity_threshold) or not 0.0 <= opacity_threshold <= 1.0:
            raise ValueError("--final_opacity_cull must be finite and in [0, 1]")
    if ratio_threshold is not None:
        if not np.isfinite(ratio_threshold) or ratio_threshold < 1.0:
            raise ValueError(
                "--final_ratio_cull must be finite and greater than or equal to 1"
            )


def _stable_sigmoid(values: np.ndarray) -> np.ndarray:
    """Evaluate sigmoid without overflow for large-magnitude logits."""
    result = np.empty_like(values, dtype=np.float64)
    positive = values >= 0.0
    result[positive] = 1.0 / (1.0 + np.exp(-values[positive]))
    exp_values = np.exp(values[~positive])
    result[~positive] = exp_values / (1.0 + exp_values)
    return result


def _require_fields(names: tuple[str, ...], available: tuple[str, ...]) -> None:
    missing = [name for name in names if name not in available]
    if missing:
        raise ValueError(f"PLY is missing required field(s): {', '.join(missing)}")


def _finite_field(data: np.ndarray, name: str) -> np.ndarray:
    values = np.asarray(data[name], dtype=np.float64)
    if not np.isfinite(values).all():
        raise ValueError(f"PLY field '{name}' contains NaN or infinity")
    return values


def _opacity_remove_mask(data: np.ndarray, threshold: float) -> np.ndarray:
    opacity = _finite_field(data, "opacity")
    return _stable_sigmoid(opacity) < threshold


def _ratio_remove_mask(data: np.ndarray, threshold: float) -> np.ndarray:
    scale_names = ("scale_0", "scale_1", "scale_2")
    log_scales = np.column_stack([_finite_field(data, name) for name in scale_names])
    ordered = np.sort(log_scales, axis=1)[:, ::-1]
    # The PLY contains log-scales, so compare differences in log-space.
    return (ordered[:, 0] - ordered[:, 1]) < np.log(threshold)


def _filtered_vertex_element(vertex: PlyElement, kept_data: np.ndarray) -> PlyElement:
    """Slice vertex rows while retaining its property schema and comments."""
    return PlyElement.describe(
        kept_data,
        "vertex",
        comments=list(vertex.comments),
    )


def default_output_path(input_path: Path) -> Path:
    if input_path.name == ORIGIN_NAME:
        return input_path.with_name(DEFAULT_FINAL_NAME)
    if input_path.name == RGB_ORIGIN_NAME:
        return input_path.with_name(RGB_DEFAULT_FINAL_NAME)
    return input_path.with_name(f"{input_path.stem}_final_cull{input_path.suffix}")


def cull_ply(
    input_path: Path,
    output_path: Path,
    opacity_threshold: Optional[float] = None,
    ratio_threshold: Optional[float] = None,
) -> dict[str, int]:
    """Filter a standard Gaussian PLY and return row-count statistics."""
    _validate_thresholds(opacity_threshold, ratio_threshold)
    input_path = input_path.expanduser()
    output_path = output_path.expanduser()
    if input_path.resolve() == output_path.resolve():
        raise ValueError("Input and output must be different files")

    ply = PlyData.read(str(input_path))
    if "vertex" not in ply:
        raise ValueError(f"{input_path} does not contain a vertex element")

    vertex = ply["vertex"]
    names = tuple(vertex.data.dtype.names or ())
    remove_opacity = np.zeros(len(vertex.data), dtype=bool)
    remove_ratio = np.zeros(len(vertex.data), dtype=bool)

    if opacity_threshold is not None:
        _require_fields(("opacity",), names)
        remove_opacity = _opacity_remove_mask(vertex.data, opacity_threshold)
    if ratio_threshold is not None:
        _require_fields(("scale_0", "scale_1", "scale_2"), names)
        remove_ratio = _ratio_remove_mask(vertex.data, ratio_threshold)

    remove = remove_opacity | remove_ratio
    kept_data = vertex.data[~remove]
    new_vertex = _filtered_vertex_element(vertex, kept_data)

    elements = [new_vertex if element.name == "vertex" else element for element in ply.elements]
    output_ply = PlyData(
        elements,
        text=ply.text,
        byte_order=ply.byte_order,
        comments=ply.comments,
        obj_info=ply.obj_info,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_ply.write(str(output_path))

    return {
        "input": len(vertex.data),
        "removed_opacity": int(remove_opacity.sum()),
        "removed_ratio": int(remove_ratio.sum()),
        "removed": int(remove.sum()),
        "output": len(kept_data),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Cull exported Curve-Gaussian 3DGS Gaussians without retraining."
    )
    parser.add_argument("--input", required=True, type=Path, help="Input Gaussian PLY")
    parser.add_argument("--output", type=Path, help="Output PLY; defaults beside the input")
    parser.add_argument(
        "--final_opacity_cull",
        type=float,
        default=None,
        help="Remove Gaussians whose decoded opacity is strictly below this probability",
    )
    parser.add_argument(
        "--final_ratio_cull",
        type=float,
        default=None,
        help="Remove Gaussians whose long/second-longest axis ratio is strictly below this value",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    input_path = args.input.expanduser()
    output_path = (args.output or default_output_path(input_path)).expanduser()
    stats = cull_ply(
        input_path,
        output_path,
        opacity_threshold=args.final_opacity_cull,
        ratio_threshold=args.final_ratio_cull,
    )
    print(f"Input:  {input_path}")
    print(f"Output: {output_path}")
    print(
        f"Gaussians: {stats['input']} -> {stats['output']} "
        f"(removed {stats['removed']})"
    )
    print(f"Removed by opacity: {stats['removed_opacity']}")
    print(f"Removed by ratio:   {stats['removed_ratio']}")
    if args.final_opacity_cull is None and args.final_ratio_cull is None:
        print("No culling thresholds supplied; wrote a schema-preserving copy.")


if __name__ == "__main__":
    main()
