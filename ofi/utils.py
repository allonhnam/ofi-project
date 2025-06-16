# ofi/utils.py
import pandas as pd
from sklearn.decomposition import PCA

def align_clock(df, freq="1s"):
    """Outer-join resample, fill missing with zeros."""
    return df.resample(freq).sum().fillna(0)

def rolling_pca(mat: pd.DataFrame, window: int = 500) -> PCA:
    pca = PCA(n_components=1)
    pca.fit(mat.iloc[:window])
    return pca
