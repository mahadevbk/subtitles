#!/bin/bash

# Ensure the script is run using bash
if [ -z "$BASH_VERSION" ]; then
    echo "❌ Please run this script using bash: bash run_subtitles.sh"
    exit 1
fi

# === Config ===
VENV_DIR="./venv"
SCRIPT_NAME="subtitles.py"
PY="$VENV_DIR/bin/python"
PIP="$VENV_DIR/bin/pip"

echo "🔧 Setting up virtual environment..."

# Step 1: Create virtual environment if needed
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    echo "✅ Virtual environment created at $VENV_DIR"
else
    echo "ℹ️ Virtual environment already exists."
fi

# Step 2: Upgrade pip inside venv
"$PY" -m pip install --upgrade pip

# Step 3: Install required packages in the venv
echo "📦 Installing required packages..."
"$PIP" install subliminal guessit babelfish

# Step 4: Run the subtitle downloader
echo "🚀 Running the subtitle downloader..."
"$PY" "$SCRIPT_NAME"

echo "✅ Done."

