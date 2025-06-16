#!/usr/bin/env python
"""
Compute Best-, Multi-, and Integrated-level OFI for a single stock.

Usage
-----
python scripts/build_single_stock_ofi.py \
       --csv data/first_25000_rows.csv \
       --freq 1s \
       --depth 10 \
       --out  features/ofi_single.parquet
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sklearn.decomposition import PCA

from ofi import (
    Loader,
    compute_increments,
    best_level_ofi,
    multi_level_vector,
    integrated_ofi,
)


def main(cfg):
    # 1) read
    colmap = dict(item.split("=", 1) for item in cfg.colmap.split(",") if item)
    snap = Loader(cfg.csv, colmap=colmap).load_raw()
    incr = compute_increments(snap)

    # 2) build features
    ofi_best = best_level_ofi(incr, freq=cfg.freq)
    ofi_vec = multi_level_vector(incr, depth=cfg.depth, freq=cfg.freq)

    # fit PCA on entire sample (or adapt to rolling)
    pca = PCA(n_components=1).fit(ofi_vec)
    ofi_int = integrated_ofi(ofi_vec, pca=pca)

    # 3) merge and write
    feats = pd.concat([ofi_best, ofi_int, ofi_vec], axis=1)
    cfg.out.parent.mkdir(parents=True, exist_ok=True)
    feats.to_parquet(cfg.out, compression="snappy")
    print(f"✅ wrote {len(feats):,} rows → {cfg.out}")


if __name__ == "__main__":
    pa = argparse.ArgumentParser()
    pa.add_argument("--colmap", type=str, default="",
                help="comma-sep rename e.g. ts_event=timestamp,depth=level")
    pa.add_argument("--csv", type=Path, required=True, help="input snapshot CSV")
    pa.add_argument("--timecol", default="timestamp",
                help="column name holding nanosecond epoch timestamps")
    pa.add_argument("--freq", default="1s", help="resampling horizon")
    pa.add_argument("--depth", type=int, default=10, help="LOB levels")
    pa.add_argument("--out", type=Path, required=True, help="output file")
    main(pa.parse_args())
