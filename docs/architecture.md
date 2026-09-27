# AUTOVAULT AI — System Architecture

> **Version:** 1.0.0 | **Last Updated:** September 2026 | **Author:** AUTOVAULT AI Team
> **Project:** Automotive Risk, Value & Ownership Intelligence Platform

---

## 1. System Overview

AUTOVAULT AI is an end-to-end, multi-model residual value forecasting and total cost of ownership (TCO) intelligence platform engineered for the automotive market. The platform addresses fundamental information asymmetry in used-vehicle pricing, financing, and fleet hold-sell decision-making.

By synthesizing classical actuarial depreciation schedules, machine learning models (gradient-boosted trees and ensembles), explainable AI (SHAP), and financial mathematics, AUTOVAULT AI answers critical questions for buyers, lenders, dealerships, and fleet managers:

1. **Residual Valuation:** What is the vehicle worth today and across a 1–7 year holding horizon under varying mileage and market stress conditions?
2. **Component & Mechanical Health:** How do age, odometer readings, and city operating conditions degrade mechanical, electrical, and powertrain subsystems?
3. **Total Cost of Ownership (TCO):** What is the true comprehensive monthly and annual cash outflow when factoring in reducing-balance financing (EMI), fuel/energy consumption, insurance, routine servicing, and unexpected repair risk?
4. **Actionable Risk Profiling:** What is the vehicle's liquidity risk, segment volatility index, and financial obligation burden (FOIR)?

---

## 2. ASCII System Diagram

