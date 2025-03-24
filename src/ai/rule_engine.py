"""
Orca Slicer Settings Generator - Rule Engine
Module for the rule-based component of the AI recommendation engine
"""

import json
import os
from typing import Dict, List, Any, Optional, Tuple, Union

class RuleEngine:
    """
    Rule-based expert system for 3D printing settings recommendations.
    
    This class implements the rule-based component of the hybrid AI approach,
    providing explainable recommendations based on expert knowledge.
    """
    
    def __init__(self, rules_file: str = None):
        """
        Initialize the rule engine.
        
        Args:
            rules_file: Path to JSON file containing rule definitions
        """
        self.rules_file = rules_file
        self.rules = {}
        self.load_rules()
    
    def load_rules(self):
        """Load rules from the rules file."""
        if not self.rules_file or not os.path.exists(self.rules_file):
            # Initialize with default rules if file doesn't exist
            self.rules = self._get_default_rules()
            return
        
        try:
            with open(self.rules_file, 'r') as f:
                self.rules = json.load(f)
        except Exception as e:
            print(f"Error loading rules: {e}")
            self.rules = self._get_default_rules()
    
    def save_rules(self, output_file: str = None):
        """Save rules to a file."""
        file_path = output_file or self.rules_file
        if not file_path:
            return False
        
        try:
            with open(file_path, 'w') as f:
                json.dump(self.rules, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving rules: {e}")
            return False
    
    def _get_default_rules(self) -> Dict[str, Any]:
        """Get default rule definitions."""
        return {
            "material_rules": {
                "PLA": {
                    "temperature": {
                        "min": 190,
                        "max": 220,
                        "optimal": 205,
                        "quality_offset": -5,
                        "speed_offset": 10
                    },
                    "bed_temperature": {
                        "min": 50,
                        "max": 60,
                        "optimal": 55
                    },
                    "cooling": {
                        "min": 80,
                        "max": 100,
                        "optimal": 100
                    },
                    "retraction": {
                        "direct_drive": {
                            "distance": 0.8,
                            "speed": 35
                        },
                        "bowden": {
                            "distance": 5.0,
                            "speed": 45
                        }
                    }
                },
                "PETG": {
                    "temperature": {
                        "min": 220,
                        "max": 250,
                        "optimal": 235,
                        "quality_offset": -5,
                        "speed_offset": 10
                    },
                    "bed_temperature": {
                        "min": 70,
                        "max": 85,
                        "optimal": 75
                    },
                    "cooling": {
                        "min": 30,
                        "max": 60,
                        "optimal": 50
                    },
                    "retraction": {
                        "direct_drive": {
                            "distance": 1.0,
                            "speed": 30
                        },
                        "bowden": {
                            "distance": 6.0,
                            "speed": 40
                        }
                    }
                },
                "ABS": {
                    "temperature": {
                        "min": 230,
                        "max": 260,
                        "optimal": 245,
                        "quality_offset": -5,
                        "speed_offset": 10
                    },
                    "bed_temperature": {
                        "min": 90,
                        "max": 110,
                        "optimal": 100
                    },
                    "cooling": {
                        "min": 0,
                        "max": 30,
                        "optimal": 20
                    },
                    "retraction": {
                        "direct_drive": {
                            "distance": 0.8,
                            "speed": 30
                        },
                        "bowden": {
                            "distance": 5.0,
                            "speed": 40
                        }
                    }
                },
                "TPU": {
                    "temperature": {
                        "min": 220,
                        "max": 250,
                        "optimal": 235,
                        "quality_offset": -5,
                        "speed_offset": 10
                    },
                    "bed_temperature": {
                        "min": 30,
                        "max": 50,
                        "optimal": 40
                    },
                    "cooling": {
                        "min": 50,
                        "max": 100,
                        "optimal": 80
                    },
                    "retraction": {
                        "direct_drive": {
                            "distance": 0.5,
                            "speed": 20
                        },
                        "bowden": {
                            "distance": 2.0,
                            "speed": 20
                        }
                    }
                }
            },
            "printer_rules": {
                "cartesian": {
                    "max_speed": 150,
                    "max_acceleration": 3000,
                    "jerk": 10
                },
                "delta": {
                    "max_speed": 200,
                    "max_acceleration": 4000,
                    "jerk": 15
                },
                "corexy": {
                    "max_speed": 180,
                    "max_acceleration": 3500,
                    "jerk": 12
                }
            },
            "nozzle_rules": {
                "0.2": {
                    "min_layer_height": 0.08,
                    "max_layer_height": 0.16,
                    "optimal_layer_height": 0.12,
                    "line_width": 0.22
                },
                "0.3": {
                    "min_layer_height": 0.12,
                    "max_layer_height": 0.24,
                    "optimal_layer_height": 0.16,
                    "line_width": 0.33
                },
                "0.4": {
                    "min_layer_height": 0.12,
                    "max_layer_height": 0.32,
                    "optimal_layer_height": 0.2,
                    "line_width": 0.44
                },
                "0.5": {
                    "min_layer_height": 0.15,
                    "max_layer_height": 0.4,
                    "optimal_layer_height": 0.25,
                    "line_width": 0.55
                },
                "0.6": {
                    "min_layer_height": 0.18,
                    "max_layer_height": 0.48,
                    "optimal_layer_height": 0.3,
                    "line_width": 0.66
                },
                "0.8": {
                    "min_layer_height": 0.24,
                    "max_layer_height": 0.64,
                    "optimal_layer_height": 0.4,
                    "line_width": 0.88
                },
                "1.0": {
                    "min_layer_height": 0.3,
                    "max_layer_height": 0.8,
                    "optimal_layer_height": 0.5,
                    "line_width": 1.1
                }
            },
            "purpose_rules": {
                "functional": {
                    "wall_line_count": 3,
                    "infill_density": 30,
                    "infill_pattern": "cubic",
                    "top_layers": 5,
                    "bottom_layers": 4
                },
                "visual": {
                    "wall_line_count": 2,
                    "infill_density": 15,
                    "infill_pattern": "gyroid",
                    "top_layers": 4,
                    "bottom_layers": 3
                },
                "miniature": {
                    "wall_line_count": 2,
                    "infill_density": 10,
                    "infill_pattern": "gyroid",
                    "top_layers": 4,
                    "bottom_layers": 3,
                    "z_hop_enable": True,
                    "support_enable": True,
                    "support_angle": 60
                },
                "large": {
                    "wall_line_count": 2,
                    "infill_density": 10,
                    "infill_pattern": "grid",
                    "top_layers": 3,
                    "bottom_layers": 3,
                    "adhesion_type": "brim",
                    "brim_width": 8
                }
            },
            "quality_rules": {
                "ultra": {
                    "layer_height_factor": 0.25,
                    "speed_factor": 0.7,
                    "outer_wall_speed_factor": 0.5,
                    "ironing_enabled": True
                },
                "high": {
                    "layer_height_factor": 0.3,
                    "speed_factor": 0.8,
                    "outer_wall_speed_factor": 0.6,
                    "ironing_enabled": False
                },
                "standard": {
                    "layer_height_factor": 0.4,
                    "speed_factor": 1.0,
                    "outer_wall_speed_factor": 0.7,
                    "ironing_enabled": False
                },
                "draft": {
                    "layer_height_factor": 0.6,
                    "speed_factor": 1.2,
                    "outer_wall_speed_factor": 0.8,
                    "ironing_enabled": False
                },
                "ultra_draft": {
                    "layer_height_factor": 0.75,
                    "speed_factor": 1.5,
                    "outer_wall_speed_factor": 0.9,
                    "ironing_enabled": False
                }
            },
            "speed_rules": {
                "ultra_slow": {
                    "print_speed": 30,
                    "outer_wall_speed_factor": 0.5,
                    "inner_wall_speed_factor": 0.8,
                    "infill_speed_factor": 1.2,
                    "travel_speed_factor": 1.5
                },
                "slow": {
                    "print_speed": 40,
                    "outer_wall_speed_factor": 0.5,
                    "inner_wall_speed_factor": 0.8,
                    "infill_speed_factor": 1.2,
                    "travel_speed_factor": 1.5
                },
                "normal": {
                    "print_speed": 50,
                    "outer_wall_speed_factor": 0.5,
                    "inner_wall_speed_factor": 0.8,
                    "infill_speed_factor": 1.2,
                    "travel_speed_factor": 1.5
                },
                "fast": {
                    "print_speed": 70,
                    "outer_wall_speed_factor": 0.5,
                    "inner_wall_speed_factor": 0.8,
                    "infill_speed_factor": 1.2,
                    "travel_speed_factor": 1.5
                },
                "ultra_fast": {
                    "print_speed": 100,
                    "outer_wall_speed_factor": 0.6,
                    "inner_wall_speed_factor": 0.9,
                    "infill_speed_factor": 1.3,
                    "travel_speed_factor": 1.5
                }
            },
            "strength_rules": {
                "ultra_strong": {
                    "wall_line_count": 4,
                    "infill_density": 50,
                    "infill_pattern": "cubic",
                    "top_layers_factor": 1.5,
                    "bottom_layers_factor": 1.5
                },
                "strong": {
                    "wall_line_count": 3,
                    "infill_density": 30,
                    "infill_pattern": "cubic",
                    "top_layers_factor": 1.2,
                    "bottom_layers_factor": 1.2
                },
                "normal": {
                    "wall_line_count": 3,
                    "infill_density": 20,
                    "infill_pattern": "gyroid",
                    "top_layers_factor": 1.0,
                    "bottom_layers_factor": 1.0
                },
                "light": {
                    "wall_line_count": 2,
                    "infill_density": 15,
                    "infill_pattern": "gyroid",
                    "top_layers_factor": 0.8,
                    "bottom_layers_factor": 0.8
                },
                "ultra_light": {
                    "wall_line_count": 2,
                    "infill_density": 10,
                    "infill_pattern": "grid",
                    "top_layers_factor": 0.7,
                    "bottom_layers_factor": 0.7
                }
            },
            "setting_dependencies": {
                "layer_height": {
                    "affects": ["initial_layer_height", "top_layers", "bottom_layers"],
                    "affected_by": ["nozzle_size"]
                },
                "line_width": {
                    "affects": ["wall_thickness"],
                    "affected_by": ["nozzle_size"]
                },
                "wall_line_count": {
                    "affects": ["wall_thickness"],
                    "affected_by": ["strength_importance"]
                },
                "print_speed": {
                    "affects": ["outer_wall_speed", "inner_wall_speed", "infill_speed"],
                    "affected_by": ["quality_importance", "speed_importance"]
                },
                "material_print_temperature": {
                    "affects": ["cooling"],
                    "affected_by": ["material_type", "print_speed"]
                }
            }
        }
    
    def apply_rules(
        self,
        printer_info: Dict[str, Any],
        material_info: Dict[str, Any],
        nozzle_size: float,
        print_requirements: Dict[str, Any],
        current_settings: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply rules to generate or modify settings.
        
        Args:
            printer_info: Dictionary with printer information
            material_info: Dictionary with material information
            nozzle_size: Nozzle diameter in mm
            print_requirements: Dictionary with print requirements
            current_settings: Dictionary with current settings (can be empty)
            
        Returns:
            Dictionary with updated settings
        """
        # Start with current settings or empty dict
        settings = current_settings.copy() if current_settings else {}
        
        # Apply rules in a specific order to handle dependencies correctly
        settings = self._apply_material_rules(settings, material_info, printer_info)
        settings = self._apply_nozzle_rules(settings, nozzle_size)
        settings = self._apply_printer_rules(settings, printer_info)
        settings = self._apply_purpose_rules(settings, print_requirements)
        settings = self._apply_quality_rules(settings, print_requirements, nozzle_size)
        settings = self._apply_speed_rules(settings, print_requirements)
        settings = self._apply_strength_rules(settings, print_requirements)
        
        # Apply setting dependencies to ensure consistency
        settings = self._apply_dependencies(settings)
        
        return settings
    
    def _apply_material_rules(
        self,
        settings: Dict[str, Any],
        material_info: Dict[str, Any],
        printer_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply material-specific rules."""
        material_type = material_info.get('type', 'PLA')
        
        # Get material rules
        material_rules = self.rules.get('material_rules', {}).get(material_type)
        if not material_rules:
            return settings
        
        # Apply temperature rules
        temp_rules = material_rules.get('temperature', {})
        if temp_rules:
            settings['material_print_temperature'] = temp_rules.get('optimal')
        
        # Apply bed temperature rules
        bed_temp_rules = material_rules.get('bed_temperature', {})
        if bed_temp_rules:
            settings['material_bed_temperature'] = bed_temp_rules.get('optimal')
        
        # Apply cooling rules
        cooling_rules = material_rules.get('cooling', {})
        if cooling_rules:
            settings['cooling_enable'] = True
            settings['fan_speed'] = cooling_rules.get('optimal')
            settings['initial_fan_speed'] = cooling_rules.get('min')
        
        # Apply retraction rules based on extruder type
        retraction_rules = material_rules.get('retraction', {})
        if retraction_rules:
            extruder_type = 'direct_drive' if printer_info.get('direct_drive') else 'bowden'
            extruder_rules = retraction_rules.get(extruder_type, {})
            
            if extruder_rules:
                settings['retraction_enable'] = True
                settings['retraction_distance'] = extruder_rules.get('distance')
                settings['retraction_speed'] = extruder_rules.get('speed')
        
        return settings
    
    def _apply_nozzle_rules(
        self,
        settings: Dict[str, Any],
        nozzle_size: float
    ) -> Dict[str, Any]:
        """Apply nozzle-specific rules."""
        # Convert to string for lookup
        nozzle_key = str(nozzle_size)
        
        # Find closest nozzle size if exact match not found
        if nozzle_key not in self.rules.get('nozzle_rules', {}):
            nozzle_sizes = [float(k) for k in self.rules.get('nozzle_rules', {}).keys()]
            closest = min(nozzle_sizes, key=lambda x: abs(x - nozzle_size))
            nozzle_key = str(closest)
        
        nozzle_rules = self.rules.get('nozzle_rules', {}).get(nozzle_key)
        if not nozzle_rules:
            return settings
        
        # Apply layer height rules
        settings['layer_height'] = nozzle_rules.get('optimal_layer_height')
        
        # Apply line width rules
        settings['line_width'] = nozzle_rules.get('line_width')
        
        return settings
    
    def _apply_printer_rules(
        self,
        settings: Dict[str, Any],
        printer_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply printer-specific rules."""
        printer_type = printer_info.get('printer_type', 'cartesian')
        
        printer_rules = self.rules.get('printer_rules', {}).get(printer_type)
        if not printer_rules:
            return settings
        
        # Apply speed and acceleration rules
        settings['travel_speed'] = printer_rules.get('max_speed')
        
        # Apply printer-specific settings
        if printer_type == 'delta':
            # Delta printers often benefit from these settings
            settings['z_hop_enable'] = True
            settings['z_hop_height'] = 0.2
        
        return settings
    
    def _apply_purpose_rules(
        self,
        settings: Dict[str, Any],
        print_requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply purpose-specific rules."""
        purpose = print_requirements.get('purpose', 'visual')
        
        purpose_rules = self.rules.get('purpose_rules', {}).get(purpose)
        if not purpose_rules:
            return settings
        
        # Apply purpose-specific settings
        for key, value in purpose_rules.items():
            settings[key] = value
        
        return settings
    
    def _apply_quality_rules(
        self,
        settings: Dict[str, Any],
        print_requirements: Dict[str, Any],
        nozzle_size: float
    ) -> Dict[str, Any]:
        """Apply quality-specific rules."""
        quality_importance = print_requirements.get('surface_quality_importance', 3)
        
        # Map importance to quality level
        quality_level = 'standard'
        if quality_importance >= 5:
            quality_level = 'ultra'
        elif quality_importance >= 4:
            quality_level = 'high'
        elif quality_importance <= 2:
            quality_level = 'draft'
        elif quality_importance <= 1:
            quality_level = 'ultra_draft'
        
        quality_rules = self.rules.get('quality_rules', {}).get(quality_level)
        if not quality_rules:
            return settings
        
        # Apply layer height adjustment
        if 'layer_height' in settings:
            # Find closest nozzle size for reference
            nozzle_key = str(nozzle_size)
            if nozzle_key not in self.rules.get('nozzle_rules', {}):
                nozzle_sizes = [float(k) for k in self.rules.get('nozzle_rules', {}).keys()]
                closest = min(nozzle_sizes, key=lambda x: abs(x - nozzle_size))
                nozzle_key = str(closest)
            
            nozzle_rules = self.rules.get('nozzle_rules', {}).get(nozzle_key, {})
            max_layer_height = nozzle_rules.get('max_layer_height', nozzle_size * 0.8)
            
            # Apply layer height factor
            layer_height_factor = quality_rules.get('layer_height_factor', 0.4)
            settings['layer_height'] = round(max_layer_height * layer_height_factor, 2)
        
        # Apply speed adjustments
        if 'print_speed' in settings:
            speed_factor = quality_rules.get('speed_factor', 1.0)
            settings['print_speed'] = round(settings['print_speed'] * speed_factor)
        
        # Apply outer wall speed adjustment
        if 'print_speed' in settings:
            outer_wall_speed_factor = quality_rules.get('outer_wall_speed_factor', 0.7)
            settings['outer_wall_speed'] = round(settings['print_speed'] * outer_wall_speed_factor)
        
        # Apply ironing setting
        settings['ironing_enabled'] = quality_rules.get('ironing_enabled', False)
        
        return settings
    
    def _apply_speed_rules(
        self,
        settings: Dict[str, Any],
        print_requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply speed-specific rules."""
        speed_importance = print_requirements.get('speed_importance', 3)
        
        # Map importance to speed level
        speed_level = 'normal'
        if speed_importance >= 5:
            speed_level = 'ultra_fast'
        elif speed_importance >= 4:
            speed_level = 'fast'
        elif speed_importance <= 2:
            speed_level = 'slow'
        elif speed_importance <= 1:
            speed_level = 'ultra_slow'
        
        speed_rules = self.rules.get('speed_rules', {}).get(speed_level)
        if not speed_rules:
            return settings
        
        # Apply base print speed
        settings['print_speed'] = speed_rules.get('print_speed', 50)
        
        # Apply derived speeds
        outer_wall_speed_factor = speed_rules.get('outer_wall_speed_factor', 0.5)
        inner_wall_speed_factor = speed_rules.get('inner_wall_speed_factor', 0.8)
        infill_speed_factor = speed_rules.get('infill_speed_factor', 1.2)
        travel_speed_factor = speed_rules.get('travel_speed_factor', 1.5)
        
        settings['outer_wall_speed'] = round(settings['print_speed'] * outer_wall_speed_factor)
        settings['inner_wall_speed'] = round(settings['print_speed'] * inner_wall_speed_factor)
        settings['infill_speed'] = round(settings['print_speed'] * infill_speed_factor)
        settings['travel_speed'] = round(settings['print_speed'] * travel_speed_factor)
        
        return settings
    
    def _apply_strength_rules(
        self,
        settings: Dict[str, Any],
        print_requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply strength-specific rules."""
        strength_importance = print_requirements.get('strength_importance', 3)
        
        # Map importance to strength level
        strength_level = 'normal'
        if strength_importance >= 5:
            strength_level = 'ultra_strong'
        elif strength_importance >= 4:
            strength_level = 'strong'
        elif strength_importance <= 2:
            strength_level = 'light'
        elif strength_importance <= 1:
            strength_level = 'ultra_light'
        
        strength_rules = self.rules.get('strength_rules', {}).get(strength_level)
        if not strength_rules:
            return settings
        
        # Apply wall count
        settings['wall_line_count'] = strength_rules.get('wall_line_count', 3)
        
        # Apply infill settings
        settings['infill_density'] = strength_rules.get('infill_density', 20)
        settings['infill_pattern'] = strength_rules.get('infill_pattern', 'gyroid')
        
        # Apply top/bottom layer adjustments
        if 'layer_height' in settings:
            top_layers_factor = strength_rules.get('top_layers_factor', 1.0)
            bottom_layers_factor = strength_rules.get('bottom_layers_factor', 1.0)
            
            # Base values
            base_top_layers = 4
            base_bottom_layers = 3
            
            settings['top_layers'] = round(base_top_layers * top_layers_factor)
            settings['bottom_layers'] = round(base_bottom_layers * bottom_layers_factor)
            
            # Calculate thicknesses
            settings['top_thickness'] = settings['top_layers'] * settings['layer_height']
            settings['bottom_thickness'] = settings['bottom_layers'] * settings['layer_height']
        
        return settings
    
    def _apply_dependencies(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Apply setting dependencies to ensure consistency."""
        dependencies = self.rules.get('setting_dependencies', {})
        
        # Process each setting that has dependencies
        for setting_name, deps in dependencies.items():
            if setting_name not in settings:
                continue
            
            # Process settings affected by this setting
            for affected_setting in deps.get('affects', []):
                if affected_setting == 'initial_layer_height' and 'layer_height' in settings:
                    settings['initial_layer_height'] = round(settings['layer_height'] * 1.5, 2)
                
                elif affected_setting == 'top_layers' and 'layer_height' in settings:
                    if 'top_thickness' in settings:
                        settings['top_layers'] = round(settings['top_thickness'] / settings['layer_height'])
                
                elif affected_setting == 'bottom_layers' and 'layer_height' in settings:
                    if 'bottom_thickness' in settings:
                        settings['bottom_layers'] = round(settings['bottom_thickness'] / settings['layer_height'])
                
                elif affected_setting == 'wall_thickness' and 'line_width' in settings:
                    if 'wall_line_count' in settings:
                        settings['wall_thickness'] = settings['wall_line_count'] * settings['line_width']
                
                elif affected_setting == 'outer_wall_speed' and 'print_speed' in settings:
                    if 'outer_wall_speed' not in settings:
                        settings['outer_wall_speed'] = round(settings['print_speed'] * 0.5)
                
                elif affected_setting == 'inner_wall_speed' and 'print_speed' in settings:
                    if 'inner_wall_speed' not in settings:
                        settings['inner_wall_speed'] = round(settings['print_speed'] * 0.8)
                
                elif affected_setting == 'infill_speed' and 'print_speed' in settings:
                    if 'infill_speed' not in settings:
                        settings['infill_speed'] = round(settings['print_speed'] * 1.2)
        
        # Ensure adhesion settings are consistent
        if 'adhesion_type' in settings:
            if settings['adhesion_type'] == 'skirt':
                settings['brim_width'] = 0
            elif settings['adhesion_type'] == 'brim':
                settings['skirt_line_count'] = 0
            elif settings['adhesion_type'] == 'raft':
                settings['skirt_line_count'] = 0
                settings['brim_width'] = 0
        
        # Ensure support settings are consistent
        if 'support_enable' in settings and not settings['support_enable']:
            settings['support_type'] = 'none'
        
        return settings
    
    def get_explanation(
        self,
        setting_name: str,
        setting_value: Any,
        printer_info: Dict[str, Any],
        material_info: Dict[str, Any],
        print_requirements: Dict[str, Any]
    ) -> str:
        """
        Generate an explanation for a setting value based on rules.
        
        Args:
            setting_name: Name of the setting
            setting_value: Value of the setting
            printer_info: Dictionary with printer information
            material_info: Dictionary with material information
            print_requirements: Dictionary with print requirements
            
        Returns:
            Explanation string
        """
        # Common settings explanations
        if setting_name == 'layer_height':
            return self._explain_layer_height(setting_value, print_requirements)
        
        elif setting_name == 'material_print_temperature':
            return self._explain_temperature(setting_value, material_info, print_requirements)
        
        elif setting_name == 'print_speed':
            return self._explain_print_speed(setting_value, print_requirements)
        
        elif setting_name == 'infill_density':
            return self._explain_infill_density(setting_value, print_requirements)
        
        elif setting_name == 'wall_line_count':
            return self._explain_wall_count(setting_value, print_requirements)
        
        elif setting_name == 'retraction_distance':
            return self._explain_retraction_distance(setting_value, printer_info, material_info)
        
        # Generic explanation
        return f"Setting {setting_name} has value {setting_value} based on printer, material, and print requirements."
    
    def _explain_layer_height(self, value: float, requirements: Dict[str, Any]) -> str:
        """Generate explanation for layer height setting."""
        quality_importance = requirements.get('surface_quality_importance', 3)
        speed_importance = requirements.get('speed_importance', 3)
        
        if value <= 0.1:
            quality_text = "very fine"
            detail_text = "maximum detail"
            speed_text = "significantly longer"
        elif value <= 0.16:
            quality_text = "fine"
            detail_text = "high detail"
            speed_text = "longer"
        elif value <= 0.24:
            quality_text = "standard"
            detail_text = "good detail"
            speed_text = "standard"
        elif value <= 0.32:
            quality_text = "coarse"
            detail_text = "reduced detail"
            speed_text = "faster"
        else:
            quality_text = "very coarse"
            detail_text = "minimal detail"
            speed_text = "much faster"
        
        if quality_importance > speed_importance:
            reason = f"prioritizing quality over speed (quality importance: {quality_importance}, speed importance: {speed_importance})"
        elif speed_importance > quality_importance:
            reason = f"prioritizing speed over quality (speed importance: {speed_importance}, quality importance: {quality_importance})"
        else:
            reason = "balancing quality and speed equally"
        
        return (
            f"Layer height of {value}mm uses {quality_text} layers for {detail_text}, "
            f"resulting in {speed_text} print times. This value was selected {reason}."
        )
    
    def _explain_temperature(self, value: float, material_info: Dict[str, Any], requirements: Dict[str, Any]) -> str:
        """Generate explanation for temperature setting."""
        material_type = material_info.get('type', 'PLA')
        min_temp = material_info.get('temp_range_min', 190)
        max_temp = material_info.get('temp_range_max', 220)
        mid_temp = (min_temp + max_temp) / 2
        
        purpose = requirements.get('purpose', 'visual')
        strength_importance = requirements.get('strength_importance', 3)
        
        if value < mid_temp:
            temp_text = "lower end"
            effect_text = "better detail and reduced stringing, but potentially weaker layer adhesion"
        elif value > mid_temp:
            temp_text = "higher end"
            effect_text = "better layer adhesion and strength, but potentially more stringing"
        else:
            temp_text = "middle"
            effect_text = "balanced detail and strength"
        
        if purpose == 'functional' or strength_importance >= 4:
            reason = "prioritizing strength and layer adhesion"
        elif purpose == 'visual':
            reason = "prioritizing visual quality and detail"
        else:
            reason = "balancing quality and strength"
        
        return (
            f"Print temperature of {value}°C is in the {temp_text} of the recommended range "
            f"for {material_type} ({min_temp}°C-{max_temp}°C), providing {effect_text}. "
            f"This temperature was selected {reason}."
        )
    
    def _explain_print_speed(self, value: float, requirements: Dict[str, Any]) -> str:
        """Generate explanation for print speed setting."""
        speed_importance = requirements.get('speed_importance', 3)
        quality_importance = requirements.get('surface_quality_importance', 3)
        
        if value <= 30:
            speed_text = "very slow"
            quality_text = "maximum quality"
            time_text = "significantly longer"
        elif value <= 45:
            speed_text = "slow"
            quality_text = "high quality"
            time_text = "longer"
        elif value <= 60:
            speed_text = "standard"
            quality_text = "good quality"
            time_text = "standard"
        elif value <= 80:
            speed_text = "fast"
            quality_text = "reduced quality"
            time_text = "shorter"
        else:
            speed_text = "very fast"
            quality_text = "minimal quality"
            time_text = "much shorter"
        
        if speed_importance > quality_importance:
            reason = f"prioritizing speed over quality (speed importance: {speed_importance}, quality importance: {quality_importance})"
        elif quality_importance > speed_importance:
            reason = f"prioritizing quality over speed (quality importance: {quality_importance}, speed importance: {speed_importance})"
        else:
            reason = "balancing speed and quality equally"
        
        return (
            f"Print speed of {value}mm/s is {speed_text}, resulting in {quality_text} and {time_text} print times. "
            f"This value was selected {reason}."
        )
    
    def _explain_infill_density(self, value: float, requirements: Dict[str, Any]) -> str:
        """Generate explanation for infill density setting."""
        strength_importance = requirements.get('strength_importance', 3)
        material_usage = requirements.get('material_usage_importance', 3)
        
        if value <= 10:
            density_text = "very low"
            strength_text = "minimal strength"
            usage_text = "minimal material"
        elif value <= 20:
            density_text = "low"
            strength_text = "moderate strength"
            usage_text = "reduced material"
        elif value <= 30:
            density_text = "medium"
            strength_text = "good strength"
            usage_text = "moderate material"
        elif value <= 50:
            density_text = "high"
            strength_text = "high strength"
            usage_text = "increased material"
        else:
            density_text = "very high"
            strength_text = "maximum strength"
            usage_text = "maximum material"
        
        if strength_importance > material_usage:
            reason = f"prioritizing strength over material usage (strength importance: {strength_importance}, material usage importance: {material_usage})"
        elif material_usage > strength_importance:
            reason = f"prioritizing material savings over strength (material usage importance: {material_usage}, strength importance: {strength_importance})"
        else:
            reason = "balancing strength and material usage equally"
        
        return (
            f"Infill density of {value}% provides {density_text} internal fill, resulting in {strength_text} "
            f"while using {usage_text}. This value was selected {reason}."
        )
    
    def _explain_wall_count(self, value: int, requirements: Dict[str, Any]) -> str:
        """Generate explanation for wall count setting."""
        strength_importance = requirements.get('strength_importance', 3)
        material_usage = requirements.get('material_usage_importance', 3)
        
        if value <= 1:
            count_text = "minimum"
            strength_text = "minimal strength"
            usage_text = "minimal material"
        elif value == 2:
            count_text = "low"
            strength_text = "moderate strength"
            usage_text = "reduced material"
        elif value == 3:
            count_text = "standard"
            strength_text = "good strength"
            usage_text = "moderate material"
        elif value == 4:
            count_text = "high"
            strength_text = "high strength"
            usage_text = "increased material"
        else:
            count_text = "very high"
            strength_text = "maximum strength"
            usage_text = "maximum material"
        
        if strength_importance > material_usage:
            reason = f"prioritizing strength over material usage (strength importance: {strength_importance}, material usage importance: {material_usage})"
        elif material_usage > strength_importance:
            reason = f"prioritizing material savings over strength (material usage importance: {material_usage}, strength importance: {strength_importance})"
        else:
            reason = "balancing strength and material usage equally"
        
        return (
            f"{value} perimeter walls provides {count_text} shell thickness, resulting in {strength_text} "
            f"while using {usage_text} for the outer shell. This value was selected {reason}."
        )
    
    def _explain_retraction_distance(self, value: float, printer_info: Dict[str, Any], material_info: Dict[str, Any]) -> str:
        """Generate explanation for retraction distance setting."""
        is_direct_drive = printer_info.get('direct_drive', True)
        material_type = material_info.get('type', 'PLA')
        
        extruder_type = "direct drive" if is_direct_drive else "Bowden"
        
        if is_direct_drive:
            if value <= 0.5:
                distance_text = "very short"
                effect_text = "minimal filament pulling, which may not prevent all stringing"
            elif value <= 1.0:
                distance_text = "short"
                effect_text = "moderate filament pulling, balancing retraction and extrusion reliability"
            elif value <= 1.5:
                distance_text = "medium"
                effect_text = "significant filament pulling, good for reducing stringing"
            else:
                distance_text = "long"
                effect_text = "maximum filament pulling, which may cause extrusion issues"
        else:  # Bowden
            if value <= 3.0:
                distance_text = "very short"
                effect_text = "minimal filament pulling, which may not prevent all stringing"
            elif value <= 5.0:
                distance_text = "short"
                effect_text = "moderate filament pulling, may not be enough for Bowden setups"
            elif value <= 7.0:
                distance_text = "medium"
                effect_text = "significant filament pulling, good for reducing stringing"
            else:
                distance_text = "long"
                effect_text = "maximum filament pulling, which may cause extrusion issues"
        
        material_factor = ""
        if material_type == "PETG":
            material_factor = "PETG typically requires slightly higher retraction distances to prevent stringing."
        elif material_type == "TPU":
            material_factor = "TPU is flexible and often works better with reduced or disabled retraction."
        
        return (
            f"Retraction distance of {value}mm is {distance_text} for a {extruder_type} extruder, "
            f"providing {effect_text}. {material_factor}"
        )
