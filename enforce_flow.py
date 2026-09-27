import glob
import os

# Target pages 02 to 08
files = glob.glob(r"c:\Users\KRISH\AutoVault-AI\app\pages\0[2-8]*.py")

guardrail_code = """
if "vehicle_data" not in st.session_state or not st.session_state.vehicle_data:
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
    
    # Check if already injected
    if "st.stop()" in content and "vehicle_data" in content:
        continue
    
    # Insert right after build_sidebar()
    parts = content.split("build_sidebar()")
    if len(parts) > 1:
        new_content = parts[0] + "build_sidebar()\n" + guardrail_code + parts[1]
        with open(f, "w", encoding="utf-8") as file:
            file.write(new_content)
        print(f"Patched {os.path.basename(f)}")
    else:
        print(f"Could not find build_sidebar() in {os.path.basename(f)}")
