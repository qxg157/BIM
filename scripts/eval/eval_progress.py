"""Evaluate volumetric progress quantification against survey ground truth."""
import argparse
import numpy as np
import pandas as pd

def volume_metrics(auto, survey):
    ae = np.abs(auto - survey)
    ape = ae / np.maximum(np.abs(survey), 1.0) * 100
    return {"MAE_m3": ae.mean(), "RMSE_m3": np.sqrt((ae**2).mean()),
            "MAPE_pct": ape.mean(), "MaxError_pct": ape.max()}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--auto-dir", default="proc/pcl_diff")
    parser.add_argument("--survey-dir", required=True)
    parser.add_argument("--out-dir", default="results/progress")
    args = parser.parse_args()
