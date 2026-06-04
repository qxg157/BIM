"""Temporal alignment of multi-rate sensor streams.
Converts all timestamps to UTC via GNSS master clock,
aggregates 50Hz IMU to 1Hz windows (mean+std -> 12-dim)."""
import argparse, pathlib, struct
import numpy as np
import pandas as pd

GNSS_HZ, IMU_HZ, OBD_HZ = 1, 50, 1
IMU_AGG_STATS = ("mean", "std")
IMU_CHANNELS = ("ax", "ay", "az", "gx", "gy", "gz")

def aggregate_imu(raw: np.ndarray, window: int = IMU_HZ) -> np.ndarray:
    n_windows = len(raw) // window
    raw = raw[: n_windows * window].reshape(n_windows, window, -1)
    return np.concatenate([raw.mean(1), raw.std(1)], axis=-1)

def align_streams(gnss_df, imu_arr, obd_df, ref_epoch):
    gnss_df["ts_aligned"] = (gnss_df["ts_utc"] - ref_epoch).astype("int64") // 10**9
    obd_df["ts_aligned"] = (obd_df["ts_utc"] - ref_epoch).astype("int64") // 10**9
    imu_1hz = aggregate_imu(imu_arr)
    return gnss_df, imu_1hz, obd_df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--equipment-id", required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--data-root", type=pathlib.Path, default="sensor_raw")
    parser.add_argument("--out-dir", type=pathlib.Path, default="proc/aligned")
    args = parser.parse_args()
    # ... processing omitted for brevity
