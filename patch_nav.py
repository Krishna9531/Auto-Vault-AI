import glob
import re

files = glob.glob(r"c:\Users\KRISH\AutoVault-AI\app\pages\*.py")

inject = """
# Custom navigation
try:
    from app.components.navigation import build_sidebar
    build_sidebar()
except Exception as e:
    pass
"""

for fpath in files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "build_sidebar()" in content:
        continue
        
    # Find st.set_page_config(...)
    match = re.search(r'st\.set_page_config\([^)]*\)', content)
    if match:
        end_idx = match.end()
        new_content = content[:end_idx] + "\n" + inject + content[end_idx:]
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)
    else:
        # If no set_page_config is found, just inject near top but after imports
        print(f"No set_page_config found in {fpath}")

print("Done patching.")
