# API Specification for Orca Slicer Settings Generator

This document outlines the API design for the Orca Slicer Settings Generator application, detailing the interfaces between components and external systems.

## Overview

The API is designed with a modular approach, separating concerns between the AI recommendation engine, profile management, settings database, and user interface. This design enables:

1. Clean separation between frontend and backend components
2. Extensibility for future features
3. Testability of individual components
4. Potential for future web service deployment

## Core API Components

### 1. AI Recommendation Engine API

The AI engine provides intelligent recommendations for slicer settings based on printer, material, and user requirements.

#### 1.1 Profile Generation

```python
def generate_profile(
    printer_id: int,
    material_id: int,
    nozzle_size: float,
    print_requirements: dict,
    base_profile_id: Optional[int] = None
) -> dict:
    """
    Generate an optimized profile based on printer, material and requirements.
    
    Args:
        printer_id: Database ID of the printer
        material_id: Database ID of the material
        nozzle_size: Nozzle diameter in mm
        print_requirements: Dict containing print priorities and requirements
            {
                'strength_importance': int(1-5),
                'surface_quality_importance': int(1-5),
                'speed_importance': int(1-5),
                'material_usage_importance': int(1-5),
                'dimensional_accuracy_importance': int(1-5),
                'purpose': str('functional'|'visual'|'miniature'|'large'),
                'custom_requirements': Optional[str]
            }
        base_profile_id: Optional ID of profile to use as starting point
        
    Returns:
        Dictionary containing complete profile with all settings
    """
```

#### 1.2 Setting Recommendation

```python
def recommend_setting(
    setting_name: str,
    printer_id: int,
    material_id: int,
    nozzle_size: float,
    current_settings: dict,
    print_requirements: dict
) -> dict:
    """
    Get AI recommendation for a specific setting.
    
    Args:
        setting_name: Name of the setting to recommend
        printer_id: Database ID of the printer
        material_id: Database ID of the material
        nozzle_size: Nozzle diameter in mm
        current_settings: Dict of current profile settings
        print_requirements: Dict containing print priorities
        
    Returns:
        {
            'value': recommended value,
            'confidence': float(0-1),
            'explanation': str,
            'alternatives': [
                {'value': alt_value, 'explanation': str},
                ...
            ]
        }
    """
```

#### 1.3 Setting Explanation

```python
def explain_setting(
    setting_name: str,
    setting_value: Any,
    context: dict
) -> dict:
    """
    Generate explanation for why a setting has a particular value.
    
    Args:
        setting_name: Name of the setting to explain
        setting_value: Current value of the setting
        context: Dict containing relevant context (printer, material, etc.)
        
    Returns:
        {
            'explanation': str,
            'impact': str,
            'trade_offs': str,
            'related_settings': [str]
        }
    """
```

#### 1.4 Profile Comparison

```python
def compare_profiles(
    profile_id_1: int,
    profile_id_2: int
) -> dict:
    """
    Compare two profiles and explain differences.
    
    Args:
        profile_id_1: Database ID of first profile
        profile_id_2: Database ID of second profile
        
    Returns:
        {
            'differences': [
                {
                    'setting': str,
                    'value_1': Any,
                    'value_2': Any,
                    'explanation': str,
                    'impact': str
                },
                ...
            ],
            'summary': str,
            'print_time_difference': float,  # estimated % difference
            'quality_difference': float,     # estimated % difference
            'strength_difference': float     # estimated % difference
        }
    """
```

#### 1.5 AI Model Training

```python
def train_model(
    training_data: List[dict],
    model_type: str = 'default'
) -> dict:
    """
    Train or update the AI model with new data.
    
    Args:
        training_data: List of training examples
        model_type: Type of model to train
        
    Returns:
        {
            'success': bool,
            'model_metrics': dict,
            'training_time': float
        }
    """
```

### 2. Profile Management API

Handles CRUD operations for printer profiles.

#### 2.1 Profile Operations

```python
def create_profile(profile_data: dict) -> int:
    """Create a new profile and return its ID."""
    
def get_profile(profile_id: int) -> dict:
    """Retrieve a profile by ID."""
    
def update_profile(profile_id: int, profile_data: dict) -> bool:
    """Update an existing profile."""
    
def delete_profile(profile_id: int) -> bool:
    """Delete a profile by ID."""
    
def list_profiles(filters: dict = None) -> List[dict]:
    """List profiles with optional filtering."""
    
def export_profile(profile_id: int, format: str = 'json') -> str:
    """Export a profile to the specified format."""
    
def import_profile(profile_data: str, format: str = 'json') -> int:
    """Import a profile from the specified format."""
```

#### 2.2 Profile Validation

```python
def validate_profile(profile_data: dict) -> dict:
    """
    Validate a profile for consistency and correctness.
    
    Args:
        profile_data: Complete profile data
        
    Returns:
        {
            'valid': bool,
            'errors': [str],
            'warnings': [str]
        }
    """
```

### 3. Settings Database API

Manages the database of 3D printing settings, their metadata, and relationships.

#### 3.1 Setting Operations

```python
def get_setting(setting_name: str) -> dict:
    """Get metadata for a specific setting."""
    
def list_settings(category: str = None) -> List[dict]:
    """List all settings, optionally filtered by category."""
    
def get_setting_dependencies(setting_name: str) -> List[dict]:
    """Get dependencies for a specific setting."""
    
def get_setting_impact(setting_name: str) -> dict:
    """Get impact information for a setting."""
```

#### 3.2 Printer Operations

```python
def create_printer(printer_data: dict) -> int:
    """Create a new printer definition."""
    
def get_printer(printer_id: int) -> dict:
    """Get printer information by ID."""
    
def list_printers() -> List[dict]:
    """List all available printers."""
    
def update_printer(printer_id: int, printer_data: dict) -> bool:
    """Update printer information."""
```

