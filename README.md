# ISG Screen Analysis

Analysis code for the live-cell imaging (Incucyte) ISG screen described in:

<!-- > **[Paper title]** — *Authors et al., Journal, Year.*  
> DOI: [doi link] -->

---

## Overview

This repository contains the analysis pipeline for a genome-wide ISG (Interferon-Stimulated Gene) screen performed using the Incucyte live-cell imaging system. The screen tested ~300 ISGs against 7 viruses to identify candidates with antiviral activity.

The fluorescence readout — **Green Integrated Intensity / Red Integrated Intensity (GII/RII)** — serves as a proxy for viral replication: a higher GII/RII ratio indicates greater reporter expression and therefore stronger ISG-mediated restriction.

**Viruses screened:**

| Code | Virus |
|------|-------|
| V1 | HSV-1 |
| V2 | MeV |
| V3 | RVFV |
| V4 | VACV |
| V5 | YFV |
| V6 | VSV |
| V7 | SFV |
| V8 | SARS-CoV-2 |

---

## Repository structure

```
├── main_analysis.ipynb   # Main analysis notebook (run this)
├── requirements.txt      # Python dependencies
├── data/
│   ├── fluorescence/     # Incucyte GII/RII export files (virus-infected plates)
│   └── viability/        # Incucyte GII export files (mock-infected control plates)
└── src/
    ├── read_data.py       # I/O helpers for Incucyte .txt exports
    ├── process_signal.py  # Signal denoising (median + Savitzky-Golay smoothing)
    ├── fit_data.py        # Curve fitting (sigmoid, exponential, linear)
    └── virus2mock.py      # Mapping of virus plates to matched mock controls
```

### Data file naming convention

```
V<virus>_S<set>_R<replicate>.txt
```

- **V** — virus ID (0 = mock/uninfected control)
- **S** — set number (1–4, each set corresponds to one 96-well plate of ~75 ISGs)
- **R** — biological replicate number

---

## Analysis pipeline

The notebook `main_analysis.ipynb` runs the following steps:

1. **Viability screen** — exponential fits to GII on mock-infected plates identify knockouts that cause cellular toxicity. Toxic KOs are excluded from downstream analysis.
2. **Fluorescence data loading** — GII/RII time-series are loaded for all virus–ISG–replicate combinations.
3. **Signal cleaning** — early-timepoint noise is removed and the signal is smoothed with a median + Savitzky-Golay filter pipeline.
4. **Sigmoid fitting** — a logistic growth model is fit to each time-series to extract parameters: *K* (amplitude), *τ* (induction time), *β* (growth rate), and *c* (baseline).
5. **Normalisation** — fitted parameters are normalised to the mean of 5 non-targeting controls (NTCs) per plate.
6. **Merging** — normalised fluorescence and viability parameters are merged into a single output DataFrame.

---

## Setup and usage

### Requirements

- Python ≥ 3.9

### Installation

1. [Install Python](https://www.python.org/downloads/) or [install conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation).

2. Clone this repository:
   ```bash
   git clone <repo-url>
   cd isg_analysis
   ```

3. Create a virtual environment:
   ```bash
   python -m venv isg_screen
   ```

4. Activate the environment:
   - **Unix/macOS:** `source isg_screen/bin/activate`
   - **Windows:** `.\isg_screen\Scripts\Activate`

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Launch the notebook:
   ```bash
   jupyter notebook main_analysis.ipynb
   ```

More information on virtual environments is available in the [Python documentation](https://docs.python.org/3/library/venv.html).
