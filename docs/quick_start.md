# Orca Slicer Settings Generator - Quick Start Guide

This quick start guide will help you get up and running with the Orca Slicer Settings Generator on your SonicPad with Debian running Klipper firmware.

## Installation

1. Open a terminal on your SonicPad
2. Run the following commands:

```bash
# Install dependencies
sudo apt update
sudo apt install -y python3-pip python3-venv git

# Clone the repository
git clone https://github.com/yourusername/orca-slicer-settings-generator.git
cd orca-slicer-settings-generator

# Install Python dependencies
pip3 install -r requirements.txt

# Start the application
python3 src/ui/app.py
```

3. Access the application at `http://localhost:5000`

For detailed installation instructions, see the [Installation Guide](installation.md).

## First-Time Setup

### 1. Create a Printer Profile

1. Click **Printers** → **Add New Printer**
2. Enter your SonicPad printer details:
   - Name: "My SonicPad Printer"
   - Check "Use Klipper"
   - Enter your bed size and nozzle diameter
3. Click **Save**

### 2. Create a Material Profile

1. Click **Materials** → **Add New Material**
2. Enter your filament details:
   - Name: "My PLA"
   - Material Type: "PLA"
   - Diameter: 1.75mm
   - Temperature Range: 190-220°C
3. Click **Save**

### 3. Generate Your First Profile

1. Click **Generate**
2. Select your printer and material profiles
3. Set your print requirements using the sliders
4. Click **Generate Profile**
5. Review the AI-recommended settings
6. Click **Save**

### 4. Export to Orca Slicer

1. Click **Processes**
2. Find your new profile
3. Click **Export** → **Orca Slicer Format**
4. Import the file into Orca Slicer

## Klipper Optimization

For optimal results with your SonicPad running Klipper:

1. Click **Settings** → **Klipper Integration**
2. Enable Pressure Advance and Input Shaping
3. Enter your calibrated values or use the calibration tools
4. Click **Save**

## Next Steps

- Explore the [User Guide](user_guide.md) for detailed information
- Check the [Technical Documentation](technical_docs.md) for advanced features
- Visit the Help section in the application for setting-specific information

For any issues, refer to the [Troubleshooting Guide](troubleshooting.md).
