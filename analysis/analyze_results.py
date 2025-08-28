"""
Compute one-way ANOVA for each metric (SUS, NASA_TLX, time_min, iterations, satisfaction).

Expected CSV: data/user_study_logs.csv with columns:
  participant_id, interface (conversational|form|hybrid), SUS, NASA_TLX, time_min, iterations, satisfaction

Usage:
  python analysis/analyze_results.py --input data/user_study_logs.csv
"""

import argparse
import pandas as pd
import numpy as np
from scipy import stats

def anova_report(df, metric):
    groups = [g[metric].dropna().values for _, g in df.groupby("interface")]
    labels = list(df.groupby("interface").groups.keys())
    F, p = stats.f_oneway(*groups)
    # Degrees of freedom for one-way ANOVA:
    k = len(groups)
    n_total = sum(len(g) for g in groups)
    df1 = k - 1
    df2 = n_total - k
    means = {lab: float(np.mean(g)) for lab, g in zip(labels, groups)}
    sds = {lab: float(np.std(g, ddof=1)) for lab, g in zip(labels, groups)}
    return {"metric": metric, "F": F, "df1": df1, "df2": df2, "p": p, "means": means, "sds": sds}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out_csv", default="analysis/anova_results.csv")
    args = ap.parse_args()

    df = pd.read_csv(args.input)
    results = []
    for metric in ["SUS", "NASA_TLX", "time_min", "iterations", "satisfaction"]:
        res = anova_report(df, metric)
        results.append(res)
        print(f"{metric}: F({res['df1']},{res['df2']}) = {res['F']:.2f}, p = {res['p']:.4g}")
        print("  Means ± SD:")
        for lab in sorted(res["means"].keys()):
            print(f"   - {lab}: {res['means'][lab]:.2f} ± {res['sds'][lab]:.2f}")
    # Save flat CSV
    flat = []
    for r in results:
        row = {"metric": r["metric"], "F": r["F"], "df": f"{r['df1']},{r['df2']}", "p": r["p"]}
        for lab, m in r["means"].items():
            row[f"mean_{lab}"] = m
        for lab, s in r["sds"].items():
            row[f"sd_{lab}"] = s
        flat.append(row)
    pd.DataFrame(flat).to_csv(args.out_csv, index=False)
    print(f"\nSaved ANOVA table -> {args.out_csv}")

if __name__ == "__main__":
    main()
