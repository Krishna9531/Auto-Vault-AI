# Reports Directory — AUTOVAULT AI

This directory holds all generated analysis outputs, evaluation artifacts,
and the final project report. It is structured into three sub-directories.

---

## Directory Layout

```
reports/
├── figures/          # All charts, plots, and visualisations
├── model_results/    # Serialised metrics, predictions, and evaluation artefacts
└── final_report/     # Polished PDF / HTML report for stakeholders
```

---

## `figures/`

Stores every plot produced during EDA, feature engineering, and model evaluation.

| File Pattern | Contents |
|---|---|
| `eda_price_distribution.png` | Histogram of vehicle purchase prices across the dataset |
| `eda_depreciation_by_fuel.png` | Box plots: depreciation % grouped by fuel type |
| `eda_mileage_vs_resale.png` | Scatter: annual km vs resale value with fuel-type colour coding |
| `eda_age_vs_value.png` | Line plot: mean residual value vs vehicle age per segment |
| `eda_correlation_heatmap.png` | Pearson correlation matrix of all numerical features |
| `model_feature_importance.png` | Bar chart of top-20 SHAP feature importances |
| `model_residuals.png` | Residual plot: predicted vs actual resale values |
| `model_learning_curve.png` | Train / validation RMSE across training set size |
| `model_calibration.png` | Reliability diagram for confidence interval calibration |
| `tco_sensitivity_tornado.png` | Tornado chart: TCO sensitivity to each input parameter |

### How to Regenerate EDA Figures

Run the EDA notebook or script:

```bash
# Option A — Jupyter notebook
jupyter notebook notebooks/01_eda.ipynb

# Option B — standalone script (headless / CI-friendly)
python scripts/run_eda.py --output-dir reports/figures/
```

All figures are saved at **300 DPI** PNG by default. Pass `--format pdf` for
vector output suitable for the final report.

> **Note:** Figures are **not committed** to version control (`.gitkeep` is).
> They are regenerated from raw data on demand. CI pipelines run EDA as a
> required step before model training.

---

## `model_results/`

Stores numerical outputs from model training and evaluation runs.

| File Pattern | Contents |
|---|---|
| `metrics_depreciation.json` | MAE, RMSE, MAPE, R² for the depreciation model |
| `metrics_health.json` | Classification report + AUC for VehicleHealthModel |
| `metrics_maintenance.json` | Risk score calibration metrics + cost MAE |
| `cv_results_depreciation.csv` | Cross-validation fold-level results (5-fold, time-based) |
| `shap_values.npz` | SHAP value arrays for the test split (for post-hoc analysis) |
| `predictions_test.csv` | Ground-truth vs predicted values on the held-out test set |
| `confusion_matrix_health.csv` | Confusion matrix for health risk tier classification |
| `hyperparameter_search.json` | Best params from Optuna / GridSearch run |

### How to Regenerate Model Results

```bash
# Train all models and save artefacts
python scripts/train_models.py --config configs/model_config.yaml

# Run evaluation only (requires trained models in models/)
python scripts/evaluate_models.py --output-dir reports/model_results/
```

Results include **timestamp suffixes** when `--versioned` flag is used,
e.g. `metrics_depreciation_20260926_2251.json`.

> **Tip:** Use `mlflow ui` to browse run history interactively if MLflow
> tracking is enabled in `configs/model_config.yaml`.

---

## `final_report/`

The compiled stakeholder-facing report, auto-generated from templates.

| File | Contents |
|---|---|
| `autovault_report.pdf` | Full PDF report with all sections, figures, and tables |
| `autovault_report.html` | Self-contained HTML version for browser viewing |
| `executive_summary.md` | One-page markdown summary for quick stakeholder review |

### How to Generate the Final Report

```bash
# Requires: figures/ and model_results/ to be populated first
python scripts/generate_report.py

# For a specific date range of data
python scripts/generate_report.py --start 2025-01-01 --end 2026-09-26
```

The report template lives in `scripts/templates/report_template.md` and is
rendered via **Jinja2 + WeasyPrint** (PDF) or **Pandoc** (HTML).

---

## Quick Reference — Full Regeneration Pipeline

```bash
# 1. Run EDA → populates figures/
python scripts/run_eda.py --output-dir reports/figures/

# 2. Train and evaluate models → populates model_results/
python scripts/train_models.py
python scripts/evaluate_models.py --output-dir reports/model_results/

# 3. Compile final report → populates final_report/
python scripts/generate_report.py
```

> **Important:** Always regenerate in order (1 → 2 → 3). The report
> generator imports figure paths from `figures/` and metrics from
> `model_results/` — missing files will cause template rendering errors.
