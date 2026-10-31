import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import numpy as np
from plyfile import PlyData, PlyElement

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import view_filled_ply as viewer


class FilledPlyTests(unittest.TestCase):
    def test_radius_filters_both_clouds_and_keeps_boundary(self):
        original = np.array([[-2., 0, 0], [0, 0, 0], [2, 0, 0]])
        filled = np.array([[0., 0, 0], [0, 1, 0], [0, 0, 2]])
        mask = viewer.find_added_points(original, filled, 1e-6)
        black, clipped, added, center = viewer.filter_display_radius(
            original, filled, mask, 1.0)
        np.testing.assert_array_equal(center, [0, 0, 0])
        np.testing.assert_array_equal(black, [[0, 0, 0]])
        np.testing.assert_array_equal(clipped, [[0, 0, 0], [0, 1, 0]])
        np.testing.assert_array_equal(added, [False, True])

    def test_custom_center_can_leave_only_added_points_or_nothing(self):
        original = np.array([[0., 0, 0]])
        filled = np.array([[0., 0, 0], [5, 0, 0]])
        mask = np.array([False, True])
        black, clipped, added, _ = viewer.filter_display_radius(
            original, filled, mask, 0.5, [5, 0, 0])
        self.assertEqual(black.shape, (0, 3))
        np.testing.assert_array_equal(clipped, [[5, 0, 0]])
        np.testing.assert_array_equal(added, [True])
        black, clipped, added, _ = viewer.filter_display_radius(
            original, filled, mask, 0.5, [10, 0, 0])
        self.assertEqual(len(black) + len(clipped) + len(added), 0)
        output = io.StringIO()
        with redirect_stdout(output):
            viewer.run_viewer(black, clipped, added, None)
        self.assertIn("No visible points remain", output.getvalue())

    def test_radius_preserves_labels_near_boundary(self):
        original = np.array([[1.0000001, 0, 0]])
        filled = np.array([[1., 0, 0]])
        mask = viewer.find_added_points(original, filled, 1e-6)
        black, _, added, _ = viewer.filter_display_radius(
            original, filled, mask, 1.0, [0, 0, 0])
        self.assertEqual(len(black), 0)
        np.testing.assert_array_equal(added, [False])

    def test_invalid_radius_arguments(self):
        for options in (["--radius", "0"], ["--radius", "-1"],
                        ["--radius", "nan"], ["--radius", "inf"],
                        ["--center", "0", "0", "0"],
                        ["--radius", "1", "--center", "nan", "0", "0"]):
            with self.subTest(options=options), redirect_stdout(io.StringIO()):
                with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as exc:
                    viewer.main(options)
                self.assertEqual(exc.exception.code, 2)

    def test_filtered_and_reordered_original_points(self):
        original = np.array([[0, 0, 0], [1, 0, 0], [2, 0, 0]])
        filled = np.array([[2, 0, 0], [3, 0, 0], [0, 0, 0]])
        np.testing.assert_array_equal(
            viewer.find_added_points(original, filled, 1e-6), [False, True, False])

    def test_tolerance_and_coincident_points(self):
        original = np.array([[0, 0, 0]])
        filled = np.array([[0, 0, 0], [1e-7, 0, 0], [1e-4, 0, 0]])
        np.testing.assert_array_equal(
            viewer.find_added_points(original, filled, 1e-6), [False, False, True])
        np.testing.assert_array_equal(
            viewer.find_added_points(original, filled, 0), [False, True, True])

    def test_invalid_tolerance(self):
        points = np.zeros((1, 3))
        for tolerance in (-1, np.nan, np.inf):
            with self.assertRaises(ValueError):
                viewer.find_added_points(points, points, tolerance)

    def test_read_and_no_gui_do_not_modify_files(self):
        with tempfile.TemporaryDirectory() as directory:
            paths = [Path(directory) / name for name in ("input.ply", "input_filled.ply")]
            for path, count in zip(paths, (2, 3)):
                rows = np.zeros(count, dtype=[("x", "f4"), ("y", "f4"), ("z", "f4")])
                rows["x"] = np.arange(count)
                PlyData([PlyElement.describe(rows, "vertex")], text=count == 2).write(str(path))
            before = [path.read_bytes() for path in paths]
            np.testing.assert_array_equal(viewer.load_points(paths[0]), [[0, 0, 0], [1, 0, 0]])
            self.assertEqual(viewer.main([directory, "--no-gui"]), 0)
            self.assertEqual(before, [path.read_bytes() for path in paths])

    def test_nonfinite_points_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.ply"
            rows = np.array([(np.nan, 0, 0)], dtype=[("x", "f4"), ("y", "f4"), ("z", "f4")])
            PlyData([PlyElement.describe(rows, "vertex")]).write(str(path))
            with self.assertRaises(ValueError):
                viewer.load_points(path)

    def test_merged_counts_keep_original_points_missing_from_filled(self):
        with tempfile.TemporaryDirectory() as directory:
            for name, coordinates in (("input.ply", [0, 1, 2]),
                                      ("input_filled.ply", [2, 3])):
                rows = np.zeros(len(coordinates),
                                dtype=[("x", "f4"), ("y", "f4"), ("z", "f4")])
                rows["x"] = coordinates
                PlyData([PlyElement.describe(rows, "vertex")]).write(
                    str(Path(directory) / name))
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(viewer.main([directory, "--no-gui"]), 0)
            self.assertIn("Merged display (original + filled): 3 black / 1 red",
                          output.getvalue())
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(viewer.main([
                    directory, "--no-gui", "--radius", "1", "--center", "2", "0", "0",
                ]), 0)
            self.assertIn("Merged display (original + filled): 2 black / 1 red",
                          output.getvalue())


if __name__ == "__main__":
    unittest.main()
