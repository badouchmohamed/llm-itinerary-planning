"""
Generate bar plots with error bars for Figures 1 & 2.

Usage:
  python analysis/plots.py --input data/user_study_logs.csv --outdir figures/
"""

import argparse
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def _agg(df, metric):
    g = df.groupby("interface")[metric].agg(["mean", "std"]).reindex(["conversational","form","hybrid"])
    return g

def bar_with_error(ax, agg_df, title, ylabel):
    x = np.arange(len(agg_df))
    ax.bar(x, agg_df["mean"].values, yerr=agg_df["std"].values, capsize=5)
    ax.set_xticks(x)
    ax.set_xticklabels(agg_df.index.str.capitalize())
    ax.set_ylabel(ylabel)
    ax.set_title(title)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--outdir", default="figures")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    df = pd.read_csv(args.input)

    # Figure 1: SUS and NASA-TLX
    fig1, axes1 = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
    agg_sus = _agg(df, "SUS")
    agg_tlx = _agg(df, "NASA_TLX")
    bar_with_error(axes1[0], agg_sus, "SUS (0–100)", "Score")
    bar_with_error(axes1[1], agg_tlx, "NASA-TLX (0–100)", "Score")
    fig1.suptitle("Usability and Cognitive Load Across Interfaces")
    f1_path = os.path.join(args.outdir, "figure1_sus_tlx.png")
    fig1.savefig(f1_path, dpi=300)
    print(f"Saved {f1_path}")

    # Figure 2: Time, Iterations, Satisfaction
    fig2, axes2 = plt.subplots(1, 3, figsize=(14, 4), constrained_layout=True)
    agg_time = _agg(df, "time_min")
    agg_iter = _agg(df, "iterations")
    agg_sat = _agg(df, "satisfaction")
    bar_with_error(axes2[0], agg_time, "Completion Time (min)", "Minutes")
    bar_with_error(axes2[1], agg_iter, "Iterations (#)", "#")
    bar_with_error(axes2[2], agg_sat, "Satisfaction (1–5)", "Rating")
    fig2.suptitle("Efficiency and Satisfaction Across Interfaces")
    f2_path = os.path.join(args.outdir, "figure2_efficiency_satisfaction.png")
    fig2.savefig(f2_path, dpi=300)
    print(f"Saved {f2_path}")

if __name__ == "__main__":
    main()
