"""
Orca Slicer Settings Generator - Profile Module Initialization
Main initialization file for the profile generation component
"""

import os
from typing import Dict, Any, Optional

# Import profile components
from .profile_database import ProfileDatabase
from .profile_generator import ProfileGenerator

class ProfileManager:
    """
    Main manager class for the profile generation component of Orca Slicer Settings Generator.
    
    This class initializes and coordinates profile database and generator components,
    providing a unified interface for the rest of the application.
    """
    
    def __init__(self, data_dir: str = None):
        """
        Initialize the profile manager.
        
        Args:
            data_dir: Directory containing profile data files
        """
        self.data_dir = data_dir or os.path.join(os.path.dirname(__file__), '..', 'data')
        
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize components
        self.profile_db = ProfileDatabase(data_dir=self.data_dir)
        self.profile_generator = ProfileGenerator(data_dir=self.data_dir)
    
    # Printer profile methods
    
    def create_printer_profile(self, **kwargs) -> str:
        """Create a new printer profile."""
        return self.profile_generator.create_printer_profile(**kwargs)
    
    def update_printer_profile(self, printer_id: str, printer_data: Dict[str, Any]) -> bool:
        """Update an existing printer profile."""
        return self.profile_db.update_printer(printer_id, printer_data)
    
    def get_printer_profile(self, printer_id: str) -> Optional[Dict[str, Any]]:
        """Get a printer profile by ID."""
        return self.profile_db.get_printer(printer_id)
    
    def get_all_printer_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Get all printer profiles."""
        return self.profile_db.get_all_printers()
    
    def delete_printer_profile(self, printer_id: str) -> bool:
        """Delete a printer profile."""
        return self.profile_db.delete_printer(printer_id)
    
    def get_printer_templates(self) -> list:
        """Get all available printer templates."""
        return self.profile_generator.get_printer_templates()
    
    # Material profile methods
    
    def create_material_profile(self, **kwargs) -> str:
        """Create a new material profile."""
        return self.profile_generator.create_material_profile(**kwargs)
    
    def update_material_profile(self, material_id: str, material_data: Dict[str, Any]) -> bool:
        """Update an existing material profile."""
        return self.profile_db.update_material(material_id, material_data)
    
    def get_material_profile(self, material_id: str) -> Optional[Dict[str, Any]]:
        """Get a material profile by ID."""
        return self.profile_db.get_material(material_id)
    
    def get_all_material_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Get all material profiles."""
        return self.profile_db.get_all_materials()
    
    def delete_material_profile(self, material_id: str) -> bool:
        """Delete a material profile."""
        return self.profile_db.delete_material(material_id)
    
    def get_material_templates(self) -> list:
        """Get all available material templates."""
        return self.profile_generator.get_material_templates()
    
    # Process profile methods
    
    def generate_process_profile(self, **kwargs) -> str:
        """Generate an optimized process profile using AI."""
        return self.profile_generator.generate_process_profile(**kwargs)
    
    def optimize_process_profile(self, process_id: str, print_requirements: Dict[str, Any]) -> str:
        """Optimize an existing process profile using AI."""
        return self.profile_generator.optimize_process_profile(process_id, print_requirements)
    
    def update_process_profile(self, process_id: str, process_data: Dict[str, Any]) -> bool:
        """Update an existing process profile."""
        return self.profile_db.update_process(process_id, process_data)
    
    def get_process_profile(self, process_id: str) -> Optional[Dict[str, Any]]:
        """Get a process profile by ID."""
        return self.profile_db.get_process(process_id)
    
    def get_all_process_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Get all process profiles."""
        return self.profile_db.get_all_processes()
    
    def delete_process_profile(self, process_id: str) -> bool:
        """Delete a process profile."""
        return self.profile_db.delete_process(process_id)
    
    def get_process_templates(self) -> list:
        """Get all available process templates."""
        return self.profile_generator.get_process_templates()
    
    def compare_process_profiles(self, process_id_1: str, process_id_2: str) -> Dict[str, Any]:
        """Compare two process profiles and explain differences."""
        return self.profile_generator.compare_process_profiles(process_id_1, process_id_2)
    
    # Import/Export methods
    
    def export_profile_to_orca(self, profile_id: str, profile_type: str, output_file: str) -> bool:
        """Export a profile to Orca Slicer format."""
        return self.profile_generator.export_profile_to_orca(profile_id, profile_type, output_file)
    
    def import_profile_from_orca(self, profile_file: str, profile_type: str) -> Optional[str]:
        """Import a profile from Orca Slicer format."""
        return self.profile_generator.import_profile_from_orca(profile_file, profile_type)
    
    # Utility methods
    
    def save_all_profiles(self) -> bool:
        """Save all profiles to database files."""
        return self.profile_db.save_all()
