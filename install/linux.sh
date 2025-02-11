#!/bin/bash
# =====================================================
#  Install Script for Correspond on Linux
# =====================================================

echo "====================================================="
echo "Setting up the Correspond project on Linux..."
echo "====================================================="

# ---- Set Up Python Virtual Environment for Backend ----
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Python backend setup complete."
cd ..

# ---- Build the C# Frontend Project ----
echo "Building C# UI project..."
cd frontend/CorrespondUI

# This assumes the dotnet CLI is installed and available.
dotnet build

echo "C# UI project build complete."
cd ../..

echo "====================================================="
echo "Installation complete."
echo "You can now run the Python service and launch the C# UI."
