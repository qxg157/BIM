"""Dynamic fleet graph construction at each timestep.
Edge criteria: distance <= rho AND zone adjacency <= 1."""
import json, argparse
import numpy as np
from scipy.spatial.distance import pdist, squareform

def build_graph_t(positions, zones, rho=100.0):
    N = len(positions)
    D = squareform(pdist(positions))
    dist_mask = D <= rho
    zone_mask = np.abs(zones[:, None] - zones[None, :]) <= 1
    adj = dist_mask & zone_mask
    np.fill_diagonal(adj, False)
    edges = np.argwhere(adj)
    weights = 1.0 / (D[edges[:, 0], edges[:, 1]] + 1e-6)
    return edges, weights

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fused-dir", default="proc/fused")
    parser.add_argument("--rho", type=float, default=100.0)
    parser.add_argument("--out-dir", default="proc/graph_snap")
    args = parser.parse_args()
