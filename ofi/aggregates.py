# ofi/aggregates.py
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA


def _signed(df: pd.DataFrame) -> pd.Series:
    """Vectorised helper: +bid events, -ask events."""
    return df["delta_q"].where(df["side"] == "bid", -df["delta_q"])


def best_level_ofi(incr: pd.DataFrame, freq: str = "1s") -> pd.Series:
    """Aggregate signed size deltas at level 1 into a time-series."""
    return (
        incr.query("level == 1")
        .assign(s=_signed)
        .groupby(pd.Grouper(key="timestamp", freq=freq), observed=True)
        .s.sum()
        .rename("ofi_best")
    )


def multi_level_vector(
    incr: pd.DataFrame, *, depth: int = 10, freq: str = "1s"
) -> pd.DataFrame:
    """Return a matrix (time × level) of OFI for the first *depth* levels."""
    mat = (
        incr.query("level <= @depth")
        .assign(s=_signed)
        .groupby(
            [pd.Grouper(key="timestamp", freq=freq), "level"], observed=True
        )
        .s.sum()
        .unstack(fill_value=0)
        .add_prefix("ofi_")
        .sort_index(axis=1)
    )
    return mat


def integrated_ofi(vec: pd.DataFrame, *, pca: PCA | None = None) -> pd.Series:
    """Scalar ‘integrated’ OFI = first PC of multi-level vector."""
    if pca is None:
        pca = PCA(n_components=1).fit(vec)
    w = pca.components_[0]
    w /= np.abs(w).sum()
    return vec.mul(w, axis=1).sum(axis=1).rename("ofi_int")


def cross_asset_panel(ofi_dict: dict[str, pd.Series]):
    """Stack multiple single-stock series into an xarray 3-D panel."""
    import xarray as xr

    aligned = xr.Dataset(
        {k: (("time",), s) for k, s in ofi_dict.items()}
    ).to_array("stock")
    return aligned  # dims: (stock, time)
