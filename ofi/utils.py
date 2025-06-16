# ofi/utils.py
from __future__ import annotations

import pandas as pd
from sklearn.decomposition import PCA


def align_clock(series, freq="1s"):
    """Convenience wrapper: outer-join resample + ffill zeros."""
    return series.resample(freq).sum().fillna(0)


def rolling_pca(mat: pd.DataFrame, *, window: int = 10_000) -> PCA:
    """Fit a 1-factor PCA on the most-recent *window* rows."""
    if len(mat) < window:
        window = len(mat)
    pca = PCA(n_components=1).fit(mat.iloc[-window:])
    return pca
