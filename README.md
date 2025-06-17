# OFI-Project

End-to-end pipeline for constructing the four Order-Flow Imbalance (OFI)
feature families required in the assignment.

* **Best-Level OFI**
* **Multi-Level OFI**
* **Integrated OFI**
* **Cross-Asset OFI**

---

## 0  Quick setup

```bash
# clone

# create and activate venv
python -m venv .venv
source .venv/bin/activate        # PowerShell → .\.venv\Scripts\Activate.ps1

# install package + deps
pip install -e .
pip install pyarrow               # for Parquet (optional but recommended)
