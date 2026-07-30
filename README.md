# granulens 🪨🔬

> **Automated Digital Granulometry & Particle Size Distribution using Computer Vision**

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`granulens` is a lightweight Python tool and CLI designed to extract particle size distribution (PSD) from digital images of grains, aggregates, and sediments. Using classic image processing (Adaptive Thresholding + Watershed Segmentation), it isolates touching particles, calculates geometric metrics, and plots cumulative particle-size distribution curves ($D_{10}$, $D_{50}$, $D_{90}$).

---

## 📸 Visual Overview

| Input Image | Watershed Segmentation | Cumulative PSD Curve |
|:---:|:---:|:---:|
| ![](docs/assets/input_sample.png) | ![](docs/assets/segmented_sample.png) | ![](docs/assets/psd_curve.png) |

---

## ✨ Key Features

* 🔍 **Touching Particle Separation:** Uses distance transform + Watershed algorithm to isolate overlapping or touching grains.
* 📏 **Scale Calibration:** Convert pixels to millimeters via direct scale factor (`--scale`) or reference marker.
* 📊 **Granulometric Indicators:** Automatic calculation of $D_{10}$, $D_{50}$ (median grain size), and $D_{90}$.
* 💻 **Dual Mode:** Use it as a terminal CLI tool or import it directly as a Python module.
* 📁 **Export Capabilities:** Export overlay images (PNG), cumulative plots, and raw metrics (CSV/JSON).

---

## 🚀 Quickstart

### Installation

Clone the repository and install the package locally:

```bash
git clone [https://github.com/seu-usuario/granulens.git](https://github.com/seu-usuario/granulens.git)
cd granulens
pip install -e .
```
## CLI Usage
Analyze an image directly from the terminal
```bash
# Analyze image with a scale factor of 0.05 mm/pixel
granulens analyze examples/sample_grains.png --scale 0.05 --output ./results
```
## Python API
```bash
from granulens import GranuLens

# Initialize analyzer with scale factor (mm per pixel)
analyzer = GranuLens(scale_mm_per_px=0.05)

# Process target image
results = analyzer.process("examples/sample_grains.png")

# Inspect key granulometric parameters
print(f"Total grains detected: {results.total_particles}")
print(f"D50 (Median size): {results.d50:.2f} mm")

# Save segmented output and cumulative curve
results.save_plots("./output/")
```
## Computed Metrics
For every detected particle, `granulens` calculates:

* **Equivalent Diameter ($d_{eq}$):** $d_{eq} = 2 \cdot \sqrt{\frac{\text{Area}}{\pi}}$
* **Feret Diameters:** Maximum and minimum calipers.
* **Aspect Ratio & Sphericity:** Particle shape indicators.

## License
Distributed under the MIT License. See LICENSE for more information.
