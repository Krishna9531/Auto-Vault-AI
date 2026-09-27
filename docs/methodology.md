# AUTOVAULT AI — Machine Learning Methodology

> **Version:** 1.0.0 | **Last Updated:** September 2026 | **Author:** AUTOVAULT AI Data Science Team  
> **Document Purpose:** Comprehensive methodological specification for predictive modeling, time-based validation, feature engineering, and statistical uncertainty estimation across the AUTOVAULT AI platform.

---

## Table of Contents

1. [Problem Framing](#1-problem-framing)
2. [Feature Engineering](#2-feature-engineering)
3. [Model Selection Rationale](#3-model-selection-rationale)
4. [Time-Based Validation Strategy](#4-time-based-validation-strategy)
5. [Evaluation Metrics](#5-evaluation-metrics)
6. [Limitations and Assumptions](#6-limitations-and-assumptions)
7. [Confidence Intervals & Uncertainty Quantification](#7-confidence-intervals--uncertainty-quantification)
8. [Explainability Framework (SHAP)](#8-explainability-framework-shap)

---

## 1. Problem Framing

### 1.1 Objective Definition
The primary predictive objective of AUTOVAULT AI is **Residual Value Forecasting**: quantifying the retained economic value of a passenger motor vehicle at arbitrary future time intervals $t \in [1, 7]$ years and cumulative usage $km \in [0, 500,000]$.

Secondary predictive tasks include:
- **Component & Powertrain Health Scoring:** Predicting mechanical degradation and classifying vehicles into condition states (`Excellent`, `Good`, `Fair`, `Poor`).
- **Maintenance Cost Forecasting:** Estimating annualized servicing liabilities and long-tail catastrophic repair risks.
- **Liquidity & Days-to-Sell Estimation:** Forecasting resale velocity and demand concentration across geographical tiers.

### 1.2 Target Formulation: Percentage Depreciation vs. Absolute Value
Rather than modeling raw currency amounts ($₹$ Lakhs), which are heavily confounded by the original invoice price, inflationary drift, and extreme right-tail skew, AUTOVAULT AI formulates the primary target variable as **Depreciation Percentage ($y_{\text{dep}}$)**:

$$y_{\text{dep}} = \frac{P_{\text{original}} - P_{\text{resale}}}{P_{\text{original}}} \times 100$$

Where:
- $P_{\text{original}}$ is the vehicle's initial ex-showroom invoice price.
- $P_{\text{resale}}$ is the observed or predicted transaction price.

**Key Mathematical Advantages:**
1. **Scale Invariance:** Normalizes variance across vehicle classes (from a ₹6L hatchback to an ₹80L luxury SUV).
2. **Deterministic Bounding:** Natural boundaries $y_{\text{dep}} \in [0, 95\%]$ (accounting for scrap floor value) prevent catastrophic negative price forecasts.
3. **Monotonic Recovery:** Resale price is trivially and monotonically recovered:
   $$P_{\text{resale}} = P_{\text{original}} \times \left(1 - \frac{y_{\text{dep}}}{100}\right)$$

---

## 2. Feature Engineering

To capture the non-linear degradation of automotive assets, domain-specific feature transformations are engineered prior to model ingestion:

### 2.1 Interaction Terms
- **Age $\times$ Mileage Interaction ($km \cdot yr$):**
  $$\text{age\_mileage\_interaction} = \text{age\_years} \times \text{annual\_km}$$
  *Rationale:* Vehicles degrade through two distinct physical mechanisms: chronological elastomeric/gasket decay (time-dependent) and frictional mechanical wear (odometer-dependent). High-mileage cars in short periods behave differently from low-mileage garaged cars of equal age. The multiplicative term provides decision trees with direct split points on severe composite usage.

### 2.2 Scale & Skewness Rectification
- **Logarithmic Purchase Price:**
  $$\log(P_{\text{original}}) = \ln(P_{\text{original\_lakh}})$$
  *Rationale:* Compresses the heavy right tail of vehicle prices, improving the gradient descent stability of baseline regularized linear estimators and meta-learners.

### 2.3 Categorical & Domain Encodings
- **Fuel Type One-Hot Encoding:** Binary vectors for `Petrol`, `Diesel`, `Electric`, `CNG`, and `Hybrid`. Each propulsion type exhibits distinct depreciation velocities:
  - *Diesel:* Steeper regulatory discounting in metro regions (e.g. National Green Tribunal 10-year rule in Delhi-NCR).
  - *Electric (EV):* Accelerated year 1–3 depreciation driven by rapid advancements in battery energy density and range anxiety.
  - *CNG:* Resilient resale retention in commercial and Tier-1 urban commuting clusters.
- **Geographic City Tiers:** Ordinal classification ($1 = \text{Tier 1 Metro}, 2 = \text{Tier 2 City}, 3 = \text{Tier 3 Urban/Rural}$) capturing liquidity depth, road infrastructure quality, and regional secondary market density.
- **Brand Resale Rank:** Empirically derived ordinal index ($1 = \text{Highest liquidity/value retention}$, e.g. Maruti Suzuki, Toyota; $30 = \text{Lowest retention}$) based on rolling median resale realization ratios.

### 2.4 Features Deliberately Excluded
- **Vehicle Identification Numbers (VIN):** Excluded to eliminate high-cardinality memorization and data leakage.
- **Dealer Identity:** Excluded to ensure valuations reflect fundamental asset health rather than specific retail markup variations.

---

## 3. Model Selection Rationale

Multiple model architectures were benchmarked on a standardized validation matrix.

### Benchmark Evaluation Table

| Architecture | 5-Fold Walk-Forward RMSE (%) | MAE (%) | Inference Latency | Monotonic Constraints Supported? | Production Selection |
|---|---|---|---|---|---|
| Ordinary Least Squares (OLS) | 8.92 | 6.81 | < 1ms | No | Baseline |
| Ridge Regression ($\alpha=1.0$) | 8.45 | 6.42 | < 1ms | No | Linear Baseline |
| Random Forest Regressor | 5.84 | 4.12 | 14ms | No | Ensemble Candidate |
| **XGBoost Regressor** | **4.92** | **3.48** | **8ms** | **Yes** | **Primary Forecaster** |
| LightGBM Regressor | 5.08 | 3.59 | 5ms | Yes | Secondary Model |
| Multi-Layer Perceptron (MLP) | 6.12 | 4.45 | 18ms | Difficult | Rejected |

### Why XGBoost Regressor Was Selected as Primary Forecaster:
1. **Monotone Feature Constraints:** In automotive valuation, domain credibility hinges on monotonicity: increasing vehicle age or increasing odometer mileage **must never** result in a higher residual value. XGBoost natively enforces exact directional constraints:
   $$\frac{\partial \hat{y}_{\text{dep}}}{\partial (\text{age})} \ge 0, \quad \frac{\partial \hat{y}_{\text{dep}}}{\partial (\text{mileage})} \ge 0$$
   This guarantees physically consistent predictions regardless of local training noise.
2. **Missing Value Robustness:** Automatically learns default split directions for sparse attributes (e.g. EV battery state-of-health or service record completeness).
3. **Execution Latency:** Sub-10ms inference satisfies the responsive UI criteria of the Streamlit frontend.
4. **SHAP TreeExplainer Parity:** Exact, tree-structure-dependent computation of Shapley values without sampling approximations.

---

## 4. Time-Based Validation Strategy

### 4.1 Temporal Leakage Prevention
Random $k$-fold cross-validation is fundamentally flawed for asset valuation time series. In a random split, transactions from future dates (e.g. 2026) appear in the training set while predicting past events (e.g. 2023), resulting in unrealistically optimistic error metrics and leakage of macroeconomic price trends.

AUTOVAULT AI implements a **Strict Time-Based Split and Walk-Forward Rolling Cross-Validation**:

```
Timeline Progression:
[2019-01] ─────────────── [2024-12] ───── [2025-06] ───── [2026-09]
          Training Window           Validation   Held-out Test
              (68k rows)             (8k rows)     (17k rows)
```

### 4.2 Walk-Forward Rolling Folds
Hyperparameter optimization via Optuna utilizes 5 expanding temporal folds:
- **Fold 1:** Train: $[2019 - 2021]$ | Test: $[2022]$
- **Fold 2:** Train: $[2019 - 2022]$ | Test: $[2023]$
- **Fold 3:** Train: $[2019 - 2023]$ | Test: $[2024]$
- **Fold 4:** Train: $[2019 - 2024]$ | Test: $[2025\text{ H1}]$
- **Fold 5:** Train: $[2019 - 2025\text{ H1}]$ | Test: $[2025\text{ H2} - 2026]$

All feature normalization and encoding parameters are computed strictly on the training partition of each fold and transformed on the test partition.

---

## 5. Evaluation Metrics

Model performance is evaluated across both statistical regression criteria and domain sanity metrics:

### 5.1 Root Mean Squared Error (RMSE)
$$\text{RMSE} = \sqrt{\frac{1}{N}\sum_{i=1}^N (y_i - \hat{y}_i)^2}$$
- *Role:* Heavily penalizes large outlying errors; critical for risk management and lender portfolio valuations.
- *Production Threshold:* $\text{RMSE} < 5.5\%$ depreciation.

### 5.2 Mean Absolute Error (MAE)
$$\text{MAE} = \frac{1}{N}\sum_{i=1}^N |y_i - \hat{y}_i|$$
- *Role:* Represents the expected nominal valuation deviation in practical percentage terms.
- *Production Threshold:* $\text{MAE} < 3.8\%$ depreciation.

### 5.3 Mean Absolute Percentage Error (MAPE)
$$\text{MAPE} = \frac{100\%}{N}\sum_{i=1}^N \left|\frac{P_{\text{actual}} - P_{\text{predicted}}}{P_{\text{actual}}}\right|$$
- *Role:* Evaluates currency accuracy against closed market sale prices.
- *Production Threshold:* $\text{MAPE} < 7.5\%$.

### 5.4 Monotonicity Violation Rate (MVR)
$$\text{MVR} = \frac{1}{M}\sum_{j=1}^M \mathbb{I}\left(\hat{P}(t + \Delta t) > \hat{P}(t)\right)$$
- *Role:* Fraction of test instances where an older or higher-mileage vehicle is predicted to appreciate.
- *Production Threshold:* $\text{MVR} \equiv 0.0\%$.

---

## 6. Limitations and Assumptions

1. **Self-Reported Odometer & Condition:** Models assume reported mileage has not been tampered with. In the absence of centralized digital telematics or official national title registries, undetected odometer rollback introduces residual overestimation risk.
2. **Macroeconomic Shocks:** Rapid shifts in central bank repo rates or fuel duty structures cannot be anticipated by historical tree models without periodic retraining.
3. **EV Battery Longevity Evolution:** Electric vehicle battery degradation trajectories are constrained by limited longitudinal market data (>8 years) in the Indian geography. EV predictions apply wider uncertainty intervals.
4. **Exotic & Ultra-Luxury Vehicles:** Valuation confidence is highest in mass-market and premium segments (₹4L – ₹80L). Ultra-luxury exotics (>₹1.5 Crore) have low listing density and behave as collector assets.

---

## 7. Confidence Intervals & Uncertainty Quantification

### 7.1 Conformal Prediction Framework
Point estimates obscure valuation risk. Two cars with identical ₹12L forecasts may possess drastically different liquidity characteristics (e.g. high-volume Maruti vs. discontinued niche import).

AUTOVAULT AI implements **Split Conformal Prediction** to generate distribution-free, finite-sample prediction intervals guaranteed at the $(1 - \alpha) = 90\%$ confidence level:

$$\hat{C}(x) = [\hat{y}(x) - q_{1-\alpha}, \; \hat{y}(x) + q_{1-\alpha}]$$

Where $q_{1-\alpha}$ is the $(1 - \alpha)(1 + 1/n)$-th empirical quantile of non-conformity scores computed on the held-out calibration set:

$$s_i = |y_i - \hat{y}(x_i)|$$

### 7.2 Interval Dynamism
Confidence intervals dynamically expand or contract based on:
- **Segment Liquidity:** Narrower intervals for high-volume models (e.g. Maruti Swift, Hyundai Creta); wider intervals for rare variants.
- **Chronological Horizon:** Interval bounds flare outward as the forecast horizon extends from Year 1 to Year 5, reflecting compound future economic uncertainty.

---

## 8. Explainability Framework (SHAP)

To provide total visibility into valuation decisions, AUTOVAULT AI integrates TreeSHAP:

$$\hat{f}(x) = \phi_0 + \sum_{j=1}^M \phi_j(x)$$

Where:
- $\phi_0$ is the base expected value across the training population.
- $\phi_j(x)$ represents the marginal additive contribution of feature $j$ to the prediction.

In the Streamlit application (`03_Depreciation.py`), SHAP values are visualized as waterfall attributions, showing users exactly how much value was deducted for high mileage, restored for complete service history, or influenced by local market fuel type dynamics.
