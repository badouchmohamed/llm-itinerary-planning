"""
Generate sentence embeddings for activities and queries using all-MiniLM-L6-v2.

Usage:
  python embeddings/generate_embeddings.py --input data/travel_activities.csv --text_col description \
      --id_col activity_id --out embeddings/activities_embeddings.npy --out_index embeddings/activities_index.csv
"""

import argparse
import numpy as np
import pandas as pd
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="CSV with activity metadata")
    ap.add_argument("--text_col", default="description")
    ap.add_argument("--id_col", default="activity_id")
    ap.add_argument("--out", required=True, help="Output .npy file for embeddings")
    ap.add_argument("--out_index", required=True, help="Output CSV with id -> row mapping")
    args = ap.parse_args()

    df = pd.read_csv(args.input)
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    texts = df[args.text_col].fillna("").astype(str).tolist()
    vecs = model.encode(texts, batch_size=128, show_progress_bar=True, normalize_embeddings=True)
    np.save(args.out, vecs)
    pd.DataFrame({args.id_col: df[args.id_col], "row": range(len(df))}).to_csv(args.out_index, index=False)
    print(f"Saved {len(df)} embeddings -> {args.out}")

if __name__ == "__main__":
    main()
