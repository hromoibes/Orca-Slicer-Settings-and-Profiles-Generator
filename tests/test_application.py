#!/usr/bin/env python3
"""
Orca Slicer Settings Generator - Test Suite
Unit and integration tests for the application
"""

import os
import sys
import unittest
import json
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Add parent directory to path to import application modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ai import AIManager
from src.profiles import ProfileManager

class TestAIComponent(unittest.TestCase):
    """Test cases for the AI component."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.ai_manager = AIManager(data_dir=self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_ai_initialization(self):
        """Test AI manager initialization."""
        self.assertIsNotNone(self.ai_manager)
        self.assertEqual(self.ai_manager.data_dir, self.temp_dir)
    
    def test_generate_profile(self):
        """Test profile generation."""
        # Mock printer and material data
        printer_id = "test_printer"
        material_id = "test_material"
        nozzle_size = 0.4
        print_requirements = {
            "purpose": "visual",
            "surface_quality_importance": 4,
            "strength_importance": 3,
            "speed_importance": 2,
            "material_usage_importance": 3
        }
        
        # Create directories needed for the test
        os.makedirs(os.path.join(self.temp_dir, 'printers'), exist_ok=True)
        os.makedirs(os.path.join(self.temp_dir, 'materials'), exist_ok=True)
        
        # Create mock printer and material files
        with open(os.path.join(self.temp_dir, 'printers', f"{printer_id}.json"), 'w') as f:
            json.dump({
                "id": printer_id,
                "name": "Test Printer",
                "vendor": "Test",
                "model": "Test Model",
                "use_klipper": True
            }, f)
            
        with open(os.path.join(self.temp_dir, 'materials', f"{material_id}.json"), 'w') as f:
            json.dump({
                "id": material_id,
                "name": "Test Material",
                "type": "PLA"
            }, f)
            
        profile = self.ai_manager.generate_profile(
            printer_id, material_id, nozzle_size, print_requirements, None, True
        )
        
        # Verify profile was generated
        self.assertIsNotNone(profile)
        self.assertIn("settings", profile)
        self.assertIn("layer_height", profile["settings"])
        self.assertEqual(profile["settings"]["layer_height"], 0.1)
    
    def test_explain_setting(self):
        """Test setting explanation."""
        setting_name = "layer_height"
        setting_value = 0.2
        context = {"printer_type": "cartesian", "material_type": "PLA"}
        
        explanation = self.ai_manager.explain_setting(setting_name, setting_value, context)
        
        # Verify explanation was generated
        self.assertIsNotNone(explanation)
        self.assertIn("explanation", explanation)

class TestProfileComponent(unittest.TestCase):
    """Test cases for the profile component."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.profile_manager = ProfileManager(data_dir=self.temp_dir)
        
        # Create directories needed for the test
        os.makedirs(os.path.join(self.temp_dir, 'printers'), exist_ok=True)
        os.makedirs(os.path.join(self.temp_dir, 'materials'), exist_ok=True)
        os.makedirs(os.path.join(self.temp_dir, 'processes'), exist_ok=True)
        
        # Initialize database files
        with open(os.path.join(self.temp_dir, 'printers.json'), 'w') as f:
            json.dump({
                'version': '1.0.0',
                'last_updated': '2023-01-01T00:00:00',
                'items': {}
            }, f)
            
        with open(os.path.join(self.temp_dir, 'materials.json'), 'w') as f:
            json.dump({
                'version': '1.0.0',
                'last_updated': '2023-01-01T00:00:00',
                'items': {}
            }, f)
            
        with open(os.path.join(self.temp_dir, 'processes.json'), 'w') as f:
            json.dump({
                'version': '1.0.0',
                'last_updated': '2023-01-01T00:00:00',
                'items': {}
            }, f)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_profile_manager_initialization(self):
        """Test profile manager initialization."""
        self.assertIsNotNone(self.profile_manager)
        self.assertEqual(self.profile_manager.data_dir, self.temp_dir)
    
    def test_create_printer_profile(self):
        """Test printer profile creation."""
        printer_id = self.profile_manager.create_printer_profile(
            name="Test Printer",
            vendor="Test Vendor",
            model="Test Model",
            bed_size=[220, 220],
            max_height=250,
            nozzle_diameter=0.4,
            is_direct_drive=True,
            printer_type="cartesian",
            use_klipper=True
        )
        
        # Verify printer profile was created
        self.assertIsNotNone(printer_id)
        
        # Retrieve and verify printer profile
        printer = self.profile_manager.get_printer_profile(printer_id)
        self.assertIsNotNone(printer)
        self.assertEqual(printer["name"], "Test Printer")
        self.assertEqual(printer["vendor"], "Test Vendor")
        self.assertEqual(printer["model"], "Test Model")
        self.assertEqual(printer["bed_size"], [220, 220])
        self.assertEqual(printer["max_print_height"], 250)
        self.assertEqual(printer["nozzle_diameter"], 0.4)
        self.assertTrue(printer["direct_drive"])
        self.assertEqual(printer["printer_type"], "cartesian")
        self.assertTrue(printer["use_klipper"])
    
    def test_create_material_profile(self):
        """Test material profile creation."""
        material_id = self.profile_manager.create_material_profile(
            name="Test PLA",
            vendor="Test Vendor",
            material_type="PLA",
            color="#FF0000",
            diameter=1.75,
            temp_range=[190, 220],
            bed_temp_range=[50, 60]
        )
        
        # Verify material profile was created
        self.assertIsNotNone(material_id)
        
        # Retrieve and verify material profile
        material = self.profile_manager.get_material_profile(material_id)
        self.assertIsNotNone(material)
        self.assertEqual(material["name"], "Test PLA")
        self.assertEqual(material["vendor"], "Test Vendor")
        self.assertEqual(material["type"], "PLA")
        self.assertEqual(material["color"], "#FF0000")
        self.assertEqual(material["diameter"], 1.75)
        self.assertEqual(material["temp_range_min"], 190)
        self.assertEqual(material["temp_range_max"], 220)
        self.assertEqual(material["bed_temp_range_min"], 50)
        self.assertEqual(material["bed_temp_range_max"], 60)
    
    def test_generate_process_profile(self):
        """Test process profile generation."""
        # Create printer and material profiles first
        printer_id = self.profile_manager.create_printer_profile(
            name="Test Printer",
            vendor="Test Vendor",
            model="Test Model",
            bed_size=[220, 220],
            max_height=250,
            nozzle_diameter=0.4,
            is_direct_drive=True,
            printer_type="cartesian",
            use_klipper=True
        )
        
        material_id = self.profile_manager.create_material_profile(
            name="Test PLA",
            vendor="Test Vendor",
            material_type="PLA",
            color="#FF0000",
            diameter=1.75,
            temp_range=[190, 220],
            bed_temp_range=[50, 60]
        )
        
        # Create mock AI manager
        mock_ai_result = {
            "settings": {
                "layer_height": 0.2,
                "print_speed": 50,
                "infill_density": 20,
                "temperature": 210,
                "bed_temperature": 60
            }
        }
        
        # Create process profile
        with patch('src.profiles.profile_generator.AIManager') as mock_ai:
            # Configure the mock
            mock_instance = mock_ai.return_value
            mock_instance.generate_profile.return_value = mock_ai_result
            
            # Replace the AI manager in the profile generator
            self.profile_manager.profile_generator.ai_manager = mock_instance
            
            process_id = self.profile_manager.generate_process_profile(
                name="Test Process",
                printer_id=printer_id,
                material_id=material_id,
                nozzle_size=0.4,
                print_requirements={
                    "quality": 0.5,
                    "strength": 0.5,
                    "speed": 0.5,
                    "material_usage": 0.5
                }
            )
        
        # Verify process profile was created
        self.assertIsNotNone(process_id)
        
        # Retrieve and verify process profile
        process = self.profile_manager.get_process_profile(process_id)
        self.assertIsNotNone(process)
        self.assertEqual(process["name"], "Test Process")
        self.assertEqual(process["printer_id"], printer_id)
        self.assertEqual(process["material_id"], material_id)
        self.assertEqual(process["nozzle_diameter"], 0.4)
        self.assertEqual(process["layer_height"], 0.2)
        self.assertEqual(process["print_speed"], 50)
        self.assertEqual(process["infill_density"], 20)
        self.assertEqual(process["temperature"], 210)
        self.assertEqual(process["bed_temperature"], 60)

