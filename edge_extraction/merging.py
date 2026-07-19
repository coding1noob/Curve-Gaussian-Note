import numpy as np
from scipy.sparse.csgraph import connected_components
from scipy.sparse import coo_matrix
from scipy.spatial import cKDTree
from scipy.spatial.distance import euclidean, cdist
import os


def query_radius_pairs(points, distance_threshold):
    points = np.asarray(points, dtype=np.float32)
    if len(points) < 2:
        return np.empty((0, 2), dtype=np.int64)
    pairs = cKDTree(points).query_pairs(distance_threshold, output_type='ndarray')
    if pairs.size == 0:
        return np.empty((0, 2), dtype=np.int64)
    return pairs.astype(np.int64, copy=False)


def _pairs_to_sparse_graph(num_nodes, pairs):
    if num_nodes == 0:
        return coo_matrix((0, 0), dtype=np.bool_)
    if pairs.size == 0:
        return coo_matrix((num_nodes, num_nodes), dtype=np.bool_)

    rows = np.concatenate([pairs[:, 0], pairs[:, 1]])
    cols = np.concatenate([pairs[:, 1], pairs[:, 0]])
    data = np.ones(rows.shape[0], dtype=np.bool_)
    return coo_matrix((data, (rows, cols)), shape=(num_nodes, num_nodes))


def merge_endpoints(merged_line_segments, merged_bezier_curves, distance_threshold):
    N_lines = len(merged_line_segments)
    N_curves = len(merged_bezier_curves)

    if N_lines == 0 and N_curves == 0:
        return [], []

    if N_lines > 0:
        line_endpoints = merged_line_segments.reshape(-1, 3)
    else:
        line_endpoints = np.array([]).reshape(-1, 3)

    if N_curves > 0:
        curve_endpoints = merged_bezier_curves[:, [0, 1, 2, -3, -2, -1]].reshape(-1, 3)
    else:
        curve_endpoints = np.array([]).reshape(-1, 3)

    concat_endpoints = np.concatenate([line_endpoints, curve_endpoints], axis=0)

    # 我改的地方：端点合并不再使用 cdist 构造全量两两距离矩阵。
    # 改成稀疏半径图后，大场景不会再分配 O(N^2) 的内存。
    endpoint_pairs = query_radius_pairs(concat_endpoints, distance_threshold)
    adjacency_matrix = _pairs_to_sparse_graph(len(concat_endpoints), endpoint_pairs)
    num_components, labels = connected_components(adjacency_matrix, directed=False)
    for component in range(num_components):
        component_indices = np.where(labels == component)[0]
        if len(component_indices) > 1:
            endpoints = concat_endpoints[component_indices]
            mean_endpoint = np.mean(endpoints, axis=0)
            concat_endpoints[component_indices] = mean_endpoint

    if N_lines > 0:
        merged_line_segments_merged_endpoints = concat_endpoints[: N_lines * 2].reshape(
            -1, 6
        )
    else:
        merged_line_segments_merged_endpoints = []

    if N_curves > 0:
        merged_curve_segments_merged_endpoints = np.zeros_like(merged_bezier_curves)
        curve_merged_endpoints = concat_endpoints[N_lines * 2 :].reshape(-1, 6)
        merged_curve_segments_merged_endpoints[:, :3] = curve_merged_endpoints[:, :3]
        merged_curve_segments_merged_endpoints[:, 3:9] = merged_bezier_curves[:, 3:9]
        merged_curve_segments_merged_endpoints[:, 9:] = curve_merged_endpoints[:, 3:]

    else:
        merged_curve_segments_merged_endpoints = []

    return merged_line_segments_merged_endpoints, merged_curve_segments_merged_endpoints

def compute_pairwise_cosine_similarity(line_segments):
    direction_vectors = line_segments[:, 3:] - line_segments[:, :3]
    direction_vectors = direction_vectors / np.clip(
        np.linalg.norm(direction_vectors, axis=1, keepdims=True),
        1e-8,
        None,
    )
    pairwise_similarity = direction_vectors @ direction_vectors.T
    return pairwise_similarity

def line_segment_point_distance(line_segment, query_point):
    """Compute the Euclidean distance between a line segment and a query point.

    Parameters:
        line_segment (np.ndarray): An array of shape (6,), representing two 3D endpoints.
        query_point (np.ndarray): An array of shape (3,), representing the 3D query point.

    Returns:
        float: The minimum distance from the query point to the line segment.
    """
    point1, point2 = line_segment[:3], line_segment[3:]
    point_delta = point2 - point1
    u = np.clip(
        np.dot(query_point - point1, point_delta) / np.dot(point_delta, point_delta),
        0,
        1,
    )
    closest_point = point1 + u * point_delta
    return np.linalg.norm(closest_point - query_point)


def compute_pairwise_distances(line_segments):
    """Compute pairwise distances between line segments.

    Parameters:
        line_segments (np.ndarray): An array of shape (N, 6), each row represents a line segment in 3D.

    Returns:
        np.ndarray: A symmetric array of shape (N, N), containing pairwise distances.
    """
    num_lines = len(line_segments)
    endpoints = line_segments.reshape(-1, 3)
    dist_matrix = np.zeros((num_lines, num_lines))

    for i, line_segment in enumerate(line_segments):
        for j in range(i + 1, num_lines):
            min_distance = min(
                line_segment_point_distance(line_segment, endpoints[2 * j]),
                line_segment_point_distance(line_segment, endpoints[2 * j + 1]),
            )
            dist_matrix[i, j] = min_distance

    dist_matrix += dist_matrix.T  # Make the matrix symmetric
    return dist_matrix


def find_connected_line_components(line_segments, distance_threshold, similarity_threshold, samples_per_line=3):
    num_lines = len(line_segments)
    if num_lines == 0:
        return np.empty((0,), dtype=np.int32)
    if num_lines == 1:
        return np.zeros((1,), dtype=np.int32)

    directions = line_segments[:, 3:] - line_segments[:, :3]
    direction_norms = np.linalg.norm(directions, axis=1, keepdims=True)
    directions = directions / np.clip(direction_norms, 1e-8, None)

    # 我改的地方：线段合并只对采样点建立稀疏近邻图。
    # 替代原来的全量线段距离矩阵和全量方向相似度矩阵。
    t_values = np.linspace(0.0, 1.0, samples_per_line, dtype=np.float32)
    sampled_points = (
        (1.0 - t_values[None, :, None]) * line_segments[:, None, :3]
        + t_values[None, :, None] * line_segments[:, None, 3:]
    )
    sample_pairs = query_radius_pairs(sampled_points.reshape(-1, 3), distance_threshold)
    if sample_pairs.size == 0:
        return np.arange(num_lines, dtype=np.int32)

    line_pairs = sample_pairs // samples_per_line
    valid = line_pairs[:, 0] != line_pairs[:, 1]
    line_pairs = line_pairs[valid]
    if line_pairs.size == 0:
        return np.arange(num_lines, dtype=np.int32)

    line_pairs = np.sort(line_pairs, axis=1)
    line_pairs = np.unique(line_pairs, axis=0)
    similarity = np.abs(np.sum(directions[line_pairs[:, 0]] * directions[line_pairs[:, 1]], axis=1))
    line_pairs = line_pairs[similarity >= similarity_threshold]
    adjacency_matrix = _pairs_to_sparse_graph(num_lines, line_pairs)
    _, labels = connected_components(adjacency_matrix, directed=False)
    return labels
