# Database Schema Design for Orca Slicer Settings Generator

This document details the database schema design for storing and managing profiles, settings, and related data in the Orca Slicer Settings Generator application.

## Overview

The database will use SQLite for local storage, providing a lightweight yet powerful solution that doesn't require a separate server. The schema is designed to efficiently represent the complex relationships between 3D printing settings while maintaining flexibility for future extensions.

## Entity-Relationship Diagram

```
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│               │       │               │       │               │
│    Printers   │       │   Profiles    │       │   Materials   │
│               │◄─────►│               │◄─────►│               │
└───────┬───────┘       └───────┬───────┘       └───────┬───────┘
        │                       │                       │
        │                       │                       │
        │                       ▼                       │
        │               ┌───────────────┐               │
        │               │               │               │
        └──────────────►│    Settings   │◄──────────────┘
                        │               │
                        └───────┬───────┘
                                │
                                │
                                ▼
                        ┌───────────────┐
                        │               │
                        │ Dependencies  │
                        │               │
                        └───────────────┘
```

## Table Definitions

### Printers

Stores information about 3D printer models and their capabilities.

```sql
CREATE TABLE printers (
    printer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer TEXT NOT NULL,
    model TEXT NOT NULL,
    printer_type TEXT NOT NULL,  -- 'cartesian', 'delta', 'corexy', etc.
    build_volume_x REAL NOT NULL,
    build_volume_y REAL NOT NULL,
    build_volume_z REAL NOT NULL,
    max_temp INTEGER NOT NULL,
    heated_bed BOOLEAN NOT NULL,
    direct_drive BOOLEAN NOT NULL,
    default_nozzle_size REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(manufacturer, model)
);
```

### Materials

Stores information about filament materials and their properties.

```sql
CREATE TABLE materials (
    material_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,  -- 'PLA', 'PETG', 'ABS', etc.
    manufacturer TEXT,
    temp_range_min INTEGER NOT NULL,
    temp_range_max INTEGER NOT NULL,
    bed_temp_min INTEGER NOT NULL,
    bed_temp_max INTEGER NOT NULL,
    cooling_min INTEGER NOT NULL,
    cooling_max INTEGER NOT NULL,
    density REAL,
    diameter REAL NOT NULL DEFAULT 1.75,
    special_considerations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, manufacturer)
);
```

### Settings

Stores metadata about all available settings in Orca Slicer.

```sql
CREATE TABLE settings (
    setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    display_name TEXT NOT NULL,
    description TEXT,
    category TEXT NOT NULL,  -- 'quality', 'speed', 'material', etc.
    subcategory TEXT,
    data_type TEXT NOT NULL,  -- 'float', 'int', 'bool', 'enum', etc.
    default_value TEXT,
    min_value TEXT,
    max_value TEXT,
    unit TEXT,
    impact_level INTEGER NOT NULL,  -- 1-5, with 5 being highest impact
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name)
);
```

### Dependencies

Stores relationships and dependencies between different settings.

```sql
CREATE TABLE dependencies (
    dependency_id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_id_1 INTEGER NOT NULL,
    setting_id_2 INTEGER NOT NULL,
    relationship_type TEXT NOT NULL,  -- 'affects', 'requires', 'conflicts', etc.
    relationship_strength REAL NOT NULL,  -- 0.0 to 1.0
    description TEXT,
    formula TEXT,  -- Optional mathematical relationship
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (setting_id_1) REFERENCES settings(setting_id),
    FOREIGN KEY (setting_id_2) REFERENCES settings(setting_id),
    UNIQUE(setting_id_1, setting_id_2, relationship_type)
);
```

### Profiles

Stores complete printer profiles with all settings.

```sql
CREATE TABLE profiles (
    profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    printer_id INTEGER,
    material_id INTEGER,
    nozzle_size REAL NOT NULL,
    layer_height REAL NOT NULL,
    is_system_profile BOOLEAN NOT NULL DEFAULT 0,
    is_user_modified BOOLEAN NOT NULL DEFAULT 0,
    parent_profile_id INTEGER,
    user_rating INTEGER,  -- 1-5 stars
    feedback TEXT,
    settings_json TEXT NOT NULL,  -- Complete JSON of all settings
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (printer_id) REFERENCES printers(printer_id),
    FOREIGN KEY (material_id) REFERENCES materials(material_id),
    FOREIGN KEY (parent_profile_id) REFERENCES profiles(profile_id)
);
```

