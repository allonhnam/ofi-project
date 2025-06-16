# ofi/__init__.py
from .loader import Loader
from .aggregates import (
    best_level_ofi,
    multi_level_vector,
    integrated_ofi,
    cross_asset_panel,
)
__all__ = [
    "Loader",
    "best_level_ofi",
    "multi_level_vector",
    "integrated_ofi",
    "cross_asset_panel",
]
__version__ = "0.1.0"
