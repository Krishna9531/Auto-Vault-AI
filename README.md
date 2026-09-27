# AUTOVAULT AI
### Automotive Risk, Value & Ownership Intelligence

> **Predict. Protect. Profit.**  
> An end-to-end machine learning platform that forecasts vehicle residual values, quantifies ownership risk, and delivers actionable intelligence for buyers, sellers, lenders, and fleet operators.

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.37-red?logo=streamlit)](https://streamlit.io)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.1-orange)](https://xgboost.readthedocs.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Problem Statement

The used-vehicle market is a $1.2 trillion global industry plagued by **asymmetric information**. Buyers overpay. Sellers underprice. Lenders mis-price risk. Fleet operators bleed value through suboptimal hold-sell decisions.

Traditional valuation tools (KBB, Edmunds, Black Book) provide static, point-in-time estimates based on aggregate market data. They fail to account for:

- **Depreciation non-linearity** across trims, powertrains, and geographic micro-markets
- **Risk-adjusted residual value** under economic stress scenarios
- **Ownership cost forecasting** (insurance, fuel, maintenance, registration)
- **Market timing signals** — the best month to buy or sell a specific vehicle

**AUTOVAULT AI** closes this gap with a fully integrated ML pipeline that ingests multi-source market data, trains ensemble forecasting models, and surfaces predictions through an interactive Streamlit dashboard.

---

## Architecture Overview

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                            AUTOVAULT AI PLATFORM                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   ┌─────────────────────────────────────────────────────────────────────┐   ║
║   │                        DATA INGESTION LAYER                         │   ║
║   │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   ║
║   │  │  Market APIs  │  │  CSV / Excel  │  │  Web Scraper (BS4/Req)  │  │   ║
║   │  │  (auctions,   │  │  (OEM MSRP,  │  │  (Listings, classifieds) │  │   ║
║   │  │   sales data) │  │   fuel data) │  └──────────────────────────┘  │   ║
║   │  └──────┬───────┘  └──────┬───────┘             │                  │   ║
║   └─────────┼─────────────────┼─────────────────────┼──────────────────┘   ║
║             │                 │                      │                       ║
║   ┌─────────▼─────────────────▼──────────────────────▼──────────────────┐   ║
║   │                      PROCESSING LAYER                                │   ║
║   │        Cleaning → Feature Engineering → Encoding → Scaling          │   ║
║   └──────────────────────────────┬───────────────────────────────────────┘  ║
║                                  │                                           ║
║   ┌──────────────────────────────▼───────────────────────────────────────┐  ║
║   │                       ML MODEL LAYER                                 │  ║
║   │   ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌─────────────┐  │  ║
║   │   │  XGBoost   │  │  LightGBM  │  │  Random    │  │   Linear    │  │  ║
║   │   │  Residual  │  │  Deprec.   │  │  Forest    │  │   Baseline  │  │  ║
║   │   │ Forecaster │  │   Curve    │  │  Ensemble  │  │   (Ridge)   │  │  ║
║   │   └────────────┘  └────────────┘  └────────────┘  └─────────────┘  │  ║
║   │                       ↓  Stacking / Voting Ensemble  ↓               │  ║
║   └──────────────────────────────┬───────────────────────────────────────┘  ║
║                                  │                                           ║
║   ┌──────────────────────────────▼───────────────────────────────────────┐  ║
║   │                    INTELLIGENCE & ANALYTICS LAYER                    │  ║
║   │    SHAP Explainability  │  Risk Scoring  │  Scenario Simulation      │  ║
║   └──────────────────────────────┬───────────────────────────────────────┘  ║
║                                  │                                           ║
║   ┌──────────────────────────────▼───────────────────────────────────────┐  ║
║   │                   STREAMLIT DASHBOARD (UI LAYER)                     │  ║
║   │   Valuation Tool │ Depreciation Curves │ Risk Report │ Market Pulse  │  ║
║   └──────────────────────────────────────────────────────────────────────┘  ║
║                                  │                                           ║
║   ┌──────────────────────────────▼───────────────────────────────────────┐  ║
║   │              PERSISTENCE LAYER (PostgreSQL + SQLAlchemy)             │  ║
║   └──────────────────────────────────────────────────────────────────────┘  ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Modules

| # | Module | Description |
|---|--------|-------------|
| 1 | **Data Ingestion** (`src/ingestion/`) | Multi-source data collectors: auction APIs, CSV loaders, web scrapers for live listings |
| 2 | **Feature Engineering** (`src/features/`) | VIN decoding, depreciation curve derivation, geo-encoding, seasonality flags, macro indicators |
| 3 | **Model Training** (`src/models/`) | XGBoost + LightGBM ensemble for residual value; Ridge baseline; cross-validated pipeline |
| 4 | **Explainability** (`src/explainability/`) | SHAP waterfall and beeswarm plots, feature importance ranking per prediction |
| 5 | **Risk Engine** (`src/risk/`) | Composite risk scoring: market liquidity, segment volatility, ownership cost index |
| 6 | **Scenario Simulator** (`src/simulator/`) | Monte Carlo hold-sell simulation; stress testing under macro shock scenarios |
| 7 | **Database Layer** (`src/db/`) | SQLAlchemy ORM models, Alembic migrations, query helpers for PostgreSQL |
| 8 | **Dashboard** (`app/`) | Streamlit multi-page app: Valuation, Depreciation, Risk Report, Market Pulse, Settings |

---

## Installation

### Prerequisites
- Python 3.11+
- PostgreSQL 15+ (or SQLite for local dev)
- Git

### 1 — Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Auto-Residual-Forecaster.git
cd "Auto Residual Forecaster"
```

### 2 — Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3 — Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4 — Configure Environment
```bash
cp .env.example .env
# Edit .env with your database credentials and config values
```

### 5 — Initialize the Database
```bash
python -m src.db.init_db
```

### 6 — Run the Dashboard
```bash
streamlit run app/main.py
```

The app will be available at `http://localhost:8501`.

---

## Usage

### Instant Vehicle Valuation
1. Navigate to **Valuation Tool** in the sidebar
2. Enter make, model, year, mileage, trim, and condition
3. Click **Run Forecast** — get predicted residual value with confidence interval
4. Expand **SHAP Explanation** to see which features drove the estimate

### Depreciation Curve Explorer
- Select up to 5 vehicles to overlay depreciation curves (12–60 months)
- Toggle between **absolute value** and **% retained** views
- Export curve data as CSV or Excel

### Risk Report
- Input a target vehicle and holding period
- Receive a composite **Risk Score (0–100)** with sub-scores for:
  - Market Liquidity Risk
  - Segment Volatility
  - Ownership Cost Index
  - Macro Sensitivity

### Market Pulse
- Live-updated heatmap of market conditions by segment and region
- Seasonal buy/sell timing signals
- Auction vs. retail spread tracker

---

## Data Sources

| Source | Type | Refresh |
|--------|------|---------|
| Auction market feeds | API / CSV | Weekly |
| OEM MSRP & invoice data | CSV (manual) | Per model year |
| Used listing aggregators | Web scraper | Daily |
| US fuel price indices (EIA) | API | Weekly |
| CPI / macro indicators (FRED) | API | Monthly |
| Insurance rate benchmarks | CSV | Quarterly |
| Registration & title data | CSV (state) | Annual |

> **Note:** Raw data files are excluded from version control (see `.gitignore`). Place source files in `data/raw/` before running the ingestion pipeline.

---

## ML Methodology

### Target Variable
`residual_value_pct` — the vehicle's retained value as a percentage of original MSRP at a given age and mileage.

### Feature Space
| Category | Features |
|----------|----------|
| Vehicle Identity | Make, Model, Trim, Body Style, Drivetrain, Engine |
| Condition | Mileage, Accident History, Service Records, Condition Grade |
| Market | Segment Supply/Demand Ratio, Regional Auction Index, Days on Market |
| Macro | CPI, Fuel Price, Interest Rate, Unemployment Rate |
| Temporal | Model Age (months), Month of Year, Quarter |

### Model Pipeline
```
Raw Features
    │
    ▼
Preprocessing (Imputation → Encoding → Scaling)
    │
    ├──► XGBoost Regressor  ─┐
    ├──► LightGBM Regressor  ├──► Stacking Meta-Learner (Ridge) ──► Final Prediction
    └──► Random Forest       ─┘
```

### Validation Strategy
- **Time-based split**: Train on data through T-12 months, validate on T-6 to T, test on T to present
- **Walk-forward CV**: 5-fold rolling window cross-validation to prevent data leakage
- **Metrics**: RMSE, MAE, MAPE, R²

### Explainability
SHAP (SHapley Additive exPlanations) TreeExplainer is used to generate per-prediction feature attributions, enabling transparent, auditable valuations.

---

## Project Structure

```
Auto Residual Forecaster/
│
├── app/                        # Streamlit multi-page dashboard
│   ├── main.py                 # Entry point, navigation, global config
│   └── pages/
│       ├── 01_valuation.py     # Vehicle valuation & SHAP explainer
│       ├── 02_depreciation.py  # Depreciation curve explorer
│       ├── 03_risk_report.py   # Risk scoring & scenario simulation
│       ├── 04_market_pulse.py  # Market heatmap & timing signals
│       └── 05_settings.py      # App configuration & data refresh
│
├── src/
│   ├── ingestion/              # Data collection modules
│   │   ├── __init__.py
│   │   ├── auction_loader.py
│   │   ├── listing_scraper.py
│   │   └── macro_fetcher.py
│   │
│   ├── features/               # Feature engineering pipeline
│   │   ├── __init__.py
│   │   ├── pipeline.py
│   │   ├── encoders.py
│   │   └── depreciation_curves.py
│   │
│   ├── models/                 # Model training & inference
│   │   ├── __init__.py
│   │   ├── trainer.py
│   │   ├── predictor.py
│   │   └── evaluator.py
│   │
│   ├── explainability/         # SHAP analysis
│   │   ├── __init__.py
│   │   └── shap_engine.py
│   │
│   ├── risk/                   # Risk scoring engine
│   │   ├── __init__.py
│   │   └── risk_scorer.py
│   │
│   ├── simulator/              # Scenario simulation
│   │   ├── __init__.py
│   │   └── monte_carlo.py
│   │
│   ├── db/                     # Database ORM & helpers
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── session.py
│   │   └── init_db.py
│   │
│   └── utils/                  # Shared utilities
│       ├── __init__.py
│       ├── config.py
│       └── logger.py
│
├── data/
│   ├── raw/                    # Source data (gitignored)
│   └── processed/              # Cleaned, engineered data (gitignored)
│
├── models/                     # Serialized model artifacts (gitignored)
│
├── notebooks/                  # Exploratory analysis notebooks
│   ├── 01_eda.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_experiments.ipynb
│
├── tests/                      # Unit & integration tests
│   ├── test_features.py
│   ├── test_models.py
│   └── test_risk.py
│
├── .env.example                # Environment template
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Limitations & Future Work

### Current Limitations
- **Data dependency**: Model accuracy is directly tied to the quality and recency of input data. Without live auction feeds, forecasts rely on historical snapshots.
- **US-centric**: Feature engineering and data sources are optimized for the US market. Adaptation for other markets requires additional data sourcing.
- **EV coverage**: Electric vehicle residual value dynamics differ significantly from ICE vehicles; the current feature set is partially adapted for EVs.
- **No real-time pricing**: The scraper pulls listing data in batch; true real-time pricing requires a dedicated API subscription.

### Roadmap
- [ ] **v1.1** — Integrate live auction API feeds (Manheim, ADESA)
- [ ] **v1.2** — EV-specific depreciation model with battery health factor
- [ ] **v1.3** — Lender risk API endpoint (REST) for programmatic access
- [ ] **v2.0** — Neural network time-series model (Temporal Fusion Transformer) for 5-year residual forecasting
- [ ] **v2.1** — Fleet portfolio optimizer with hold-sell calendar
- [ ] **v2.2** — Multi-market expansion (UK, Canada, Australia)
- [ ] **v3.0** — Real-time market data integration + automated model retraining pipeline

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Ensure all tests pass before submitting:

```bash
pytest tests/ -v --tb=short
```

---

## License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 AUTOVAULT AI Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<p align="center">
  Built with ⚡ by the AUTOVAULT AI team · 2026
</p>
