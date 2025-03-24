#!/bin/bash
# Deployment script for Orca Slicer Settings Generator
# This script prepares and packages the application for deployment

# Set variables
APP_NAME="orca-slicer-settings-generator"
VERSION="1.0.0"
OUTPUT_DIR="/home/ubuntu/orca_slicer_generator/dist"
SOURCE_DIR="/home/ubuntu/orca_slicer_generator"

# Create output directory
mkdir -p $OUTPUT_DIR

# Create requirements.txt file
echo "Creating requirements.txt..."
cat > $SOURCE_DIR/requirements.txt << EOL
flask==2.0.1
scikit-learn==1.0.2
numpy==1.21.4
pandas==1.3.4
werkzeug==2.0.2
jinja2==3.0.2
itsdangerous==2.0.1
click==8.0.3
EOL

# Create setup script
echo "Creating setup script..."
cat > $SOURCE_DIR/setup.py << EOL
from setuptools import setup, find_packages

setup(
    name="orca_slicer_settings_generator",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "scikit-learn",
        "numpy",
        "pandas",
        "werkzeug",
    ],
    author="Manus AI",
    author_email="info@example.com",
    description="AI-powered settings generator for Orca Slicer with Klipper support",
    keywords="3d printing, orca slicer, klipper, ai, settings",
    url="https://github.com/yourusername/orca-slicer-settings-generator",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
)
EOL

# Create initialization script
echo "Creating initialization script..."
cat > $SOURCE_DIR/scripts/initialize_db.py << EOL
#!/usr/bin/env python3
"""
Initialize the database for Orca Slicer Settings Generator
"""

import os
import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def initialize_database():
    """Initialize the database files and directories."""
    # Define data directory
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    
    # Create data directories
    os.makedirs(os.path.join(data_dir, 'printers'), exist_ok=True)
    os.makedirs(os.path.join(data_dir, 'materials'), exist_ok=True)
    os.makedirs(os.path.join(data_dir, 'processes'), exist_ok=True)
    
    # Create database files
    db_template = {
        'version': '1.0.0',
        'last_updated': datetime.now().isoformat(),
        'items': {}
    }
    
    # Create printer database
    with open(os.path.join(data_dir, 'printers.json'), 'w') as f:
        json.dump(db_template, f, indent=2)
    
    # Create material database
    with open(os.path.join(data_dir, 'materials.json'), 'w') as f:
        json.dump(db_template, f, indent=2)
    
    # Create process database
    with open(os.path.join(data_dir, 'processes.json'), 'w') as f:
        json.dump(db_template, f, indent=2)
    
    print("Database initialized successfully!")
    
    # Create default SonicPad profile
    create_default_sonicpad_profile(data_dir)

def create_default_sonicpad_profile(data_dir):
    """Create a default SonicPad printer profile."""
    import uuid
    
    # SonicPad printer profile
    sonicpad_profile = {
        "id": str(uuid.uuid4()),
        "name": "SonicPad Default",
        "vendor": "Creality",
        "model": "SonicPad",
        "bed_size": [220, 220],
        "max_print_height": 250,
        "nozzle_diameter": 0.4,
        "direct_drive": False,
        "printer_type": "cartesian",
        "use_klipper": True,
        "klipper_settings": {
            "pressure_advance": 0.05,
            "input_shaping": {
                "enabled": True,
                "method": "mzv",
                "frequency_x": 37.8,
                "frequency_y": 42.2
            }
        },
        "created": datetime.now().isoformat(),
        "modified": datetime.now().isoformat()
    }
    
    # Load printer database
    with open(os.path.join(data_dir, 'printers.json'), 'r') as f:
        printers_db = json.load(f)
    
    # Add SonicPad profile
    printers_db['items'][sonicpad_profile['id']] = sonicpad_profile
    
    # Save printer database
    with open(os.path.join(data_dir, 'printers.json'), 'w') as f:
        json.dump(printers_db, f, indent=2)
    
    # Save printer-specific file
    with open(os.path.join(data_dir, 'printers', f"{sonicpad_profile['id']}.json"), 'w') as f:
        json.dump(sonicpad_profile, f, indent=2)
    
    print(f"Created default SonicPad profile: {sonicpad_profile['id']}")

if __name__ == '__main__':
    initialize_database()
EOL

# Create run script
echo "Creating run script..."
cat > $SOURCE_DIR/run.sh << EOL
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
python src/ui/app.py \$@

# Deactivate virtual environment on exit
deactivate
EOL

# Make scripts executable
chmod +x $SOURCE_DIR/run.sh
mkdir -p $SOURCE_DIR/scripts
chmod +x $SOURCE_DIR/scripts/initialize_db.py

# Create README file
echo "Creating README file..."
cat > $SOURCE_DIR/README.md << EOL
# Orca Slicer Settings Generator

An AI-powered settings generator for Orca Slicer with special support for SonicPad with Debian running Klipper firmware.

## Features

- AI-powered settings recommendations
- Klipper-specific optimizations
- Comprehensive profile management
- Detailed explanations of settings
- Easy export to Orca Slicer

## Documentation

- [Installation Guide](docs/installation.md)
- [Quick Start Guide](docs/quick_start.md)
- [User Guide](docs/user_guide.md)
- [Technical Documentation](docs/technical_docs.md)

## Installation

See the [Installation Guide](docs/installation.md) for detailed instructions.

Quick install:

\`\`\`bash
# Install dependencies
sudo apt update
sudo apt install -y python3-pip python3-venv git

# Clone the repository
git clone https://github.com/yourusername/orca-slicer-settings-generator.git
cd orca-slicer-settings-generator

# Run the application
./run.sh
\`\`\`

## Usage

Access the application at http://localhost:5000 after starting it with \`./run.sh\`.

See the [User Guide](docs/user_guide.md) for detailed usage instructions.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
EOL

# Create LICENSE file
echo "Creating LICENSE file..."
cat > $SOURCE_DIR/LICENSE << EOL
MIT License

Copyright (c) 2025 Manus AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOL

# Create package
echo "Creating package..."
cd $SOURCE_DIR
tar -czf $OUTPUT_DIR/$APP_NAME-$VERSION.tar.gz \
    --exclude="*.pyc" \
    --exclude="__pycache__" \
    --exclude=".git" \
    --exclude="dist" \
    --exclude="*.egg-info" \
    .

# Create zip package for Windows users
echo "Creating zip package..."
cd $SOURCE_DIR
zip -r $OUTPUT_DIR/$APP_NAME-$VERSION.zip \
    . \
    -x "*.pyc" \
    -x "*__pycache__*" \
    -x ".git/*" \
    -x "dist/*" \
    -x "*.egg-info/*"

echo "Deployment preparation complete!"
echo "Packages created:"
echo "- $OUTPUT_DIR/$APP_NAME-$VERSION.tar.gz"
echo "- $OUTPUT_DIR/$APP_NAME-$VERSION.zip"
