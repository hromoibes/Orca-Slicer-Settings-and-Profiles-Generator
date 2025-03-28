"""
Orca Slicer Settings Generator - Settings Metadata
Module for managing settings metadata and relationships
"""

import os
import json
from typing import Dict, List, Any, Optional, Tuple, Union

class SettingsMetadata:
    """
    Manages metadata about 3D printing settings, their properties, and relationships.
    
    This class provides access to information about all available settings in Orca Slicer,
    including their types, ranges, impacts, and dependencies.
    """
    
    def __init__(self, metadata_file: str = None):
        """
        Initialize the settings metadata manager.
        
        Args:
            metadata_file: Path to JSON file containing settings metadata
        """
        self.metadata_file = metadata_file
        self.settings = {}
        self.categories = {}
        self.dependencies = {}
        self.load_metadata()
    
    def load_metadata(self):
        """Load settings metadata from file."""
        if not self.metadata_file or not os.path.exists(self.metadata_file):
            # Initialize with default metadata if file doesn't exist
            self._initialize_default_metadata()
            return
        
        try:
            with open(self.metadata_file, 'r') as f:
                data = json.load(f)
                self.settings = data.get('settings', {})
                self.categories = data.get('categories', {})
                self.dependencies = data.get('dependencies', {})
        except Exception as e:
            print(f"Error loading settings metadata: {e}")
            self._initialize_default_metadata()
    
    def save_metadata(self, output_file: str = None):
        """Save settings metadata to file."""
        file_path = output_file or self.metadata_file
        if not file_path:
            return False
        
        try:
            data = {
                'settings': self.settings,
                'categories': self.categories,
                'dependencies': self.dependencies
            }
            
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings metadata: {e}")
            return False
    
    def _initialize_default_metadata(self):
        """Initialize with default settings metadata."""
        self.categories = self._get_default_categories()
        self.settings = self._get_default_settings()
        self.dependencies = self._get_default_dependencies()
    
    def _get_default_categories(self) -> Dict[str, Any]:
        """Get default categories structure."""
        return {
            "quality": {
                "display_name": "Quality",
                "description": "Settings that affect the quality and detail of the print",
                "order": 1
            },
            "shell": {
                "display_name": "Shell",
                "description": "Settings for the outer shell of the print",
                "order": 2
            },
            "infill": {
                "display_name": "Infill",
                "description": "Settings for the internal structure of the print",
                "order": 3
            },
            "material": {
                "display_name": "Material",
                "description": "Settings related to the printing material",
                "order": 4
            },
            "speed": {
                "display_name": "Speed",
                "description": "Settings that control printing speed",
                "order": 5
            },
            "travel": {
                "display_name": "Travel",
                "description": "Settings for non-printing movements",
                "order": 6
            },
            "cooling": {
                "display_name": "Cooling",
                "description": "Settings for cooling during printing",
                "order": 7
            },
            "support": {
                "display_name": "Support",
                "description": "Settings for support structures",
                "order": 8
            },
            "adhesion": {
                "display_name": "Build Plate Adhesion",
                "description": "Settings for bed adhesion",
                "order": 9
            },
            "experimental": {
                "display_name": "Experimental",
                "description": "Experimental and advanced settings",
                "order": 10
            }
        }
    
    def _get_default_settings(self) -> Dict[str, Any]:
        """Get default settings metadata."""
        return {
            # Quality settings
            "layer_height": {
                "display_name": "Layer Height",
                "description": "Height of each printed layer. Lower values create finer details but increase print time.",
                "category": "quality",
                "subcategory": "height",
                "data_type": "float",
                "unit": "mm",
                "default_value": 0.2,
                "min_value": 0.05,
                "max_value": 0.8,
                "impact_level": 5,
                "common_values": [0.1, 0.12, 0.16, 0.2, 0.24, 0.28, 0.32]
            },
            "initial_layer_height": {
                "display_name": "Initial Layer Height",
                "description": "Height of the first layer. A thicker first layer improves bed adhesion.",
                "category": "quality",
                "subcategory": "height",
                "data_type": "float",
                "unit": "mm",
                "default_value": 0.3,
                "min_value": 0.1,
                "max_value": 0.8,
                "impact_level": 4,
                "common_values": [0.2, 0.25, 0.3, 0.35, 0.4]
            },
            "line_width": {
                "display_name": "Line Width",
                "description": "Width of a single printed line. Usually slightly larger than nozzle diameter.",
                "category": "quality",
                "subcategory": "width",
                "data_type": "float",
                "unit": "mm",
                "default_value": 0.44,
                "min_value": 0.1,
                "max_value": 2.0,
                "impact_level": 4,
                "common_values": [0.35, 0.4, 0.44, 0.48, 0.5, 0.6, 0.8]
            },
            
            # Shell settings
            "wall_thickness": {
                "display_name": "Wall Thickness",
                "description": "Thickness of the outer shell. Calculated as wall line count multiplied by line width.",
                "category": "shell",
                "subcategory": "walls",
                "data_type": "float",
                "unit": "mm",
                "default_value": 1.2,
                "min_value": 0.1,
                "max_value": 10.0,
                "impact_level": 4,
                "common_values": [0.8, 1.2, 1.6, 2.0, 2.4]
            },
            "wall_line_count": {
                "display_name": "Wall Line Count",
                "description": "Number of perimeter lines for the outer shell.",
                "category": "shell",
                "subcategory": "walls",
                "data_type": "int",
                "unit": "count",
                "default_value": 3,
                "min_value": 1,
                "max_value": 10,
                "impact_level": 4,
                "common_values": [2, 3, 4, 5]
            },
            "top_thickness": {
                "display_name": "Top Thickness",
                "description": "Thickness of the top layers. Calculated as top layers multiplied by layer height.",
                "category": "shell",
                "subcategory": "top_bottom",
                "data_type": "float",
                "unit": "mm",
                "default_value": 1.0,
                "min_value": 0.1,
                "max_value": 10.0,
                "impact_level": 3,
                "common_values": [0.8, 1.0, 1.2, 1.6, 2.0]
            },
            "top_layers": {
                "display_name": "Top Layers",
                "description": "Number of solid layers at the top of the print.",
                "category": "shell",
                "subcategory": "top_bottom",
                "data_type": "int",
                "unit": "count",
                "default_value": 5,
                "min_value": 0,
                "max_value": 20,
                "impact_level": 3,
                "common_values": [3, 4, 5, 6, 8]
            },
            "bottom_thickness": {
                "display_name": "Bottom Thickness",
                "description": "Thickness of the bottom layers. Calculated as bottom layers multiplied by layer height.",
                "category": "shell",
                "subcategory": "top_bottom",
                "data_type": "float",
                "unit": "mm",
                "default_value": 1.0,
                "min_value": 0.1,
                "max_value": 10.0,
                "impact_level": 3,
                "common_values": [0.8, 1.0, 1.2, 1.6, 2.0]
            },
            "bottom_layers": {
                "display_name": "Bottom Layers",
                "description": "Number of solid layers at the bottom of the print.",
                "category": "shell",
                "subcategory": "top_bottom",
                "data_type": "int",
                "unit": "count",
                "default_value": 4,
                "min_value": 0,
                "max_value": 20,
                "impact_level": 3,
                "common_values": [3, 4, 5, 6]
            },
            
            # Infill settings
            "infill_density": {
                "display_name": "Infill Density",
                "description": "Percentage of infill inside the print. Higher values create stronger parts but use more material.",
                "category": "infill",
                "subcategory": "density",
                "data_type": "float",
                "unit": "%",
                "default_value": 20.0,
                "min_value": 0.0,
                "max_value": 100.0,
                "impact_level": 5,
                "common_values": [0, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100]
            },
            "infill_pattern": {
                "display_name": "Infill Pattern",
                "description": "Pattern used for internal infill structure. Different patterns offer various strength and material usage trade-offs.",
                "category": "infill",
                "subcategory": "pattern",
                "data_type": "enum",
                "default_value": "gyroid",
                "options": ["grid", "lines", "triangles", "cubic", "gyroid", "honeycomb", "concentric", "zigzag"],
                "impact_level": 4
            },
            
            # Material settings
            "material_print_temperature": {
                "display_name": "Printing Temperature",
                "description": "Temperature of the nozzle during printing. Depends on material type.",
                "category": "material",
                "subcategory": "temperature",
                "data_type": "int",
                "unit": "°C",
                "default_value": 205,
                "min_value": 150,
                "max_value": 300,
                "impact_level": 5,
                "common_values": [180, 190, 200, 210, 220, 230, 240, 250, 260]
            },
            "material_bed_temperature": {
                "display_name": "Bed Temperature",
                "description": "Temperature of the build plate. Depends on material type.",
                "category": "material",
                "subcategory": "temperature",
                "data_type": "int",
                "unit": "°C",
                "default_value": 60,
                "min_value": 0,
                "max_value": 150,
                "impact_level": 4,
                "common_values": [0, 50, 60, 70, 80, 90, 100, 110]
            },
            "material_flow": {
                "display_name": "Flow Rate",
                "description": "Percentage of material flow. Adjust to fine-tune extrusion amount.",
                "category": "material",
                "subcategory": "flow",
                "data_type": "float",
                "unit": "%",
                "default_value": 100.0,
                "min_value": 50.0,
                "max_value": 200.0,
                "impact_level": 3,
                "common_values": [90, 95, 100, 105, 110]
            },
            
            # Speed settings
            "print_speed": {
                "display_name": "Print Speed",
                "description": "Base speed for printing movements. Other speeds are derived from this value.",
                "category": "speed",
                "subcategory": "speed",
                "data_type": "float",
                "unit": "mm/s",
                "default_value": 50.0,
                "min_value": 5.0,
                "max_value": 300.0,
                "impact_level": 5,
                "common_values": [30, 40, 50, 60, 70, 80, 100]
            },
            "infill_speed": {
                "display_name": "Infill Speed",
                "description": "Speed for printing infill. Usually faster than outer walls.",
                "category": "speed",
                "subcategory": "speed",
                "data_type": "float",
                "unit": "mm/s",
                "default_value": 80.0,
                "min_value": 5.0,
                "max_value": 300.0,
                "impact_level": 3,
                "common_values": [40, 50, 60, 70, 80, 100, 120]
            },
            "outer_wall_speed": {
                "display_name": "Outer Wall Speed",
                "description": "Speed for printing outer walls. Usually slower for better quality.",
                "category": "speed",
                "subcategory": "speed",
                "data_type": "float",
                "unit": "mm/s",
                "default_value": 25.0,
                "min_value": 1.0,
                "max_value": 200.0,
                "impact_level": 4,
                "common_values": [15, 20, 25, 30, 40, 50]
            },
            "inner_wall_speed": {
                "display_name": "Inner Wall Speed",
                "description": "Speed for printing inner walls.",
                "category": "speed",
                "subcategory": "speed",
                "data_type": "float",
                "unit": "mm/s",
                "default_value": 50.0,
                "min_value": 5.0,
                "max_value": 200.0,
                "impact_level": 3,
                "common_values": [30, 40, 50, 60, 70, 80]
            },
            "travel_speed": {
                "display_name": "Travel Speed",
                "description": "Speed for non-printing movements.",
                "category": "speed",
                "subcategory": "speed",
                "data_type": "float",
                "unit": "mm/s",
                "default_value": 150.0,
                "min_value": 50.0,
                "max_value": 500.0,
                "impact_level": 2,
                "common_values": [100, 120, 150, 180, 200, 250]
            },
            
            # Travel settings
            "retraction_enable": {
                "display_name": "Enable Retraction",
                "description": "Whether to retract filament during travel moves to reduce stringing.",
                "category": "travel",
                "subcategory": "retraction",
                "data_type": "bool",
                "default_value": True,
                "impact_level": 5
            },
            "retraction_distance": {
                "display_name": "Retraction Distance",
                "description": "Distance to retract filament. Direct drive extruders need less retraction than Bowden setups.",
                "category": "travel",
                "subcategory": "retraction",
                "data_type": "float",
                "unit": "mm",
                "default_value": 5.0,
                "min_value": 0.0,
                "max_value": 10.0,
                "impact_level": 4,
                "common_values": [0.5, 0.8, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
            },
            "retraction_speed": {
                "display_name": "Retraction Speed",
                "description": "Speed at which filament is retracted and unretracted.",
                "category": "travel",
                "subcategory": "retraction",
                "data_type": "float",
                "unit": "mm/s",
                "default_value": 45.0,
                "min_value": 5.0,
                "max_value": 150.0,
                "impact_level": 3,
                "common_values": [20, 25, 30, 35, 40, 45, 50, 60, 70]
            },
            "z_hop_enable": {
                "display_name": "Z Hop When Retracted",
                "description": "Whether to lift the nozzle when retracting to avoid hitting the print.",
                "category": "travel",
                "subcategory": "z_hop",
                "data_type": "bool",
                "default_value": False,
                "impact_level": 3
            },
            "z_hop_height": {
                "display_name": "Z Hop Height",
                "description": "Height to lift the nozzle when Z hop is enabled.",
                "category": "travel",
                "subcategory": "z_hop",
                "data_type": "float",
                "unit": "mm",
                "default_value": 0.2,
                "min_value": 0.1,
                "max_value": 2.0,
                "impact_level": 2,
                "common_values": [0.1, 0.2, 0.3, 0.4, 0.5]
            },
            
            # Cooling settings
            "cooling_enable": {
                "display_name": "Enable Print Cooling",
                "description": "Whether to enable the part cooling fan during printing.",
                "category": "cooling",
                "subcategory": "fan",
                "data_type": "bool",
                "default_value": True,
                "impact_level": 4
            },
            "fan_speed": {
                "display_name": "Fan Speed",
                "description": "Speed of the part cooling fan. Higher values improve cooling but can reduce layer adhesion.",
                "category": "cooling",
                "subcategory": "fan",
                "data_type": "float",
                "unit": "%",
                "default_value": 100.0,
                "min_value": 0.0,
                "max_value": 100.0,
                "impact_level": 4,
                "common_values": [0, 20, 40, 50, 60, 80, 100]
            },
            "initial_fan_speed": {
                "display_name": "Initial Fan Speed",
                "description": "Fan speed for the first few layers. Lower values improve bed adhesion.",
                "category": "cooling",
                "subcategory": "fan",
                "data_type": "float",
                "unit": "%",
                "default_value": 0.0,
                "min_value": 0.0,
                "max_value": 100.0,
                "impact_level": 3,
                "common_values": [0, 20, 40, 50, 60, 80, 100]
            },
            
            # Support settings
            "support_enable": {
                "display_name": "Generate Support",
                "description": "Whether to generate support structures for overhangs.",
                "category": "support",
                "subcategory": "support",
                "data_type": "bool",
                "default_value": False,
                "impact_level": 5
            },
            "support_type": {
                "display_name": "Support Placement",
                "description": "Where to place support structures.",
                "category": "support",
                "subcategory": "support",
                "data_type": "enum",
                "default_value": "everywhere",
                "options": ["none", "buildplate", "everywhere"],
                "impact_level": 4
            },
            "support_angle": {
                "display_name": "Support Overhang Angle",
                "description": "Minimum angle for support generation. Lower values create more support.",
                "category": "support",
                "subcategory": "support",
                "data_type": "float",
                "unit": "°",
                "default_value": 50.0,
                "min_value": 0.0,
                "max_value": 90.0,
                "impact_level": 4,
                "common_values": [30, 40, 45, 50, 55, 60, 70]
            },
            
            # Adhesion settings
            "adhesion_type": {
                "display_name": "Build Plate Adhesion Type",
                "description": "Type of adhesion helper to use.",
                "category": "adhesion",
                "subcategory": "adhesion",
                "data_type": "enum",
                "default_value": "skirt",
                "options": ["none", "skirt", "brim", "raft"],
                "impact_level": 4
            },
            "skirt_line_count": {
                "display_name": "Skirt Line Count",
                "description": "Number of skirt lines to print around the model.",
                "category": "adhesion",
                "subcategory": "skirt",
                "data_type": "int",
                "unit": "count",
                "default_value": 3,
                "min_value": 0,
                "max_value": 20,
                "impact_level": 2,
                "common_values": [1, 2, 3, 4, 5]
            },
            "brim_width": {
                "display_name": "Brim Width",
                "description": "Width of the brim in mm.",
                "category": "adhesion",
                "subcategory": "brim",
                "data_type": "float",
                "unit": "mm",
                "default_value": 8.0,
                "min_value": 0.0,
                "max_value": 30.0,
                "impact_level": 3,
                "common_values": [4, 6, 8, 10, 12, 15, 20]
            },
            
            # Experimental settings
            "ironing_enabled": {
                "display_name": "Enable Ironing",
                "description": "Whether to enable ironing for smooth top surfaces.",
                "category": "experimental",
                "subcategory": "ironing",
                "data_type": "bool",
                "default_value": False,
                "impact_level": 3
            },
            "adaptive_layers": {
                "display_name": "Adaptive Layers",
                "description": "Whether to vary layer height based on model geometry.",
                "category": "experimental",
                "subcategory": "adaptive",
                "data_type": "bool",
                "default_value": False,
                "impact_level": 4
            }
        }
    
    def _get_default_dependencies(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get default setting dependencies."""
        return {
            "layer_height": [
                {
                    "affects": "initial_layer_height",
                    "relationship": "multiplier",
                    "factor": 1.5,
                    "description": "Initial layer height is typically 1.5x the regular layer height"
                },
                {
                    "affects": "top_layers",
                    "relationship": "inverse",
                    "description": "Thinner layers require more top layers to maintain top thickness"
                },
                {
                    "affects": "bottom_layers",
                    "relationship": "inverse",
                    "description": "Thinner layers require more bottom layers to maintain bottom thickness"
                },
                {
                    "affects": "print_speed",
                    "relationship": "inverse",
                    "description": "Thinner layers typically require slower print speeds"
                }
            ],
            "nozzle_size": [
                {
                    "affects": "layer_height",
                    "relationship": "range",
                    "min_factor": 0.25,
                    "max_factor": 0.8,
                    "description": "Layer height should be between 25% and 80% of nozzle diameter"
                },
                {
                    "affects": "line_width",
                    "relationship": "multiplier",
                    "factor": 1.1,
                    "description": "Line width is typically 110% of nozzle diameter"
                }
            ],
            "line_width": [
                {
                    "affects": "wall_thickness",
                    "relationship": "multiplier",
                    "factor_source": "wall_line_count",
                    "description": "Wall thickness is line width multiplied by wall line count"
                }
            ],
            "print_speed": [
                {
                    "affects": "outer_wall_speed",
                    "relationship": "multiplier",
                    "factor": 0.5,
                    "description": "Outer wall speed is typically 50% of print speed"
                },
                {
                    "affects": "inner_wall_speed",
                    "relationship": "multiplier",
                    "factor": 0.8,
                    "description": "Inner wall speed is typically 80% of print speed"
                },
                {
                    "affects": "infill_speed",
                    "relationship": "multiplier",
                    "factor": 1.2,
                    "description": "Infill speed is typically 120% of print speed"
                },
                {
                    "affects": "travel_speed",
                    "relationship": "multiplier",
                    "factor": 1.5,
                    "description": "Travel speed is typically 150% of print speed"
                }
            ],
            "retraction_enable": [
                {
                    "affects": "z_hop_enable",
                    "relationship": "requirement",
                    "description": "Z hop requires retraction to be enabled"
                }
            ],
            "support_enable": [
                {
                    "affects": "support_type",
                    "relationship": "requirement",
                    "description": "Support type is only relevant when supports are enabled"
                },
                {
                    "affects": "support_angle",
                    "relationship": "requirement",
                    "description": "Support angle is only relevant when supports are enabled"
                }
            ],
            "adhesion_type": [
                {
                    "affects": "skirt_line_count",
                    "relationship": "conditional",
                    "condition": "equals",
                    "value": "skirt",
                    "description": "Skirt line count is only relevant when adhesion type is skirt"
                },
                {
                    "affects": "brim_width",
                    "relationship": "conditional",
                    "condition": "equals",
                    "value": "brim",
                    "description": "Brim width is only relevant when adhesion type is brim"
                }
            ]
        }
    
    def get_setting(self, setting_name: str) -> Dict[str, Any]:
        """
        Get metadata for a specific setting.
        
        Args:
            setting_name: Name of the setting
            
        Returns:
            Dictionary with setting metadata or empty dict if not found
        """
        return self.settings.get(setting_name, {})
    
    def get_settings_by_category(self, category: str) -> Dict[str, Dict[str, Any]]:
        """
        Get all settings in a specific category.
        
        Args:
            category: Category name
            
        Returns:
            Dictionary of settings in the category
        """
        result = {}
        for name, setting in self.settings.items():
            if setting.get('category') == category:
                result[name] = setting
        return result
    
    def get_settings_by_impact(self, min_impact: int = 1, max_impact: int = 5) -> Dict[str, Dict[str, Any]]:
        """
        Get settings within a specific impact level range.
        
        Args:
            min_impact: Minimum impact level (1-5)
            max_impact: Maximum impact level (1-5)
            
        Returns:
            Dictionary of settings within the impact range
        """
        result = {}
        for name, setting in self.settings.items():
            impact = setting.get('impact_level', 0)
            if min_impact <= impact <= max_impact:
                result[name] = setting
        return result
    
    def get_dependencies(self, setting_name: str) -> List[Dict[str, Any]]:
        """
        Get dependencies for a specific setting.
        
        Args:
            setting_name: Name of the setting
            
        Returns:
            List of dependency dictionaries
        """
        return self.dependencies.get(setting_name, [])
    
    def get_dependent_settings(self, setting_name: str) -> List[str]:
        """
        Get settings that are affected by a specific setting.
        
        Args:
            setting_name: Name of the setting
            
        Returns:
            List of setting names that are affected
        """
        result = []
        for name, deps in self.dependencies.items():
            for dep in deps:
                if dep.get('affects') == setting_name:
                    result.append(name)
        return result
    
    def get_all_categories(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all categories with metadata.
        
        Returns:
            Dictionary of categories
        """
        return self.categories
    
    def add_setting(self, name: str, metadata: Dict[str, Any]) -> bool:
        """
        Add a new setting to the metadata.
        
        Args:
            name: Setting name
            metadata: Setting metadata dictionary
            
        Returns:
            Success status
        """
        if name in self.settings:
            return False
        
        self.settings[name] = metadata
        return True
    
    def update_setting(self, name: str, metadata: Dict[str, Any]) -> bool:
        """
        Update an existing setting's metadata.
        
        Args:
            name: Setting name
            metadata: New setting metadata dictionary
            
        Returns:
            Success status
        """
        if name not in self.settings:
            return False
        
        self.settings[name] = metadata
        return True
    
    def add_dependency(self, setting_name: str, dependency: Dict[str, Any]) -> bool:
        """
        Add a dependency for a setting.
        
        Args:
            setting_name: Name of the setting
            dependency: Dependency dictionary
            
        Returns:
            Success status
        """
        if setting_name not in self.dependencies:
            self.dependencies[setting_name] = []
        
        self.dependencies[setting_name].append(dependency)
        return True
