# ofi/loader.py
from __future__ import annotations
import pandas as pd

class Loader:
    """
    Flexible CSV → DataFrame reader.

    Parameters
    ----------
    path      : CSV file
    tz        : timezone for display (optional)
    colmap    : dict that maps *your* column names to
                ['timestamp', 'level', 'side', 'price', 'size']
                e.g.  {"ts_event": "timestamp", "depth": "level"}
    """

    def __init__(self, path, *, tz: str | None = None, colmap: dict[str, str] | None = None):
        self.path = path
        self.tz = tz
        # default identity map; user-supplied keys override
        self.colmap = {"timestamp": "timestamp", "level": "level",
                       "side": "side", "price": "price", "size": "size"}
        if colmap:
            self.colmap.update({v: k for k, v in colmap.items()})  # reverse map

    # ------------------------------------------------------------------ #
    def load_raw(self) -> pd.DataFrame:
        df = pd.read_csv(self.path)
        df.columns = [c.strip() for c in df.columns]           # trim spaces
        df = df.rename(columns=self.colmap)

        required = {"timestamp", "level", "side", "price", "size"}
        if missing := required - set(df.columns):
            raise ValueError(f"Missing columns after rename: {missing}\n"
                             f"Current cols: {df.columns.tolist()}")

        print("[Loader] final columns:", df.columns.tolist())

        df = (
            df.assign(
                timestamp=lambda x: pd.to_datetime(x["timestamp"], unit="ns", utc=True).dt.tz_convert(self.tz),
                side=lambda x: x["side"].map({0: "bid", 1: "ask", "B": "bid", "S": "ask"}),
            )
            .astype({"level": "int8", "price": "float64", "size": "int32", "side": "category"})
            .sort_values("timestamp")
            .reset_index(drop=True)
        )
        return df
