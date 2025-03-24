# Orca Slicer Settings Generator - User Guide

This comprehensive guide will help you get the most out of the Orca Slicer Settings Generator for your SonicPad with Debian running Klipper firmware.

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Creating Printer Profiles](#creating-printer-profiles)
4. [Creating Material Profiles](#creating-material-profiles)
5. [Generating Process Profiles](#generating-process-profiles)
6. [AI Recommendations](#ai-recommendations)
7. [Klipper Integration](#klipper-integration)
8. [Exporting Profiles to Orca Slicer](#exporting-profiles-to-orca-slicer)
9. [Advanced Settings](#advanced-settings)
10. [Tips and Best Practices](#tips-and-best-practices)

## Introduction

The Orca Slicer Settings Generator is a powerful tool designed to help you create optimized 3D printing profiles for your SonicPad with Debian running Klipper firmware. Using open-source AI technology, it analyzes your printer capabilities, material properties, and print requirements to generate settings that produce the best possible results.

Key features include:
- AI-powered settings recommendations
- Klipper-specific optimizations
- Comprehensive profile management
- Detailed explanations of settings
- Easy export to Orca Slicer

## Getting Started

After installing the application (see [Installation Guide](installation.md)), access it through your web browser at `http://localhost:5000` or `http://<sonicpad-ip>:5000` if accessing from another device.

The main dashboard provides an overview of your profiles and quick access to all features:

- **Printers**: Manage your printer profiles
- **Materials**: Manage your material profiles
- **Processes**: View and manage your process profiles
- **Generate**: Create new process profiles with AI recommendations
- **Help**: Access detailed information about 3D printing settings

## Creating Printer Profiles

1. Click on the **Printers** tab in the navigation menu
2. Click the **Add New Printer** button
3. Fill in the printer details:
   - **Name**: A descriptive name for your printer
   - **Vendor**: The manufacturer of your printer
   - **Model**: The specific model
   - **Bed Size**: The dimensions of your print bed (width × depth)
   - **Max Height**: The maximum print height
   - **Nozzle Diameter**: The diameter of your nozzle (typically 0.4mm)
   - **Direct Drive**: Check if your printer uses direct drive extrusion
   - **Printer Type**: Select the printer type (Cartesian, Delta, CoreXY, etc.)
   - **Use Klipper**: Check this option for your SonicPad with Klipper
4. For Klipper-enabled printers, additional options will appear:
   - **Pressure Advance**: Enable and set pressure advance values
   - **Input Shaping**: Configure input shaping parameters
   - **Resonance Compensation**: Set resonance compensation values
5. Click **Save** to create the printer profile

## Creating Material Profiles

1. Click on the **Materials** tab in the navigation menu
2. Click the **Add New Material** button
3. Fill in the material details:
   - **Name**: A descriptive name for the material
   - **Vendor**: The manufacturer of the filament
   - **Material Type**: Select the material type (PLA, PETG, ABS, etc.)
   - **Color**: Select or enter the color code
   - **Diameter**: The filament diameter (typically 1.75mm)
   - **Temperature Range**: The recommended nozzle temperature range
   - **Bed Temperature Range**: The recommended bed temperature range
4. Advanced properties (optional):
   - **Density**: The material density
   - **Shrinkage Factor**: The material shrinkage factor
   - **Flow Rate Multiplier**: The flow rate adjustment factor
5. Click **Save** to create the material profile

## Generating Process Profiles

1. Click on the **Generate** tab in the navigation menu
2. Select a printer profile from the dropdown menu
3. Select a material profile from the dropdown menu
4. Enter the nozzle size (if different from the printer's default)
5. Set your print requirements using the sliders:
   - **Quality**: Prioritize surface finish and detail
   - **Strength**: Prioritize structural integrity
   - **Speed**: Prioritize faster print times
   - **Material Usage**: Prioritize filament efficiency
6. Click **Generate Profile** to create a new process profile with AI-optimized settings
7. Review the generated settings and explanations
8. Optionally, adjust any settings manually
9. Click **Save** to store the profile

## AI Recommendations

The AI recommendation engine analyzes your printer capabilities, material properties, and print requirements to generate optimal settings. For each setting, you'll see:

- **Value**: The recommended setting value
- **Explanation**: Why this value was chosen
- **Impact**: How this setting affects print quality, strength, speed, and material usage
- **Trade-offs**: What compromises are being made with this setting
- **Related Settings**: Other settings that interact with this one

To get the most from the AI recommendations:

1. Be specific about your print requirements using the sliders
2. Review the explanations to understand the reasoning
3. Make incremental adjustments if needed
4. Use the comparison tool to see how changes affect the print

## Klipper Integration

The Orca Slicer Settings Generator includes special optimizations for Klipper firmware on your SonicPad:

### Pressure Advance

Pressure advance helps reduce oozing and improve corner quality by adjusting the pressure in the extruder.

1. Go to the **Settings** tab
2. Select the **Klipper Integration** section
3. Enable **Pressure Advance**
4. Enter your calibrated pressure advance value or use the calibration tool

### Input Shaping

Input shaping reduces ringing and ghosting artifacts by compensating for printer vibrations.

1. Go to the **Settings** tab
2. Select the **Klipper Integration** section
3. Enable **Input Shaping**
4. Select the shaping method (MZV, ZV, 2HUMP_EI, etc.)
5. Enter the frequency and damping parameters

### Resonance Compensation

Resonance compensation further reduces artifacts by compensating for specific resonance frequencies.

1. Go to the **Settings** tab
2. Select the **Klipper Integration** section
3. Enable **Resonance Compensation**
4. Upload your ADXL345 accelerometer data or enter values manually

## Exporting Profiles to Orca Slicer

Once you've created and optimized your profiles, you can export them for use in Orca Slicer:

1. Go to the **Processes** tab
2. Find the process profile you want to export
3. Click the **Export** button
4. Select **Orca Slicer Format**
5. Choose a save location
6. Click **Export**

To import the profile into Orca Slicer:

1. Open Orca Slicer
2. Go to **File** > **Import** > **Import Config**
3. Navigate to your exported profile
4. Select the file and click **Open**
5. The profile will be imported and available for use

## Advanced Settings

For users who want more control, the Advanced Settings section provides access to all available settings:

1. Go to the **Settings** tab
2. Select the **Advanced** section
3. Use the search function to find specific settings
4. Adjust values as needed
5. Click **Save** to apply changes

Key advanced settings for Klipper users:

- **Firmware Retraction**: Enable to use Klipper's firmware-based retraction
- **Adaptive Bed Leveling**: Configure mesh bed leveling parameters
- **Velocity Limits**: Set maximum velocity and acceleration values
- **Extruder Pressure**: Fine-tune pressure advance settings

## Tips and Best Practices

### For SonicPad with Klipper

1. **Calibrate First**: Always calibrate your printer's extruder steps, pressure advance, and input shaping before generating profiles
2. **Start Conservative**: Begin with more conservative settings and gradually optimize
3. **Test Prints**: Use calibration prints to verify and fine-tune settings
4. **Temperature Towers**: Create temperature towers to find the optimal temperature for each filament
5. **Backup Configs**: Always backup your Klipper configuration files before making changes

### General 3D Printing

1. **Layer Height**: Smaller layer heights improve detail but increase print time
2. **Print Speed**: Lower speeds generally improve quality but increase print time
3. **Infill Density**: Higher infill improves strength but uses more material
4. **Cooling**: Proper cooling is essential for overhangs and bridging
5. **Bed Adhesion**: Use the appropriate bed adhesion method for your material

For more detailed information on specific settings, visit the **Help** section in the application.
