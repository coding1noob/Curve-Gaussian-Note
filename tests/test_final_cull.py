from __future__ import annotations

import json
import math
import tempfile
import sys
import unittest
from pathlib import Path

import numpy as np
from plyfile import PlyData, PlyElement

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import final_cull


VERTEX_DTYPE = [
    ("x", "f4"),
    ("y", "f4"),
    ("z", "f4"),
    ("opacity", "f4"),
    ("scale_0", "f4"),
    ("scale_1", "f4"),
    ("scale_2", "f4"),
    ("rot_0", "f4"),
    ("rot_1", "f4"),
    ("custom", "i4"),
]


def make_vertex() -> np.ndarray:
    rows = np.empty(4, dtype=VERTEX_DTYPE)
    rows["x"] = np.arange(4)
    rows["y"] = 10
    rows["z"] = 20
    rows["opacity"] = [math.log(0.1 / 0.9), 0.0, math.log(0.9 / 0.1), 0.0]
    # Ratios are 2, 1, 4, and 2. The scale order is intentionally varied.
    rows["scale_0"] = np.log([4.0, 2.0, 1.0, 2.0])
    rows["scale_1"] = np.log([2.0, 2.0, 4.0, 1.0])
    rows["scale_2"] = np.log([1.0, 2.0, 1.0, 1.0])
    rows["rot_0"] = [1.0, 2.0, 3.0, 4.0]
    rows["rot_1"] = 7.0
    rows["custom"] = np.arange(100, 104)
    return rows


def make_long_length_vertex() -> np.ndarray:
    lengths = np.array([1.0] * 20 + [2.0, 0.01], dtype=np.float64)
    rows = np.zeros(len(lengths), dtype=VERTEX_DTYPE)
    rows["x"] = np.arange(len(lengths))
    rows["scale_0"] = np.log(lengths)
    rows["scale_1"] = np.log(lengths)
    rows["scale_2"] = np.log(lengths)
    return rows


def write_ply(path: Path, rows: np.ndarray, text: bool = False) -> None:
    face = np.empty(1, dtype=[("vertex_indices", "i4", (3,))])
    face["vertex_indices"] = [[0, 1, 2]]
    vertex = PlyElement.describe(rows, "vertex", comments=["vertex metadata"])
    face_element = PlyElement.describe(face, "face")
    PlyData(
        [vertex, face_element],
        text=text,
        comments=["file metadata"],
        obj_info=["test object"],
    ).write(str(path))


