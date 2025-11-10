#!/bin/bash

echo "🚀 Starting Growth Potential Explainer Dashboard..."
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Set up virtual environment
VENV_DIR="venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment."
        exit 1
    fi
    echo "✅ Virtual environment created!"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet

# Check if dependencies are installed
echo "📦 Checking dependencies..."
if ! python -m streamlit --version &> /dev/null
then
    echo "⚠️  Dependencies not found. Installing..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies. Please check your internet connection and try again."
        exit 1
    fi
    echo "✅ Dependencies installed successfully!"
else
    echo "✅ Dependencies found!"
fi

echo ""
echo "🎯 Launching dashboard..."
echo "👉 The app will open at http://localhost:8501"
echo ""

# Run streamlit
streamlit run app.py
