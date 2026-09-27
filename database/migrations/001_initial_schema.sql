-- Migration 001: Initial Schema setup for AUTOVAULT AI

CREATE TABLE vehicles (
    vehicle_id SERIAL PRIMARY KEY,
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    variant VARCHAR(100) NOT NULL,
    year INT NOT NULL,
    fuel_type VARCHAR(50) NOT NULL,
    transmission VARCHAR(50) NOT NULL,
    engine_cc INT,
    power_bhp INT,
    torque_nm INT,
    claimed_mileage_kmpl DECIMAL(10, 2),
    seating_capacity INT NOT NULL,
    kerb_weight_kg INT,
    fuel_tank_l DECIMAL(10, 2),
    battery_capacity_kwh DECIMAL(10, 2),
    range_km INT,
    charging_speed_kw DECIMAL(10, 2),
    warranty_years INT,
    service_interval_km INT,
    base_price_lakh DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE vehicle_specs (
    spec_id SERIAL PRIMARY KEY,
    vehicle_id INT REFERENCES vehicles(vehicle_id) ON DELETE CASCADE,
    spec_key VARCHAR(100) NOT NULL,
    spec_value VARCHAR(255) NOT NULL,
    unit VARCHAR(50),
    source VARCHAR(255)
);

CREATE TABLE used_vehicle_listings (
    listing_id SERIAL PRIMARY KEY,
    vehicle_id INT REFERENCES vehicles(vehicle_id) ON DELETE CASCADE,
    listing_date DATE NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100),
    manufacture_year INT NOT NULL,
    current_age_years DECIMAL(10, 2) NOT NULL,
    odometer_km INT NOT NULL,
    num_owners INT,
    accident_history BOOLEAN,
    service_history_complete BOOLEAN,
    color VARCHAR(50),
    transmission VARCHAR(50),
    listing_price_lakh DECIMAL(10, 2) NOT NULL,
    source_platform VARCHAR(100),
    url TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE maintenance_schedule (
    schedule_id SERIAL PRIMARY KEY,
    vehicle_id INT REFERENCES vehicles(vehicle_id) ON DELETE CASCADE,
    service_km INT NOT NULL,
    service_type VARCHAR(100),
    parts TEXT[],
    estimated_cost_inr DECIMAL(10, 2),
    labour_cost_inr DECIMAL(10, 2),
    source VARCHAR(255)
);

CREATE TABLE maintenance_events (
    event_id SERIAL PRIMARY KEY,
    vehicle_id INT REFERENCES vehicles(vehicle_id) ON DELETE CASCADE,
    event_km INT NOT NULL,
    event_age_months INT,
    event_type VARCHAR(100),
    actual_cost_inr DECIMAL(10, 2),
    severity VARCHAR(50),
    source VARCHAR(255)
);

CREATE TABLE fuel_prices (
    price_id SERIAL PRIMARY KEY,
    fuel_type VARCHAR(50) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    price_per_litre DECIMAL(10, 2) NOT NULL,
    effective_date DATE NOT NULL,
    source VARCHAR(255)
);

CREATE TABLE battery_cycles (
    cycle_id SERIAL PRIMARY KEY,
    battery_id VARCHAR(100) NOT NULL,
    cycle_number INT NOT NULL,
    temperature_celsius DECIMAL(10, 2),
    voltage_v DECIMAL(10, 4),
    current_a DECIMAL(10, 4),
    capacity_ah DECIMAL(10, 4),
    soh_percent DECIMAL(5, 2),
    dod_percent DECIMAL(5, 2),
    chemistry VARCHAR(50),
    source_dataset VARCHAR(255)
);

CREATE TABLE insurance_rates (
    rate_id SERIAL PRIMARY KEY,
    vehicle_id INT REFERENCES vehicles(vehicle_id) ON DELETE CASCADE,
    insurer VARCHAR(100) NOT NULL,
    coverage_type VARCHAR(100),
    annual_premium_lakh DECIMAL(10, 2) NOT NULL,
    idv_lakh DECIMAL(10, 2) NOT NULL,
    year INT NOT NULL,
    source VARCHAR(255)
);

CREATE TABLE financing_rates (
    rate_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL,
    loan_type VARCHAR(100),
    min_rate_percent DECIMAL(5, 2),
    max_rate_percent DECIMAL(5, 2),
    max_tenure_months INT,
    processing_fee_percent DECIMAL(5, 2),
    effective_date DATE NOT NULL
);

CREATE TABLE predictions (
    prediction_id SERIAL PRIMARY KEY,
    vehicle_id INT REFERENCES vehicles(vehicle_id) ON DELETE CASCADE,
    prediction_type VARCHAR(50) NOT NULL,
    input_json JSONB,
    output_json JSONB,
    confidence_score DECIMAL(5, 4),
    model_version VARCHAR(50),
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE scenarios (
    scenario_id SERIAL PRIMARY KEY,
    user_session TEXT,
    vehicle_id INT REFERENCES vehicles(vehicle_id) ON DELETE CASCADE,
    scenario_params JSONB,
    results JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_vehicles_brand_model ON vehicles(brand, model);
CREATE INDEX idx_used_vehicle_listings_vehicle_id ON used_vehicle_listings(vehicle_id);
CREATE INDEX idx_fuel_prices_effective_date ON fuel_prices(effective_date);
CREATE INDEX idx_battery_cycles_battery_id ON battery_cycles(battery_id);
CREATE INDEX idx_predictions_vehicle_id ON predictions(vehicle_id);