class TestIntegration(unittest.TestCase):
    """Integration tests for the application."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.profile_manager = ProfileManager(data_dir=self.temp_dir)
        self.ai_manager = AIManager(data_dir=self.temp_dir)
        
        # Create directories needed for the test
        os.makedirs(os.path.join(self.temp_dir, 'printers'), exist_ok=True)
        os.makedirs(os.path.join(self.temp_dir, 'materials'), exist_ok=True)
        os.makedirs(os.path.join(self.temp_dir, 'processes'), exist_ok=True)
        
        # Initialize database files
        with open(os.path.join(self.temp_dir, 'printers.json'), 'w') as f:
            json.dump({
                'version': '1.0.0',
                'last_updated': '2023-01-01T00:00:00',
                'items': {}
            }, f)
            
        with open(os.path.join(self.temp_dir, 'materials.json'), 'w') as f:
            json.dump({
                'version': '1.0.0',
                'last_updated': '2023-01-01T00:00:00',
                'items': {}
            }, f)
            
        with open(os.path.join(self.temp_dir, 'processes.json'), 'w') as f:
            json.dump({
                'version': '1.0.0',
                'last_updated': '2023-01-01T00:00:00',
                'items': {}
            }, f)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_end_to_end_profile_generation(self):
        """Test end-to-end profile generation workflow."""
        # Create mock AI manager
        mock_ai_result = {
            "settings": {
                "layer_height": 0.2,
                "print_speed": 50,
                "infill_density": 20,
                "temperature": 210,
                "bed_temperature": 60
            }
        }
        
        # Create printer and material profiles
        with patch('src.profiles.profile_generator.AIManager') as mock_ai:
            # Configure the mock
            mock_instance = mock_ai.return_value
            mock_instance.generate_profile.return_value = mock_ai_result
            
            # Replace the AI manager in the profile generator
            self.profile_manager.profile_generator.ai_manager = mock_instance
            
            # Create printer profile
            printer_id = self.profile_manager.create_printer_profile(
                name="SonicPad Test",
                vendor="Creality",
                model="SonicPad",
                bed_size=[220, 220],
                max_height=250,
                nozzle_diameter=0.4,
                is_direct_drive=False,
                printer_type="cartesian",
                use_klipper=True
            )
            
            # Create material profile
            material_id = self.profile_manager.create_material_profile(
                name="Test PLA",
                vendor="Generic",
                material_type="PLA",
                color="#FFFFFF",
                diameter=1.75,
                temp_range=[190, 220],
                bed_temp_range=[50, 60]
            )
            
            # Generate process profile
            process_id = self.profile_manager.generate_process_profile(
                name="SonicPad PLA Standard",
                printer_id=printer_id,
                material_id=material_id,
                nozzle_size=0.4,
                print_requirements={
                    "quality": 0.5,
                    "strength": 0.5,
                    "speed": 0.5,
                    "material_usage": 0.5
                }
            )
            
            # Retrieve process profile
            process = self.profile_manager.get_process_profile(process_id)
            
            # Verify process profile
            self.assertIsNotNone(process)
            self.assertEqual(process["name"], "SonicPad PLA Standard")
            self.assertEqual(process["printer_id"], printer_id)
            self.assertEqual(process["material_id"], material_id)
            self.assertEqual(process["layer_height"], 0.2)
            
            # Export profile
            export_path = os.path.join(self.temp_dir, "test_export.json")
            result = self.profile_manager.export_profile_to_orca(process_id, "process", export_path)
            
            # Verify export
            self.assertTrue(result)
            self.assertTrue(os.path.exists(export_path))
            
            # Load exported profile
            with open(export_path, 'r') as f:
                exported = json.load(f)
                
            # Verify exported profile
            self.assertEqual(exported["name"], "SonicPad PLA Standard")
            self.assertEqual(exported["type"], "process")
            self.assertIn("settings", exported)
            self.assertIn("layer_height", exported["settings"])

if __name__ == '__main__':
    unittest.main()
