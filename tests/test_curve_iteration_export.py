"""Test snapshot export without importing the CUDA training/rasterizer stack."""

import ast
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import Mock

import numpy as np
from plyfile import PlyData, PlyElement
import torch


def load_export_functions():
    source = Path(__file__).resolve().parents[1] / "train.py"
    tree = ast.parse(source.read_text())
    names = {"_inverse_sigmoid_np", "save_curve_gaussians_for_3dgs_note",
             "save_iteration_curve_ply"}
    functions = [node for node in tree.body
                 if isinstance(node, ast.FunctionDef) and node.name in names]
    namespace = dict(os=os, shutil=shutil, torch=torch, np=np,
                     PlyData=PlyData, PlyElement=PlyElement,
                     RGB2SH=lambda rgb: (rgb - 0.5) / 0.28209479177387814)
    exec(compile(ast.Module(body=functions, type_ignores=[]), str(source), "exec"), namespace)
    return namespace


class IterationExportTests(unittest.TestCase):
    def test_intermediate_snapshot_refreshes_geometry_and_exports_standard_ply(self):
        functions = load_export_functions()
        model = Mock()
        model.get_xyz = torch.tensor([[1., 2., 3.], [4., 5., 6.]])
        model.get_rgb = torch.tensor([[0.2], [0.8]])
        model.get_opacity = torch.tensor([[0.1], [0.9]])
        model.get_scaling = torch.ones(2, 3) * 0.03
        model.get_rotation = torch.tensor([[1., 0., 0., 0.]]).repeat(2, 1)
        with tempfile.TemporaryDirectory() as directory:
            path = functions["save_iteration_curve_ply"](model, directory, 500)
            self.assertEqual(Path(path).name, "curve_3dgs_init_iter_500.ply")
            model.prepare_scaling_rot.assert_called_once_with()
            rows = PlyData.read(path)["vertex"].data
            self.assertEqual(len(rows), 2)
            self.assertTrue({"f_dc_0", "f_rest_44", "opacity", "scale_2", "rot_3"}
                            .issubset(rows.dtype.names))
            np.testing.assert_allclose(rows["scale_0"], np.log(0.03))
            np.testing.assert_allclose(rows["x"], [1, 4])
            np.testing.assert_allclose(rows["opacity"], np.log([0.1 / 0.9, 0.9 / 0.1]),
                                       rtol=1e-6)

    def test_final_snapshot_is_exact_copy_without_reexport_or_model_mutation(self):
        functions = load_export_functions()
        exporter = Mock()
        functions["save_curve_gaussians_for_3dgs_note"] = exporter
        model = Mock()
        with tempfile.TemporaryDirectory() as directory:
            final = Path(directory) / "curve_3dgs_init.ply"
            final.write_bytes(b"already culled final PLY")
            path = functions["save_iteration_curve_ply"](
                model, directory, 30000, final_ply=str(final))
            self.assertEqual(Path(path).read_bytes(), final.read_bytes())
            exporter.assert_not_called()
            model.prepare_scaling_rot.assert_not_called()

    def test_iteration_filenames_do_not_overwrite_each_other(self):
        functions = load_export_functions()
        with tempfile.TemporaryDirectory() as directory:
            final = Path(directory) / "curve_3dgs_init.ply"
            paths = []
            for iteration in (1, 500, 2000, 5000, 10000, 30000):
                final.write_bytes(str(iteration).encode())
                paths.append(functions["save_iteration_curve_ply"](
                    None, directory, iteration, final_ply=str(final)))
            self.assertEqual(len(set(paths)), 6)
            self.assertEqual(Path(paths[0]).read_bytes(), b"1")
            self.assertEqual(Path(paths[-1]).read_bytes(), b"30000")


if __name__ == "__main__":
    unittest.main()
