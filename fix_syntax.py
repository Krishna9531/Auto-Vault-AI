import glob
import re

files = glob.glob(r"c:\Users\KRISH\AutoVault-AI\app\pages\0[2-8]*.py")

good_header = """# Custom navigation
try:
    from app.components.navigation import build_sidebar
    build_sidebar()
except Exception as e:
    pass

if "vehicle_data" not in st.session_state or not st.session_state.vehicle_data:
    import streamlit as st
    st.markdown("<div style='text-align:center; padding: 60px 20px;'><h2 style='color:#FF2800; font-weight:900;'>VEHICLE REQUIRED</h2><p style='color:#555; font-size:1.1rem; margin-bottom: 30px;'>Please configure a vehicle first to view this analysis module.</p></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("← GO TO VEHICLE INPUT", use_container_width=True, type="primary"):
            st.switch_page("pages/01_Vehicle_Input.py")
    st.stop()
"""

for f in files:
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
    
    # We will find the start of "# Custom navigation" and the end of "except Exception as e:\n    pass\n" or "except Exception as e:\n    pass"
    # Actually, it's easier to just wipe out everything between "# Custom navigation" and "st.stop()\n\nexcept Exception as e:\n    pass"
    
    # Let's do a regex replacement for the broken block
    pattern = re.compile(r'# Custom navigation.*?st\.stop\(\)\n\nexcept Exception as e:\n    pass', re.DOTALL)
    
    if pattern.search(content):
        new_content = pattern.sub(good_header, content)
        with open(f, "w", encoding="utf-8") as file:
            file.write(new_content)
        print(f"Fixed {f}")
    else:
        # Also check if it's already fixed or has a different variation
        pattern2 = re.compile(r'# Custom navigation.*?st\.stop\(\)', re.DOTALL)
        # We need to be careful not to delete too much.
        pass

