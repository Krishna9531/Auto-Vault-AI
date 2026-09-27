# AUTOVAULT AI — Data Dictionary

> **Version:** 1.0.0 | **Last Updated:** September 2026 | **Author:** AUTOVAULT AI Team
> This document describes every database table, master CSV, and processed dataset utilised across the AUTOVAULT AI platform. It serves as the single source of truth for column schemas, data types, physical units, nullability, and business descriptions.

---

## Table of Contents

1. [vehicle_master.csv](#1-vehicle_mastercsv)
2. [vehicles_raw.csv](#2-vehicles_rawcsv)
3. [market_listings.csv](#3-market_listingscsv)
4. [fuel_prices.csv](#4-fuel_pricescsv)
5. [insurance_rates.csv](#5-insurance_ratescsv)
6. [maintenance_records.csv](#6-maintenance_recordscsv)
7. [city_tiers.csv](#7-city_tierscsv)
8. [processed/features_train.csv](#8-processedfeatures_traincsv)
9. [processed/features_test.csv](#9-processedfeatures_testcsv)
10. [Database ORM Tables](#10-database-orm-tables)

---

## 1. `vehicle_master.csv`

**Source:** Official OEM catalogues, ARAI certification bulletins, and curated Indian automotive specs.  
**Location:** `data/vehicle_master.csv` (or `data/raw/vehicle_master.csv`)  
**Purpose:** Canonical benchmark dataset defining production models, trim specifications, baseline prices, and factory ratings used throughout exploratory analyses, model lookups, and TCO calculations.

| Column | Type | Unit | Description | Nullable | Example Value |
|---|---|---|---|---|---|
| `vehicle_id` | str | — | Unique internal vehicle identifier | No | `VM-HYU-CRT-01` |
| `brand` | str | — | Vehicle manufacturer name | No | `Hyundai` |
| `model` | str | — | Primary vehicle model line | No | `Creta` |
| `variant` | str | — | Specific trim level / package designation | No | `SX(O) Turbo` |
| `body_type` | str | — | Body classification (`Hatchback`, `Sedan`, `SUV`, `MUV`, `Coupe`) | No | `SUV` |
| `segment` | str | — | Market segment class (`A`, `B`, `C`, `D`, `E`, `Luxury`) | No | `C` |
| `fuel_type` | str | — | Primary propulsion energy (`Petrol`, `Diesel`, `Electric`, `CNG`, `Hybrid`) | No | `Petrol` |
| `transmission` | str | — | Transmission type (`Manual`, `Automatic`, `DCT`, `CVT`, `AMT`) | No | `Automatic` |
| `manufacture_year` | int | Year | Calendar year of manufacture | No | `2022` |
| `ex_showroom_price` | float | ₹ (INR) | Original ex-showroom sticker price in Indian Rupees | No | `1850000.0` |
| `purchase_price_lakh` | float | ₹ Lakh | Purchase price normalised in Lakhs (1 Lakh = ₹1,00,000) | No | `18.5` |
| `engine_cc` | int | cc | Internal combustion engine displacement (0 for EVs) | Yes | `1497` |
| `power_bhp` | float | BHP | Peak brake horsepower output | No | `138.0` |
| `torque_nm` | float | Nm | Peak engine or motor torque output | No | `242.0` |
| `claimed_mileage_kmpl` | float | km/L | ARAI-certified fuel efficiency (km per litre) | Yes | `16.8` |
| `battery_capacity_kwh` | float | kWh | Total usable battery pack energy (EV only) | Yes | `40.5` |
| `electric_range_km` | float | km | ARAI/MIDC certified all-electric driving range | Yes | `312.0` |
| `seating_capacity` | int | Persons | Number of passenger seats | No | `5` |
| `ground_clearance_mm` | int | mm | Unladen vehicle ground clearance | Yes | `190` |
| `safety_rating_stars` | int | Stars | Global NCAP / Bharat NCAP crash safety rating (0–5) | Yes | `3` |
| `warranty_years` | int | Years | Standard factory warranty duration | No | `3` |
| `baseline_residual_5yr` | float | ₹ Lakh | Estimated actuarial residual value after 5 years standard use | No | `9.25` |

---

## 2. `vehicles_raw.csv`

**Source:** Aggregated web scraped listings from Indian used car marketplaces (Cars24, CarDekho, OLX Autos).  
**Location:** `data/raw/vehicles_raw.csv`  
**Purpose:** Historical used car transaction and listing records used for ML training and validation.

| Column | Type | Unit | Description | Nullable | Example Value |
|---|---|---|---|---|---|
| `listing_id` | str | — | Source listing identifier with platform prefix | No | `CD-4872931` |
| `brand` | str | — | Manufacturer name | No | `Hyundai` |
| `model` | str | — | Model name | No | `Creta` |
| `variant` | str | — | Variant name | Yes | `SX(O)` |
| `fuel_type` | str | — | Fuel classification | No | `Petrol` |
| `transmission` | str | — | `Manual` or `Automatic` | No | `Automatic` |
| `manufacture_year` | int | Year | Year vehicle rolled off the assembly line | No | `2021` |
| `registration_year` | int | Year | Year of official registration with state RTO | Yes | `2021` |
| `age_years` | float | Years | Fractional vehicle age at time of listing (`current_year - mfg_year`) | No | `3.5` |
| `mileage_km` | int | km | Total odometer distance travelled | No | `42500` |
| `annual_km` | float | km/yr | Derived annual usage rate (`mileage_km / age_years`) | No | `12142.8` |
| `purchase_price_lakh` | float | ₹ Lakh | Original purchase ex-showroom cost in Lakhs | Yes | `18.5` |
| `listing_price_lakh` | float | ₹ Lakh | Current asking price posted by seller | No | `12.8` |
| `negotiated_price_lakh` | float | ₹ Lakh | Final verified transaction price (if closed sale) | Yes | `12.2` |
| `num_owners` | int | Count | Number of prior registered vehicle owners | No | `1` |
| `city` | str | — | Listing municipality | No | `Mumbai` |
| `state` | str | — | State abbreviation | No | `MH` |
| `service_history_complete` | bool | — | Boolean flag indicating complete OEM service stamps | No | `True` |
| `accident_history` | bool | — | Boolean flag indicating past insurance claim / accident record | No | `False` |
| `insurance_valid` | bool | — | Flag indicating active insurance policy | Yes | `True` |
| `scrape_date` | date | YYYY-MM-DD | Date record was scraped | No | `2026-08-15` |
| `sold` | bool | — | Flag indicating whether the vehicle was marked sold | Yes | `True` |

---

## 3. `market_listings.csv`

**Source:** Real-time auction APIs and live dealer platform inventory feeds.  
**Location:** `data/raw/market_listings.csv`  
**Purpose:** Provides immediate active inventory depth, price spreads, and platform demand velocity.

| Column | Type | Unit | Description | Nullable | Example Value |
|---|---|---|---|---|---|
| `listing_id` | str | — | Unique active inventory identifier | No | `C24-9031827` |
| `brand` | str | — | Vehicle brand | No | `Maruti Suzuki` |
| `model` | str | — | Model name | No | `Swift` |
| `fuel_type` | str | — | Fuel type | No | `Petrol` |
| `listing_price_lakh` | float | ₹ Lakh | Real-time seller asking price | No | `7.40` |
| `city` | str | — | Geolocation market city | No | `Pune` |
| `demand_score` | float | 0–100 | Platform proprietary listing popularity index | Yes | `72.3` |
| `days_on_market` | int | Days | Number of days listing has remained active | No | `18` |
| `similar_listings_count` | int | Count | Total comparable active units in the same market radius | No | `47` |
| `price_vs_avg_pct` | float | % | Deviation from regional segment average asking price | No | `-4.2` |
| `fetch_date` | date | YYYY-MM-DD | Ingestion timestamp | No | `2026-09-20` |

---

## 4. `fuel_prices.csv`

**Source:** Petroleum Planning & Analysis Cell (PPAC), Ministry of Petroleum and Natural Gas, India.  
**Location:** `data/raw/fuel_prices.csv`  
**Purpose:** Historical and prevailing fuel/energy retail rates used in TCO modeling.

| Column | Type | Unit | Description | Nullable | Example Value |
|---|---|---|---|---|---|
| `date` | date | YYYY-MM-DD | Effective rate date | No | `2026-09-01` |
| `city` | str | — | Indian municipality | No | `Delhi` |
| `state` | str | — | Indian state / union territory abbreviation | No | `DL` |
| `petrol_price_per_litre` | float | ₹/L | Retail pump price for standard petrol | No | `96.72` |
| `diesel_price_per_litre` | float | ₹/L | Retail pump price for standard diesel | No | `89.62` |
| `cng_price_per_kg` | float | ₹/kg | Retail compressed natural gas pump price | Yes | `75.50` |
| `electricity_tariff_kwh` | float | ₹/kWh | Residential slab rate for home EV charging | Yes | `7.80` |

---

## 5. `insurance_rates.csv`

**Source:** Insurance Regulatory and Development Authority of India (IRDAI) grid and aggregator actuarial tables.  
**Location:** `data/raw/insurance_rates.csv`  
**Purpose:** Determines annual insurance premium curves based on segment, age, and IDV.

| Column | Type | Unit | Description | Nullable | Example Value |
|---|---|---|---|---|---|
| `segment` | str | — | Segment tier (`A`, `B`, `C`, `D`, `E`, `Luxury`) | No | `C` |
| `fuel_type` | str | — | Vehicle fuel type | No | `Petrol` |
| `age_band` | str | — | Age category (`0-1yr`, `1-3yr`, `3-5yr`, `5-10yr`, `10yr+`) | No | `1-3yr` |
| `idv_pct_of_original` | float | % | Insured Declared Value as % of original invoice | No | `70.0` |
| `base_premium_pct` | float | % of IDV | Comprehensive own-damage annual premium rate | No | `2.10` |
| `zero_dep_addon_pct` | float | % of IDV | Zero-depreciation bumper-to-bumper rider rate | Yes | `0.35` |
| `third_party_fixed_inr` | float | ₹ (INR) | Mandatory statutory third-party liability premium | No | `3416.0` |
| `ncb_discount_pct` | float | % | Maximum allowable No-Claim Bonus discount | No | `25.0` |

---

## 6. `maintenance_records.csv`

**Source:** Anonymized authorized dealership service history logs and fleet telematics.  
**Location:** `data/raw/maintenance_records.csv`  
**Purpose:** Training data for component wear curves and LightGBM repair cost forecasting.

| Column | Type | Unit | Description | Nullable | Example Value |
|---|---|---|---|---|---|
| `record_id` | str | — | Unique hash of maintenance invoice | No | `SRV-894721` |
| `brand` | str | — | Vehicle brand | No | `Tata` |
| `model` | str | — | Vehicle model | No | `Nexon` |
| `fuel_type` | str | — | Vehicle fuel type | No | `Diesel` |
| `odometer_at_service` | int | km | Odometer reading when service was opened | No | `45000` |
| `vehicle_age_at_service` | float | Years | Fractional age when vehicle was serviced | No | `3.2` |
| `service_type` | str | — | Category (`Scheduled`, `Unscheduled`, `Recall`, `Warranty`) | No | `Scheduled` |
| `component_category` | str | — | Subsystem (`Engine`, `Brakes`, `Suspension`, `Electrical`, `Battery`) | No | `Brakes` |
| `parts_cost` | float | ₹ (INR) | Total cost of replacement parts and consumables | No | `4200.0` |
| `labour_cost` | float | ₹ (INR) | Total workshop labour charges | No | `1800.0` |
| `total_bill_amount` | float | ₹ (INR) | Net invoice total inclusive of GST | No | `7080.0` |

---

## 7. `city_tiers.csv`

**Source:** Ministry of Housing and Urban Affairs (MoHUA) tier classifications.  
**Location:** `data/raw/city_tiers.csv`  
**Purpose:** Provides geographic economic clustering and infrastructure density metrics.

| Column | Type | Unit | Description | Nullable | Example Value |
|---|---|---|---|---|---|
| `city` | str | — | Official city name | No | `Bangalore` |
| `state` | str | — | State abbreviation | No | `KA` |
| `tier` | int | 1/2/3 | Government economic classification (1=Metro, 2=City, 3=Town) | No | `1` |
| `charging_stations_count` | int | Count | Registered public EV commercial charging stations | Yes | `840` |
| `road_quality_index` | float | 0–10 | Standardized municipal infrastructure index | Yes | `7.2` |

---

## 8. `processed/features_train.csv` & `processed/features_test.csv`

**Source:** Output of feature engineering pipeline applied to historical listing data.  
**Location:** `data/processed/features_train.csv`, `data/processed/features_test.csv`  
**Purpose:** Exact numerical matrices passed to XGBoost, LightGBM, and Random Forest models.

| Column | Type | Unit | Mathematical Rationale / Description | Nullable | Example Value |
|---|---|---|---|---|---|
| `age_years` | float | Years | Standardized vehicle chronological age | No | `3.5` |
| `mileage_km` | int | km | Odometer reading | No | `42500` |
| `annual_km` | float | km/yr | Normalized annual intensity (`mileage_km / age_years`) | No | `12142.8` |
| `age_mileage_interaction` | float | km·yr | Product interaction capturing accelerated wear | No | `42500.0` |
| `purchase_price_lakh` | float | ₹ Lakh | Baseline ex-showroom price | No | `18.5` |
| `log_purchase_price` | float | log(₹ Lakh) | Natural log of purchase price to compress tail skewness | No | `2.917` |
| `fuel_type_petrol` | int | 0/1 | Binary indicator for Petrol | No | `1` |
| `fuel_type_diesel` | int | 0/1 | Binary indicator for Diesel | No | `0` |
| `fuel_type_electric` | int | 0/1 | Binary indicator for Electric | No | `0` |
| `fuel_type_cng` | int | 0/1 | Binary indicator for CNG | No | `0` |
| `fuel_type_hybrid` | int | 0/1 | Binary indicator for Hybrid | No | `0` |
| `transmission_auto` | int | 0/1 | Binary indicator: 1 = Automatic, 0 = Manual | No | `1` |
| `num_owners` | int | Count | Previous owners count | No | `1` |
| `service_history_complete` | int | 0/1 | 1 if complete OEM stamps verified, else 0 | No | `1` |
| `accident_history` | int | 0/1 | 1 if structural accident history recorded, else 0 | No | `0` |
| `city_tier` | int | 1/2/3 | Ordinal city tier classification | No | `1` |
| `brand_popularity_rank` | int | 1–30 | Brand resale liquidity ranking (1 = highest demand) | No | `2` |
| `target_depreciation_pct` | float | % | **Target Variable:** `((purchase_price - resale_price) / purchase_price) × 100` | No | `34.1` |

---

## 9. Database ORM Tables (`src/db/models.py`)

When persisting interactive valuations, scenarios, and user histories, AUTOVAULT AI maps data to relational schemas via SQLAlchemy:

### 9.1 Table: `vehicles`
Stores core vehicle specifications and catalog records.
- `id` (Integer, Primary Key)
- `brand` (String(64), Non-null)
- `model` (String(64), Non-null)
- `variant` (String(64), Nullable)
- `fuel_type` (String(32), Non-null)
- `manufacture_year` (Integer, Non-null)
- `purchase_price` (Float, Non-null) — In INR
- `created_at` (DateTime, Default UTC)

### 9.2 Table: `valuations`
Records forecasted residual value evaluations generated by the model engine.
- `id` (Integer, Primary Key)
- `vehicle_id` (Integer, Foreign Key → `vehicles.id`)
- `current_mileage` (Integer, Non-null)
- `annual_mileage` (Integer, Non-null)
- `predicted_current_val` (Float, Non-null) — Resale value today in INR
- `predicted_val_yr1` through `predicted_val_yr5` (Float) — 5-year trajectory
- `ci_lower_bound` (Float, Non-null) — Lower 90% confidence bound
- `ci_upper_bound` (Float, Non-null) — Upper 90% confidence bound
- `model_version` (String(32), Non-null)
- `created_at` (DateTime, Default UTC)

### 9.3 Table: `loan_records`
Underwriting records and amortization parameters from the financing engine.
- `id` (Integer, Primary Key)
- `vehicle_id` (Integer, Foreign Key → `vehicles.id`)
- `principal_amount` (Float, Non-null)
- `annual_rate_pct` (Float, Non-null)
- `tenure_months` (Integer, Non-null)
- `monthly_emi` (Float, Non-null)
- `total_interest` (Float, Non-null)
- `total_payment` (Float, Non-null)
- `applicant_monthly_income` (Float, Nullable)
- `foir_ratio_pct` (Float, Nullable)
- `created_at` (DateTime, Default UTC)

### 9.4 Table: `risk_assessments`
Multifaceted risk scores computed by Module 5.
- `id` (Integer, Primary Key)
- `vehicle_id` (Integer, Foreign Key → `vehicles.id`)
- `overall_health_score` (Integer, 0–100)
- `liquidity_risk_score` (Integer, 0–100)
- `volatility_risk_score` (Integer, 0–100)
- `composite_risk_rating` (String(16)) — `Low`, `Medium`, `High`, `Critical`
- `created_at` (DateTime, Default UTC)
