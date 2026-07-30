# GranuLens 🔬

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Automated Digital Granulometry and Particle Size Distribution (PSD) Analysis using Computer Vision.**

**GranuLens** is an open-source Python library and CLI application engineered to automate grain and particle analysis from digital imagery. Designed for geoscientists, materials engineers, and researchers, GranuLens leverages classic computer vision algorithms—including Gaussian filtering, Otsu's thresholding, Distance Transforms, and the Watershed algorithm—to segment touching particles and compute comprehensive geometrical metrics alongside Particle Size Distribution ($D_{10}$, $D_{50}$, $D_{90}$).

---

## 🌟 Key Features

* **Advanced Particle Segmentation:** Separates adjacent and touching grains with high precision using Distance Transforms paired with Watershed segmentation.
* **Comprehensive Morphometrical Metrics:**
  * Area ($\text{px}^2$ and $\text{mm}^2$)
  * Equivalent Diameter ($d_{eq}$)
  * Minimum and Maximum Feret Diameters
  * Aspect Ratio & Sphericity
* **Particle Size Distribution (PSD):** Calculates cumulative passing percentages and extracts characteristic percentile diameters: **$D_{10}$**, **$D_{50}$ (median)**, and **$D_{90}$**.
* **Multi-Format Exporting:**
  * Segmented overlay image with colorized particle boundaries (`.png`).
  * High-resolution PSD cumulative curve plot (`.png`).
  * Individual grain metrics report (`.csv`).
  * Consolidated statistical summary (`.json`).
* **Dual Interface:** Accessible both as a developer-friendly Python package and as a fast, user-friendly Command Line Interface (CLI).

---

## ⚙️ Computer Vision Pipeline
Raw Image ➔ Gaussian Blur ➔ Otsu Thresholding ➔ Distance Transform ➔ Watershed ➔ Morphometric Analysis ➔ PSD Curve

1. **Preprocessing:** Converts the image to grayscale and applies Gaussian smoothing to reduce sensor noise.
2. **Thresholding:** Employs Otsu's adaptive method to separate particle foreground from background.
3. **Marker Generation:** Computes an Euclidean Distance Transform on the binary mask to locate individual particle centers.
4. **Watershed Segmentation:** Treats distance peaks as topological catchment basins, precisely delineating boundaries between contacting grains.
5. **Feature Extraction:** Contours are extracted to derive particle areas, perimeters, Feret dimensions, and cumulative distribution stats.

---
## 📦 Installation

### 1. System Dependencies (Linux / GitHub Codespaces)

OpenCV requires headless graphics libraries on Linux environments. Install them via `apt`:

```bash
sudo apt-get update && sudo apt-get install -y libgl1 libglib2.0-0
```
### 2. Python Package Installation

Clone the repository and install granulens in editable mode with development dependencies:
```bash
git clone [https://github.com/seu-usuario/granulens.git](https://github.com/seu-usuario/granulens.git)
cd granulens
pip install -e ".[dev]"
```
## 🚀 Quick Start
Option A: Command Line Interface (CLI)Analyze an image from your terminal by specifying the spatial scale ($\text{mm/px}$) and destination folder:
```bash
granulens analyze examples/sample_grains.png --scale 0.05 --output ./results
```
Available CLI Options:
| Flag | Short | Description | Default |
| :--- | :--- | :--- | :--- |
| `--scale` | `-s` | Spatial resolution conversion factor (mm/px) | `1.0` |
| `--min-distance` | `-d` | Minimum pixel distance between particle centers | `15` |
| `--output` | `-o` | Target directory for generated plots and data exports | `./results` |
| `--csv / --no-csv` | | Toggle individual particle CSV export | `Enabled` |
| `--json / --no-json` | | Toggle consolidated statistical JSON export | `Enabled` |

Option B: Python Library API

Integrate granulens directly into your data science workflows or notebooks:
```bash
from granulens.core import GranuLens

# 1. Initialize analyzer with scale factor (mm/px)
analyzer = GranuLens(scale_mm_per_px=0.05, min_distance=15)

# 2. Process image
result = analyzer.process("path/to/grains_image.png")

# 3. Access summary statistics
summary = result.summary
print(f"Total Particles: {summary.total_particles}")
print(f"D10: {summary.d10:.3f} mm")
print(f"D50: {summary.d50:.3f} mm")
print(f"D90: {summary.d90:.3f} mm")

# 4. Save visualization artifacts and export data
result.save_plots(output_dir="./results")
result.export_csv("./results/particle_metrics.csv")
result.export_json("./results/summary_stats.json")
```
## 📊 Output Artifacts
Running an analysis generates four primary artifacts in your output directory:
1. *_overlay.png: Visual validation map highlighting individual particles with transparent color fills and marked boundary lines.
2. *_psd_curve.png: Publication-ready plot featuring the cumulative particle size distribution curve and labeled $D_{10}$, $D_{50}$, and $D_{90}$ threshold lines.
3. *_metrics.csv: Tabular dataset containing detailed grain-by-grain measurements for downstream analysis in Excel, Pandas, or R.
4. *_summary.json: Structured metadata summary containing total counts, mean diameter, standard deviation, and key distribution percentiles.
## 📁 Repository Structure
```bash
granulens/
├── src/
│   └── granulens/
│       ├── __init__.py         # Package initialization & version metadata
│       ├── segmentation.py     # Otsu thresholding & Watershed segmentation
│       ├── metrics.py          # Morphometrical geometry & PSD math
│       ├── visualization.py    # Overlay rendering & Matplotlib PSD plotting
│       ├── core.py             # Orchestrator engine & exporter classes
│       └── cli.py              # CLI implementation via Typer
├── examples/
│   └── generate_sample.py      # Synthetic particle image generator
├── tests/                      # Automated unit & integration tests (pytest)
├── pyproject.toml              # Build config & package dependencies
└── README.md                   # Project documentation
```
## 🧪 Running Tests

Validate the pipeline and core segmentation math using pytest:
```bash
pytest
```
## 📜 License

Distributed under the MIT License. See LICENSE for more information.

Author: Mateus Leptokarydis
