"""Baseline model training: LSTM, TCN, Transformer, GCN."""
import argparse, json
import torch

BASELINES = {
    "lstm": "models/baselines/lstm/config.json",
    "tcn": "models/baselines/tcn/config.json",
    "transformer": "models/baselines/transformer/config.json",
    "gcn": "models/baselines/gcn/config.json",
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=list(BASELINES.keys()), required=True)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
