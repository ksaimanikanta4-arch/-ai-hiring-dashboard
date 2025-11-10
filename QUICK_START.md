# 🚀 Quick Start Guide

## Problem: "streamlit: command not found"

This happens because `streamlit` is installed in the virtual environment, not system-wide.

## ✅ Solution: Use the run script (Easiest)

Simply run:
```bash
./run.sh
```

This script automatically:
- ✅ Activates the virtual environment
- ✅ Checks/installs dependencies
- ✅ Launches the dashboard

## 🔧 Alternative: Manual Activation

If you prefer to run it manually:

```bash
# 1. Activate the virtual environment
source venv/bin/activate

# 2. Run streamlit
streamlit run app.py

# 3. When done, deactivate (optional)
deactivate
```

## 🤖 AI Assistant Setup

1. Make sure you have a `.env` file in the project root
2. Add your Groq API key:
   ```
   GROQ_API_KEY=gsk_your_actual_key_here
   ```
3. Get a free key at: https://console.groq.com/keys

## 📝 Troubleshooting

### If `./run.sh` doesn't work:
```bash
# Make sure it's executable
chmod +x run.sh

# Then run it
./run.sh
```

### If virtual environment is missing:
```bash
# Create it
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Check if everything is installed:
```bash
python3 verify_setup.py
```

## 🎯 What to Expect

1. The script will show progress messages
2. Dependencies will install (first time only)
3. Browser will open automatically at `http://localhost:8501`
4. You'll see the Growth Potential Explainer dashboard

## 💡 Tips

- **First run**: Takes 1-2 minutes to install dependencies
- **Subsequent runs**: Takes just a few seconds
- **To stop**: Press `Ctrl+C` in the terminal
- **Port**: If 8501 is busy, Streamlit will use 8502, 8503, etc.

