# AUTOVAULT AI — Model Artifact Store

This directory holds **trained, serialised model artifacts** for all AUTOVAULT AI prediction pipelines.
Each sub-folder corresponds to one prediction domain and follows the same internal convention.

---

## Directory Layout

```
models/
├── depreciation/   — Residual value & percentage-depreciation regressors
├── health/         — Vehicle health score classifiers / regressors
├── battery/        — EV battery degradation & SoH (State-of-Health) models
├── maintenance/    — Predictive maintenance risk models
├── tco/            — Total Cost of Ownership estimators and lookup tables
└── risk/           — Composite risk scoring and tier classification models
```

---

## What Goes Inside Each Sub-folder

### `depreciation/`
| File | Description |
|------|-------------|
| `depreciation_model.pkl` | Primary trained regressor (XGBoost / RandomForest) for residual value % |
| `depreciation_scaler.pkl` | Fitted `StandardScaler` / `MinMaxScaler` used at inference time |
| `depreciation_feature_names.json` | Ordered list of feature column names the model expects |
| `depreciation_eval_report.json` | Hold-out evaluation metrics: MAE, RMSE, R², MAPE |
| `depreciation_feature_importance.json` | Feature importance scores from the trained model |

### `health/`
| File | Description |
|------|-------------|
| `health_model.pkl` | Vehicle health score regressor (0–100 scale) |
| `health_scaler.pkl` | Fitted feature scaler |
| `health_feature_names.json` | Ordered feature column list |
| `health_eval_report.json` | Evaluation metrics on test set |
| `health_feature_importance.json` | Feature importances / SHAP summary |

### `battery/`
| File | Description |
|------|-------------|
| `battery_model.pkl` | EV battery SoH regression model |
| `battery_scaler.pkl` | Fitted scaler (temperature, cycle-count features are sensitive) |
| `battery_feature_names.json` | Feature column list |
| `battery_eval_report.json` | RMSE, R², degradation-curve fit quality |
| `battery_feature_importance.json` | Feature importances |

### `maintenance/`
| File | Description |
|------|-------------|
| `maintenance_model.pkl` | Predictive maintenance risk classifier / regressor |
| `maintenance_scaler.pkl` | Fitted scaler |
| `maintenance_feature_names.json` | Feature column list |
| `maintenance_eval_report.json` | Precision, Recall, F1, AUC for risk bands |
| `maintenance_feature_importance.json` | Feature importances |

### `tco/`
| File | Description |
|------|-------------|
| `tco_model.pkl` | TCO estimator (may be rule-based + ML hybrid) |
| `fuel_cost_lookup.json` | City-wise fuel / electricity cost lookup table |
| `insurance_lookup.json` | Insurance premium lookup by segment and age |
| `tco_eval_report.json` | Back-test accuracy against known TCO data |

### `risk/`
| File | Description |
|------|-------------|
| `risk_model.pkl` | Composite risk scorer (Low / Medium / High / Critical) |
| `risk_scaler.pkl` | Fitted scaler |
| `risk_feature_names.json` | Feature column list |
| `risk_eval_report.json` | Classification report and confusion matrix |
| `risk_feature_importance.json` | Feature importances |

---

## Serialisation Convention

- All Python objects are serialised with **`joblib`** (preferred over `pickle` for NumPy arrays).
- Model files should be versioned using the naming pattern:
  `<domain>_model_v<MAJOR>.<MINOR>.pkl` — e.g. `depreciation_model_v1.2.pkl`
- The unversioned name (e.g. `depreciation_model.pkl`) always points to / is a copy of the **current production model**.

## Evaluation Report Schema

Every `*_eval_report.json` must follow this schema:

```json
{
  "model_version": "1.0",
  "trained_on": "YYYY-MM-DD",
  "n_train_samples": 0,
  "n_test_samples":  0,
  "metrics": {
    "mae":  0.0,
    "rmse": 0.0,
    "r2":   0.0,
    "mape": 0.0
  },
  "notes": ""
}
```

---

> **Do not commit large `.pkl` files directly to git.**
> Use Git LFS or store artifacts in a dedicated object store (S3, GCS, Azure Blob)
> and track only the metadata JSON files in version control.
