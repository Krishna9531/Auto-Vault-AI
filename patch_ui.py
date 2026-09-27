import re
import sys

file_path = r"c:\Users\KRISH\AutoVault-AI\app\pages\01_Vehicle_Input.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix format_price recursion error
content = re.sub(r'return format_price\(val_lakhs\)', r'return f"Rs.{val_lakhs:.2f}L"', content)

# Remove ALL help kwargs from selectbox, number_input, slider, etc.
content = re.sub(r',\s*help="[^"]*"', '', content)
content = re.sub(r",\s*help='[^']*'", '', content)

# Replace 3 columns with 4 columns
new_selectors = """sel1, sel2, sel3, sel4 = st.columns(4)

with sel1:
    brand = st.selectbox("BRAND", filtered_brands,
                         index=filtered_brands.index("Hyundai") if "Hyundai" in filtered_brands else 0)

bdata = DB.get(brand, {})

# Find all unique body types (segments) for this brand
all_body_types = list(set([data.get("seg", "Other") for m, data in bdata.items()]))
all_body_types.sort()

with sel2:
    body_type = st.selectbox("BODY TYPE", ["All"] + all_body_types)

if body_type == "All":
    models = list(bdata.keys())
else:
    models = [m for m, data in bdata.items() if data.get("seg") == body_type]
    
# Fallback if list is empty for some reason
if not models: models = list(bdata.keys())

with sel3:
    model = st.selectbox("MODEL", models)

mdata    = bdata.get(model, {})
variants = mdata.get("v", ["Standard"])
prices   = mdata.get("p", [10.0])
fuels    = mdata.get("f", ["Petrol"])
seg_name = mdata.get("seg", "")

with sel4:
    variant_opts = [f"{v}  —  {format_price(p)}" for v, p in zip(variants, prices)]
    v_sel = st.selectbox("VARIANT", variant_opts)
    vi       = variant_opts.index(v_sel)
    variant  = variants[vi]
    ex_price = prices[vi]"""

# Substitute the block
pattern = re.compile(r'sel1, sel2, sel3 = st\.columns\(3\).*?ex_price = prices\[vi\]', re.DOTALL)
content = pattern.sub(new_selectors, content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed layout, added Body Type dropdown, removed tooltips and fixed recursion error.")
