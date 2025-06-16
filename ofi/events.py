# ofi/events.py
from dataclasses import dataclass
import pandas as pd

@dataclass
class OFIIncrement:
    timestamp: pd.Timestamp
    level: int
    side: str   # 'bid' or 'ask'
    delta_q: int

def compute_increments(book_df: pd.DataFrame) -> pd.DataFrame:
    """Compute signed queue-size deltas between successive snapshots."""
    book_df = book_df.sort_values("timestamp")
    shifted = book_df.groupby(["level", "side"]).shift(1)
    out = book_df.copy()
    out["delta_q"] = (
        # eq. (1)–(2): sign depends on price move direction
        (book_df["size"] - shifted["size"])
        .fillna(0)
        .astype("int32")
    )
    return out[["timestamp", "level", "side", "delta_q"]]
