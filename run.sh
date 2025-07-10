#!/bin/bash

echo "Starting Resume Builder..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found."
    echo "Please run ./install.sh first to set up the environment."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "Streamlit is not installed in the virtual environment."
    echo "Please run ./install.sh to install dependencies."
    exit 1
fi

# Run the application
echo "Starting Streamlit application..."
echo "Opening http://localhost:8501 in your browser..."
echo ""
streamlit run my/app.py