```
╔══════════════════════════════════════════════════════════════════════════════════════════╗
║                                  AUTOVAULT AI PLATFORM                                   ║
╠══════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                          ║
║   ┌──────────────────────────────────────────────────────────────────────────────────┐   ║
║   │                   MODULE 1: DATA INGESTION & SOURCING LAYER                      │   ║
║   │  ┌──────────────────┐  ┌───────────────────┐  ┌───────────────────────────────┐  │   ║
║   │  │  Auction Feeds   │  │    OEM & MSRP     │  │   Live Listing Scraper        │  │   ║
║   │  │  & Partner APIs  │  │    Master CSVs    │  │   (Cardekho, Cars24, Portals) │  │   ║
║   │  └─────────┬────────┘  └─────────┬─────────┘  └───────────────┬───────────────┘  │   ║
║   │            │                     │                            │                  │   ║
║   │            ▼                     ▼                            ▼                  │   ║
║   │       [ Schema Validation  •  Type Checking  •  Deduplication  •  Raw Cache ]    │   ║
║   └──────────────────────────────────┬───────────────────────────────────────────────┘   ║
║                                      │                                                   ║
║   ┌──────────────────────────────────▼───────────────────────────────────────────────┐   ║
║   │              MODULE 2: FEATURE ENGINEERING & PREPROCESSING LAYER                 │   ║
║   │  ┌──────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────┐  │   ║
║   │  │ Age × Mileage Inter. │  │ One-Hot / Target Encode │  │ Geo & City Tiers    │  │   ║
║   │  │ Log Price Transform  │  │ Outlier Winsorization   │  │ Fuel / EV Metrics   │  │   ║
║   │  └──────────────────────┘  └─────────────────────────┘  └─────────────────────┘  │   ║
║   └──────────────────────────────────┬───────────────────────────────────────────────┘   ║
║                                      │                                                   ║
║   ┌──────────────────────────────────▼───────────────────────────────────────────────┐   ║
║   │                    MODULE 3: MACHINE LEARNING MODEL LAYER                        │   ║
║   │  ┌────────────────────────┐  ┌───────────────────────┐  ┌─────────────────────┐  │   ║
║   │  │   XGBoost Regressor    │  │   LightGBM Forecaster │  │   Random Forest     │  │   ║
║   │  │  (Monotone Residuals)  │  │   (Maintenance Cost)  │  │   (Health Classifier)│ │   ║
║   │  └───────────┬────────────┘  └───────────┬───────────┘  └──────────┬──────────┘  │   ║
║   │              │                           │                         │             │   ║
║   │              ▼                           ▼                         ▼             │   ║
║   │  ┌────────────────────────────────────────────────────────────────────────────┐  │   ║
║   │  │              Ensemble Blending & Conformal Confidence Bounds (90% CI)      │  │   ║
║   │  └───────────────────────────────────────┬────────────────────────────────────┘  │   ║
║   └──────────────────────────────────────────┼───────────────────────────────────────┘   ║
║                                              │                                           ║
║         ┌────────────────────────────────────┼────────────────────────────────────┐      ║
║         │                                    │                                    │      ║
║   ┌─────▼─────────────────────────┐  ┌───────▼──────────────────────────┐  ┌──────▼────┐ ║
║   │    MODULE 4: EXPLAINABILITY   │  │      MODULE 5: RISK ENGINE       │  │ MODULE 6: │ ║
║   │            (SHAP)             │  │   Composite Risk & Volatility    │  │ SCENARIO  │ ║
║   │ • TreeExplainer Attributions  │  │ • Liquidity Risk Index (0-100)   │  │ SIMULATOR │ ║
║   │ • Waterfall & Beeswarm Plots  │  │ • Mechanical Exposure Score      │  │ • Monte   │ ║
║   │ • Factor Relative Drivers     │  │ • Debt Burden / FOIR Limits      │  │   Carlo   │ ║
║   └──────────────┬────────────────┘  └───────────────┬──────────────────┘  └─────┬─────┘ ║
║                  │                                   │                           │       ║
║                  └───────────────────┬───────────────┴───────────────────────────┘       ║
║                                      │                                                   ║
║   ┌──────────────────────────────────▼───────────────────────────────────────────────┐   ║
║   │             MODULE 7: FINANCIAL COMPUTATION & PERSISTENCE LAYER                  │   ║
║   │  ┌────────────────────────┐  ┌───────────────────────┐  ┌─────────────────────┐  │   ║
║   │  │ Reducing-Balance EMI   │  │ Rule Depreciation     │  │ SQLAlchemy ORM      │  │   ║
║   │  │ Amortization Schedule  │  │ Actuarial Fallbacks   │  │ SQLite / PostgreSQL │  │   ║
║   │  └────────────────────────┘  └───────────────────────┘  └─────────────────────┘  │   ║
║   └──────────────────────────────────┬───────────────────────────────────────────────┘   ║
║                                      │                                                   ║
║   ┌──────────────────────────────────▼───────────────────────────────────────────────┐   ║
║   │                MODULE 8: STREAMLIT PRESENTATION LAYER (BRUTALIST UI)             │   ║
║   │  [01 Input]  [02 Health]  [03 Depreciation]  [04 Maintenance]                    │   ║
║   │  [05 TCO]    [06 Risk]    [07 Simulator]     [08 Comparison Benchmarks]          │   ║
║   └──────────────────────────────────────────────────────────────────────────────────┘   ║
╚══════════════════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Module Descriptions (8 Core Modules)

### Module 1: Data Ingestion Layer (`src/ingestion/` & `src/data/loader.py`)
- **Purpose:** Ingests heterogeneous automotive records from multiple channels (dealer scraping, OEM MSRP catalogues, live auction partner feeds, and regional fuel price indices).
- **Core Functions:** 
  - Validates schema conformance using strict typed contracts.
  - Implements defensive type-casting, duplicate detection, and missing-value logging.
  - Handles batch loading of historical snapshots (`data/raw/`) and cached runtime listings.

### Module 2: Feature Engineering & Preprocessing (`src/features/` & `src/data/preprocessor.py`)
- **Purpose:** Transforms raw vehicular specifications into high-signal numerical representations optimized for tree-based algorithms and linear estimators.
- **Core Transformations:**
  - `age_mileage_interaction = age_years × annual_km`: Captures compounding degradation for vehicles driven aggressively over long durations.
  - `log_purchase_price = ln(purchase_price)`: Eliminates right-skewness across entry-level hatchbacks to premium luxury sedans.
  - Categorical encoding: One-hot encoding for fuel types (`Petrol`, `Diesel`, `EV`, `CNG`, `Hybrid`) and ordinal rank encoding for geographical city tiers (Tier 1 Metro vs. Tier 2/3).
  - Outlier winsorization and median imputation for sparse technical parameters (e.g. EV battery state of health, torque, power).

### Module 3: ML Model Layer & Forecaster (`src/models/`)
- **Purpose:** Houses predictive machine learning estimators trained with strict cross-validation.
- **Components:**
  - `DepreciationModel` (`XGBoostRegressor`): Predicts percentage residual retention with monotonic constraints (`age_years ≤ 0`, `mileage_km ≤ 0`) to prevent unrealistic value appreciation.
  - `VehicleHealthModel` (`RandomForestClassifier`): Evaluates subsystem wear and maps diagnostic inputs to continuous 0–100 health metrics and qualitative tiers (`Excellent`, `Good`, `Fair`, `Poor`).
  - `MaintenanceModel` (`LightGBMRegressor`): Uses Tweedie loss to forecast annual routine and catastrophic maintenance expenditures.
  - Conformal prediction bounds: Computes 90% confidence intervals around expected residual curves.

### Module 4: Explainability Engine (`src/explainability/` & `src/models/shap_engine.py`)
- **Purpose:** Provides complete algorithmic transparency to satisfy consumer trust and financial regulatory auditing requirements.
- **Components:**
  - Implements TreeSHAP (`shap.TreeExplainer`) on gradient boosted trees.
  - Generates local waterfall plots showing positive/negative contributions of mileage, fuel type, ownership count, and brand reputation to the final valuation.
  - Computes global feature importance rankings across demographic slices.

### Module 5: Risk Engine & Reliability Scoring (`src/risk/`)
- **Purpose:** Synthesizes multifaceted risk vectors into normalized, actionable risk indices.
- **Key Metrics:**
  - **Market Liquidity Risk (0–100):** Evaluates days-on-market metrics and regional demand depth.
  - **Segment Volatility Risk:** Tracks variance in resale realizations within vehicle classes under fluctuating macroeconomic cycles.
  - **Ownership Burden Index:** Compares debt service requirements (EMI) and operational costs against owner income thresholds (FOIR limits).

### Module 6: Scenario Simulator & Monte Carlo (`src/simulator/`)
- **Purpose:** Empowers fleet planners and prospective car owners to stress-test future residual positions against macro volatility.
- **Capabilities:**
  - Monte Carlo simulation: Runs 1,000+ stochastic trials fluctuating annual mileage, fuel price spikes, and unexpected repair shocks.
  - Hold-Sell Optimization: Identifies the optimal exit month where marginal maintenance cost overtakes residual depreciation deceleration.

### Module 7: Financial Computation & Valuation Engine (`src/finance/` & `src/db/`)
- **Purpose:** Executes exact financial mathematics, loan underwriting criteria, and state persistence.
- **Components:**
  - `src/finance/emi.py`: Reducing-balance monthly EMI calculation, full monthly amortization schedules, and Fixed Obligation to Income Ratio (FOIR) underwriting limits.
  - `src/finance/depreciation.py`: Deterministic, actuarial rule-based depreciation curves by fuel type (used as benchmark baseline and ML cold-start fallback).
  - `src/finance/tco.py`: Full multi-year Total Cost of Ownership aggregation (Financing Interest + Depreciation + Fuel + Insurance + Servicing).
  - `src/db/`: SQLAlchemy ORM models, session factories, and database persistence layer for vehicle assets and analysis records.

### Module 8: Streamlit Presentation Layer (`app/`)
- **Purpose:** Delivers a responsive, brutalist/minimalist user interface with instant reactive computation.
- **Modular Views:**
  1. `01_Vehicle_Input.py`: Primary parameter acquisition (specifications, usage patterns, loan terms).
  2. `02_Vehicle_Health.py`: Diagnostics, subsystem degradation scores, and EV battery health (SOH).
  3. `03_Depreciation.py`: 5-year interactive Plotly depreciation trajectory with confidence envelopes.
  4. `04_Maintenance.py`: Predictive servicing schedule and component replacement timelines.
  5. `05_TCO.py`: Comprehensive waterfall breakdown of cumulative 3/5/7-year ownership expenditures.
  6. `06_Risk.py`: Financial exposure radar and liquidity scorecards.
  7. `07_Simulator.py`: Interactive what-if parameter sliders and economic shock testing.
  8. `08_Compare.py`: Multi-vehicle head-to-head benchmarking.

---

## 4. Technology Stack Table

| Layer / Domain | Technology | Minimum Version | Specific Function in AUTOVAULT AI |
|---|---|---|---|
| **User Interface** | Streamlit | ≥ 1.35.0 | Multi-page brutalist web dashboard and reactive state management |
| **Interactive Charts** | Plotly Graph Objects / Express | ≥ 5.20.0 | High-performance interactive depreciation and TCO waterfall charts |
| **Core Residual Model** | XGBoost | ≥ 2.0.0 | Gradient-boosted decision trees with monotonic directional constraints |
| **Maintenance Model** | LightGBM | ≥ 4.3.0 | Fast gradient boosting optimized with Tweedie loss for skewed cost distributions |
| **Health Classification** | scikit-learn | ≥ 1.4.0 | Random Forest classification, preprocessing pipelines, StandardScaler |
| **ML Explainability** | SHAP | ≥ 0.45.0 | TreeExplainer for per-prediction local feature attribution |
| **Data Manipulation** | pandas | ≥ 2.2.0 | High-performance DataFrame querying, aggregation, and time indexing |
| **Numerical Processing** | NumPy | ≥ 1.26.0 | Vectorized amortization math, linear algebra, and Monte Carlo trials |
| **Scientific Computing** | SciPy | ≥ 1.13.0 | Statistical distribution fitting, confidence interval quantiles |
| **Database & ORM** | SQLAlchemy / SQLite / PostgreSQL | ≥ 2.0.0 | Structured persistence of valuation queries, vehicle catalogs, and listings |
| **Environment & Config** | PyYAML / python-dotenv | ≥ 6.0 | Externalized configuration management for financial and ML parameters |
| **Testing Framework** | pytest | ≥ 8.2.0 | Unit, regression, and test coverage validation across financial and ML pipelines |
| **Runtime Environment** | Python (CPython) | 3.11+ | Modern typing, pattern matching, and performance enhancements |

---

## 5. Data Flow

### End-to-End Data Pipeline Architecture

```
  [Raw Listing Portals]      [OEM Spec Sheets]       [PPAC / RBI Financial Feeds]
            │                        │                             │
            ▼                        ▼                             ▼
   ( data/raw/*.csv )       ( vehicle_master.csv )       ( fuel_prices / rates )
            │                        │                             │
            └────────────────────────┼─────────────────────────────┘
                                     │
                                     ▼
                      ┌─────────────────────────────┐
                      │    src/data/loader.py       │
                      │  • Schema validation        │
                      │  • Deduplication            │
                      │  • Type enforcement         │
                      └──────────────┬──────────────┘
                                     │
                                     ▼
                      ┌─────────────────────────────┐
                      │ src/features/pipeline.py    │
                      │  • Missing value imputation │
                      │  • Age × Mileage synthesis  │
                      │  • Categorical encoding     │
                      │  • Outlier winsorization    │
                      └──────────────┬──────────────┘
                                     │
                     ┌───────────────┴───────────────┐
                     │                               │
                     ▼                               ▼
       ┌───────────────────────────┐   ┌───────────────────────────┐
       │   TRAINING PIPELINE       │   │    INFERENCE PIPELINE     │
       │   (scripts/train.py)      │   │   (Live User Session)     │
       │  • Time-based splits      │   │  • Input sanitization     │
       │  • Walk-forward 5-fold CV │   │  • Feature alignment      │
       │  • Hyperparameter tuning  │   │  • Stored model loading   │
       └─────────────┬─────────────┘   └─────────────┬─────────────┘
                     │                               │
                     ▼                               ▼
       ┌───────────────────────────┐   ┌───────────────────────────┐
       │    SERIALIZED ARTIFACTS   │──►│     MODEL ENSEMBLE        │
       │    (models/*.pkl, *.json) │   │  • XGBoost Residuals      │
       │  • Tree models            │   │  • LightGBM Maintenance   │
       │  • Feature encoders       │   │  • RF Health Classifier   │
       │  • Conformal bounds       │   │  • Conformal 90% CI       │
       └───────────────────────────┘   └─────────────┬─────────────┘
                                                     │
                                                     ▼
                                       ┌───────────────────────────┐
                                       │    FINANCIAL SYNTHESIS    │
                                       │  • Reducing EMI Schedule  │
                                       │  • TCO Engine (3/5/7 yr)  │
                                       │  • Risk Score Compilation │
                                       │  • SHAP Local Attribution │
                                       └─────────────┬─────────────┘
                                                     │
                                                     ▼
                                       ┌───────────────────────────┐
                                       │ STREAMLIT BRUTALIST UI    │
                                       │  • Reactive Page Router   │
                                       │  • High-contrast Plots    │
                                       │  • Exportable Ledgers     │
                                       └───────────────────────────┘
```

### Detailed Execution Sequence
1. **User Parameters:** The user specifies vehicle metadata (make, model, year, fuel, purchase price) and operating assumptions (annual mileage, city, loan rate, tenure) via `app/pages/01_Vehicle_Input.py`.
2. **State Propagation:** Values are stored in `st.session_state.vehicle_data` and validated against physical domain bounds.
3. **Dual Forecasting:**
   - **Machine Learning Track:** Features are encoded and fed to the serialized `XGBoost` model to obtain predicted depreciation curves and conformal uncertainty bounds.
   - **Financial Benchmark Track:** `src/finance/depreciation.py` evaluates actuarial baseline curves based on historical powertrain decay benchmarks.
4. **Health & Maintenance Scoring:** `src/models/health_model.py` and `maintenance_model.py` project component wear and calculate annual repair liability.
5. **Ownership Finance Aggregation:** `src/finance/emi.py` computes reducing-balance loan repayments and amortization tables; `src/finance/tco.py` sums all vectors into a multi-year ledger.
6. **Insight & Explanations:** `src/explainability/` evaluates SHAP attributions, identifying the top drivers influencing resale preservation.
7. **Rendering:** Streamlit renders high-contrast brutalist components, metric scorecards, and Plotly visualizations.

---

## 6. Deployment Notes

### 6.1 Local Development Environment

```bash
# Clone the repository
git clone https://github.com/Krishna9531/Auto-Residual-Forecaster.git
cd "Auto Residual Forecaster"

# Initialize Python 3.11 virtual environment
python -m venv venv

# Activate environment (Windows)
venv\Scripts\activate
# Activate environment (Linux / macOS)
source venv/bin/activate

# Install all dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run the test suite
pytest tests/ -v --tb=short

# Launch the Streamlit application
streamlit run app/main.py
```

### 6.2 Containerized Deployment (Docker)

A multi-stage Docker build is recommended for lean production containers:

```dockerfile
FROM python:3.11-slim AS base
WORKDIR /app

# Install system dependencies for scientific libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

To build and run:
```bash
docker build -t autovault-ai:latest .
docker run -p 8501:8501 autovault-ai:latest
```

### 6.3 Continuous Integration & Automation (GitHub Actions)

The repository CI workflow (`.github/workflows/ci.yml`) validates pull requests:
- **Linting & Code Formatting:** Checks code style using `flake8` and `black --check`.
- **Unit & Integration Tests:** Executes all test suites in `tests/` with `pytest`.
- **Inference Smoke Testing:** Validates that `calculate_emi`, `get_yearly_values`, and model predictors execute within memory and latency targets (<500ms).

### 6.4 Production Environment Variables

| Variable Name | Default Value | Description |
|---|---|---|
| `AUTOVAULT_ENV` | `production` | Environment mode (`development`, `staging`, `production`) |
| `AUTOVAULT_DATA_DIR` | `./data` | File system location for raw and master CSV datasets |
| `AUTOVAULT_MODEL_DIR` | `./models` | File system location for serialized ML artifacts |
| `DATABASE_URL` | `sqlite:///autovault.db` | SQLAlchemy connection URI (e.g. `postgresql://user:pass@host:5432/autovault`) |
| `STREAMLIT_SERVER_PORT` | `8501` | Port on which the web dashboard listens |
| `LOG_LEVEL` | `INFO` | Application logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
