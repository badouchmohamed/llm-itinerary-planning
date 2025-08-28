"""
Re-rank activities using the weighted scoring algorithm (Eq. 2).

score = α * sim + β * f(dwell) + γ * g(click)
where:
  sim in [0,1] (cosine similarity),
  f(dwell) = min(dwell / T0, 1.0), with T0=10s (median from pilot),
  g(click) ∈ {0,1} or normalized click rate.

Usage:
  python models/rerank.py --activities data/travel_activities.csv --logs data/user_study_logs.csv \
      --alpha 0.6 --beta 0.3 --gamma 0.1 --top_k 10
"""

import argparse
import pandas as pd
import numpy as np

def normalize_dwell(dwell_sec: float, T0: float = 10.0) -> float:
    return float(min(max(dwell_sec / T0, 0.0), 1.0))

def rerank(activities_df, logs_df, alpha=0.6, beta=0.3, gamma=0.1, top_k=10):
    # Expected columns:
    # activities_df: activity_id, title, sim (0..1)
    # logs_df: activity_id, dwell_sec, clicked (0/1)
    logs_agg = logs_df.groupby("activity_id").agg(
        dwell_sec=("dwell_sec", "mean"),
        click=("clicked", "max")
    ).reset_index()
    df = activities_df.merge(logs_agg, on="activity_id", how="left")
    df["dwell_sec"] = df["dwell_sec"].fillna(0.0)
    df["click"] = df["click"].fillna(0.0)
    df["f_dwell"] = df["dwell_sec"].apply(normalize_dwell)
    df["g_click"] = df["click"].astype(float)
    df["score"] = alpha * df["sim"] + beta * df["f_dwell"] + gamma * df["g_click"]
    df = df.sort_values("score", ascending=False)
    return df.head(top_k)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--activities", required=True, help="CSV with activity_id,title,sim")
    ap.add_argument("--logs", required=True, help="CSV with activity_id,dwell_sec,clicked")
    ap.add_argument("--alpha", type=float, default=0.6)
    ap.add_argument("--beta", type=float, default=0.3)
    ap.add_argument("--gamma", type=float, default=0.1)
    ap.add_argument("--top_k", type=int, default=10)
    args = ap.parse_args()

    activities = pd.read_csv(args.activities)
    logs = pd.read_csv(args.logs)
    top = rerank(activities, logs, args.alpha, args.beta, args.gamma, args.top_k)
    print(top[["activity_id", "title", "sim", "f_dwell", "g_click", "score"]].to_string(index=False))

if __name__ == "__main__":
    main()
