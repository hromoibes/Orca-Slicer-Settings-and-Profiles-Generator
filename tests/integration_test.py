#!/usr/bin/env python3
"""
Integration test for Orca Slicer Settings Generator
Tests the complete workflow from profile creation to export
"""

import os
import sys
import json
import uuid
import shutil
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import application modules
from src.ai import AIManager
from src.profiles import ProfileManager

def create_test_data(profile_manager):
    """Create test printer and material profiles."""
    print("\nCreating test data...")
    
    # Create SonicPad printer profile
    sonicpad_id = profile_manager.create_printer_profile(
        name="SonicPad Test Printer",
        vendor="Creality",
        model="SonicPad",
        bed_size=[220, 220],
        max_height=250,
        nozzle_diameter=0.4,
        is_direct_drive=False,
        printer_type="cartesian",
        use_klipper=True
    )
    print(f"  Created SonicPad printer profile: {sonicpad_id}")
    
    # Create standard printer profile
    standard_id = profile_manager.create_printer_profile(
        name="Standard Test Printer",
        vendor="Generic",
        model="Standard",
        bed_size=[220, 220],
        max_height=250,
        nozzle_diameter=0.4,
        is_direct_drive=True,
        printer_type="cartesian",
        use_klipper=False
    )
    print(f"  Created standard printer profile: {standard_id}")
    
    # Create PLA material profile
    pla_id = profile_manager.create_material_profile(
        name="Test PLA",
        vendor="Generic",
        material_type="PLA",
        color="#FFFFFF",
        diameter=1.75,
        temp_range=[190, 220],
        bed_temp_range=[50, 60]
    )
    print(f"  Created PLA material profile: {pla_id}")
    
    # Create PETG material profile
    petg_id = profile_manager.create_material_profile(
        name="Test PETG",
        vendor="Generic",
        material_type="PETG",
        color="#00FFFF",
        diameter=1.75,
        temp_range=[230, 250],
        bed_temp_range=[70, 85]
    )
    print(f"  Created PETG material profile: {petg_id}")
    
    return [sonicpad_id, standard_id], [pla_id, petg_id]

def test_profile_generation(profile_manager, printer_ids, material_ids):
    """Test process profile generation."""
    print("\nTesting profile generation...")
    process_ids = []
    
    # Generate SonicPad PLA profile
    print("  Generating SonicPad PLA profile...")
    sonicpad_pla_id = profile_manager.generate_process_profile(
        name="SonicPad PLA Standard",
        printer_id=printer_ids[0],
        material_id=material_ids[0],
        nozzle_size=0.4,
        print_requirements={
            "quality": 0.5,
            "strength": 0.5,
            "speed": 0.5,
            "material_usage": 0.5
        }
    )
    print(f"    Created process profile: {sonicpad_pla_id}")
    process_ids.append(sonicpad_pla_id)
    
    # Generate SonicPad PETG profile
    print("  Generating SonicPad PETG profile...")
    sonicpad_petg_id = profile_manager.generate_process_profile(
        name="SonicPad PETG Standard",
        printer_id=printer_ids[0],
        material_id=material_ids[1],
        nozzle_size=0.4,
        print_requirements={
            "quality": 0.5,
            "strength": 0.7,
            "speed": 0.3,
            "material_usage": 0.5
        }
    )
    print(f"    Created process profile: {sonicpad_petg_id}")
    process_ids.append(sonicpad_petg_id)
    
    # Generate Standard PLA profile
    print("  Generating Standard PLA profile...")
    standard_pla_id = profile_manager.generate_process_profile(
        name="Standard PLA Standard",
        printer_id=printer_ids[1],
        material_id=material_ids[0],
        nozzle_size=0.4,
        print_requirements={
            "quality": 0.7,
            "strength": 0.5,
            "speed": 0.3,
            "material_usage": 0.5
        }
    )
    print(f"    Created process profile: {standard_pla_id}")
    process_ids.append(standard_pla_id)
    
    return process_ids

def test_profile_optimization(profile_manager, process_ids):
    """Test process profile optimization."""
    print("\nTesting profile optimization...")
    process_id = process_ids[0]  # Use first process profile
    
    print(f"  Optimizing process profile: {process_id}")
    optimized_id = profile_manager.optimize_process_profile(
        process_id,
        print_requirements={
            "quality": 0.8,
            "strength": 0.5,
            "speed": 0.2,
            "material_usage": 0.5
        }
    )
    print(f"    Created optimized profile: {optimized_id}")
    
    return optimized_id

def test_profile_comparison(profile_manager, process_id_1, process_id_2):
    """Test profile comparison."""
    print("\nTesting profile comparison...")
    print(f"  Comparing profiles: {process_id_1} and {process_id_2}")
    
    comparison = profile_manager.compare_process_profiles(process_id_1, process_id_2)
    
    print("  Comparison results:")
    print(f"    differences: {comparison.get('differences')}")
    print(f"    summary: {comparison.get('summary')}")
    print(f"    print_time_difference: {comparison.get('print_time_difference')}")
    print(f"    quality_difference: {comparison.get('quality_difference')}")
    print(f"    strength_difference: {comparison.get('strength_difference')}")
    
    return comparison

def test_profile_export(profile_manager, process_id, output_dir):
    """Test profile export."""
    print("\nTesting profile export...")
    
    # Get process profile
    process = profile_manager.get_process_profile(process_id)
    
    # Debug: Print process details
    print(f"  Process ID: {process_id}")
    print(f"  Process data: {process}")
    
    # Create export filename
    if process and 'name' in process:
        filename = f"{process['name'].replace(' ', '_')}.json"
        filepath = os.path.join(output_dir, filename)
        
        print(f"  Exporting profile {process_id} to {filepath}")
        result = profile_manager.export_profile_to_orca(process_id, "process", filepath)
        
        if result:
            print("  Export successful!")
            
            # Verify exported file
            with open(filepath, 'r') as f:
                exported_data = json.load(f)
                print("  Exported data preview:")
                print(f"    Name: {exported_data.get('name')}")
                print(f"    Settings count: {len(exported_data.get('settings', {}))}")
        else:
            print("  Export failed!")
    else:
        print(f"  Error: Process profile {process_id} not found or missing name")

def test_ai_explanations(ai_manager):
    """Test AI explanations."""
    print("\nTesting AI explanations...")
    
    setting_name = "layer_height"
    setting_value = 0.2
    context = {"printer_type": "cartesian", "material_type": "PLA"}
    
    explanation = ai_manager.explain_setting(setting_name, setting_value, context)
    print(f"  Explanation for {setting_name}={setting_value}:")
    print(f"    {explanation}")
    
    return explanation

def main():
    """Main test function."""
    print("=== Running Integration Tests ===")
    
    # Set up test environment
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'test'))
    output_dir = os.path.join(data_dir, 'exports')
    
    print(f"Using data directory: {data_dir}")
    print(f"Using output directory: {output_dir}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    print("\nInitializing components...")
    ai_manager = AIManager(data_dir=data_dir)
    profile_manager = ProfileManager(data_dir=data_dir)
    
    try:
        # Run tests
        printer_ids, material_ids = create_test_data(profile_manager)
        process_ids = test_profile_generation(profile_manager, printer_ids, material_ids)
        optimized_id = test_profile_optimization(profile_manager, process_ids)
        test_profile_comparison(profile_manager, process_ids[0], optimized_id)
        test_profile_export(profile_manager, optimized_id, output_dir)
        test_ai_explanations(ai_manager)
        
        print("\nAll tests completed successfully!")
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
