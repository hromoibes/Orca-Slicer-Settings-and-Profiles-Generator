#!/bin/bash
# Run script for Orca Slicer Settings Generator

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Initialize database if needed
if [ ! -d "data" ]; then
    echo "Initializing database..."
    mkdir -p data
    python scripts/initialize_db.py
fi

# Start the application
echo "Starting Orca Slicer Settings Generator..."
python src/ui/app.py $@

# Deactivate virtual environment on exit
deactivate
