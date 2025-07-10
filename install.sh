#!/bin/bash

echo "Resume Builder - Installation Script"
echo "===================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "Python 3 is installed: $(python3 --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if python3 -m venv venv; then
    echo "✓ Virtual environment created successfully"
else
    echo "Error: Failed to create virtual environment"
    echo "You may need to install python3-venv:"
    echo "  sudo apt-get install python3-venv    # For Ubuntu/Debian"
    echo "  sudo yum install python3-venv        # For CentOS/RHEL"
    exit 1
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
echo ""
echo "Installing requirements..."
if pip install -r my/requirements.txt; then
    echo "✓ All requirements installed successfully"
else
    echo "Error: Failed to install requirements"
    exit 1
fi

echo ""
echo "===================================="
echo "Installation completed successfully!"
echo ""
echo "To run the application:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run the app: streamlit run my/app.py"
echo ""
echo "Or simply run: ./run.sh"