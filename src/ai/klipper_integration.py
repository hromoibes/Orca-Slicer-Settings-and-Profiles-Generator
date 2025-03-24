"""
Orca Slicer Settings Generator - Klipper Integration
Module for Klipper-specific settings and optimizations
"""

import os
import json
from typing import Dict, List, Any, Optional, Tuple, Union

class KlipperIntegration:
    """
    Provides Klipper-specific settings and optimizations for the Orca Slicer Settings Generator.
    
    This class handles Klipper firmware specific features like pressure advance,
    input shaping, and resonance compensation to optimize print settings.
    """
    
    def __init__(self, config_file: str = None):
        """
        Initialize the Klipper integration module.
        
        Args:
            config_file: Path to JSON file containing Klipper configuration
        """
        self.config_file = config_file
        self.klipper_config = {}
        self.load_config()
    
    def load_config(self):
        """Load Klipper configuration from file."""
        if not self.config_file or not os.path.exists(self.config_file):
            # Initialize with default configuration if file doesn't exist
            self._initialize_default_config()
            return
        
        try:
            with open(self.config_file, 'r') as f:
                self.klipper_config = json.load(f)
        except Exception as e:
            print(f"Error loading Klipper configuration: {e}")
            self._initialize_default_config()
    
    def save_config(self, output_file: str = None):
        """Save Klipper configuration to file."""
        file_path = output_file or self.config_file
        if not file_path:
            return False
        
        try:
            with open(file_path, 'w') as f:
                json.dump(self.klipper_config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving Klipper configuration: {e}")
            return False
    
    def _initialize_default_config(self):
        """Initialize with default Klipper configuration."""
        self.klipper_config = {
            "printer_models": {
                "ender3": {
                    "display_name": "Creality Ender 3",
                    "pressure_advance": 0.05,
                    "pressure_advance_smooth_time": 0.04,
                    "input_shaper": {
                        "x_frequency": 37.8,
                        "y_frequency": 39.2,
                        "shaper_type_x": "mzv",
                        "shaper_type_y": "mzv",
                        "damping_ratio_x": 0.1,
                        "damping_ratio_y": 0.1
                    },
                    "max_accel": 3000,
                    "max_accel_to_decel": 1500,
                    "square_corner_velocity": 5.0
                },
                "ender3_v2": {
                    "display_name": "Creality Ender 3 V2",
                    "pressure_advance": 0.06,
                    "pressure_advance_smooth_time": 0.04,
                    "input_shaper": {
                        "x_frequency": 39.5,
                        "y_frequency": 41.2,
                        "shaper_type_x": "mzv",
                        "shaper_type_y": "mzv",
                        "damping_ratio_x": 0.1,
                        "damping_ratio_y": 0.1
                    },
                    "max_accel": 3500,
                    "max_accel_to_decel": 1750,
                    "square_corner_velocity": 5.0
                },
                "ender5": {
                    "display_name": "Creality Ender 5",
                    "pressure_advance": 0.05,
                    "pressure_advance_smooth_time": 0.04,
                    "input_shaper": {
                        "x_frequency": 42.5,
                        "y_frequency": 38.7,
                        "shaper_type_x": "mzv",
                        "shaper_type_y": "mzv",
                        "damping_ratio_x": 0.1,
                        "damping_ratio_y": 0.1
                    },
                    "max_accel": 4000,
                    "max_accel_to_decel": 2000,
                    "square_corner_velocity": 5.0
                },
                "prusa_i3_mk3s": {
                    "display_name": "Prusa i3 MK3S",
                    "pressure_advance": 0.045,
                    "pressure_advance_smooth_time": 0.04,
                    "input_shaper": {
                        "x_frequency": 49.8,
                        "y_frequency": 41.5,
                        "shaper_type_x": "mzv",
                        "shaper_type_y": "mzv",
                        "damping_ratio_x": 0.1,
                        "damping_ratio_y": 0.1
                    },
                    "max_accel": 4500,
                    "max_accel_to_decel": 2250,
                    "square_corner_velocity": 5.0
                },
                "voron_2.4": {
                    "display_name": "Voron 2.4",
                    "pressure_advance": 0.035,
                    "pressure_advance_smooth_time": 0.03,
                    "input_shaper": {
                        "x_frequency": 58.2,
                        "y_frequency": 55.4,
                        "shaper_type_x": "mzv",
                        "shaper_type_y": "mzv",
                        "damping_ratio_x": 0.1,
                        "damping_ratio_y": 0.1
                    },
                    "max_accel": 10000,
                    "max_accel_to_decel": 5000,
                    "square_corner_velocity": 8.0
                },
                "sonic_pad_default": {
                    "display_name": "Sonic Pad Default",
                    "pressure_advance": 0.05,
                    "pressure_advance_smooth_time": 0.04,
                    "input_shaper": {
                        "x_frequency": 40.0,
                        "y_frequency": 40.0,
                        "shaper_type_x": "mzv",
                        "shaper_type_y": "mzv",
                        "damping_ratio_x": 0.1,
                        "damping_ratio_y": 0.1
                    },
                    "max_accel": 4000,
                    "max_accel_to_decel": 2000,
                    "square_corner_velocity": 5.0
                }
            },
            "material_pressure_advance": {
                "PLA": {
                    "direct_drive": 0.03,
                    "bowden": 0.05
                },
                "PETG": {
                    "direct_drive": 0.06,
                    "bowden": 0.08
                },
                "ABS": {
                    "direct_drive": 0.04,
                    "bowden": 0.06
                },
                "TPU": {
                    "direct_drive": 0.25,
                    "bowden": 0.35
                },
                "NYLON": {
                    "direct_drive": 0.06,
                    "bowden": 0.08
                }
            },
            "klipper_start_gcode": {
                "default": [
                    "G28 ; home all axes",
                    "G1 Z5 F5000 ; lift nozzle",
                    "M104 S{material_print_temperature} ; set extruder temp",
                    "M140 S{material_bed_temperature} ; set bed temp",
                    "M190 S{material_bed_temperature} ; wait for bed temp",
                    "M109 S{material_print_temperature} ; wait for extruder temp",
                    "G92 E0 ; reset extruder",
                    "G1 Z0.3 F240",
                    "G1 X10 Y10 F3000",
                    "G1 X100 Y10 E15 F1500 ; prime line",
                    "G1 X100 Y10.4 F5000",
                    "G1 X10 Y10.4 E30 F1500 ; prime line",
                    "G92 E0 ; reset extruder"
                ],
                "with_pressure_advance": [
                    "G28 ; home all axes",
                    "G1 Z5 F5000 ; lift nozzle",
                    "M104 S{material_print_temperature} ; set extruder temp",
                    "M140 S{material_bed_temperature} ; set bed temp",
                    "M190 S{material_bed_temperature} ; wait for bed temp",
                    "M109 S{material_print_temperature} ; wait for extruder temp",
                    "SET_PRESSURE_ADVANCE ADVANCE={pressure_advance} SMOOTH_TIME={pressure_advance_smooth_time}",
                    "G92 E0 ; reset extruder",
                    "G1 Z0.3 F240",
                    "G1 X10 Y10 F3000",
                    "G1 X100 Y10 E15 F1500 ; prime line",
                    "G1 X100 Y10.4 F5000",
                    "G1 X10 Y10.4 E30 F1500 ; prime line",
                    "G92 E0 ; reset extruder"
                ],
                "with_input_shaper": [
                    "G28 ; home all axes",
                    "G1 Z5 F5000 ; lift nozzle",
                    "M104 S{material_print_temperature} ; set extruder temp",
                    "M140 S{material_bed_temperature} ; set bed temp",
                    "M190 S{material_bed_temperature} ; wait for bed temp",
                    "M109 S{material_print_temperature} ; wait for extruder temp",
                    "SET_PRESSURE_ADVANCE ADVANCE={pressure_advance} SMOOTH_TIME={pressure_advance_smooth_time}",
                    "SET_INPUT_SHAPER SHAPER_FREQ_X={shaper_freq_x} SHAPER_FREQ_Y={shaper_freq_y} SHAPER_TYPE_X={shaper_type_x} SHAPER_TYPE_Y={shaper_type_y}",
                    "G92 E0 ; reset extruder",
                    "G1 Z0.3 F240",
                    "G1 X10 Y10 F3000",
                    "G1 X100 Y10 E15 F1500 ; prime line",
                    "G1 X100 Y10.4 F5000",
                    "G1 X10 Y10.4 E30 F1500 ; prime line",
                    "G92 E0 ; reset extruder"
                ]
            },
            "klipper_end_gcode": {
                "default": [
                    "G91 ; relative positioning",
                    "G1 E-2 F2700 ; retract a bit",
                    "G1 E-2 Z0.2 F2400 ; retract and raise Z",
                    "G1 X5 Y5 F3000 ; wipe out",
                    "G1 Z10 ; raise Z more",
                    "G90 ; absolute positioning",
                    "G1 X0 Y220 ; present print",
                    "M106 S0 ; turn off fan",
                    "M104 S0 ; turn off extruder",
                    "M140 S0 ; turn off bed",
                    "M84 X Y E ; disable motors"
                ]
            },
            "klipper_settings": {
                "additional_slicer_settings": [
                    {
                        "name": "pressure_advance",
                        "display_name": "Pressure Advance",
                        "description": "Klipper pressure advance value to compensate for pressure in the extruder",
                        "category": "material",
                        "subcategory": "klipper",
                        "data_type": "float",
                        "default_value": 0.05,
                        "min_value": 0.0,
                        "max_value": 1.0,
                        "impact_level": 4
                    },
                    {
                        "name": "pressure_advance_smooth_time",
                        "display_name": "PA Smooth Time",
                        "description": "Pressure advance smooth time to reduce vibrations",
                        "category": "material",
                        "subcategory": "klipper",
                        "data_type": "float",
                        "default_value": 0.04,
                        "min_value": 0.0,
                        "max_value": 0.2,
                        "impact_level": 3
                    },
                    {
                        "name": "input_shaper_x_freq",
                        "display_name": "Input Shaper X Frequency",
                        "description": "Resonance frequency for X axis input shaping",
                        "category": "speed",
                        "subcategory": "klipper",
                        "data_type": "float",
                        "default_value": 40.0,
                        "min_value": 5.0,
                        "max_value": 100.0,
                        "impact_level": 4
                    },
                    {
                        "name": "input_shaper_y_freq",
                        "display_name": "Input Shaper Y Frequency",
                        "description": "Resonance frequency for Y axis input shaping",
                        "category": "speed",
                        "subcategory": "klipper",
                        "data_type": "float",
                        "default_value": 40.0,
                        "min_value": 5.0,
                        "max_value": 100.0,
                        "impact_level": 4
                    },
                    {
                        "name": "input_shaper_type_x",
                        "display_name": "Input Shaper X Type",
                        "description": "Type of input shaper to use for X axis",
                        "category": "speed",
                        "subcategory": "klipper",
                        "data_type": "enum",
                        "default_value": "mzv",
                        "options": ["zv", "mzv", "zvd", "ei", "2hump_ei", "3hump_ei"],
                        "impact_level": 3
                    },
                    {
                        "name": "input_shaper_type_y",
                        "display_name": "Input Shaper Y Type",
                        "description": "Type of input shaper to use for Y axis",
                        "category": "speed",
                        "subcategory": "klipper",
                        "data_type": "enum",
                        "default_value": "mzv",
                        "options": ["zv", "mzv", "zvd", "ei", "2hump_ei", "3hump_ei"],
                        "impact_level": 3
                    },
                    {
                        "name": "max_accel",
                        "display_name": "Maximum Acceleration",
                        "description": "Maximum acceleration for print moves",
                        "category": "speed",
                        "subcategory": "klipper",
                        "data_type": "int",
                        "default_value": 4000,
                        "min_value": 500,
                        "max_value": 20000,
                        "impact_level": 4
                    },
                    {
                        "name": "max_accel_to_decel",
                        "display_name": "Max Accel to Decel",
                        "description": "Maximum acceleration to deceleration",
                        "category": "speed",
                        "subcategory": "klipper",
                        "data_type": "int",
                        "default_value": 2000,
                        "min_value": 500,
                        "max_value": 10000,
                        "impact_level": 3
                    },
                    {
                        "name": "square_corner_velocity",
                        "display_name": "Square Corner Velocity",
                        "description": "Maximum velocity change at corners",
                        "category": "speed",
                        "subcategory": "klipper",
                        "data_type": "float",
                        "default_value": 5.0,
                        "min_value": 1.0,
                        "max_value": 15.0,
                        "impact_level": 3
                    },
                    {
                        "name": "use_firmware_retraction",
                        "display_name": "Use Firmware Retraction",
                        "description": "Use Klipper firmware retraction instead of slicer retraction",
                        "category": "travel",
                        "subcategory": "klipper",
                        "data_type": "bool",
                        "default_value": False,
                        "impact_level": 3
                    }
                ]
            }
        }
    
    def get_printer_config(self, printer_model: str) -> Dict[str, Any]:
        """
        Get Klipper configuration for a specific printer model.
        
        Args:
            printer_model: Name of the printer model
            
        Returns:
            Dictionary with printer configuration or default if not found
        """
        printer_models = self.klipper_config.get('printer_models', {})
        
        # Try to find exact match
        if printer_model in printer_models:
            return printer_models[printer_model]
        
        # Try to find partial match
        for model, config in printer_models.items():
            if printer_model.lower() in model.lower() or model.lower() in printer_model.lower():
                return config
        
        # Return Sonic Pad default if available, otherwise first printer in list
        if 'sonic_pad_default' in printer_models:
            return printer_models['sonic_pad_default']
        elif printer_models:
            return next(iter(printer_models.values()))
        
        # Return empty dict if no printers defined
        return {}
    
    def get_material_pressure_advance(self, material_type: str, is_direct_drive: bool) -> float:
        """
        Get recommended pressure advance value for a material.
        
        Args:
            material_type: Type of material (PLA, PETG, etc.)
            is_direct_drive: Whether the printer has a direct drive extruder
            
        Returns:
            Recommended pressure advance value
        """
        material_pa = self.klipper_config.get('material_pressure_advance', {})
        
        # Default values if not found
        default_value = 0.03 if is_direct_drive else 0.05
        
        if material_type not in material_pa:
            return default_value
        
        extruder_type = 'direct_drive' if is_direct_drive else 'bowden'
        return material_pa[material_type].get(extruder_type, default_value)
    
    def get_start_gcode(self, use_pressure_advance: bool = True, use_input_shaper: bool = True) -> List[str]:
        """
        Get appropriate start G-code for Klipper.
        
        Args:
            use_pressure_advance: Whether to include pressure advance commands
            use_input_shaper: Whether to include input shaper commands
            
        Returns:
            List of G-code lines
        """
        klipper_start_gcode = self.klipper_config.get('klipper_start_gcode', {})
        
        if use_pressure_advance and use_input_shaper and 'with_input_shaper' in klipper_start_gcode:
            return klipper_start_gcode['with_input_shaper']
        elif use_pressure_advance and 'with_pressure_advance' in klipper_start_gcode:
            return klipper_start_gcode['with_pressure_advance']
        else:
            return klipper_start_gcode.get('default', [])
    
    def get_end_gcode(self) -> List[str]:
        """
        Get end G-code for Klipper.
        
        Returns:
            List of G-code lines
        """
        klipper_end_gcode = self.klipper_config.get('klipper_end_gcode', {})
        return klipper_end_gcode.get('default', [])
    
    def get_additional_settings(self) -> List[Dict[str, Any]]:
        """
        Get additional slicer settings for Klipper.
        
        Returns:
            List of setting dictionaries
        """
        klipper_settings = self.klipper_config.get('klipper_settings', {})
        return klipper_settings.get('additional_slicer_settings', [])
    
    def apply_klipper_optimizations(
        self,
        settings: Dict[str, Any],
        printer_info: Dict[str, Any],
        material_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply Klipper-specific optimizations to settings.
        
        Args:
            settings: Current settings dictionary
            printer_info: Printer information
            material_info: Material information
            
        Returns:
            Updated settings dictionary
        """
        # Get printer model configuration
        printer_model = printer_info.get('model', '').lower()
        printer_config = self.get_printer_config(printer_model)
        
        # Apply pressure advance
        is_direct_drive = printer_info.get('direct_drive', True)
        material_type = material_info.get('type', 'PLA')
        
        # Get pressure advance from printer config or material defaults
        if 'pressure_advance' in printer_config:
            settings['pressure_advance'] = printer_config['pressure_advance']
        else:
            settings['pressure_advance'] = self.get_material_pressure_advance(material_type, is_direct_drive)
        
        # Apply pressure advance smooth time
        settings['pressure_advance_smooth_time'] = printer_config.get('pressure_advance_smooth_time', 0.04)
        
        # Apply input shaper settings if available
        if 'input_shaper' in printer_config:
            input_shaper = printer_config['input_shaper']
            settings['input_shaper_x_freq'] = input_shaper.get('x_frequency', 40.0)
            settings['input_shaper_y_freq'] = input_shaper.get('y_frequency', 40.0)
            settings['input_shaper_type_x'] = input_shaper.get('shaper_type_x', 'mzv')
            settings['input_shaper_type_y'] = input_shaper.get('shaper_type_y', 'mzv')
        
        # Apply acceleration settings
        settings['max_accel'] = printer_config.get('max_accel', 4000)
        settings['max_accel_to_decel'] = printer_config.get('max_accel_to_decel', 2000)
        settings['square_corner_velocity'] = printer_config.get('square_corner_velocity', 5.0)
        
        # Optimize speeds based on input shaper
        if 'input_shaper_x_freq' in settings and 'input_shaper_y_freq' in settings:
            # Calculate maximum acceleration based on input shaper
            # This is a simplified calculation - in reality it depends on the shaper type
            min_freq = min(settings['input_shaper_x_freq'], settings['input_shaper_y_freq'])
            
            # Adjust maximum acceleration based on resonance frequency
            # Higher frequencies allow higher accelerations
            if min_freq > 50:
                settings['max_accel'] = min(settings['max_accel'], 10000)
            elif min_freq > 40:
                settings['max_accel'] = min(settings['max_accel'], 6000)
            elif min_freq > 30:
                settings['max_accel'] = min(settings['max_accel'], 4000)
            else:
                settings['max_accel'] = min(settings['max_accel'], 2000)
            
            # Set max_accel_to_decel to half of max_accel
            settings['max_accel_to_decel'] = settings['max_accel'] // 2
        
        # Adjust print speeds based on acceleration
        max_accel = settings.get('max_accel', 4000)
        if 'print_speed' in settings:
            # Higher acceleration allows higher speeds
            if max_accel >= 8000:
                settings['print_speed'] = max(settings['print_speed'], 80)
                settings['travel_speed'] = max(settings.get('travel_speed', 150), 200)
            elif max_accel >= 5000:
                settings['print_speed'] = max(settings['print_speed'], 60)
                settings['travel_speed'] = max(settings.get('travel_speed', 150), 180)
        
        # Set firmware retraction if enabled
        settings['use_firmware_retraction'] = False  # Default to off, can be enabled by user
        
        # Adjust start and end G-code
        settings['start_gcode'] = '\n'.join(self.get_start_gcode(
            use_pressure_advance=True,
            use_input_shaper=True
        ))
        settings['end_gcode'] = '\n'.join(self.get_end_gcode())
        
        return settings
    
    def generate_klipper_config(
        self,
        printer_info: Dict[str, Any],
        settings: Dict[str, Any]
    ) -> str:
        """
        Generate Klipper configuration snippet based on settings.
        
        Args:
            printer_info: Printer information
            settings: Current settings dictionary
            
        Returns:
            Klipper configuration snippet as string
        """
        config_lines = [
            "# Klipper settings generated by Orca Slicer Settings Generator",
            ""
        ]
        
        # Add pressure advance settings
        if 'pressure_advance' in settings:
            config_lines.extend([
                "[extruder]",
                f"pressure_advance: {settings.get('pressure_advance', 0.05)}",
                f"pressure_advance_smooth_time: {settings.get('pressure_advance_smooth_time', 0.04)}",
                ""
            ])
        
        # Add input shaper settings
        if 'input_shaper_x_freq' in settings and 'input_shaper_y_freq' in settings:
            config_lines.extend([
                "[input_shaper]",
                f"shaper_freq_x: {settings.get('input_shaper_x_freq', 40.0)}",
                f"shaper_freq_y: {settings.get('input_shaper_y_freq', 40.0)}",
                f"shaper_type_x: {settings.get('input_shaper_type_x', 'mzv')}",
                f"shaper_type_y: {settings.get('input_shaper_type_y', 'mzv')}",
                ""
            ])
        
        # Add max acceleration settings
        if 'max_accel' in settings:
            config_lines.extend([
                "[printer]",
                f"max_accel: {settings.get('max_accel', 4000)}",
                f"max_accel_to_decel: {settings.get('max_accel_to_decel', 2000)}",
                f"square_corner_velocity: {settings.get('square_corner_velocity', 5.0)}",
                ""
            ])
        
        return '\n'.join(config_lines)
    
    def explain_klipper_settings(self, settings: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate explanations for Klipper-specific settings.
        
        Args:
            settings: Settings dictionary
            
        Returns:
            Dictionary of setting explanations
        """
        explanations = {}
        
        # Pressure advance explanation
        if 'pressure_advance' in settings:
            pa_value = settings['pressure_advance']
            if pa_value < 0.03:
                pa_desc = "very low"
                effect = "minimal pressure compensation, may not fully prevent oozing"
            elif pa_value < 0.06:
                pa_desc = "low to moderate"
                effect = "good pressure compensation for most PLA filaments"
            elif pa_value < 0.1:
                pa_desc = "moderate to high"
                effect = "strong pressure compensation for PETG and similar filaments"
            else:
                pa_desc = "high"
                effect = "very strong pressure compensation for flexible filaments"
            
            explanations['pressure_advance'] = (
                f"Pressure Advance value of {pa_value} provides {pa_desc} compensation for pressure "
                f"in the extruder, resulting in {effect}. This helps reduce corner bulging and improves "
                f"dimensional accuracy."
            )
        
        # Input shaper explanation
        if 'input_shaper_x_freq' in settings and 'input_shaper_y_freq' in settings:
            x_freq = settings['input_shaper_x_freq']
            y_freq = settings['input_shaper_y_freq']
            x_type = settings.get('input_shaper_type_x', 'mzv')
            y_type = settings.get('input_shaper_type_y', 'mzv')
            
            shaper_types = {
                'zv': "Zero Vibration (basic, minimal smoothing)",
                'mzv': "Modified Zero Vibration (good balance of smoothing and responsiveness)",
                'zvd': "Zero Vibration Derivative (more smoothing than ZV)",
                'ei': "Exponential Input (significant smoothing)",
                '2hump_ei': "2-Hump Exponential Input (very strong smoothing)",
                '3hump_ei': "3-Hump Exponential Input (maximum smoothing)"
            }
            
            x_type_desc = shaper_types.get(x_type, x_type)
            y_type_desc = shaper_types.get(y_type, y_type)
            
            if min(x_freq, y_freq) > 50:
                freq_desc = "high"
                speed_effect = "allows for high print speeds and accelerations"
            elif min(x_freq, y_freq) > 40:
                freq_desc = "above average"
                speed_effect = "allows for good print speeds and accelerations"
            elif min(x_freq, y_freq) > 30:
                freq_desc = "average"
                speed_effect = "allows for moderate print speeds and accelerations"
            else:
                freq_desc = "low"
                speed_effect = "requires lower print speeds and accelerations to prevent ringing"
            
            explanations['input_shaper'] = (
                f"Input Shaper is configured with {freq_desc} resonance frequencies "
                f"(X: {x_freq}Hz, Y: {y_freq}Hz) and uses {x_type} for X-axis and {y_type} for Y-axis. "
                f"X-axis shaper ({x_type_desc}) and Y-axis shaper ({y_type_desc}) work together to "
                f"reduce ringing artifacts in prints. This configuration {speed_effect}."
            )
        
        # Max acceleration explanation
        if 'max_accel' in settings:
            accel = settings['max_accel']
            if accel >= 10000:
                accel_desc = "very high"
                effect = "extremely fast printing but may reduce quality on some printers"
            elif accel >= 6000:
                accel_desc = "high"
                effect = "fast printing with good quality on well-tuned printers"
            elif accel >= 3000:
                accel_desc = "moderate"
                effect = "good balance of speed and quality for most printers"
            else:
                accel_desc = "conservative"
                effect = "prioritizes print quality over speed"
            
            explanations['max_accel'] = (
                f"Maximum acceleration of {accel} mm/s² is {accel_desc}, which {effect}. "
                f"This works with Input Shaper to determine the maximum speed changes during printing."
            )
        
        return explanations
