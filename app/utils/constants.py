"""Constants for the AUTOVAULT AI project."""

BRAND_LIST = [
    "Maruti Suzuki", "Hyundai", "Tata", "Mahindra", "Kia", "Toyota", "Honda",
    "Skoda", "Volkswagen", "Renault", "MG", "Nissan", "Jeep", "Citroen",
    "BMW", "Mercedes-Benz", "Audi", "Volvo", "Jaguar", "Land Rover"
]

MODEL_DATA = {
    "Maruti Suzuki": ["Swift", "Baleno", "WagonR", "Brezza", "Ertiga", "Fronx", "Grand Vitara"],
    "Hyundai": ["Creta", "Venue", "i20", "Grand i10 Nios", "Verna", "Tucson"],
    "Tata": ["Nexon", "Punch", "Harrier", "Safari", "Tiago", "Altroz"],
    "Mahindra": ["Scorpio-N", "XUV700", "Thar", "Bolero", "XUV300"],
    "Kia": ["Seltos", "Sonet", "Carens"],
    "Toyota": ["Innova Crysta", "Fortuner", "Glanza", "Urban Cruiser Hyryder"],
    "Honda": ["City", "Amaze", "Elevate"],
    "Skoda": ["Kushaq", "Slavia", "Kodiaq"],
    "Volkswagen": ["Taigun", "Virtus", "Tiguan"],
    "Renault": ["Kiger", "Triber", "Kwid"],
    "MG": ["Hector", "Astor", "Gloster", "Comet EV"],
    "Nissan": ["Magnite"],
    "Jeep": ["Compass", "Meridian"],
    "Citroen": ["C3", "C3 Aircross", "C5 Aircross"],
    "BMW": ["3 Series", "5 Series", "X1", "X3", "X5"],
    "Mercedes-Benz": ["C-Class", "E-Class", "GLC", "GLE"],
    "Audi": ["A4", "A6", "Q3", "Q5", "Q7"],
    "Volvo": ["XC40", "XC60", "XC90"],
    "Jaguar": ["F-Pace"],
    "Land Rover": ["Range Rover Evoque", "Discovery Sport", "Defender"]
}

FUEL_TYPES = ["Petrol", "Diesel", "CNG", "Electric", "Hybrid"]

TRANSMISSION_TYPES = ["Manual", "Automatic", "iMT"]

INDIAN_CITIES = [
    "Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Ahmedabad", "Chennai",
    "Kolkata", "Surat", "Pune", "Jaipur", "Lucknow", "Kanpur", "Nagpur",
    "Indore", "Thane", "Bhopal", "Visakhapatnam", "Pimpri-Chinchwad", "Patna", "Vadodara"
]

INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"
]

TCO_COMPONENTS = [
    "Depreciation", "Fuel/Energy", "Insurance", "Maintenance", 
    "Financing Interest", "Taxes & Registration"
]

RISK_LEVELS = {
    (0, 30): "LOW",
    (31, 70): "MEDIUM",
    (71, 100): "HIGH"
}

HEALTH_THRESHOLDS = {
    "Excellent": 90,
    "Good": 75,
    "Fair": 60,
    "Poor": 0
}

DEPRECIATION_CURVES = {
    "Petrol": {1: 10, 2: 20, 3: 30, 4: 40, 5: 50},
    "Diesel": {1: 15, 2: 25, 3: 35, 4: 45, 5: 55},
    "Electric": {1: 20, 2: 30, 3: 40, 4: 50, 5: 60},
}

DEFAULT_INSURANCE_RATE = 0.03
DEFAULT_FUEL_PRICE_PETROL = 100.0
DEFAULT_FUEL_PRICE_DIESEL = 90.0
DEFAULT_ELECTRICITY_RATE = 8.0

COLOR_SCHEME = {
    "background": "#F5F5F0",
    "card_bg": "#FFFFFF",
    "text_primary": "#000000",
    "text_secondary": "#333333",
    "accent": "#FF2800",
    "border": "#000000",
    "success": "#000000",
    "warning": "#FF2800",
    "danger": "#FF2800"
}

APP_VERSION = "1.0.0"

DATA_SOURCES = {
    "Vahan Dashboard": "https://vahan.parivahan.gov.in/vahan4dashboard/",
    "Autocar India": "https://www.autocarindia.com/",
    "Team-BHP": "https://www.team-bhp.com/"
}
