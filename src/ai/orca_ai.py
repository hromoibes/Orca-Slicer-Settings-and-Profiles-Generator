"""
Orca Slicer Settings Generator - AI Component
Main module for the AI recommendation engine
"""

import os
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from typing import Dict, List, Any, Optional, Tuple, Union

class OrcaAI:
    """
    Main AI engine for Orca Slicer Settings Generator.
    
    This class implements a hybrid approach combining:
    1. Machine learning models (scikit-learn)
    2. Rule-based expert system
    3. Constraint satisfaction for setting dependencies
    """
    
    def __init__(self, data_dir: str = None):
        """
        Initialize the AI engine.
        
        Args:
            data_dir: Directory containing training data and rule definitions
        """
        self.data_dir = data_dir or os.path.join(os.path.dirname(__file__), '..', 'data')
        self.models = {}  # Store trained models
        self.rules = {}   # Store rule-based logic
        self.settings_metadata = {}  # Store settings metadata
        self.printer_metadata = {}   # Store printer capabilities
        self.material_metadata = {}  # Store material properties
        
        # Load metadata and rules
        self._load_metadata()
        self._load_rules()
        
    def _load_metadata(self):
        """Load settings, printer, and material metadata."""
        try:
            # Load settings metadata
            settings_path = os.path.join(self.data_dir, 'settings_metadata.json')
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    self.settings_metadata = json.load(f)
            
            # Load printer metadata
            printers_path = os.path.join(self.data_dir, 'printer_metadata.json')
            if os.path.exists(printers_path):
                with open(printers_path, 'r') as f:
                    self.printer_metadata = json.load(f)
            
            # Load material metadata
            materials_path = os.path.join(self.data_dir, 'material_metadata.json')
            if os.path.exists(materials_path):
                with open(materials_path, 'r') as f:
                    self.material_metadata = json.load(f)
        except Exception as e:
            print(f"Error loading metadata: {e}")
    
    def _load_rules(self):
        """Load rule-based logic from rule definitions."""
        try:
            rules_path = os.path.join(self.data_dir, 'rules.json')
            if os.path.exists(rules_path):
                with open(rules_path, 'r') as f:
                    self.rules = json.load(f)
        except Exception as e:
            print(f"Error loading rules: {e}")
    
    def train_models(self, training_data: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """
        Train machine learning models for settings prediction.
        
        Args:
            training_data: DataFrame containing training examples
                           If None, will load from data directory
        
        Returns:
            Dictionary with training results and metrics
        """
        if training_data is None:
            # Load training data from file
            data_path = os.path.join(self.data_dir, 'training_data.csv')
            if not os.path.exists(data_path):
                return {"success": False, "error": "Training data not found"}
            
            training_data = pd.read_csv(data_path)
        
        results = {}
        
        # Group settings by type for appropriate model selection
        numeric_settings = []
        categorical_settings = []
        boolean_settings = []
        
        for setting_name, metadata in self.settings_metadata.items():
            if metadata['data_type'] in ['float', 'int']:
                numeric_settings.append(setting_name)
            elif metadata['data_type'] == 'bool':
                boolean_settings.append(setting_name)
            else:
                categorical_settings.append(setting_name)
        
        # Features that will be used for prediction
        feature_columns = [
            'printer_type', 'direct_drive', 'build_volume_x', 'build_volume_y', 
            'build_volume_z', 'max_temp', 'heated_bed', 'material_type',
            'nozzle_size', 'strength_importance', 'surface_quality_importance',
            'speed_importance', 'material_usage_importance', 
            'dimensional_accuracy_importance', 'purpose'
        ]
        
        # Train models for numeric settings
        for setting in numeric_settings:
            if setting in training_data.columns:
                X = training_data[feature_columns]
                y = training_data[setting]
                
                # Handle categorical features
                X = pd.get_dummies(X, columns=['printer_type', 'material_type', 'purpose'])
                
                # Split data
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42
                )
                
                # Create and train model
                model = Pipeline([
                    ('scaler', StandardScaler()),
                    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
                ])
                
                model.fit(X_train, y_train)
                
                # Evaluate model
                train_score = model.score(X_train, y_train)
                test_score = model.score(X_test, y_test)
                
                # Store model
                self.models[setting] = {
                    'model': model,
                    'type': 'numeric',
                    'train_score': train_score,
                    'test_score': test_score,
                    'feature_columns': list(X.columns)
                }
                
                results[setting] = {
                    'train_score': train_score,
                    'test_score': test_score
                }
        
        # Train models for boolean settings
        for setting in boolean_settings:
            if setting in training_data.columns:
                X = training_data[feature_columns]
                y = training_data[setting].astype(int)
                
                # Handle categorical features
                X = pd.get_dummies(X, columns=['printer_type', 'material_type', 'purpose'])
                
                # Split data
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42
                )
                
                # Create and train model
                model = Pipeline([
                    ('scaler', StandardScaler()),
                    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
                ])
                
                model.fit(X_train, y_train)
                
                # Evaluate model
                train_score = model.score(X_train, y_train)
                test_score = model.score(X_test, y_test)
                
                # Store model
                self.models[setting] = {
                    'model': model,
                    'type': 'boolean',
                    'train_score': train_score,
                    'test_score': test_score,
                    'feature_columns': list(X.columns)
                }
                
                results[setting] = {
                    'train_score': train_score,
                    'test_score': test_score
                }
        
        # Train models for categorical settings
        for setting in categorical_settings:
            if setting in training_data.columns:
                X = training_data[feature_columns]
                y = training_data[setting]
                
                # Handle categorical features in both X and y
                X = pd.get_dummies(X, columns=['printer_type', 'material_type', 'purpose'])
                
                # Split data
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42
                )
                
                # Create and train model
                model = Pipeline([
                    ('scaler', StandardScaler()),
                    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
                ])
                
                model.fit(X_train, y_train)
                
                # Evaluate model
                train_score = model.score(X_train, y_train)
                test_score = model.score(X_test, y_test)
                
                # Store model
                self.models[setting] = {
                    'model': model,
                    'type': 'categorical',
                    'train_score': train_score,
                    'test_score': test_score,
                    'feature_columns': list(X.columns),
                    'classes': list(y.unique())
                }
                
                results[setting] = {
                    'train_score': train_score,
                    'test_score': test_score
                }
        
        # Calculate overall metrics
        avg_train_score = np.mean([r['train_score'] for r in results.values()])
        avg_test_score = np.mean([r['test_score'] for r in results.values()])
        
        return {
            'success': True,
            'models_trained': len(results),
            'avg_train_score': avg_train_score,
            'avg_test_score': avg_test_score,
            'model_results': results
        }
    
    def generate_profile(
        self,
        printer_id: int,
        material_id: int,
        nozzle_size: float,
        print_requirements: Dict[str, Any],
        base_profile_id: Optional[int] = None
    ) -> Dict[str, Any]:
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
        # This is a simplified implementation for demonstration
        # In a real implementation, we would:
        # 1. Fetch printer and material data from database
        # 2. Load base profile if provided
        # 3. Generate predictions for each setting
        # 4. Apply rules and constraints
        # 5. Return complete profile
        
        # For now, we'll create a mock implementation
        printer_info = self._get_printer_info(printer_id)
        material_info = self._get_material_info(material_id)
        
        # Start with default settings
        profile = self._get_default_settings(printer_info, material_info, nozzle_size)
        
        # Apply AI recommendations for key settings
        profile = self._apply_ai_recommendations(
            profile, printer_info, material_info, nozzle_size, print_requirements
        )
        
        # Apply rule-based adjustments
        profile = self._apply_rules(profile, printer_info, material_info, print_requirements)
        
        # Ensure setting dependencies and constraints are satisfied
        profile = self._apply_constraints(profile)
        
        # Generate explanations for key settings
        explanations = self._generate_explanations(
            profile, printer_info, material_info, print_requirements
        )
        
        return {
            'settings': profile,
            'explanations': explanations,
            'printer_id': printer_id,
            'material_id': material_id,
            'nozzle_size': nozzle_size,
            'requirements': print_requirements
        }
    
    def _get_printer_info(self, printer_id: int) -> Dict[str, Any]:
        """Get printer information from database or metadata."""
        # In a real implementation, this would fetch from database
        # For now, return mock data
        return {
            'printer_id': printer_id,
            'manufacturer': 'Prusa Research',
            'model': 'i3 MK3S+',
            'printer_type': 'cartesian',
            'build_volume_x': 250,
            'build_volume_y': 210,
            'build_volume_z': 210,
            'max_temp': 280,
            'heated_bed': True,
            'direct_drive': True,
            'default_nozzle_size': 0.4
        }
    
    def _get_material_info(self, material_id: int) -> Dict[str, Any]:
        """Get material information from database or metadata."""
        # In a real implementation, this would fetch from database
        # For now, return mock data
        return {
            'material_id': material_id,
            'name': 'Generic PLA',
            'type': 'PLA',
            'manufacturer': 'Generic',
            'temp_range_min': 190,
            'temp_range_max': 220,
            'bed_temp_min': 50,
            'bed_temp_max': 60,
            'cooling_min': 80,
            'cooling_max': 100,
            'density': 1.24,
            'diameter': 1.75
        }
    
    def _get_default_settings(
        self, 
        printer_info: Dict[str, Any], 
        material_info: Dict[str, Any],
        nozzle_size: float
    ) -> Dict[str, Any]:
        """Get default settings for the given printer and material."""
        # In a real implementation, this would load from a base profile
        # For now, return reasonable defaults for PLA
        
        # Calculate some derived values
        layer_height = round(nozzle_size * 0.4, 2)  # 40% of nozzle size is a good default
        line_width = round(nozzle_size * 1.1, 2)    # 110% of nozzle size
        
        return {
            # Quality settings
            'layer_height': layer_height,
            'initial_layer_height': layer_height * 1.5,
            'line_width': line_width,
            
            # Shell settings
            'wall_thickness': line_width * 3,
            'wall_line_count': 3,
            'top_thickness': layer_height * 6,
            'top_layers': 6,
            'bottom_thickness': layer_height * 5,
            'bottom_layers': 5,
            
            # Infill settings
            'infill_density': 20,  # 20%
            'infill_pattern': 'gyroid',
            
            # Material settings
            'material_print_temperature': (material_info['temp_range_min'] + material_info['temp_range_max']) // 2,
            'material_bed_temperature': (material_info['bed_temp_min'] + material_info['bed_temp_max']) // 2,
            'material_flow': 100,  # 100%
            
            # Speed settings
            'print_speed': 50,  # mm/s
            'infill_speed': 80,  # mm/s
            'outer_wall_speed': 25,  # mm/s
            'inner_wall_speed': 50,  # mm/s
            'travel_speed': 150,  # mm/s
            
            # Travel settings
            'retraction_enable': True,
            'retraction_distance': 0.8 if printer_info['direct_drive'] else 5.0,
            'retraction_speed': 35,
            'z_hop_enable': False,
            
            # Cooling settings
            'cooling_enable': True,
            'fan_speed': material_info['cooling_max'],
            'initial_fan_speed': material_info['cooling_min'],
            
            # Support settings
            'support_enable': False,
            'support_type': 'everywhere',
            'support_angle': 50,
            
            # Build plate adhesion settings
            'adhesion_type': 'skirt',
            'skirt_line_count': 3,
            'brim_width': 8,
            
            # Experimental settings
            'ironing_enabled': False,
            'adaptive_layers': False
        }
    
    def _apply_ai_recommendations(
        self,
        profile: Dict[str, Any],
        printer_info: Dict[str, Any],
        material_info: Dict[str, Any],
        nozzle_size: float,
        print_requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply AI-based recommendations to the profile."""
        # In a real implementation, this would use the trained models
        # For now, implement a simplified rule-based approach
        
        # Extract requirements
        strength_importance = print_requirements.get('strength_importance', 3)
        quality_importance = print_requirements.get('surface_quality_importance', 3)
        speed_importance = print_requirements.get('speed_importance', 3)
        material_usage = print_requirements.get('material_usage_importance', 3)
        accuracy = print_requirements.get('dimensional_accuracy_importance', 3)
        purpose = print_requirements.get('purpose', 'visual')
        
        # Adjust layer height based on quality vs speed
        if quality_importance > speed_importance:
            # Prioritize quality with finer layers
            profile['layer_height'] = round(max(nozzle_size * 0.25, 0.08), 2)
        elif speed_importance > quality_importance:
            # Prioritize speed with thicker layers
            profile['layer_height'] = round(min(nozzle_size * 0.75, 0.3), 2)
        
        # Recalculate derived values
        profile['initial_layer_height'] = round(profile['layer_height'] * 1.5, 2)
        profile['top_thickness'] = profile['layer_height'] * 6
        profile['top_layers'] = round(profile['top_thickness'] / profile['layer_height'])
        profile['bottom_thickness'] = profile['layer_height'] * 5
        profile['bottom_layers'] = round(profile['bottom_thickness'] / profile['layer_height'])
        
        # Adjust wall count based on strength vs material usage
        if strength_importance > material_usage:
            profile['wall_line_count'] = 4
        elif material_usage > strength_importance:
            profile['wall_line_count'] = 2
        
        profile['wall_thickness'] = profile['line_width'] * profile['wall_line_count']
        
        # Adjust infill based on strength vs material usage
        if strength_importance > 4:
            profile['infill_density'] = 40
            profile['infill_pattern'] = 'cubic'
        elif strength_importance > 3:
            profile['infill_density'] = 30
            profile['infill_pattern'] = 'gyroid'
        elif material_usage > 4:
            profile['infill_density'] = 10
            profile['infill_pattern'] = 'gyroid'
        
        # Adjust print speed based on speed vs quality
        if speed_importance > 4:
            profile['print_speed'] = 70
            profile['infill_speed'] = 100
            profile['outer_wall_speed'] = 35
            profile['inner_wall_speed'] = 70
        elif quality_importance > 4:
            profile['print_speed'] = 40
            profile['infill_speed'] = 60
            profile['outer_wall_speed'] = 20
            profile['inner_wall_speed'] = 40
        
        # Adjust temperature based on purpose
        if purpose == 'functional':
            # Higher temperature for better layer adhesion
            profile['material_print_temperature'] = min(
                material_info['temp_range_max'] - 5,
                profile['material_print_temperature'] + 10
            )
        elif purpose == 'visual':
            # Lower temperature for better details
            profile['material_print_temperature'] = max(
                material_info['temp_range_min'] + 5,
                profile['material_print_temperature'] - 5
            )
        
        # Adjust cooling based on purpose and material
        if purpose == 'miniature' and material_info['type'] == 'PLA':
            profile['fan_speed'] = 100
            profile['initial_fan_speed'] = 100
        elif purpose == 'functional' and material_info['type'] == 'PLA':
            profile['fan_speed'] = 80
        
        # Adjust support settings based on purpose
        if purpose == 'miniature':
            profile['support_enable'] = True
            profile['support_angle'] = 60
        elif purpose == 'functional':
            profile['support_enable'] = True
            profile['support_angle'] = 45
        
        # Adjust build plate adhesion based on purpose and size
        if purpose == 'large':
            profile['adhesion_type'] = 'brim'
            profile['brim_width'] = 10
        elif purpose == 'miniature':
            profile['adhesion_type'] = 'brim'
            profile['brim_width'] = 4
        
        # Adjust experimental features based on quality requirements
        if quality_importance > 4 and purpose == 'visual':
            profile['ironing_enabled'] = True
        
        if accuracy > 4:
            profile['adaptive_layers'] = True
        
        return profile
    
    def _apply_rules(
        self,
        profile: Dict[str, Any],
        printer_info: Dict[str, Any],
        material_info: Dict[str, Any],
        print_requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply rule-based adjustments to the profile."""
        # Apply material-specific rules
        if material_info['type'] == 'PETG':
            # PETG specific adjustments
            profile['retraction_distance'] = min(profile['retraction_distance'] * 1.2, 8.0)
            profile['fan_speed'] = min(profile['fan_speed'], 60)
            profile['print_speed'] = min(profile['print_speed'], 60)
        elif material_info['type'] == 'ABS':
            # ABS specific adjustments
            profile['fan_speed'] = min(profile['fan_speed'], 30)
            profile['initial_fan_speed'] = 0
            profile['adhesion_type'] = 'brim'
            profile['brim_width'] = max(profile['brim_width'], 8)
        elif material_info['type'] == 'TPU':
            # TPU specific adjustments
            profile['retraction_enable'] = False
            profile['print_speed'] = min(profile['print_speed'], 30)
            profile['outer_wall_speed'] = min(profile['outer_wall_speed'], 15)
        
        # Apply printer-specific rules
        if not printer_info['direct_drive']:
            # Bowden extruder adjustments
            profile['retraction_distance'] = max(profile['retraction_distance'], 5.0)
            profile['retraction_speed'] = min(profile['retraction_speed'], 45)
        
        if printer_info['printer_type'] == 'delta':
            # Delta printer adjustments
            profile['travel_speed'] = max(profile['travel_speed'], 200)
            profile['initial_layer_height'] = min(profile['initial_layer_height'], 0.3)
        
        # Apply purpose-specific rules
        purpose = print_requirements.get('purpose', 'visual')
        if purpose == 'miniature':
            # Miniature-specific adjustments
            profile['minimum_wall_flow'] = 90
            profile['z_hop_enable'] = True
            profile['z_hop_height'] = 0.2
        elif purpose == 'large':
            # Large model adjustments
            profile['infill_pattern'] = 'cubic' if profile['infill_density'] > 15 else 'grid'
            profile['z_seam_type'] = 'sharpest_corner'
        
        return profile
    
    def _apply_constraints(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure setting dependencies and constraints are satisfied."""
        # Ensure wall thickness matches wall count and line width
        profile['wall_thickness'] = profile['wall_line_count'] * profile['line_width']
        
        # Ensure top/bottom layer count matches thickness
        profile['top_layers'] = round(profile['top_thickness'] / profile['layer_height'])
        profile['bottom_layers'] = round(profile['bottom_thickness'] / profile['layer_height'])
        
        # Ensure support settings are consistent
        if not profile['support_enable']:
            profile['support_type'] = 'none'
        
        # Ensure adhesion settings are consistent
        if profile['adhesion_type'] == 'skirt':
            profile['brim_width'] = 0
        elif profile['adhesion_type'] == 'brim':
            profile['skirt_line_count'] = 0
        elif profile['adhesion_type'] == 'raft':
            profile['skirt_line_count'] = 0
            profile['brim_width'] = 0
        
        # Ensure retraction settings are consistent
        if not profile['retraction_enable']:
            profile['z_hop_enable'] = False
        
        return profile
    
    def _generate_explanations(
        self,
        profile: Dict[str, Any],
        printer_info: Dict[str, Any],
        material_info: Dict[str, Any],
        print_requirements: Dict[str, Any]
    ) -> Dict[str, str]:
        """Generate explanations for key settings."""
        explanations = {}
        
        # Layer height explanation
        explanations['layer_height'] = (
            f"Layer height of {profile['layer_height']}mm provides a balance between "
            f"quality and print speed. "
            f"{'This is a finer layer height for higher quality.' if profile['layer_height'] < 0.16 else ''}"
            f"{'This is a thicker layer height for faster printing.' if profile['layer_height'] > 0.2 else ''}"
        )
        
        # Wall count explanation
        explanations['wall_line_count'] = (
            f"{profile['wall_line_count']} walls provides "
            f"{'strong' if profile['wall_line_count'] >= 3 else 'adequate'} structural integrity "
            f"while {'optimizing' if profile['wall_line_count'] <= 3 else 'maintaining'} material usage."
        )
        
        # Infill explanation
        explanations['infill_density'] = (
            f"{profile['infill_density']}% infill with {profile['infill_pattern']} pattern "
            f"{'maximizes strength' if profile['infill_density'] > 30 else ''}"
            f"{'balances strength and material usage' if 15 <= profile['infill_density'] <= 30 else ''}"
            f"{'minimizes material usage' if profile['infill_density'] < 15 else ''}."
        )
        
        # Temperature explanation
        explanations['material_print_temperature'] = (
            f"Print temperature of {profile['material_print_temperature']}°C is "
            f"{'on the higher end' if profile['material_print_temperature'] > (material_info['temp_range_min'] + material_info['temp_range_max']) / 2 else 'on the lower end'} "
            f"of the recommended range for {material_info['type']}. "
            f"{'Higher temperatures improve layer adhesion but may reduce detail.' if profile['material_print_temperature'] > (material_info['temp_range_min'] + material_info['temp_range_max']) / 2 else 'Lower temperatures improve detail but may reduce layer adhesion.'}"
        )
        
        # Speed explanation
        explanations['print_speed'] = (
            f"Print speed of {profile['print_speed']}mm/s "
            f"{'prioritizes quality' if profile['print_speed'] < 50 else ''}"
            f"{'balances quality and speed' if 45 <= profile['print_speed'] <= 55 else ''}"
            f"{'prioritizes faster printing' if profile['print_speed'] > 55 else ''}."
        )
        
        # Support explanation
        if profile['support_enable']:
            explanations['support_enable'] = (
                f"Supports are enabled with a {profile['support_angle']}° threshold "
                f"to ensure proper printing of overhangs."
            )
        else:
            explanations['support_enable'] = (
                "Supports are disabled as they are likely not needed for this model "
                "based on the print purpose."
            )
        
        # Adhesion explanation
        explanations['adhesion_type'] = (
            f"{profile['adhesion_type'].capitalize()} adhesion is recommended "
            f"{'for better bed adhesion with minimal material usage' if profile['adhesion_type'] == 'skirt' else ''}"
            f"{'to prevent warping while maintaining dimensional accuracy' if profile['adhesion_type'] == 'brim' else ''}"
            f"{'to maximize bed adhesion and prevent warping' if profile['adhesion_type'] == 'raft' else ''}."
        )
        
        return explanations
    
    def recommend_setting(
        self,
        setting_name: str,
        printer_id: int,
        material_id: int,
        nozzle_size: float,
        current_settings: Dict[str, Any],
        print_requirements: Dict[str, Any]
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
        # Get printer and material info
        printer_info = self._get_printer_info(printer_id)
        material_info = self._get_material_info(material_id)
        
        # Generate a complete profile to ensure all dependencies are considered
        complete_profile = self.generate_profile(
            printer_id, material_id, nozzle_size, print_requirements
        )
        
        # Extract the recommended value for the specific setting
        recommended_value = complete_profile['settings'].get(setting_name)
        
        if recommended_value is None:
            return {
                'value': None,
                'confidence': 0.0,
                'explanation': f"Setting '{setting_name}' not found or not applicable.",
                'alternatives': []
            }
        
        # Get explanation for the setting
        explanation = complete_profile['explanations'].get(
            setting_name, 
            f"Recommended value based on printer, material, and print requirements."
        )
        
        # Generate alternative values
        alternatives = self._generate_alternatives(
            setting_name, recommended_value, printer_info, material_info, print_requirements
        )
        
        return {
            'value': recommended_value,
            'confidence': 0.85,  # Simplified confidence value
            'explanation': explanation,
            'alternatives': alternatives
        }
    
    def _generate_alternatives(
        self,
        setting_name: str,
        current_value: Any,
        printer_info: Dict[str, Any],
        material_info: Dict[str, Any],
        print_requirements: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate alternative values for a setting with explanations."""
        alternatives = []
        
        # Different alternatives based on setting type
        if setting_name == 'layer_height':
            # Layer height alternatives
            if current_value > 0.12:
                alternatives.append({
                    'value': round(current_value * 0.75, 2),
                    'explanation': "Finer layers for higher quality, but slower printing."
                })
            
            if current_value < 0.28:
                alternatives.append({
                    'value': round(current_value * 1.25, 2),
                    'explanation': "Thicker layers for faster printing, but reduced quality."
                })
        
        elif setting_name == 'infill_density':
            # Infill density alternatives
            if current_value > 15:
                alternatives.append({
                    'value': max(5, current_value - 10),
                    'explanation': "Lower infill density to save material and print time."
                })
            
            if current_value < 50:
                alternatives.append({
                    'value': min(80, current_value + 20),
                    'explanation': "Higher infill density for maximum strength."
                })
        
        elif setting_name == 'infill_pattern':
            # Infill pattern alternatives
            patterns = ['grid', 'triangles', 'cubic', 'gyroid', 'honeycomb']
            current_index = patterns.index(current_value) if current_value in patterns else 0
            
            # Suggest two alternative patterns
            for i in range(1, 3):
                alt_index = (current_index + i) % len(patterns)
                alt_pattern = patterns[alt_index]
                
                if alt_pattern == 'grid':
                    explanation = "Simple pattern, fast printing, moderate strength."
                elif alt_pattern == 'triangles':
                    explanation = "Good strength in all directions, moderate print time."
                elif alt_pattern == 'cubic':
                    explanation = "Excellent strength in all directions, higher print time."
                elif alt_pattern == 'gyroid':
                    explanation = "Excellent strength-to-weight ratio, visually appealing."
                elif alt_pattern == 'honeycomb':
                    explanation = "Maximum strength with higher material usage."
                else:
                    explanation = "Alternative infill pattern."
                
                alternatives.append({
                    'value': alt_pattern,
                    'explanation': explanation
                })
        
        elif setting_name == 'material_print_temperature':
            # Temperature alternatives
            alternatives.append({
                'value': current_value - 5,
                'explanation': "Lower temperature for better detail, but reduced layer adhesion."
            })
            
            alternatives.append({
                'value': current_value + 5,
                'explanation': "Higher temperature for better layer adhesion, but potential stringing."
            })
        
        elif setting_name == 'print_speed':
            # Print speed alternatives
            if current_value > 30:
                alternatives.append({
                    'value': current_value - 10,
                    'explanation': "Slower speed for better quality."
                })
            
            if current_value < 80:
                alternatives.append({
                    'value': current_value + 20,
                    'explanation': "Faster speed to reduce print time."
                })
        
        return alternatives
    
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
            {
                'explanation': str,
                'impact': str,
                'trade_offs': str,
                'related_settings': [str]
            }
        """
        # Get metadata for the setting
        setting_metadata = self.settings_metadata.get(setting_name, {})
        
        # Default explanation if setting not found
        if not setting_metadata:
            return {
                'explanation': f"Setting '{setting_name}' with value {setting_value}.",
                'impact': "Unknown impact.",
                'trade_offs': "Unknown trade-offs.",
                'related_settings': []
            }
        
        # Generate basic explanation based on setting type
        explanation = f"{setting_name} is set to {setting_value}"
        impact = "This setting affects print quality and performance."
        trade_offs = "There are trade-offs between quality, speed, and material usage."
        related_settings = []
        
        # Enhanced explanations for common settings
        if setting_name == 'layer_height':
            explanation = (
                f"Layer height of {setting_value}mm determines the thickness of each printed layer. "
                f"{'This is a very fine layer height for maximum detail.' if setting_value <= 0.1 else ''}"
                f"{'This is a standard layer height balancing detail and speed.' if 0.1 < setting_value <= 0.2 else ''}"
                f"{'This is a coarse layer height for faster printing.' if setting_value > 0.2 else ''}"
            )
            
            impact = (
                "Layer height has a major impact on print quality, detail level, and print time. "
                "It is one of the most important settings in 3D printing."
            )
            
            trade_offs = (
                "Thinner layers provide better detail and surface finish but significantly increase print time. "
                "Thicker layers print faster but show visible layer lines and reduced detail."
            )
            
            related_settings = [
                'initial_layer_height', 
                'line_width', 
                'print_speed',
                'top_layers',
                'bottom_layers'
            ]
        
        elif setting_name == 'print_speed':
            explanation = (
                f"Print speed of {setting_value}mm/s determines how fast the printer moves while extruding. "
                f"{'This is a slow speed prioritizing quality.' if setting_value < 40 else ''}"
                f"{'This is a balanced speed for most prints.' if 40 <= setting_value <= 60 else ''}"
                f"{'This is a fast speed prioritizing print time.' if setting_value > 60 else ''}"
            )
            
            impact = (
                "Print speed affects print time, quality, and potential artifacts. "
                "It must be balanced with other settings like temperature and cooling."
            )
            
            trade_offs = (
                "Faster speeds reduce print time but may introduce artifacts like ringing. "
                "Slower speeds improve quality but significantly increase print time."
            )
            
            related_settings = [
                'outer_wall_speed', 
                'inner_wall_speed', 
                'infill_speed',
                'material_print_temperature',
                'cooling_enable'
            ]
        
        elif setting_name == 'infill_density':
            explanation = (
                f"Infill density of {setting_value}% determines how solid the inside of the print will be. "
                f"{'This is a very low density for minimal material usage.' if setting_value <= 10 else ''}"
                f"{'This is a standard density for general purpose prints.' if 10 < setting_value <= 25 else ''}"
                f"{'This is a high density for stronger parts.' if 25 < setting_value <= 50 else ''}"
                f"{'This is a very high density approaching solid parts.' if setting_value > 50 else ''}"
            )
            
            impact = (
                "Infill density affects strength, weight, material usage, and print time. "
                "It's a key setting for balancing functionality and efficiency."
            )
            
            trade_offs = (
                "Higher infill increases strength but uses more material and takes longer to print. "
                "Lower infill saves material and time but reduces strength."
            )
            
            related_settings = [
                'infill_pattern', 
                'infill_speed', 
                'wall_line_count',
                'top_layers',
                'bottom_layers'
            ]
        
        return {
            'explanation': explanation,
            'impact': impact,
            'trade_offs': trade_offs,
            'related_settings': related_settings
        }
    
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
        # In a real implementation, this would fetch profiles from database
        # For demonstration, create two sample profiles
        profile1 = self._get_default_settings(
            self._get_printer_info(1),
            self._get_material_info(1),
            0.4
        )
        profile1['layer_height'] = 0.16
        profile1['print_speed'] = 50
        profile1['infill_density'] = 20
        
        profile2 = self._get_default_settings(
            self._get_printer_info(1),
            self._get_material_info(1),
            0.4
        )
        profile2['layer_height'] = 0.2
        profile2['print_speed'] = 70
        profile2['infill_density'] = 15
        
        # Find differences between profiles
        differences = []
        for key in profile1.keys():
            if key in profile2 and profile1[key] != profile2[key]:
                explanation = self._explain_difference(key, profile1[key], profile2[key])
                impact = self._assess_impact(key, profile1[key], profile2[key])
                
                differences.append({
                    'setting': key,
                    'value_1': profile1[key],
                    'value_2': profile2[key],
                    'explanation': explanation,
                    'impact': impact
                })
        
        # Estimate differences in print characteristics
        print_time_diff = self._estimate_print_time_difference(profile1, profile2)
        quality_diff = self._estimate_quality_difference(profile1, profile2)
        strength_diff = self._estimate_strength_difference(profile1, profile2)
        
        # Generate summary
        summary = (
            f"Profile 2 is approximately {abs(print_time_diff):.1f}% "
            f"{'faster' if print_time_diff < 0 else 'slower'} than Profile 1. "
            f"Quality is estimated to be {abs(quality_diff):.1f}% "
            f"{'better' if quality_diff > 0 else 'lower'}. "
            f"Strength is approximately {abs(strength_diff):.1f}% "
            f"{'higher' if strength_diff > 0 else 'lower'}."
        )
        
        return {
            'differences': differences,
            'summary': summary,
            'print_time_difference': print_time_diff,
            'quality_difference': quality_diff,
            'strength_difference': strength_diff
        }
    
    def _explain_difference(self, setting: str, value1: Any, value2: Any) -> str:
        """Generate explanation for a difference between two settings."""
        if setting == 'layer_height':
            return (
                f"Layer height changed from {value1}mm to {value2}mm. "
                f"{'Thinner layers provide better detail but slower printing.' if value2 < value1 else 'Thicker layers print faster but with less detail.'}"
            )
        elif setting == 'print_speed':
            return (
                f"Print speed changed from {value1}mm/s to {value2}mm/s. "
                f"{'Slower speeds generally improve quality.' if value2 < value1 else 'Faster speeds reduce print time but may affect quality.'}"
            )
        elif setting == 'infill_density':
            return (
                f"Infill density changed from {value1}% to {value2}%. "
                f"{'Lower density uses less material and prints faster.' if value2 < value1 else 'Higher density creates stronger parts but uses more material.'}"
            )
        elif setting == 'wall_line_count':
            return (
                f"Wall count changed from {value1} to {value2}. "
                f"{'Fewer walls use less material but reduce strength.' if value2 < value1 else 'More walls increase strength and water-tightness.'}"
            )
        else:
            return f"Changed from {value1} to {value2}."
    
    def _assess_impact(self, setting: str, value1: Any, value2: Any) -> str:
        """Assess the impact of a setting change."""
        if setting == 'layer_height':
            pct_change = (value2 - value1) / value1 * 100
            if pct_change > 0:
                return f"Print time reduced by approximately {0.8 * pct_change:.1f}%, quality reduced."
            else:
                return f"Print time increased by approximately {-0.8 * pct_change:.1f}%, quality improved."
        elif setting == 'print_speed':
            pct_change = (value2 - value1) / value1 * 100
            if pct_change > 0:
                return f"Print time reduced by approximately {0.7 * pct_change:.1f}%, may affect quality."
            else:
                return f"Print time increased by approximately {-0.7 * pct_change:.1f}%, quality may improve."
        elif setting == 'infill_density':
            pct_change = (value2 - value1) / value1 * 100
            if pct_change > 0:
                return f"Strength increased by approximately {0.5 * pct_change:.1f}%, material usage increased."
            else:
                return f"Strength reduced by approximately {-0.5 * pct_change:.1f}%, material usage decreased."
        else:
            return "Impact depends on specific print requirements."
    
    def _estimate_print_time_difference(self, profile1: Dict[str, Any], profile2: Dict[str, Any]) -> float:
        """Estimate percentage difference in print time between two profiles."""
        # Simplified estimation based on key factors
        # Negative means profile2 is faster
        
        factors = {
            'layer_height': 0.4,  # 40% impact
            'print_speed': 0.3,   # 30% impact
            'infill_density': 0.15,  # 15% impact
            'wall_line_count': 0.1,  # 10% impact
            'infill_pattern': 0.05   # 5% impact
        }
        
        total_diff = 0
        
        # Layer height (inverse relationship with print time)
        if 'layer_height' in profile1 and 'layer_height' in profile2:
            layer_diff = (profile2['layer_height'] / profile1['layer_height'] - 1) * -100
            total_diff += layer_diff * factors['layer_height']
        
        # Print speed (inverse relationship with print time)
        if 'print_speed' in profile1 and 'print_speed' in profile2:
            speed_diff = (profile2['print_speed'] / profile1['print_speed'] - 1) * -100
            total_diff += speed_diff * factors['print_speed']
        
        # Infill density (direct relationship with print time)
        if 'infill_density' in profile1 and 'infill_density' in profile2:
            infill_diff = (profile2['infill_density'] / profile1['infill_density'] - 1) * 100
            total_diff += infill_diff * factors['infill_density']
        
        # Wall line count (direct relationship with print time)
        if 'wall_line_count' in profile1 and 'wall_line_count' in profile2:
            wall_diff = (profile2['wall_line_count'] / profile1['wall_line_count'] - 1) * 100
            total_diff += wall_diff * factors['wall_line_count']
        
        return total_diff
    
    def _estimate_quality_difference(self, profile1: Dict[str, Any], profile2: Dict[str, Any]) -> float:
        """Estimate percentage difference in quality between two profiles."""
        # Positive means profile2 has better quality
        
        factors = {
            'layer_height': 0.5,  # 50% impact (inverse relationship)
            'print_speed': 0.2,   # 20% impact (inverse relationship)
            'outer_wall_speed': 0.15,  # 15% impact (inverse relationship)
            'wall_line_count': 0.1,  # 10% impact (direct relationship)
            'cooling_enable': 0.05   # 5% impact
        }
        
        total_diff = 0
        
        # Layer height (inverse relationship with quality)
        if 'layer_height' in profile1 and 'layer_height' in profile2:
            layer_diff = (profile1['layer_height'] / profile2['layer_height'] - 1) * 100
            total_diff += layer_diff * factors['layer_height']
        
        # Print speed (inverse relationship with quality)
        if 'print_speed' in profile1 and 'print_speed' in profile2:
            speed_diff = (profile1['print_speed'] / profile2['print_speed'] - 1) * 100
            total_diff += speed_diff * factors['print_speed']
        
        # Outer wall speed (inverse relationship with quality)
        if 'outer_wall_speed' in profile1 and 'outer_wall_speed' in profile2:
            wall_speed_diff = (profile1['outer_wall_speed'] / profile2['outer_wall_speed'] - 1) * 100
            total_diff += wall_speed_diff * factors['outer_wall_speed']
        
        # Wall line count (direct relationship with quality)
        if 'wall_line_count' in profile1 and 'wall_line_count' in profile2:
            wall_diff = (profile2['wall_line_count'] / profile1['wall_line_count'] - 1) * 100
            total_diff += wall_diff * factors['wall_line_count']
        
        return total_diff
    
    def _estimate_strength_difference(self, profile1: Dict[str, Any], profile2: Dict[str, Any]) -> float:
        """Estimate percentage difference in strength between two profiles."""
        # Positive means profile2 is stronger
        
        factors = {
            'infill_density': 0.4,  # 40% impact
            'wall_line_count': 0.3,  # 30% impact
            'layer_height': 0.1,  # 10% impact (smaller layers can be weaker)
            'material_print_temperature': 0.1,  # 10% impact
            'infill_pattern': 0.1   # 10% impact
        }
        
        total_diff = 0
        
        # Infill density (direct relationship with strength)
        if 'infill_density' in profile1 and 'infill_density' in profile2:
            infill_diff = (profile2['infill_density'] / profile1['infill_density'] - 1) * 100
            total_diff += infill_diff * factors['infill_density']
        
        # Wall line count (direct relationship with strength)
        if 'wall_line_count' in profile1 and 'wall_line_count' in profile2:
            wall_diff = (profile2['wall_line_count'] / profile1['wall_line_count'] - 1) * 100
            total_diff += wall_diff * factors['wall_line_count']
        
        # Layer height (smaller layers can be weaker in Z direction)
        if 'layer_height' in profile1 and 'layer_height' in profile2:
            layer_diff = (profile2['layer_height'] / profile1['layer_height'] - 1) * 100
            total_diff += layer_diff * factors['layer_height']
        
        # Material print temperature (higher temp often means better layer adhesion)
        if 'material_print_temperature' in profile1 and 'material_print_temperature' in profile2:
            temp_diff = (profile2['material_print_temperature'] / profile1['material_print_temperature'] - 1) * 100
            total_diff += temp_diff * factors['material_print_temperature']
        
        return total_diff
