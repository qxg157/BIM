"""Spatial registration: WGS84 -> UTM -> BIM local engineering coords.
Uses pre-calibrated R,t from calib/<eid>_spatial.json."""
import json, argparse, pathlib
import numpy as np

def wgs84_to_utm(lat, lon, zone=49):
    """Simplified UTM projection (zone 49N for central China)."""
    import pyproj
    proj = pyproj.Proj(proj="utm", zone=zone, ellps="WGS84")
    return proj(lon, lat)

def apply_rigid(pts, R, t):
    return (np.array(R) @ pts.T).T + np.array(t)

def register(gnss_df, calib_path):
    with open(calib_path) as f:
        cal = json.load(f)
    utm_coords = np.array([wgs84_to_utm(r.lat, r.lon) + (r.alt_m,)
                           for r in gnss_df.itertuples()])
    return apply_rigid(utm_coords, cal["R"], cal["t"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--equipment-id", required=True)
    parser.add_argument("--date", required=True)
    args = parser.parse_args()