class FinalCullTests(unittest.TestCase):
    def test_opacity_and_ratio_use_strict_lower_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            source = directory / "curve_3dgs_init(origin).ply"
            output = directory / "filtered.ply"
            write_ply(source, make_vertex())

            stats = final_cull.cull_ply(
                source, output, opacity_threshold=0.5, ratio_threshold=2.0
            )
            result = PlyData.read(str(output))["vertex"].data

            self.assertEqual(
                stats,
                {
                    "input": 4,
                    "removed_opacity": 1,
                    "removed_ratio": 1,
                    "removed_max_length": 0,
                    "removed_distance": 0,
                    "removed": 2,
                    "output": 2,
                },
            )
            self.assertEqual(result["custom"].tolist(), [102, 103])

    def test_ratio_is_invariant_to_scale_field_order(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            source = directory / "input.ply"
            output = directory / "output.ply"
            rows = make_vertex()[:1]
            rows["scale_0"] = math.log(1.0)
            rows["scale_1"] = math.log(4.0)
            rows["scale_2"] = math.log(2.0)
            write_ply(source, rows)

            stats = final_cull.cull_ply(source, output, ratio_threshold=2.0)
            self.assertEqual(stats["output"], 1)

            stats = final_cull.cull_ply(source, output, ratio_threshold=2.1)
            self.assertEqual(stats["output"], 0)

    def test_omitted_thresholds_copy_all_properties_and_elements(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            source = directory / "curve_3dgs_init(origin).ply"
            output = directory / "curve_3dgs_init.ply"
            rows = make_vertex()
            write_ply(source, rows, text=True)

            stats = final_cull.cull_ply(source, output)
            copied = PlyData.read(str(output))
            self.assertEqual(stats["output"], len(rows))
            self.assertEqual(copied["vertex"].data.dtype, rows.dtype)
            np.testing.assert_array_equal(copied["vertex"].data, rows)
            self.assertIn("face", copied)
            self.assertEqual(copied.comments, ["file metadata"])
            self.assertEqual(copied.obj_info, ["test object"])
            self.assertEqual(copied["vertex"].comments, ["vertex metadata"])

    def test_max_length_cull_removes_both_three_sigma_tails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            source = directory / "input.ply"
            output = directory / "output.ply"
            rows = make_long_length_vertex()
            write_ply(source, rows)

            stats = final_cull.cull_ply(source, output, max_length_cull=True)
            result = PlyData.read(str(output))["vertex"].data

            self.assertEqual(stats["removed_max_length"], 2)
            self.assertEqual(stats["removed"], 2)
            self.assertEqual(stats["output"], 20)
            self.assertEqual(result["x"].tolist(), list(range(20)))

    def test_max_length_cull_is_disabled_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            source = directory / "input.ply"
            output = directory / "output.ply"
            rows = make_long_length_vertex()
            write_ply(source, rows)

            stats = final_cull.cull_ply(source, output)

            self.assertEqual(stats["removed_max_length"], 0)
            self.assertEqual(stats["output"], len(rows))

    def test_max_length_uses_all_axes_and_cli_flags(self) -> None:
        log_scales = np.zeros((21, 3), dtype=np.float64)
        log_scales[-1, 1] = math.log(2.0)
        mask = final_cull.max_length_remove_mask_from_log_scales(log_scales)
        expected = np.zeros(21, dtype=bool)
        expected[-1] = True
        np.testing.assert_array_equal(mask, expected)

        args = final_cull.build_parser().parse_args(
            ["--input", "input.ply", "--final_maxLength_cull"]
        )
        self.assertTrue(args.final_max_length_cull)
        args = final_cull.build_parser().parse_args(["--input", "input.ply"])
        self.assertFalse(args.final_max_length_cull)

        args = final_cull.build_parser().parse_args(
            ["--input", "input.ply", "-s", "/tmp/dataset", "--final_distance_cull", "5"]
        )
        self.assertEqual(args.source_path, Path("/tmp/dataset"))
        self.assertEqual(args.final_distance_cull, 5.0)

    def test_max_length_requires_finite_scale_fields_when_enabled(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            source = directory / "input.ply"
            output = directory / "output.ply"
            rows = np.empty(
                1,
                dtype=[("x", "f4"), ("scale_0", "f4"), ("scale_1", "f4")],
            )
            rows["x"] = 0
            rows["scale_0"] = 0
            rows["scale_1"] = 0
            write_ply(source, rows)
            with self.assertRaisesRegex(ValueError, "scale_2"):
                final_cull.cull_ply(source, output, max_length_cull=True)

            rows = np.empty(1, dtype=VERTEX_DTYPE)
            rows[:] = 0
            rows["scale_1"] = np.nan
            write_ply(source, rows)
            with self.assertRaisesRegex(ValueError, "scale_1"):
                final_cull.cull_ply(source, output, max_length_cull=True)

    def test_distance_cull_uses_nearest_camera_and_strict_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            source = directory / "input.ply"
            output = directory / "output.ply"
            rows = make_vertex()
            rows["x"] = [0.0, 3.0, 4.0, 10.0]
            rows["y"] = 0.0
            rows["z"] = 0.0
            write_ply(source, rows)
            (directory / "cameras.json").write_text(
                json.dumps(
                    [
                        {"position": [0.0, 0.0, 0.0]},
                        {"position": [10.0, 0.0, 0.0]},
                    ]
                ),
                encoding="utf-8",
            )

            stats = final_cull.cull_ply(source, output, distance_threshold=3.0)
            result = PlyData.read(str(output))["vertex"].data

            self.assertEqual(stats["removed_distance"], 1)
            self.assertEqual(stats["removed"], 1)
            self.assertEqual(result["x"].tolist(), [0.0, 3.0, 10.0])

    def test_distance_cull_with_colmap_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            source = directory / "input.ply"
            output = directory / "output.ply"
            rows = make_vertex()
            rows["x"] = [0.0, 3.0, 4.0, 10.0]
            rows["y"] = 0.0
            rows["z"] = 0.0
            write_ply(source, rows)

            sparse = directory / "sparse" / "0"
            sparse.mkdir(parents=True)
            (sparse / "images.txt").write_text(
                "# header\n"
                "1 1 0 0 0 0 0 0 1 image.png\n"
                "\n"
                "2 1 0 0 0 -10 0 0 1 image2.png\n"
                "\n",
                encoding="utf-8",
            )

            stats = final_cull.cull_ply(
                source,
                output,
                distance_threshold=3.0,
                source_path=directory,
            )
            result = PlyData.read(str(output))["vertex"].data

            self.assertEqual(stats["removed_distance"], 1)
            self.assertEqual(result["x"].tolist(), [0.0, 3.0, 10.0])

        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            source = directory / "input.ply"
            output = directory / "output.ply"
            rows = np.empty(1, dtype=[("custom", "f4")])
            rows["custom"] = 1.0
            write_ply(source, rows)

            stats = final_cull.cull_ply(source, output)

            self.assertEqual(stats["removed_distance"], 0)
            self.assertEqual(stats["output"], 1)

    def test_distance_cull_validates_threshold_camera_file_and_coordinates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            source = directory / "input.ply"
            output = directory / "output.ply"
            write_ply(source, make_vertex())

            with self.assertRaisesRegex(ValueError, "finite and greater than or equal to 0"):
                final_cull.cull_ply(source, output, distance_threshold=-1.0)
            with self.assertRaisesRegex(ValueError, "finite and greater than or equal to 0"):
                final_cull.cull_ply(source, output, distance_threshold=float("nan"))
            with self.assertRaisesRegex(ValueError, "Camera file not found"):
                final_cull.cull_ply(source, output, distance_threshold=1.0)

            (directory / "cameras.json").write_text("[]", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "non-empty list"):
                final_cull.cull_ply(source, output, distance_threshold=1.0)

            rows = np.empty(1, dtype=[("x", "f4"), ("y", "f4"), ("z", "f4")])
            rows["x"] = 0.0
            rows["y"] = 0.0
            rows["z"] = np.nan
            write_ply(source, rows)
            (directory / "cameras.json").write_text(
                json.dumps([{"position": [0.0, 0.0, 0.0]}]), encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "z.*NaN"):
                final_cull.cull_ply(source, output, distance_threshold=1.0)

    def test_default_output_name(self) -> None:
        self.assertEqual(
            final_cull.default_output_path(
                Path("/tmp/curve_3dgs_init(origin).ply")
            ),
            Path("/tmp/curve_3dgs_init.ply"),
        )
        self.assertEqual(
            final_cull.default_output_path(Path("/tmp/input.ply")),
            Path("/tmp/input_final_cull.ply"),
        )

    def test_distance_cull_combines_with_other_filters(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            source = directory / "input.ply"
            output = directory / "output.ply"
            rows = make_vertex()
            rows["x"] = [0.0, 1.0, 3.0, 10.0]
            rows["y"] = 0.0
            rows["z"] = 0.0
            write_ply(source, rows)
            (directory / "cameras.json").write_text(
                json.dumps([{"position": [0.0, 0.0, 0.0]}]), encoding="utf-8"
            )

            stats = final_cull.cull_ply(
                source,
                output,
                opacity_threshold=0.5,
                distance_threshold=2.0,
            )

            self.assertEqual(stats["removed_opacity"], 1)
            self.assertEqual(stats["removed_distance"], 2)
            self.assertEqual(stats["removed"], 3)
            self.assertEqual(stats["output"], 1)

    def test_validation_and_missing_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            source = directory / "input.ply"
            output = directory / "output.ply"
            write_ply(source, make_vertex())

            with self.assertRaisesRegex(ValueError, "greater than or equal to 1"):
                final_cull.cull_ply(source, output, ratio_threshold=0.5)
            with self.assertRaisesRegex(ValueError, "different files"):
                final_cull.cull_ply(source, source, opacity_threshold=0.5)

            rows = np.empty(1, dtype=[("x", "f4")])
            rows["x"] = 0
            write_ply(source, rows)
            with self.assertRaisesRegex(ValueError, "opacity"):
                final_cull.cull_ply(source, output, opacity_threshold=0.5)
            with self.assertRaisesRegex(ValueError, "scale_0"):
                final_cull.cull_ply(source, output, ratio_threshold=2.0)


if __name__ == "__main__":
    unittest.main()
