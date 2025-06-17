# OFI-Project

 write/read Parquet; otherwise use CSV
6	Single-stock features
python scripts/build_single_stock_ofi.py \
  --csv data/first_25000_rows.csv \
  --colmap timestamp=ts_event,level=depth \
  --freq 1s --depth 10 \
  --out features/ofi_single.parquet	produces Best-level, Multi-level, Integrated OFI for one stock
7	(optional, multi-ticker) place per-ticker CSVs in data/stocks/	
8	Cross-asset panel
python scripts/build_cross_asset_ofi.py \
  --dir data/stocks \
  --colmap timestamp=ts_event,level=depth \
  --freq 1s \
  --out features/ofi_panel.nc \
  --lasso	creates ofi_panel.nc (cross-asset OFI) and lasso_loadings.nc
9	Graphs
python view_ofi_features.py	saves three PNGs in features/:
• fig1_best_vs_integrated.png (Best vs Integrated)
• fig2_multilevel_heatmap.png (Multi-level)
• fig3_cross_asset.png (Cross-asset)

That sequence reproduces every deliverable the assignment requires:

Best-Level OFI → ofi_single.parquet : ofi_best

Multi-Level OFI → ofi_single.parquet : ofi_1 … ofi_10

Integrated OFI → ofi_single.parquet : ofi_int

Cross-Asset OFI → ofi_panel.nc (and its CSV preview)
