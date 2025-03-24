# Orca Slicer Settings Generator - Technical Documentation

This technical documentation provides detailed information about the architecture, components, and implementation of the Orca Slicer Settings Generator application.

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Component Overview](#component-overview)
3. [AI Implementation](#ai-implementation)
4. [Database Structure](#database-structure)
5. [API Reference](#api-reference)
6. [Klipper Integration](#klipper-integration)
7. [Extending the Application](#extending-the-application)
8. [Troubleshooting](#troubleshooting)

## System Architecture

The Orca Slicer Settings Generator follows a modular architecture with the following layers:

- **Presentation Layer**: Web-based user interface built with Flask and Bootstrap
- **Application Layer**: Core business logic and profile management
- **AI Layer**: Machine learning and rule-based recommendation engine
- **Data Layer**: JSON-based profile storage and retrieval

### Technology Stack

- **Backend**: Python 3.8+, Flask
- **AI/ML**: scikit-learn, NumPy, custom rule engine
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Data Storage**: JSON-based file system
- **Testing**: unittest, integration tests

## Component Overview

### AI Manager (`src/ai/`)

The AI component is responsible for generating optimized 3D printer settings based on printer capabilities, material properties, and user requirements.

- **orca_ai.py**: Core AI engine that combines machine learning with rule-based systems
- **rule_engine.py**: Expert system containing rules for different materials and printer types
- **settings_metadata.py**: Information about settings, relationships, and dependencies
- **klipper_integration.py**: Klipper-specific optimizations

### Profile Manager (`src/profiles/`)

The profile management component handles the storage, retrieval, and manipulation of printer, material, and process profiles.

- **profile_database.py**: Database models for storing profiles
- **profile_generator.py**: Profile generation logic
- **__init__.py**: Unified interface for profile operations

### User Interface (`src/ui/`)

The web-based user interface provides access to all application features.

- **app.py**: Flask application and route definitions
- **templates/**: HTML templates for each page
- **static/**: CSS, JavaScript, and image assets

## AI Implementation

### Machine Learning Approach

The AI component uses a hybrid approach combining:

1. **Supervised Learning**: Trained on known-good profiles to predict optimal settings
2. **Rule-Based System**: Expert rules for handling specific scenarios
3. **Constraint Satisfaction**: Ensures settings are compatible with each other

### Training Data

The model is trained on:
- Default profiles from Orca Slicer
- Community-contributed profiles
- Theoretical optimal values based on 3D printing research

### Feature Engineering

Key features used in the model:
- Printer type and capabilities
- Material properties
- Nozzle diameter
- Print quality requirements
- Strength requirements
- Speed requirements
- Material usage requirements

### Model Selection

After evaluating multiple approaches, we selected a Random Forest model for its:
- Ability to handle non-linear relationships
- Robustness to outliers
- Good performance with limited training data
- Interpretability of results

## Database Structure

The application uses a JSON-based file system for data storage:

### Directory Structure

```
data/
├── printers.json       # Index of printer profiles
├── materials.json      # Index of material profiles
├── processes.json      # Index of process profiles
├── printers/           # Individual printer profile files
│   ├── [printer_id].json
├── materials/          # Individual material profile files
│   ├── [material_id].json
└── processes/          # Individual process profile files
    ├── [process_id].json
```

### Profile Schemas

#### Printer Profile

```json
{
  "id": "unique-id",
  "name": "Printer Name",
  "vendor": "Vendor Name",
  "model": "Model Name",
  "bed_size": [220, 220],
  "max_print_height": 250,
  "nozzle_diameter": 0.4,
  "direct_drive": true,
  "printer_type": "cartesian",
  "use_klipper": true,
  "klipper_settings": {
    "pressure_advance": 0.05,
    "input_shaping": {
      "enabled": true,
      "method": "mzv",
      "frequency_x": 37.8,
      "frequency_y": 42.2
    }
  },
  "created": "2023-01-01T00:00:00",
  "modified": "2023-01-01T00:00:00"
}
```

#### Material Profile

```json
{
  "id": "unique-id",
  "name": "Material Name",
  "vendor": "Vendor Name",
  "type": "PLA",
  "color": "#FFFFFF",
  "diameter": 1.75,
  "temp_range_min": 190,
  "temp_range_max": 220,
  "bed_temp_range_min": 50,
  "bed_temp_range_max": 60,
  "density": 1.24,
  "created": "2023-01-01T00:00:00",
  "modified": "2023-01-01T00:00:00"
}
```

#### Process Profile

```json
{
  "id": "unique-id",
  "name": "Process Name",
  "printer_id": "printer-id",
  "material_id": "material-id",
  "nozzle_diameter": 0.4,
  "layer_height": 0.2,
  "print_speed": 50,
  "temperature": 210,
  "bed_temperature": 60,
  "infill_density": 20,
  "infill_pattern": "grid",
  "retraction_distance": 5,
  "retraction_speed": 40,
  "cooling_enabled": true,
  "fan_speed": 100,
  "created": "2023-01-01T00:00:00",
  "modified": "2023-01-01T00:00:00"
}
```

## API Reference

### AI Manager API

```python
# Generate a profile with AI recommendations
profile = ai_manager.generate_profile(
    printer_id,
    material_id,
    nozzle_size,
    print_requirements,
    base_profile=None,
    use_klipper=True
)

# Get explanation for a specific setting
explanation = ai_manager.explain_setting(
    setting_name,
    setting_value,
    context
)
```

### Profile Manager API

```python
# Create a printer profile
printer_id = profile_manager.create_printer_profile(
    name, vendor, model, bed_size, max_height,
    nozzle_diameter, is_direct_drive, printer_type, use_klipper
)

# Create a material profile
material_id = profile_manager.create_material_profile(
    name, vendor, material_type, color, diameter,
    temp_range, bed_temp_range
)

# Generate a process profile
process_id = profile_manager.generate_process_profile(
    name, printer_id, material_id, nozzle_size, print_requirements
)

# Optimize an existing process profile
optimized_id = profile_manager.optimize_process_profile(
    process_id, print_requirements
)

# Compare two process profiles
comparison = profile_manager.compare_process_profiles(
    process_id_1, process_id_2
)

# Export a profile to Orca Slicer format
success = profile_manager.export_profile_to_orca(
    profile_id, profile_type, output_path
)
```

## Klipper Integration

The application includes special support for Klipper firmware on the SonicPad:

### Pressure Advance

Pressure advance settings are automatically incorporated into generated profiles based on:
- Material type
- Nozzle diameter
- Print speed
- Retraction settings

### Input Shaping

Input shaping parameters are optimized for:
- Printer geometry
- Print speed
- Acceleration values
- Resonance frequencies

### Resonance Compensation

The application can import resonance data from Klipper's ADXL345 accelerometer measurements to further optimize:
- Acceleration limits
- Jerk limits
- Corner behavior
- Velocity limits

### Firmware Retraction

When using Klipper's firmware retraction, the application adjusts:
- Retraction distance
- Retraction speed
- Extra restart distance
- Retract layer change behavior

## Extending the Application

### Adding New AI Models

To add a new AI model:

1. Create a new model class in `src/ai/models/`
2. Implement the required interface methods:
   - `train(data)`
   - `predict(features)`
   - `explain(setting, value, context)`
3. Register the model in `src/ai/orca_ai.py`

### Adding New Settings

To add support for new settings:

1. Add the setting definition to `src/ai/settings_metadata.py`
2. Define relationships with other settings
3. Add rules to `src/ai/rule_engine.py`
4. Update the UI to display the new setting

### Adding New Printer Types

To add support for new printer types:

1. Add the printer type to the printer profile schema
2. Add specific rules for the printer type in `src/ai/rule_engine.py`
3. Update the UI to support the new printer type

## Troubleshooting

### Common Issues

#### Database Errors

If profiles are not being saved or retrieved correctly:

1. Check file permissions in the data directory
2. Verify the JSON files are valid and not corrupted
3. Ensure the application has write access to the data directory

#### AI Recommendations Issues

If AI recommendations seem incorrect:

1. Verify the printer and material profiles are accurate
2. Check that print requirements are properly specified
3. Look for conflicting settings in the rule engine
4. Consider retraining the model with updated data

#### Klipper Integration Issues

If Klipper-specific features are not working:

1. Verify Klipper is properly installed and configured
2. Check that the "Use Klipper" option is enabled in the printer profile
3. Ensure pressure advance and input shaping values are valid
4. Verify the Klipper configuration file path is correct

### Logging

The application logs information to:
- Console output
- `logs/application.log`
- `logs/ai.log` (AI-specific logs)
- `logs/profiles.log` (Profile operations logs)

Log levels can be configured in `config.py`.
