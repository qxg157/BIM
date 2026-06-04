"""Run CMOEO fleet dispatch optimization and evaluate vs baselines."""
import argparse, json
import numpy as np
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.optimize import minimize

def build_problem(n_equip, n_zones, current_state):
    """Construct constrained MO problem from current fleet state."""
    pass  # see configs/optim/cmoeo_params.json

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/optim/cmoeo_params.json")
    parser.add_argument("--state-file", required=True)
    parser.add_argument("--bim-dir", default="bim")
    parser.add_argument("--out-dir", default="optim/dispatch_plans")
    args = parser.parse_args()
