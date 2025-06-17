#!/usr/bin/env python
"""
Build a cross-asset OFI panel and run Lasso to estimate cross-impact
(loadings for each target stock).

Assumes each ticker has its own CSV in a directory.

Usage
-----
python scripts/build_cross_asset_ofi.py \
       --dir data/raw/ \
       --freq 30s \
       --out  features/ofi_panel.nc
"""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import xarray as xr
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler

from ofi import Loader, compute_increments, best_level_ofi, cross_asset_panel


def build_panel(csv_dir: Path, freq: str, colmap: dict[str, str]):
    series = {}
    for csv in csv_dir.glob("*.csv"):
        ticker = csv.stem.upper().split("_")[0]  # e.g. AAPL_20240527.csv
        snap = Loader(csv, colmap=colmap).load_raw()
        incr = compute_increments(snap)
        series[ticker] = best_level_ofi(incr, freq=freq)
    return cross_asset_panel(series)  # xarray DataArray


def estimate_cross_impact(panel: xr.DataArray, alpha_grid=None):
    alphas = alpha_grid or np.logspace(-4, 0, 20)
    results = {}
    scaler = StandardScaler()

    for target in panel.stock.values:
        y = panel.sel(stock=target).to_pandas()
        X = panel.drop_sel(stock=target).to_pandas().T
        df = pd.concat({"y": y, **{c: X[c] for c in X.columns}}, axis=1).dropna()
        y_vec = df.pop("y").values
        X_mat = scaler.fit_transform(df)

        model = LassoCV(alphas=alphas, cv=5, n_jobs=-1).fit(X_mat, y_vec)
        results[target] = pd.Series(model.coef_, index=df.columns)
    return xr.DataArray(pd.DataFrame(results).T)  # stocks × predictors


def main(cfg):
    colmap = dict(item.split("=", 1) for item in cfg.colmap.split(",") if item)
    panel  = build_panel(cfg.dir, cfg.freq, colmap)
    cfg.out.parent.mkdir(parents=True, exist_ok=True)
    panel.to_netcdf(cfg.out)
    print(f" panel saved → {cfg.out}")

    if cfg.lasso:
        weights = estimate_cross_impact(panel)
        weights.to_netcdf(cfg.out.with_name("lasso_loadings.nc"))
        print(" Lasso loadings written")


if __name__ == "__main__":
    pa = argparse.ArgumentParser()
    pa.add_argument("--dir", type=Path, required=True, help="directory of CSVs")
    pa.add_argument("--freq", default="30s", help="resample horizon")
    pa.add_argument("--out", type=Path, required=True, help="output NetCDF path")
    pa.add_argument("--lasso", action="store_true", help="fit cross-impact Lasso")
    pa.add_argument("--colmap", default="",
                help="comma-sep rename, e.g. timestamp=ts_event,level=depth")
    main(pa.parse_args())
