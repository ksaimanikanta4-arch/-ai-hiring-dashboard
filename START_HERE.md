# 🎯 START HERE - How to Run the Dashboard

## ✅ The Problem You Had

You tried: `streamlit run app.py`
Error: `zsh: command not found: streamlit`

**Why?** Streamlit is installed in the virtual environment, not system-wide.

## 🚀 The Solution

### **Use the Run Script (Easiest Way):**

```bash
./run.sh
```

That's it! The script will:
1. ✅ Activate the virtual environment automatically
2. ✅ Check if dependencies are installed
3. ✅ Launch the dashboard
4. ✅ Open your browser automatically

---

## 🔧 Alternative: Manual Method

If you want to run it manually:

```bash
# Step 1: Activate virtual environment
source venv/bin/activate

# Step 2: Run the app
streamlit run app.py

# Step 3: (Optional) Deactivate when done
deactivate
```

---

## ✅ Current Status

- ✅ Virtual environment created (`venv/`)
- ✅ Dependencies installed (streamlit, plotly, pandas, numpy, groq)
- ✅ `.env` file exists with your API key
- ✅ Run script is ready (`./run.sh`)

## 🎯 Next Steps

1. **Run the dashboard:**
   ```bash
   ./run.sh
   ```

2. **Wait for it to launch** (browser opens automatically)

3. **Navigate to "🤖 AI Assistant"** in the sidebar

4. **Start asking questions!**
   - "Why did Sarah Chen score 78.4?"
   - "What's the biggest difference between Sarah and Marcus?"
   - "How can Aisha improve her Feedback Integration score?"

## 🆘 Still Having Issues?

Run the verification script:
```bash
python3 verify_setup.py
```

This will check:
- Python version
- Required files
- Installed packages

---

**Ready? Run `./run.sh` now!** 🚀

