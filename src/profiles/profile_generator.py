"""
Orca Slicer Settings Generator - Profile Generator
Module for generating optimized printer and filament profiles
"""

import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union

from ..ai import AIManager
from .profile_database import ProfileDatabase

class ProfileGenerator:
    """
    Generator for creating optimized printer and filament profiles.
    
    This class uses the AI component to generate optimized profiles based on
    printer specifications, material properties, and user requirements.
    """
    
    def __init__(self, data_dir: str = None):
        """
        Initialize the profile generator.
        
        Args:
            data_dir: Directory for storing profile data
        """
        self.data_dir = data_dir or os.path.join(os.path.dirname(__file__), '..', 'data')
        
        # Initialize AI manager and profile database
        self.ai_manager = AIManager(data_dir=self.data_dir)
        self.profile_db = ProfileDatabase(data_dir=self.data_dir)
        
        # Ensure template directories exist
        self.template_dir = os.path.join(self.data_dir, 'templates')
        os.makedirs(self.template_dir, exist_ok=True)
        
        # Load default templates
        self._initialize_templates()
    
    def _initialize_templates(self):
        """Initialize default profile templates if they don't exist."""
        # Check if template directory is empty
        if not os.listdir(self.template_dir):
            self._create_default_templates()
    
    def _create_default_templates(self):
        """Create default profile templates."""
        # Create printer templates
        printer_templates = {
            "ender3": {
                "name": "Creality Ender 3",
                "vendor": "Creality",
                "model": "Ender 3",
                "bed_size": [220, 220],
                "max_print_height": 250,
                "nozzle_diameter": 0.4,
                "direct_drive": False,
                "printer_type": "cartesian",
                "use_klipper": False
            },
            "ender3_klipper": {
                "name": "Creality Ender 3 (Klipper)",
                "vendor": "Creality",
                "model": "Ender 3",
                "bed_size": [220, 220],
                "max_print_height": 250,
                "nozzle_diameter": 0.4,
                "direct_drive": False,
                "printer_type": "cartesian",
                "use_klipper": True
            },
            "sonic_pad": {
                "name": "SonicPad Printer",
                "vendor": "Creality",
                "model": "SonicPad",
                "bed_size": [220, 220],
                "max_print_height": 250,
                "nozzle_diameter": 0.4,
                "direct_drive": False,
                "printer_type": "cartesian",
                "use_klipper": True
            }
        }
        
        # Create material templates
        material_templates = {
            "pla": {
                "name": "Generic PLA",
                "vendor": "Generic",
                "type": "PLA",
                "color": "#FFFFFF",
                "diameter": 1.75,
                "temp_range_min": 190,
                "temp_range_max": 220,
                "bed_temp_range_min": 50,
                "bed_temp_range_max": 60
            },
            "petg": {
                "name": "Generic PETG",
                "vendor": "Generic",
                "type": "PETG",
                "color": "#00FFFF",
                "diameter": 1.75,
                "temp_range_min": 230,
                "temp_range_max": 250,
                "bed_temp_range_min": 70,
                "bed_temp_range_max": 85
            }
        }
        
        # Save templates
        os.makedirs(os.path.join(self.template_dir, 'printers'), exist_ok=True)
        os.makedirs(os.path.join(self.template_dir, 'materials'), exist_ok=True)
        
        for template_id, template in printer_templates.items():
            with open(os.path.join(self.template_dir, 'printers', f"{template_id}.json"), 'w') as f:
                json.dump(template, f, indent=2)
        
        for template_id, template in material_templates.items():
            with open(os.path.join(self.template_dir, 'materials', f"{template_id}.json"), 'w') as f:
                json.dump(template, f, indent=2)
    
    # Printer profile methods
    
    def create_printer_profile(self, **kwargs) -> str:
        """
        Create a new printer profile.
        
        Args:
            name: Printer name
            vendor: Printer vendor
            model: Printer model
            bed_size: Bed size [width, depth] in mm
            max_height: Maximum print height in mm
            nozzle_diameter: Nozzle diameter in mm
            is_direct_drive: Whether the printer has a direct drive extruder
            printer_type: Printer type (cartesian, delta, corexy, etc.)
            use_klipper: Whether the printer uses Klipper firmware
            
        Returns:
            ID of the new printer profile
        """
        # Create printer data
        printer_data = {
            "name": kwargs.get('name', 'New Printer'),
            "vendor": kwargs.get('vendor', 'Unknown'),
            "model": kwargs.get('model', 'Unknown'),
            "bed_size": kwargs.get('bed_size', [220, 220]),
            "max_print_height": kwargs.get('max_height', 250),
            "nozzle_diameter": kwargs.get('nozzle_diameter', 0.4),
            "direct_drive": kwargs.get('is_direct_drive', False),
            "printer_type": kwargs.get('printer_type', 'cartesian'),
            "use_klipper": kwargs.get('use_klipper', False)
        }
        
        # Add to database
        printer_id = self.profile_db.add_printer(printer_data)
        
        return printer_id
    
    def get_printer_templates(self) -> list:
        """
        Get all available printer templates.
        
        Returns:
            List of printer templates
        """
        templates = []
        template_dir = os.path.join(self.template_dir, 'printers')
        
        if os.path.exists(template_dir):
            for filename in os.listdir(template_dir):
                if filename.endswith('.json'):
                    template_id = filename[:-5]  # Remove .json extension
                    template_path = os.path.join(template_dir, filename)
                    
                    try:
                        with open(template_path, 'r') as f:
                            template = json.load(f)
                            template['id'] = template_id
                            templates.append(template)
                    except Exception as e:
                        print(f"Error loading printer template {template_id}: {e}")
        
        return templates
    
    # Material profile methods
    
    def create_material_profile(self, **kwargs) -> str:
        """
        Create a new material profile.
        
        Args:
            name: Material name
            vendor: Material vendor
            material_type: Material type (PLA, PETG, ABS, etc.)
            color: Material color (hex code)
            diameter: Filament diameter in mm
            temp_range: Temperature range [min, max] in °C
            bed_temp_range: Bed temperature range [min, max] in °C
            
        Returns:
            ID of the new material profile
        """
        # Create material data
        material_data = {
            "name": kwargs.get('name', 'New Material'),
            "vendor": kwargs.get('vendor', 'Unknown'),
            "type": kwargs.get('material_type', 'PLA'),
            "color": kwargs.get('color', '#FFFFFF'),
            "diameter": kwargs.get('diameter', 1.75)
        }
        
        # Handle temperature ranges
        temp_range = kwargs.get('temp_range', [190, 220])
        bed_temp_range = kwargs.get('bed_temp_range', [50, 60])
        
        if isinstance(temp_range, list) and len(temp_range) == 2:
            material_data["temp_range_min"] = temp_range[0]
            material_data["temp_range_max"] = temp_range[1]
        else:
            material_data["temp_range_min"] = 190
            material_data["temp_range_max"] = 220
        
        if isinstance(bed_temp_range, list) and len(bed_temp_range) == 2:
            material_data["bed_temp_range_min"] = bed_temp_range[0]
            material_data["bed_temp_range_max"] = bed_temp_range[1]
        else:
            material_data["bed_temp_range_min"] = 50
            material_data["bed_temp_range_max"] = 60
        
        # Add to database
        material_id = self.profile_db.add_material(material_data)
        
        return material_id
    
    def get_material_templates(self) -> list:
        """
        Get all available material templates.
        
        Returns:
            List of material templates
        """
        templates = []
        template_dir = os.path.join(self.template_dir, 'materials')
        
        if os.path.exists(template_dir):
            for filename in os.listdir(template_dir):
                if filename.endswith('.json'):
                    template_id = filename[:-5]  # Remove .json extension
                    template_path = os.path.join(template_dir, filename)
                    
                    try:
                        with open(template_path, 'r') as f:
                            template = json.load(f)
                            template['id'] = template_id
                            templates.append(template)
                    except Exception as e:
                        print(f"Error loading material template {template_id}: {e}")
        
        return templates
    
    # Process profile methods
    
    def generate_process_profile(self, **kwargs) -> str:
        """
        Generate an optimized process profile using AI.
        
        Args:
            name: Process profile name
            printer_id: ID of the printer profile
            material_id: ID of the material profile
            nozzle_size: Nozzle size in mm
            print_requirements: Dictionary of print requirements
            
        Returns:
            ID of the new process profile
        """
        # Get printer and material profiles
        printer = self.profile_db.get_printer(kwargs.get('printer_id'))
        material = self.profile_db.get_material(kwargs.get('material_id'))
        
        if not printer or not material:
            print("Error: Printer or material not found")
            return None
        
        # Generate optimized settings using AI
        nozzle_size = kwargs.get('nozzle_size', 0.4)
        print_requirements = kwargs.get('print_requirements', {})
        
        ai_result = self.ai_manager.generate_profile(
            kwargs.get('printer_id'),
            kwargs.get('material_id'),
            nozzle_size,
            print_requirements,
            None,
            printer.get('use_klipper', False)
        )
        
        if not ai_result:
            print("Error: Failed to generate AI profile")
            return None
        
        # Create process profile
        process_data = {
            "name": kwargs.get('name', 'New Process'),
            "printer_id": kwargs.get('printer_id'),
            "material_id": kwargs.get('material_id'),
            "nozzle_diameter": nozzle_size,
            "created_by": "ai",
            "print_requirements": print_requirements
        }
        
        # Add settings from AI result
        for key, value in ai_result.get('settings', {}).items():
            process_data[key] = value
        
        # Add Klipper config if available
        if 'klipper_config' in ai_result:
            process_data['klipper_config'] = ai_result['klipper_config']
        
        # Add explanations if available
        if 'explanations' in ai_result:
            process_data['explanations'] = ai_result['explanations']
        
        # Add to database
        process_id = self.profile_db.add_process(process_data)
        
        return process_id
    
    def optimize_process_profile(self, process_id: str, print_requirements: Dict[str, Any]) -> str:
        """
        Optimize an existing process profile using AI.
        
        Args:
            process_id: ID of the process profile to optimize
            print_requirements: Dictionary of print requirements
            
        Returns:
            ID of the new optimized process profile
        """
        # Get process profile
        process = self.profile_db.get_process(process_id)
        
        if not process:
            print(f"Error: Process profile {process_id} not found")
            return None
        
        # Get printer and material profiles
        printer = self.profile_db.get_printer(process.get('printer_id'))
        material = self.profile_db.get_material(process.get('material_id'))
        
        if not printer or not material:
            print("Error: Printer or material not found")
            return None
        
        # Generate optimized settings using AI
        ai_result = self.ai_manager.generate_profile(
            process.get('printer_id'),
            process.get('material_id'),
            process.get('nozzle_diameter', 0.4),
            print_requirements,
            process,
            printer.get('use_klipper', False)
        )
        
        if not ai_result:
            print("Error: Failed to generate AI profile")
            return None
        
        # Create optimized process profile
        optimized_data = process.copy()
        optimized_data.pop('id', None)
        optimized_data['name'] = f"{process.get('name')} (Optimized)"
        optimized_data['parent_id'] = process_id
        optimized_data['print_requirements'] = print_requirements
        
        # Update settings from AI result
        for key, value in ai_result.get('settings', {}).items():
            optimized_data[key] = value
        
        # Update Klipper config if available
        if 'klipper_config' in ai_result:
            optimized_data['klipper_config'] = ai_result['klipper_config']
        
        # Update explanations if available
        if 'explanations' in ai_result:
            optimized_data['explanations'] = ai_result['explanations']
        
        # Add to database
        optimized_id = self.profile_db.add_process(optimized_data)
        
        return optimized_id
    
    def get_process_templates(self) -> list:
        """
        Get all available process templates.
        
        Returns:
            List of process templates
        """
        templates = []
        template_dir = os.path.join(self.template_dir, 'processes')
        
        if os.path.exists(template_dir):
            for filename in os.listdir(template_dir):
                if filename.endswith('.json'):
                    template_id = filename[:-5]  # Remove .json extension
                    template_path = os.path.join(template_dir, filename)
                    
                    try:
                        with open(template_path, 'r') as f:
                            template = json.load(f)
                            template['id'] = template_id
                            templates.append(template)
                    except Exception as e:
                        print(f"Error loading process template {template_id}: {e}")
        
        return templates
    
    def compare_process_profiles(self, process_id_1: str, process_id_2: str) -> Dict[str, Any]:
        """
        Compare two process profiles and explain differences.
        
        Args:
            process_id_1: ID of the first process profile
            process_id_2: ID of the second process profile
            
        Returns:
            Dictionary with comparison results
        """
        # Get process profiles
        process_1 = self.profile_db.get_process(process_id_1)
        process_2 = self.profile_db.get_process(process_id_2)
        
        if not process_1 or not process_2:
            print("Error: One or both process profiles not found")
            return {
                "error": "One or both process profiles not found",
                "process_1_found": process_1 is not None,
                "process_2_found": process_2 is not None
            }
        
        # Compare settings
        differences = []
        important_settings = [
            "layer_height", "print_speed", "infill_density", "temperature",
            "bed_temperature", "retraction_distance", "retraction_speed"
        ]
        
        # Calculate overall differences
        print_time_difference = 0
        quality_difference = 0
        strength_difference = 0
        
        for setting in important_settings:
            if setting in process_1 and setting in process_2 and process_1[setting] != process_2[setting]:
                value_1 = process_1[setting]
                value_2 = process_2[setting]
                
                # Generate explanation for difference
                explanation = self._explain_setting_difference(setting, value_1, value_2)
                impact = self._calculate_setting_impact(setting, value_1, value_2)
                
                differences.append({
                    "setting": setting,
                    "value_1": value_1,
                    "value_2": value_2,
                    "explanation": explanation,
                    "impact": impact
                })
                
                # Update overall differences
                if setting == "layer_height":
                    # Thinner layers = better quality but longer print time
                    ratio = value_2 / value_1 if value_1 > 0 else 1
                    print_time_difference += (1 - ratio) * 100
                    quality_difference += (ratio - 1) * 100
                
                elif setting == "print_speed":
                    # Faster speed = shorter print time but potentially lower quality
                    ratio = value_2 / value_1 if value_1 > 0 else 1
                    print_time_difference -= (ratio - 1) * 100
                    if ratio > 1.2:  # Only affect quality if speed increase is significant
                        quality_difference -= (ratio - 1) * 50
                
                elif setting == "infill_density":
                    # Higher infill = stronger but longer print time
                    diff = value_2 - value_1
                    strength_difference += diff * 0.5
                    print_time_difference += diff * 0.25
        
        # Create summary
        summary = f"Profile 2 is approximately {abs(print_time_difference):.1f}% "
        summary += "faster" if print_time_difference < 0 else "slower"
        summary += f" than Profile 1. "
        
        if abs(quality_difference) > 5:
            summary += f"Quality is estimated to be {abs(quality_difference):.1f}% "
            summary += "lower" if quality_difference < 0 else "higher"
            summary += ". "
        
        if abs(strength_difference) > 5:
            summary += f"Strength is approximately {abs(strength_difference):.1f}% "
            summary += "lower" if strength_difference < 0 else "higher"
            summary += "."
        
        return {
            "differences": differences,
            "summary": summary,
            "print_time_difference": print_time_difference,
            "quality_difference": quality_difference,
            "strength_difference": strength_difference
        }
    
    def _explain_setting_difference(self, setting: str, value_1: Any, value_2: Any) -> str:
        """Generate explanation for setting difference."""
        if setting == "layer_height":
            return f"Layer height changed from {value_1}mm to {value_2}mm. " + (
                "Thinner layers provide more detail but print slower." if value_2 < value_1 else
                "Thicker layers print faster but with less detail."
            )
        
        elif setting == "print_speed":
            return f"Print speed changed from {value_1}mm/s to {value_2}mm/s. " + (
                "Slower speeds can improve quality but increase print time." if value_2 < value_1 else
                "Faster speeds reduce print time but may affect quality."
            )
        
        elif setting == "infill_density":
            return f"Infill density changed from {value_1}% to {value_2}%. " + (
                "Higher density increases strength but uses more material and time." if value_2 > value_1 else
                "Lower density uses less material and prints faster."
            )
        
        elif setting == "temperature":
            return f"Print temperature changed from {value_1}°C to {value_2}°C. " + (
                "Lower temperatures can improve detail but may reduce layer adhesion." if value_2 < value_1 else
                "Higher temperatures improve layer adhesion but may cause stringing."
            )
        
        elif setting == "bed_temperature":
            return f"Bed temperature changed from {value_1}°C to {value_2}°C. " + (
                "Lower bed temperatures can reduce warping for some materials." if value_2 < value_1 else
                "Higher bed temperatures improve first layer adhesion."
            )
        
        elif setting == "retraction_distance":
            return f"Retraction distance changed from {value_1}mm to {value_2}mm. " + (
                "Shorter retraction can be faster but may not prevent stringing as effectively." if value_2 < value_1 else
                "Longer retraction can reduce stringing but may cause filament grinding."
            )
        
        elif setting == "retraction_speed":
            return f"Retraction speed changed from {value_1}mm/s to {value_2}mm/s. " + (
                "Slower retraction can be gentler on the filament." if value_2 < value_1 else
                "Faster retraction can reduce oozing but may cause filament grinding."
            )
        
        else:
            return f"{setting.replace('_', ' ').title()} changed from {value_1} to {value_2}."
    
    def _calculate_setting_impact(self, setting: str, value_1: Any, value_2: Any) -> str:
        """Calculate impact of setting change."""
        if setting == "layer_height":
            ratio = value_2 / value_1 if value_1 > 0 else 1
            time_impact = (1 - ratio) * 100
            return f"Print time {'increased' if time_impact > 0 else 'reduced'} by approximately {abs(time_impact):.1f}%, {'quality improved' if time_impact > 0 else 'quality reduced'}."
        
        elif setting == "print_speed":
            ratio = value_2 / value_1 if value_1 > 0 else 1
            time_impact = (1 - ratio) * 100
            return f"Print time {'increased' if time_impact > 0 else 'reduced'} by approximately {abs(time_impact):.1f}%, {'may improve quality' if time_impact > 0 else 'may affect quality'}."
        
        elif setting == "infill_density":
            diff = value_2 - value_1
            return f"{'Increased' if diff > 0 else 'Decreased'} strength and material usage."
        
        elif setting == "temperature":
            return f"{'Improved detail, reduced layer adhesion' if value_2 < value_1 else 'Improved layer adhesion, potential stringing'}."
        
        elif setting == "bed_temperature":
            return f"{'Reduced warping risk for some materials' if value_2 < value_1 else 'Improved first layer adhesion'}."
        
        elif setting == "retraction_distance" or setting == "retraction_speed":
            return f"{'May affect stringing and filament grinding' if value_2 != value_1 else 'No significant impact'}."
        
        else:
            return "Impact unknown."
    
    # Import/Export methods
    
    def export_profile_to_orca(self, profile_id: str, profile_type: str, output_file: str) -> bool:
        """
        Export a profile to Orca Slicer format.
        
        Args:
            profile_id: ID of the profile to export
            profile_type: Type of profile ('printer', 'material', or 'process')
            output_file: Path to output file
            
        Returns:
            Success status
        """
        # Get profile
        profile = None
        
        if profile_type == 'printer':
            profile = self.profile_db.get_printer(profile_id)
        elif profile_type == 'material':
            profile = self.profile_db.get_material(profile_id)
        elif profile_type == 'process':
            profile = self.profile_db.get_process(profile_id)
        
        if not profile:
            print(f"Error: Profile {profile_id} not found")
            return False
        
        # Convert to Orca Slicer format
        orca_profile = self._convert_to_orca_format(profile, profile_type)
        
        # Save to file
        try:
            with open(output_file, 'w') as f:
                json.dump(orca_profile, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting profile: {e}")
            return False
    
    def import_profile_from_orca(self, profile_file: str, profile_type: str) -> Optional[str]:
        """
        Import a profile from Orca Slicer format.
        
        Args:
            profile_file: Path to profile file
            profile_type: Type of profile ('printer', 'material', or 'process')
            
        Returns:
            ID of the imported profile or None if failed
        """
        # Load profile from file
        try:
            with open(profile_file, 'r') as f:
                orca_profile = json.load(f)
        except Exception as e:
            print(f"Error loading profile file: {e}")
            return None
        
        # Convert from Orca Slicer format
        profile = self._convert_from_orca_format(orca_profile, profile_type)
        
        # Add to database
        if profile_type == 'printer':
            return self.profile_db.add_printer(profile)
        elif profile_type == 'material':
            return self.profile_db.add_material(profile)
        elif profile_type == 'process':
            return self.profile_db.add_process(profile)
        
        return None
    
    def _convert_to_orca_format(self, profile: Dict[str, Any], profile_type: str) -> Dict[str, Any]:
        """Convert profile to Orca Slicer format."""
        orca_profile = {
            "name": profile.get('name', 'Unnamed Profile'),
            "version": "1.0.0",
            "type": profile_type,
            "settings": {}
        }
        
        # Copy settings based on profile type
        if profile_type == 'printer':
            orca_profile["vendor"] = profile.get('vendor', 'Unknown')
            orca_profile["model"] = profile.get('model', 'Unknown')
            orca_profile["settings"] = {
                "bed_shape": f"0x0,{profile.get('bed_size', [220, 220])[0]}x0,{profile.get('bed_size', [220, 220])[0]}x{profile.get('bed_size', [220, 220])[1]},0x{profile.get('bed_size', [220, 220])[1]}",
                "max_print_height": profile.get('max_print_height', 250),
                "nozzle_diameter": profile.get('nozzle_diameter', 0.4),
                "printer_technology": "FFF",
                "gcode_flavor": "marlin",
                "use_relative_e_distances": True,
                "use_firmware_retraction": profile.get('use_klipper', False),
                "silent_mode": False
            }
            
            # Add Klipper-specific settings
            if profile.get('use_klipper', False):
                orca_profile["settings"]["gcode_flavor"] = "klipper"
                orca_profile["settings"]["use_firmware_retraction"] = True
                orca_profile["settings"]["start_gcode"] = "SET_PRESSURE_ADVANCE ADVANCE={pressure_advance} SMOOTH_TIME={pressure_advance_smooth_time}\nG28 ; home all axes\nG1 Z5 F5000 ; lift nozzle"
        
        elif profile_type == 'material':
            orca_profile["vendor"] = profile.get('vendor', 'Unknown')
            orca_profile["material_type"] = profile.get('type', 'PLA')
            orca_profile["color"] = profile.get('color', '#FFFFFF')
            orca_profile["settings"] = {
                "filament_diameter": profile.get('diameter', 1.75),
                "filament_type": profile.get('type', 'PLA'),
                "temperature": profile.get('temp_range_max', 220) - 10,  # Default to 10°C below max
                "first_layer_temperature": profile.get('temp_range_max', 220),
                "bed_temperature": profile.get('bed_temp_range_min', 50) + 5,  # Default to 5°C above min
                "first_layer_bed_temperature": profile.get('bed_temp_range_max', 60)
            }
        
        elif profile_type == 'process':
            # Get basic settings
            for key, value in profile.items():
                if key not in ['id', 'created', 'modified', 'printer_id', 'material_id', 'explanations', 'klipper_config']:
                    orca_profile["settings"][key] = value
            
            # Add Klipper config as comments
            if 'klipper_config' in profile:
                orca_profile["klipper_config"] = profile['klipper_config']
                
                # Add Klipper config to start_gcode if not present
                if 'start_gcode' not in orca_profile["settings"]:
                    klipper_start = "SET_PRESSURE_ADVANCE ADVANCE={} SMOOTH_TIME={}\n".format(
                        profile['klipper_config'].get('pressure_advance', 0.05),
                        profile['klipper_config'].get('pressure_advance_smooth_time', 0.04)
                    )
                    orca_profile["settings"]["start_gcode"] = klipper_start + "G28 ; home all axes\nG1 Z5 F5000 ; lift nozzle"
        
        return orca_profile
    
    def _convert_from_orca_format(self, orca_profile: Dict[str, Any], profile_type: str) -> Dict[str, Any]:
        """Convert profile from Orca Slicer format."""
        profile = {
            "name": orca_profile.get('name', 'Imported Profile'),
            "imported": True,
            "import_date": datetime.now().isoformat()
        }
        
        # Copy settings based on profile type
        if profile_type == 'printer':
            profile["vendor"] = orca_profile.get('vendor', 'Unknown')
            profile["model"] = orca_profile.get('model', 'Unknown')
            
            # Parse bed shape
            bed_shape = orca_profile.get('settings', {}).get('bed_shape', '0x0,220x0,220x220,0x220')
            try:
                points = bed_shape.split(',')
                max_x = max(int(p.split('x')[0]) for p in points)
                max_y = max(int(p.split('x')[1]) for p in points)
                profile["bed_size"] = [max_x, max_y]
            except:
                profile["bed_size"] = [220, 220]
            
            profile["max_print_height"] = orca_profile.get('settings', {}).get('max_print_height', 250)
            profile["nozzle_diameter"] = orca_profile.get('settings', {}).get('nozzle_diameter', 0.4)
            profile["direct_drive"] = False  # Default, can't determine from Orca profile
            profile["printer_type"] = "cartesian"  # Default, can't determine from Orca profile
            
            # Detect Klipper
            gcode_flavor = orca_profile.get('settings', {}).get('gcode_flavor', 'marlin')
            use_firmware_retraction = orca_profile.get('settings', {}).get('use_firmware_retraction', False)
            start_gcode = orca_profile.get('settings', {}).get('start_gcode', '')
            
            profile["use_klipper"] = (gcode_flavor == 'klipper' or 
                                     'SET_PRESSURE_ADVANCE' in start_gcode or 
                                     'PRESSURE_ADVANCE' in start_gcode)
        
        elif profile_type == 'material':
            profile["vendor"] = orca_profile.get('vendor', 'Unknown')
            profile["type"] = orca_profile.get('material_type', 'PLA')
            profile["color"] = orca_profile.get('color', '#FFFFFF')
            profile["diameter"] = orca_profile.get('settings', {}).get('filament_diameter', 1.75)
            
            # Temperature ranges
            first_temp = orca_profile.get('settings', {}).get('first_layer_temperature', 220)
            normal_temp = orca_profile.get('settings', {}).get('temperature', 210)
            profile["temp_range_min"] = min(first_temp, normal_temp) - 10
            profile["temp_range_max"] = max(first_temp, normal_temp) + 10
            
            first_bed_temp = orca_profile.get('settings', {}).get('first_layer_bed_temperature', 60)
            normal_bed_temp = orca_profile.get('settings', {}).get('bed_temperature', 50)
            profile["bed_temp_range_min"] = min(first_bed_temp, normal_bed_temp) - 5
            profile["bed_temp_range_max"] = max(first_bed_temp, normal_bed_temp) + 5
        
        elif profile_type == 'process':
            # Copy all settings
            for key, value in orca_profile.get('settings', {}).items():
                profile[key] = value
            
            # Extract Klipper config if present
            if 'klipper_config' in orca_profile:
                profile['klipper_config'] = orca_profile['klipper_config']
            elif 'start_gcode' in orca_profile.get('settings', {}):
                start_gcode = orca_profile['settings']['start_gcode']
                if 'SET_PRESSURE_ADVANCE' in start_gcode:
                    # Try to extract pressure advance values
                    import re
                    pa_match = re.search(r'SET_PRESSURE_ADVANCE\s+ADVANCE=([0-9.]+)', start_gcode)
                    pa_smooth_match = re.search(r'SMOOTH_TIME=([0-9.]+)', start_gcode)
                    
                    if pa_match or pa_smooth_match:
                        profile['klipper_config'] = {}
                        if pa_match:
                            profile['klipper_config']['pressure_advance'] = float(pa_match.group(1))
                        if pa_smooth_match:
                            profile['klipper_config']['pressure_advance_smooth_time'] = float(pa_smooth_match.group(1))
        
        return profile
