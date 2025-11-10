#!/usr/bin/env python3
"""
Quick setup verification script
"""
import sys

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ required. Found: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_imports():
    """Check if required packages can be imported"""
    packages = ['streamlit', 'plotly', 'pandas', 'numpy']
    missing = []
    
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is NOT installed")
            missing.append(package)
    
    return len(missing) == 0

def check_files():
    """Check if required files exist"""
    import os
    required_files = ['app.py', 'candidate_data.py', 'requirements.txt']
    missing = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} is missing")
            missing.append(file)
    
    return len(missing) == 0

if __name__ == "__main__":
    print("🔍 Verifying setup...")
    print("")
    
    all_good = True
    all_good &= check_python_version()
    print("")
    all_good &= check_files()
    print("")
    all_good &= check_imports()
    print("")
    
    if all_good:
        print("🎉 All checks passed! You're ready to run the dashboard.")
        print("   Run: ./run.sh or python3 -m streamlit run app.py")
    else:
        print("⚠️  Some checks failed. Please install missing dependencies:")
        print("   pip3 install -r requirements.txt")
        sys.exit(1)

