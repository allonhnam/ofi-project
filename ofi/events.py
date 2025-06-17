# ofi/events.py
"""
Transform successive snapshots into signed queue-size increments (OFI events).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(slots=True)
class OFIIncrement:  # ═════════════════════════════════════════════════ #
    timestamp: pd.Timestamp
    level: int
    side: str      # 'bid' or 'ask'
    delta_q: int   # signed size change


def compute_increments(book: pd.DataFrame) -> pd.DataFrame:
    """Return a tidy frame of signed size deltas for every (timestamp, level, side).

    Sign convention
    ---------------
    +  for events that *increase* buy-side pressure (bid adds, ask cancels)
    -  for events that *increase* sell-side pressure (ask adds, bid cancels)

    The rule follows Cont et al. (2023) equations (1)–(2).
    """
    book = book.sort_values(["timestamp", "side", "level"]).copy()

    # Shift one observation back within each (level, side) queue
    prev = (
        book
        .groupby(["level", "side"], observed=True)   # ← add observed=True
        .shift(1)
)
    # price change flags ---------------------------------------------------- #
    bid_mask = book["side"] == "bid"
    ask_mask = ~bid_mask

    # ΔQ when the price at that level is unchanged
    delta_size = book["size"].sub(prev["size"]).fillna(book["size"])

    # sign flip for the ask side
    signed_q = np.where(bid_mask, delta_size, -delta_size).astype("int32")

    out = book[["timestamp", "level", "side"]].copy()
    out["delta_q"] = signed_q
    return out
