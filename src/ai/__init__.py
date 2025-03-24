"""
Orca Slicer Settings Generator - AI Module Initialization
Main initialization file for the AI component
"""

import os
import sys
from typing import Dict, Any, Optional

# Import AI components
from .orca_ai import OrcaAI
from .rule_engine import RuleEngine
from .settings_metadata import SettingsMetadata
from .klipper_integration import KlipperIntegration

class AIManager:
    """
    Main manager class for the AI component of Orca Slicer Settings Generator.
    
    This class initializes and coordinates all AI subcomponents, providing
    a unified interface for the rest of the application.
    """
    
    def __init__(self, data_dir: str = None):
        """
        Initialize the AI manager.
        
        Args:
            data_dir: Directory containing AI data files
        """
        self.data_dir = data_dir or os.path.join(os.path.dirname(__file__), '..', 'data')
        
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize components
        self.settings_metadata = SettingsMetadata(
            metadata_file=os.path.join(self.data_dir, 'settings_metadata.json')
        )
        
        self.rule_engine = RuleEngine(
            rules_file=os.path.join(self.data_dir, 'rules.json')
        )
        
        self.klipper_integration = KlipperIntegration(
            config_file=os.path.join(self.data_dir, 'klipper_config.json')
        )
        
        self.orca_ai = OrcaAI(data_dir=self.data_dir)
        
        # Initialize component integration
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize and integrate AI components."""
        # Save default metadata and rules if files don't exist
        self.settings_metadata.save_metadata()
        self.rule_engine.save_rules()
        self.klipper_integration.save_config()
        
        # Add Klipper settings to metadata
        self._integrate_klipper_settings()
    
    def _integrate_klipper_settings(self):
        """Integrate Klipper settings into metadata."""
        # Get Klipper-specific settings
        klipper_settings = self.klipper_integration.get_additional_settings()
        
        # Add each setting to metadata
        for setting in klipper_settings:
            self.settings_metadata.add_setting(setting['name'], setting)
    
    def generate_profile(
        self,
        printer_id: int,
        material_id: int,
        nozzle_size: float,
        print_requirements: Dict[str, Any],
        base_profile_id: Optional[int] = None,
        use_klipper: bool = True
    ) -> Dict[str, Any]:
        """
        Generate an optimized profile based on printer, material and requirements.
        
        Args:
            printer_id: Database ID of the printer
            material_id: Database ID of the material
            nozzle_size: Nozzle diameter in mm
            print_requirements: Dict containing print priorities and requirements
            base_profile_id: Optional ID of profile to use as starting point
            use_klipper: Whether to apply Klipper-specific optimizations
            
        Returns:
            Dictionary containing complete profile with all settings
        """
        # Generate base profile using OrcaAI
        profile = self.orca_ai.generate_profile(
            printer_id, material_id, nozzle_size, print_requirements, base_profile_id
        )
        
        # Apply Klipper optimizations if requested
        if use_klipper:
            printer_info = self.orca_ai._get_printer_info(printer_id)
            material_info = self.orca_ai._get_material_info(material_id)
            
            profile['settings'] = self.klipper_integration.apply_klipper_optimizations(
                profile['settings'], printer_info, material_info
            )
            
            # Add Klipper configuration snippet
            profile['klipper_config'] = self.klipper_integration.generate_klipper_config(
                printer_info, profile['settings']
            )
            
            # Add Klipper-specific explanations
            klipper_explanations = self.klipper_integration.explain_klipper_settings(
                profile['settings']
            )
            profile['explanations'].update(klipper_explanations)
        
        return profile
    
    def recommend_setting(
        self,
        setting_name: str,
        printer_id: int,
        material_id: int,
        nozzle_size: float,
        current_settings: Dict[str, Any],
        print_requirements: Dict[str, Any],
        use_klipper: bool = True
    ) -> Dict[str, Any]:
        """
        Get AI recommendation for a specific setting.
        
        Args:
            setting_name: Name of the setting to recommend
            printer_id: Database ID of the printer
            material_id: Database ID of the material
            nozzle_size: Nozzle diameter in mm
            current_settings: Dict of current profile settings
            print_requirements: Dict containing print priorities
            use_klipper: Whether to apply Klipper-specific optimizations
            
        Returns:
            Recommendation dictionary
        """
        # Get base recommendation from OrcaAI
        recommendation = self.orca_ai.recommend_setting(
            setting_name, printer_id, material_id, nozzle_size, 
            current_settings, print_requirements
        )
        
        # Apply Klipper-specific recommendations if applicable
        if use_klipper and setting_name.startswith(('pressure_advance', 'input_shaper', 'max_accel')):
            printer_info = self.orca_ai._get_printer_info(printer_id)
            material_info = self.orca_ai._get_material_info(material_id)
            
            # Apply Klipper optimizations to a copy of current settings
            optimized_settings = current_settings.copy()
            optimized_settings = self.klipper_integration.apply_klipper_optimizations(
                optimized_settings, printer_info, material_info
            )
            
            # Update recommendation with Klipper-optimized value
            if setting_name in optimized_settings:
                recommendation['value'] = optimized_settings[setting_name]
                
                # Add Klipper-specific explanation
                klipper_explanations = self.klipper_integration.explain_klipper_settings(
                    {setting_name: optimized_settings[setting_name]}
                )
                if setting_name in klipper_explanations:
                    recommendation['explanation'] = klipper_explanations[setting_name]
                elif 'input_shaper' in klipper_explanations and setting_name.startswith('input_shaper'):
                    recommendation['explanation'] = klipper_explanations['input_shaper']
        
        return recommendation
    
    def explain_setting(
        self,
        setting_name: str,
        setting_value: Any,
        context: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Generate explanation for why a setting has a particular value.
        
        Args:
            setting_name: Name of the setting to explain
            setting_value: Current value of the setting
            context: Dict containing relevant context (printer, material, etc.)
            
        Returns:
            Explanation dictionary
        """
        # Get base explanation from OrcaAI
        explanation = self.orca_ai.explain_setting(
            setting_name, setting_value, context
        )
        
        # Add Klipper-specific explanations if applicable
        if setting_name.startswith(('pressure_advance', 'input_shaper', 'max_accel')):
            klipper_explanations = self.klipper_integration.explain_klipper_settings(
                {setting_name: setting_value}
            )
            
            if setting_name in klipper_explanations:
                explanation['explanation'] = klipper_explanations[setting_name]
            elif 'input_shaper' in klipper_explanations and setting_name.startswith('input_shaper'):
                explanation['explanation'] = klipper_explanations['input_shaper']
        
        return explanation
    
    def compare_profiles(
        self,
        profile_id_1: int,
        profile_id_2: int
    ) -> Dict[str, Any]:
        """
        Compare two profiles and explain differences.
        
        Args:
            profile_id_1: Database ID of first profile
            profile_id_2: Database ID of second profile
            
        Returns:
            Comparison dictionary
        """
        # Use OrcaAI for profile comparison
        return self.orca_ai.compare_profiles(profile_id_1, profile_id_2)
    
    def train_models(self, training_data_path: str = None) -> Dict[str, Any]:
        """
        Train or update the AI models with new data.
        
        Args:
            training_data_path: Path to training data file
            
        Returns:
            Training results dictionary
        """
        # Use OrcaAI for model training
        return self.orca_ai.train_models()
    
    def get_setting_metadata(self, setting_name: str) -> Dict[str, Any]:
        """
        Get metadata for a specific setting.
        
        Args:
            setting_name: Name of the setting
            
        Returns:
            Setting metadata dictionary
        """
        return self.settings_metadata.get_setting(setting_name)
    
    def get_settings_by_category(self, category: str) -> Dict[str, Dict[str, Any]]:
        """
        Get all settings in a specific category.
        
        Args:
            category: Category name
            
        Returns:
            Dictionary of settings in the category
        """
        return self.settings_metadata.get_settings_by_category(category)
    
    def get_klipper_start_gcode(self, use_pressure_advance: bool = True, use_input_shaper: bool = True) -> str:
        """
        Get Klipper-specific start G-code.
        
        Args:
            use_pressure_advance: Whether to include pressure advance commands
            use_input_shaper: Whether to include input shaper commands
            
        Returns:
            Start G-code as string
        """
        gcode_lines = self.klipper_integration.get_start_gcode(
            use_pressure_advance, use_input_shaper
        )
        return '\n'.join(gcode_lines)
    
    def get_klipper_end_gcode(self) -> str:
        """
        Get Klipper-specific end G-code.
        
        Returns:
            End G-code as string
        """
        gcode_lines = self.klipper_integration.get_end_gcode()
        return '\n'.join(gcode_lines)
    
    def get_klipper_config(self, printer_model: str) -> Dict[str, Any]:
        """
        Get Klipper configuration for a specific printer model.
        
        Args:
            printer_model: Name of the printer model
            
        Returns:
            Printer configuration dictionary
        """
        return self.klipper_integration.get_printer_config(printer_model)
