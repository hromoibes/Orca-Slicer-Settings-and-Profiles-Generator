# Orca Slicer Settings Generator - Installation Guide

This guide provides instructions for installing and setting up the Orca Slicer Settings Generator on your SonicPad with Debian running Klipper firmware.

## System Requirements

- SonicPad with Debian (https://github.com/Jpe230/SonicPad-Debian)
- Klipper firmware
- Python 3.8 or higher
- 500MB free disk space
- Internet connection (for initial setup)

## Installation Steps

### 1. Install Dependencies

Open a terminal on your SonicPad and run the following commands:

```bash
# Update package lists
sudo apt update

# Install required packages
sudo apt install -y python3-pip python3-venv git

# Install required Python packages
pip3 install flask scikit-learn numpy pandas werkzeug
```

### 2. Download the Application

```bash
# Clone the repository
git clone https://github.com/yourusername/orca-slicer-settings-generator.git
cd orca-slicer-settings-generator
```

### 3. Set Up Virtual Environment (Optional but Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies in virtual environment
pip install -r requirements.txt
```

### 4. Initialize the Application

```bash
# Create data directories
mkdir -p data/printers data/materials data/processes

# Initialize database files
python3 scripts/initialize_db.py
```

### 5. Start the Application

```bash
# Start the web server
python3 src/ui/app.py
```

The application will be available at `http://localhost:5000` on your SonicPad.

### 6. Access from Other Devices (Optional)

To access the application from other devices on your network:

```bash
# Start the server with network access
python3 src/ui/app.py --host 0.0.0.0
```

Then access the application using your SonicPad's IP address: `http://<sonicpad-ip>:5000`

## Klipper-Specific Configuration

The Orca Slicer Settings Generator is pre-configured to work with Klipper firmware on your SonicPad. It includes optimizations for:

- Pressure advance
- Input shaping
- Resonance compensation
- Adaptive bed leveling

To ensure optimal integration with your Klipper setup:

1. Navigate to the Settings page in the application
2. Select the "Klipper Integration" tab
3. Enter the path to your Klipper configuration file (typically `/home/pi/klipper_config/printer.cfg`)
4. Click "Import Klipper Settings" to automatically configure the application based on your Klipper setup

## Troubleshooting

If you encounter any issues during installation:

- Ensure your SonicPad is running the latest version of Debian
- Verify that Klipper is properly installed and configured
- Check that all dependencies are installed correctly
- Ensure you have sufficient disk space and memory

For additional help, please refer to the [Troubleshooting Guide](troubleshooting.md) or open an issue on the GitHub repository.