### ProfileSettings

Stores individual setting values for each profile, enabling efficient querying and comparison.

```sql
CREATE TABLE profile_settings (
    profile_setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    setting_id INTEGER NOT NULL,
    value TEXT NOT NULL,
    is_modified BOOLEAN NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profile_id) REFERENCES profiles(profile_id),
    FOREIGN KEY (setting_id) REFERENCES settings(setting_id),
    UNIQUE(profile_id, setting_id)
);
```

### UserFeedback

Stores user feedback on generated profiles to improve AI recommendations.

```sql
CREATE TABLE user_feedback (
    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,  -- 1-5
    comments TEXT,
    print_success BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profile_id) REFERENCES profiles(profile_id)
);
```

### PrintRequirements

Stores user requirements for print jobs to guide profile generation.

```sql
CREATE TABLE print_requirements (
    requirement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    strength_importance INTEGER NOT NULL DEFAULT 3,  -- 1-5
    surface_quality_importance INTEGER NOT NULL DEFAULT 3,  -- 1-5
    speed_importance INTEGER NOT NULL DEFAULT 3,  -- 1-5
    material_usage_importance INTEGER NOT NULL DEFAULT 3,  -- 1-5
    dimensional_accuracy_importance INTEGER NOT NULL DEFAULT 3,  -- 1-5
    custom_requirements TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Indexes

To optimize query performance, we'll create the following indexes:

```sql
-- Profiles indexes
CREATE INDEX idx_profiles_printer ON profiles(printer_id);
CREATE INDEX idx_profiles_material ON profiles(material_id);
CREATE INDEX idx_profiles_layer_height ON profiles(layer_height);
CREATE INDEX idx_profiles_nozzle_size ON profiles(nozzle_size);

-- Settings indexes
CREATE INDEX idx_settings_category ON settings(category);
CREATE INDEX idx_settings_impact ON settings(impact_level);

-- Profile settings indexes
CREATE INDEX idx_profile_settings_profile ON profile_settings(profile_id);
CREATE INDEX idx_profile_settings_setting ON profile_settings(setting_id);
```

## Data Migration and Initialization

The database will be initialized with:

1. **Settings metadata**: All available Orca Slicer settings with descriptions
2. **Dependencies**: Known relationships between settings
3. **Common printers**: Pre-populated list of popular 3D printer models
4. **Common materials**: Standard filament types and their properties
5. **Base profiles**: Default profiles extracted from Orca Slicer

## Query Examples

### Get all settings for a profile

```sql
SELECT s.name, s.display_name, s.category, ps.value
FROM profile_settings ps
JOIN settings s ON ps.setting_id = s.setting_id
WHERE ps.profile_id = ?
ORDER BY s.category, s.display_name;
```

### Find profiles for a specific printer and material

```sql
SELECT p.*
FROM profiles p
WHERE p.printer_id = ? AND p.material_id = ?
ORDER BY p.created_at DESC;
```

### Get settings with high impact on print quality

```sql
SELECT *
FROM settings
WHERE impact_level >= 4
ORDER BY impact_level DESC, category;
```

### Find dependencies for a specific setting

```sql
SELECT s2.name, d.relationship_type, d.relationship_strength
FROM dependencies d
JOIN settings s1 ON d.setting_id_1 = s1.setting_id
JOIN settings s2 ON d.setting_id_2 = s2.setting_id
WHERE s1.name = ?
ORDER BY d.relationship_strength DESC;
```

## Versioning and Updates

The database schema includes timestamps on all tables to track when records are created or modified. This will help with:

1. Synchronizing data between different installations
2. Tracking changes to profiles over time
3. Supporting future features like profile version history

## Backup and Recovery

The SQLite database file will be designed for easy backup:

1. Regular automatic backups to a backup directory
2. Export/import functionality for profiles
3. Schema version tracking for future upgrades

## Conclusion

This database schema provides a solid foundation for the Orca Slicer Settings Generator. It efficiently represents the complex relationships between 3D printing settings while maintaining flexibility for future extensions. The use of SQLite ensures the application remains lightweight and portable while still providing robust data storage capabilities.
