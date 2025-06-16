# ofi/loader.py
import pandas as pd

class Loader:
    """CSV → tidy DataFrame loader."""

    def __init__(self, path: str) -> None:
        self.path = path

    def load_raw(self) -> pd.DataFrame:
        """Return dataframe with columns:
        timestamp (ns), level, price, size, side ('bid'/'ask').
        """
        df = pd.read_csv(self.path)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ns")
        #  infer side from +/- sign convention or explicit column
        df["side"] = df["side"].map({0: "bid", 1: "ask"})
        return df
