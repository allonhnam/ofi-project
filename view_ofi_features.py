# view_ofi_features.py
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------------------------------- #
# 1.  Load the feature files                                                  #
# --------------------------------------------------------------------------- #
base = Path("features")
single_csv = base / "ofi_single_preview.csv"   # best / multi / integrated
panel_csv  = base / "ofi_panel_wide.csv"       # cross-asset best-level

if not single_csv.exists() or not panel_csv.exists():
    raise FileNotFoundError(
        "CSV files not found. Make sure you ran the build scripts:\n"
        "  features/ofi_single_preview.csv\n"
        "  features/ofi_panel_wide.csv"
    )

single = pd.read_csv(single_csv, index_col=0, parse_dates=True)
panel  = pd.read_csv(panel_csv,  index_col=0, parse_dates=True)

# --------------------------------------------------------------------------- #
# 2.  Figure 1 – best-level vs integrated OFI                                 #
# --------------------------------------------------------------------------- #
plt.figure(figsize=(11, 4))
single["ofi_best"].plot(label="Best-level OFI")
single["ofi_int"].plot(label="Integrated OFI", linestyle="--")
plt.title("Single-stock OFI features (1-second sampling)")
plt.xlabel("timestamp")
plt.ylabel("signed size")
plt.legend()
plt.tight_layout()
plt.show()

# --------------------------------------------------------------------------- #
# 3.  Figure 2 – cross-asset best-level OFI panel                             #
# --------------------------------------------------------------------------- #
plt.figure(figsize=(11, 4))

# Plot up to 5 tickers to keep the picture readable
for col in panel.columns[:5]:
    panel[col].plot(label=col)

plt.title("Cross-asset best-level OFI (1-second sampling)")
plt.xlabel("timestamp")
plt.ylabel("signed size")
plt.legend(ncol=3)
plt.tight_layout()
plt.show()