#### 3.3 Material Operations

```python
def create_material(material_data: dict) -> int:
    """Create a new material definition."""
    
def get_material(material_id: int) -> dict:
    """Get material information by ID."""
    
def list_materials() -> List[dict]:
    """List all available materials."""
    
def update_material(material_id: int, material_data: dict) -> bool:
    """Update material information."""
```

### 4. User Feedback API

Collects and processes user feedback to improve AI recommendations.

```python
def submit_feedback(
    profile_id: int,
    rating: int,
    comments: str = None,
    print_success: bool = None
) -> bool:
    """Submit user feedback for a profile."""
    
def get_feedback_stats(profile_id: int) -> dict:
    """Get aggregated feedback statistics for a profile."""
```

### 5. Export/Import API

Handles exporting and importing profiles to/from Orca Slicer format.

```python
def export_to_orca(
    profile_id: int,
    export_path: str
) -> bool:
    """
    Export a profile to Orca Slicer format.
    
    Args:
        profile_id: Database ID of the profile
        export_path: Path to save the exported file
        
    Returns:
        Success status
    """
    
def import_from_orca(
    file_path: str
) -> int:
    """
    Import a profile from Orca Slicer format.
    
    Args:
        file_path: Path to the Orca Slicer profile file
        
    Returns:
        Database ID of the imported profile
    """
```

## Data Models

### Profile Model

```python
class Profile:
    """Represents a complete printer profile with all settings."""
    
    profile_id: int
    name: str
    description: str
    printer_id: int
    material_id: int
    nozzle_size: float
    layer_height: float
    is_system_profile: bool
    is_user_modified: bool
    parent_profile_id: Optional[int]
    user_rating: Optional[int]
    feedback: Optional[str]
    settings: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
```

### Setting Model

```python
class Setting:
    """Represents metadata about a single slicer setting."""
    
    setting_id: int
    name: str
    display_name: str
    description: str
    category: str
    subcategory: Optional[str]
    data_type: str  # 'float', 'int', 'bool', 'enum', etc.
    default_value: Any
    min_value: Optional[Any]
    max_value: Optional[Any]
    unit: Optional[str]
    impact_level: int  # 1-5
```

### Printer Model

```python
class Printer:
    """Represents a 3D printer model."""
    
    printer_id: int
    manufacturer: str
    model: str
    printer_type: str  # 'cartesian', 'delta', 'corexy', etc.
    build_volume_x: float
    build_volume_y: float
    build_volume_z: float
    max_temp: int
    heated_bed: bool
    direct_drive: bool
    default_nozzle_size: float
```

### Material Model

```python
class Material:
    """Represents a filament material."""
    
    material_id: int
    name: str
    type: str  # 'PLA', 'PETG', 'ABS', etc.
    manufacturer: Optional[str]
    temp_range_min: int
    temp_range_max: int
    bed_temp_min: int
    bed_temp_max: int
    cooling_min: int
    cooling_max: int
    density: Optional[float]
    diameter: float
    special_considerations: Optional[str]
```

## API Implementation Details

### Technology Stack

The API will be implemented using:

1. **Python**: Core language for all components
2. **SQLite**: Database backend via SQLAlchemy ORM
3. **scikit-learn**: Machine learning framework for AI component
4. **FastAPI**: For potential future REST API exposure
5. **Pydantic**: For data validation and serialization

### Error Handling

All API functions will use a consistent error handling approach:

1. **Validation Errors**: Raised when input parameters fail validation
2. **Not Found Errors**: Raised when requested resources don't exist
3. **Permission Errors**: Raised when operations aren't permitted
4. **System Errors**: Raised for internal errors

Example error response:

```python
{
    'error': True,
    'error_type': 'validation_error',
    'message': 'Invalid printer ID',
    'details': {
        'field': 'printer_id',
        'reason': 'Printer with ID 123 not found'
    }
}
```

### Versioning

The API will use semantic versioning:

1. **Major version**: Incompatible API changes
2. **Minor version**: Backwards-compatible new functionality
3. **Patch version**: Backwards-compatible bug fixes

## Integration Points

### 1. Integration with Orca Slicer

The application will integrate with Orca Slicer through:

1. **File Export**: Generating compatible profile files
2. **File Import**: Reading existing Orca Slicer profiles
3. **Future Potential**: Direct plugin integration

### 2. Integration with External Data Sources

The application can integrate with:

1. **Community Profile Repositories**: For importing community-created profiles
2. **Material Databases**: For up-to-date material properties
3. **Printer Specifications**: For new printer models

## Security Considerations

1. **Input Validation**: All API inputs will be strictly validated
2. **SQL Injection Prevention**: Using parameterized queries via ORM
3. **File Path Validation**: Preventing path traversal attacks
4. **Error Handling**: Not exposing sensitive information in errors

## Performance Considerations

1. **Caching**: Frequently accessed data will be cached
2. **Batch Processing**: Operations on multiple items will use batch processing
3. **Asynchronous Processing**: Long-running operations will be asynchronous
4. **Database Indexing**: Proper indexes for common query patterns

## Future API Extensions

1. **REST API**: Exposing functionality as a web service
2. **Cloud Sync**: Syncing profiles across devices
3. **Community Features**: Sharing and rating profiles
4. **Advanced Analytics**: Print success prediction and analysis

## Conclusion

This API specification provides a comprehensive framework for the Orca Slicer Settings Generator application. The modular design separates concerns between components while providing clear interfaces for integration. The API is designed to be extensible, allowing for future enhancements and features as the application evolves.
