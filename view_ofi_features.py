# view_ofi_features.py
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1.  Load the feature files                                                  
base = Path("features")
single_csv = base / "ofi_single_preview.csv"
panel_csv  = base / "ofi_panel_wide.csv"

if not single_csv.exists() or not panel_csv.exists():
    raise FileNotFoundError(
        "CSV files not found. Make sure you ran the build scripts:\n"
        "  features/ofi_single_preview.csv\n"
        "  features/ofi_panel_wide.csv"
    )

single = pd.read_csv(single_csv, index_col=0, parse_dates=True)
panel  = pd.read_csv(panel_csv,  index_col=0, parse_dates=True)

# ensure output dir exists
base.mkdir(exist_ok=True)

# Figure 1 – Best-level vs Integrated OFI                                     
plt.figure(figsize=(10, 4))
single["ofi_best"].plot(label="Best-level")
single["ofi_int"].plot(label="Integrated", linestyle="--")
plt.title("Best-level vs Integrated OFI (single stock)")
plt.xlabel("Time (1 s)")
plt.ylabel("Signed size")
plt.legend()
plt.tight_layout()
plt.savefig(base / "fig1_best_vs_integrated.png", dpi=120)
plt.show()

# Figure 2 – Multi-level OFI heat-map                                         
levels = [c for c in single.columns if c.startswith("ofi_") and c != "ofi_best"]
subset = single.iloc[:300][levels].T     # first 5 minutes
plt.figure(figsize=(10, 3))
plt.imshow(subset, aspect="auto", interpolation="nearest")
plt.yticks(range(len(levels)), [f"L{i}" for i in range(1, len(levels)+1)])
plt.title("Multi-level OFI (levels 1-10, first 5 min)")
plt.xlabel("Time (1 s)")
plt.colorbar(label="Signed size")
plt.tight_layout()
plt.savefig(base / "fig2_multilevel_heatmap.png", dpi=120)
plt.show()


# Figure 3 – Cross-asset Best-level OFI                                       
plt.figure(figsize=(10, 4))
for col in panel.columns[:5]:            # first 5 tickers
    panel[col].plot(label=col)
plt.title("Cross-asset Best-level OFI (aligned 1 s clock)")
plt.xlabel("Time")
plt.ylabel("Signed size")
plt.legend(ncol=3)
plt.tight_layout()
plt.savefig(base / "fig3_cross_asset.png", dpi=120)
plt.show()
