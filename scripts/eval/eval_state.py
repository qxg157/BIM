"""Evaluate equipment state recognition: accuracy, macro P/R/F1, confusion."""
import argparse, json
import numpy as np
from sklearn.metrics import (accuracy_score, precision_recall_fscore_support,
                             confusion_matrix)

STATE_NAMES = ["idle", "travel_loaded", "travel_empty", "excavating",
               "dumping", "spreading", "compacting"]

def evaluate(y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    p, r, f1, _ = precision_recall_fscore_support(y_true, y_pred, average="macro")
    cm = confusion_matrix(y_true, y_pred, normalize="true")
    return {"accuracy": acc, "macro_precision": p, "macro_recall": r,
            "macro_f1": f1, "confusion_matrix": cm.tolist()}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pred-file", required=True)
    parser.add_argument("--label-file", required=True)
    parser.add_argument("--out-dir", default="results/state_recog")
    args = parser.parse_args()
