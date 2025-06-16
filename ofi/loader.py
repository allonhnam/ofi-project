# ofi/loader.py
"""
Low-level CSV → pandas reader for simple ITCH-style order-book snapshots.
Adapt as needed if your field names differ.
"""

from __future__ import annotations

import pandas as pd


class Loader:
    """Read a raw snapshot file into a tidy long-format DataFrame.

    Expected columns in *path*:
        timestamp | level | price | size | side
    """

    def __init__(self, path: str, tz: str | None = None) -> None:
        self.path = path
        self.tz = tz  # e.g. 'America/New_York' for wall-clock plots

    # ------------------------------------------------------------ #
    # public API
    # ------------------------------------------------------------ #
    def load_raw(self) -> pd.DataFrame:
        df = pd.read_csv(self.path)

        # --- basic hygiene -------------------------------------------------- #
        df = (
            df.rename(columns=str.lower)
            .assign(
                timestamp=lambda x: pd.to_datetime(
                    x["timestamp"], unit="ns", utc=True
                ).dt.tz_convert(self.tz),
                side=lambda x: x["side"].map({0: "bid", 1: "ask"}),
            )
            .astype(
                {
                    "level": "int8",
                    "price": "float64",
                    "size": "int32",
                    "side": "category",
                }
            )
            .sort_values("timestamp")
            .reset_index(drop=True)
        )

        missing = {"timestamp", "level", "price", "size", "side"} - set(df.columns)
        if missing:
            raise ValueError(f"CSV is missing columns: {missing}")

        return df
