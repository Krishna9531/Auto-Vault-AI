import re

file_path = r"c:\Users\KRISH\AutoVault-AI\app\pages\01_Vehicle_Input.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Inject format_price helper
format_helper = """
def format_price(val_lakhs):
    if val_lakhs >= 100:
        return f"Rs.{val_lakhs/100:.2f}Cr"
    return f"Rs.{val_lakhs:.2f}L"
"""
# Insert after imports
if "def format_price" not in content:
    content = content.replace("import datetime", "import datetime\n" + format_helper)

# 2. Add Luxury Brands to DB
luxury_brands = """
    "Ferrari": {
        "SF90 Stradale": {"v":["Base"], "p":[750.0], "f":["Hybrid"], "seg":"Supercar"},
        "296 GTB":       {"v":["Base"], "p":[540.0], "f":["Hybrid"], "seg":"Supercar"},
        "Roma":          {"v":["Base"], "p":[376.0], "f":["Petrol"], "seg":"Grand Tourer"},
        "Purosangue":    {"v":["Base"], "p":[1050.0], "f":["Petrol"], "seg":"Super SUV"}
    },
    "Bugatti": {
        "Chiron":        {"v":["Base", "Pur Sport", "Super Sport"], "p":[1920.0, 2400.0, 2800.0], "f":["Petrol"], "seg":"Hypercar"}
    },
    "Koenigsegg": {
        "Jesko":         {"v":["Absolut", "Attack"], "p":[2400.0, 2600.0], "f":["Petrol"], "seg":"Hypercar"},
        "Gemera":        {"v":["Base"], "p":[1600.0], "f":["Hybrid"], "seg":"Hypercar"}
    },
"""
if '"Ferrari"' not in content:
    content = content.replace("DB = {\n", "DB = {\n" + luxury_brands)

# 3. Replace all hardcoded string formats with format_price
# Examples: f"Rs.{p:.2f}L", f"Rs.{ex_price:.2f}L", f"Rs.{v:.2f}L", Rs.{ex_price:.2f}L, etc.

content = re.sub(r'f"Rs\.\{([a-zA-Z0-9_]+)\:\.2f\}L"', r'format_price(\1)', content)
content = re.sub(r'f"Rs\.\{([a-zA-Z0-9_]+)\[-1\]\:\.2f\}L"', r'format_price(\1[-1])', content)
content = re.sub(r'f"Rs\.\{([a-zA-Z0-9_]+) / 100000\:\.2f\}L"', r'format_price(\1 / 100000)', content)
# For HTML snippets
content = re.sub(r'Rs\.\{([a-zA-Z0-9_]+)\:\.2f\}L', r'{format_price(\1)}', content)
content = re.sub(r'Rs\.\{([a-zA-Z0-9_]+)\[-1\]\:\.2f\}L', r'{format_price(\1[-1])}', content)
content = re.sub(r'Rs\.\{([a-zA-Z0-9_]+)/100000\:\.2f\}L', r'{format_price(\1/100000)}', content)
content = re.sub(r'Rs\.\{([a-zA-Z0-9_]+)\:\.1f\}L', r'{format_price(\1)}', content)

# Check specifically for Plotly templates
content = content.replace('hovertemplate="<b>%{x}</b><br>Rs.%{y:.2f}L<extra></extra>"', 'hovertemplate="<b>%{x}</b><br>Rs.%{y:.2f}L<extra></extra>"') # Actually, plotly needs JS formatting for tooltips if we want dynamic cr/L. Since Plotly y is numeric, we can't easily use python format_price in JS hovertemplate. I'll just change the text array which is python side!

# Actually, the hovertemplate uses the text array if we specify text.
content = content.replace('hovertemplate="<b>%{x}</b><br>Rs.%{y:.2f}L<extra></extra>"', 'hovertemplate="<b>%{x}</b><br>%{text}<extra></extra>"')
content = content.replace('hovertemplate="Year %{x}: Rs.%{text}<extra></extra>"', 'hovertemplate="Year %{x}: %{text}<extra></extra>"')
content = content.replace('hovertemplate="<b>%{x}</b><br>Rs.%{y:.2f}L per year<extra></extra>"', 'hovertemplate="<b>%{x}</b><br>%{text} per year<extra></extra>"')

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated Vehicle Input successfully.")
