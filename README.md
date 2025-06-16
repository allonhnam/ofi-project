# OFI-Project

Code & notes for constructing **Order Flow Imbalance (OFI)** features and reproducing the cross-impact results from Cont *et al.* (2023).

## Quick-start

```bash
git clone https://github.com/your-handle/ofi-project.git
cd ofi-project
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"        # requires a `pyproject.toml` or setup.cfg
jupyter lab notebooks/01_feature_demo.ipynb
