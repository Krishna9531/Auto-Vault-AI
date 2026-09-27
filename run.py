"""
AUTOVAULT AI — Launch Script
Run with: python run.py
"""

import subprocess
import sys
import os
from pathlib import Path


def check_requirements():
    """Check that critical packages are installed."""
    required = ["streamlit", "pandas", "numpy", "plotly", "sklearn"]
    missing = []
    for pkg in required:
        try:
            __import__(pkg.replace("-", "_"))
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    return True


def main():
    root = Path(__file__).parent
    app_entry = root / "app" / "main.py"

    print("=" * 60)
    print("  AUTOVAULT AI")
    print("  Automotive Risk, Value & Ownership Intelligence")
    print("=" * 60)
    print()

    if not check_requirements():
        sys.exit(1)

    print("✅ Dependencies OK")
    print(f"🚀 Starting Streamlit — http://localhost:8501")
    print()

    env = os.environ.copy()
    env["PYTHONPATH"] = str(root)

    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", str(app_entry),
         "--server.port=8501",
         "--server.headless=false",
         "--theme.base=light"],
        env=env,
        cwd=str(root),
    )


if __name__ == "__main__":
    main()
