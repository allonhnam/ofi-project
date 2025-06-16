# ofi/aggregates.py
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

def _signed(df: pd.DataFrame) -> pd.Series:
    return df["delta_q"].where(df["side"] == "bid", -df["delta_q"])

def best_level_ofi(incr: pd.DataFrame, freq: str = "1s") -> pd.Series:
    return (
        incr.query("level == 1")
        .assign(s=_signed)
        .groupby(pd.Grouper(key="timestamp", freq=freq))
        .s.sum()
        .rename("ofi_best")
    )

def multi_level_vector(incr: pd.DataFrame, M: int = 10, freq: str = "1s") -> pd.DataFrame:
    vec = (
        incr.query("level <= @M")
        .assign(s=_signed)
        .groupby([pd.Grouper(key="timestamp", freq=freq), "level"])
        .s.sum()
        .unstack(fill_value=0)
        .add_prefix("ofi_")
    )
    return vec

def integrated_ofi(vec: pd.DataFrame, pca: PCA) -> pd.Series:
    w = pca.components_[0]
    w = w / np.abs(w).sum()
    return vec.mul(w, axis=1).sum(axis=1).rename("ofi_int")

def cross_asset_panel(ofi_series_dict: dict) -> "xarray.DataArray":
    """Collect multiple stock series into a 3-D panel."""
    import xarray as xr
    aligned = xr.concat(
        [xr.DataArray(s, dims=("time")) for s in ofi_series_dict.values()],
        dim="stock",
    )
    aligned.coords["stock"] = list(ofi_series_dict.keys())
    return aligned
