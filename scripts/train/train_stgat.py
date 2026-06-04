"""ST-GAT training script with joint classification + productivity loss."""
import json, argparse, os, time
import torch
import torch.nn as nn
from torch_geometric.data import DataLoader
# from models.stgat import STGAT  # internal module

def weighted_ce(logits, targets, class_weights):
    return nn.functional.cross_entropy(logits, targets, weight=class_weights)

def smooth_l1(pred, target, beta=1.0):
    return nn.functional.smooth_l1_loss(pred, target, beta=beta)

def joint_loss(cls_logits, cls_targets, prod_pred, prod_target,
               class_weights, lam=0.3):
    return weighted_ce(cls_logits, cls_targets, class_weights) + \
           lam * smooth_l1(prod_pred, prod_target)

def train_epoch(model, loader, optimizer, class_weights, lam, device):
    model.train()
    total = 0.0
    for batch in loader:
        batch = batch.to(device)
        cls_out, prod_out = model(batch)
        loss = joint_loss(cls_out, batch.y, prod_out, batch.prod,
                         class_weights, lam)
        optimizer.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        total += loss.item() * batch.num_graphs
    return total / len(loader.dataset)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="models/stgat/hparams.json")
    parser.add_argument("--data-dir", default="proc/graph_snap")
    parser.add_argument("--label-file", default="proc/labels/annotation_index.csv")
    parser.add_argument("--ckpt-dir", default="models/stgat/ckpt")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", default="cuda:0")
    args = parser.parse_args()
