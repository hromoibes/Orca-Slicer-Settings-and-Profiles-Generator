"""
Orca Slicer Settings Generator - Profile Models
Database models for printer and filament profiles
"""

import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union

class ProfileDatabase:
    """
    Database for storing and retrieving printer and filament profiles.
    
    This class manages the storage and retrieval of profiles in a JSON-based
    database structure, with support for importing and exporting Orca Slicer
    compatible profile formats.
    """
    
    def __init__(self, data_dir: str = None):
        """
        Initialize the profile database.
        
        Args:
            data_dir: Directory for storing profile data
        """
        self.data_dir = data_dir or os.path.join(os.path.dirname(__file__), '..', 'data')
        
        # Ensure data directories exist
        self.printer_dir = os.path.join(self.data_dir, 'printers')
        self.material_dir = os.path.join(self.data_dir, 'materials')
        self.process_dir = os.path.join(self.data_dir, 'processes')
        
        os.makedirs(self.printer_dir, exist_ok=True)
        os.makedirs(self.material_dir, exist_ok=True)
        os.makedirs(self.process_dir, exist_ok=True)
        
        # Initialize database files
        self.printer_db_file = os.path.join(self.data_dir, 'printers.json')
        self.material_db_file = os.path.join(self.data_dir, 'materials.json')
        self.process_db_file = os.path.join(self.data_dir, 'processes.json')
        
        # Load or initialize databases
        self.printers = self._load_database(self.printer_db_file, 'printers')
        self.materials = self._load_database(self.material_db_file, 'materials')
        self.processes = self._load_database(self.process_db_file, 'processes')
    
    def _load_database(self, db_file: str, db_type: str) -> Dict[str, Any]:
        """
        Load database from file or initialize if not exists.
        
        Args:
            db_file: Path to database file
            db_type: Type of database ('printers', 'materials', or 'processes')
            
        Returns:
            Database dictionary
        """
        if os.path.exists(db_file):
            try:
                with open(db_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading {db_type} database: {e}")
        
        # Initialize empty database
        return {
            'version': '1.0.0',
            'last_updated': datetime.now().isoformat(),
            'items': {}
        }
    
    def _save_database(self, db_file: str, db_data: Dict[str, Any]) -> bool:
        """
        Save database to file.
        
        Args:
            db_file: Path to database file
            db_data: Database dictionary
            
        Returns:
            Success status
        """
        try:
            # Update last updated timestamp
            db_data['last_updated'] = datetime.now().isoformat()
            
            # Ensure items key exists
            if 'items' not in db_data:
                db_data['items'] = {}
                
            with open(db_file, 'w') as f:
                json.dump(db_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving database: {e}")
            return False
    
    def save_all(self) -> bool:
        """
        Save all databases to files.
        
        Returns:
            Success status
        """
        printer_success = self._save_database(self.printer_db_file, self.printers)
        material_success = self._save_database(self.material_db_file, self.materials)
        process_success = self._save_database(self.process_db_file, self.processes)
        
        return printer_success and material_success and process_success
    
    # Printer profile methods
    
    def add_printer(self, printer_data: Dict[str, Any]) -> str:
        """
        Add a new printer profile.
        
        Args:
            printer_data: Printer profile data
            
        Returns:
            ID of the new printer profile
        """
        # Generate unique ID if not provided
        printer_id = printer_data.get('id', str(uuid.uuid4()))
        
        # Add metadata
        printer_data['id'] = printer_id
        printer_data['created'] = datetime.now().isoformat()
        printer_data['modified'] = printer_data['created']
        
        # Add to database
        # Fix: Initialize items if not present
        if 'items' not in self.printers:
            self.printers['items'] = {}
            
        self.printers['items'][printer_id] = printer_data
        self._save_database(self.printer_db_file, self.printers)
        
        # Save printer-specific file
        printer_file = os.path.join(self.printer_dir, f"{printer_id}.json")
        with open(printer_file, 'w') as f:
            json.dump(printer_data, f, indent=2)
        
        return printer_id
    
    def update_printer(self, printer_id: str, printer_data: Dict[str, Any]) -> bool:
        """
        Update an existing printer profile.
        
        Args:
            printer_id: ID of the printer profile to update
            printer_data: Updated printer profile data
            
        Returns:
            Success status
        """
        # Fix: Initialize items if not present
        if 'items' not in self.printers:
            self.printers['items'] = {}
            
        if printer_id not in self.printers['items']:
            return False
        
        # Preserve creation date
        created = self.printers['items'][printer_id].get('created', datetime.now().isoformat())
        
        # Update metadata
        printer_data['id'] = printer_id
        printer_data['created'] = created
        printer_data['modified'] = datetime.now().isoformat()
        
        # Update in database
        self.printers['items'][printer_id] = printer_data
        self._save_database(self.printer_db_file, self.printers)
        
        # Update printer-specific file
        printer_file = os.path.join(self.printer_dir, f"{printer_id}.json")
        with open(printer_file, 'w') as f:
            json.dump(printer_data, f, indent=2)
        
        return True
    
    def get_printer(self, printer_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a printer profile by ID.
        
        Args:
            printer_id: ID of the printer profile
            
        Returns:
            Printer profile data or None if not found
        """
        # Fix: Initialize items if not present
        if 'items' not in self.printers:
            self.printers['items'] = {}
            
        return self.printers['items'].get(printer_id)
    
    def get_all_printers(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all printer profiles.
        
        Returns:
            Dictionary of printer profiles
        """
        # Fix: Initialize items if not present
        if 'items' not in self.printers:
            self.printers['items'] = {}
            
        return self.printers['items']
    
    def delete_printer(self, printer_id: str) -> bool:
        """
        Delete a printer profile.
        
        Args:
            printer_id: ID of the printer profile to delete
            
        Returns:
            Success status
        """
        # Fix: Initialize items if not present
        if 'items' not in self.printers:
            self.printers['items'] = {}
            
        if printer_id not in self.printers['items']:
            return False
        
        # Remove from database
        del self.printers['items'][printer_id]
        self._save_database(self.printer_db_file, self.printers)
        
        # Remove printer-specific file
        printer_file = os.path.join(self.printer_dir, f"{printer_id}.json")
        if os.path.exists(printer_file):
            os.remove(printer_file)
        
        return True
    
    # Material profile methods
    
    def add_material(self, material_data: Dict[str, Any]) -> str:
        """
        Add a new material profile.
        
        Args:
            material_data: Material profile data
            
        Returns:
            ID of the new material profile
        """
        # Generate unique ID if not provided
        material_id = material_data.get('id', str(uuid.uuid4()))
        
        # Add metadata
        material_data['id'] = material_id
        material_data['created'] = datetime.now().isoformat()
        material_data['modified'] = material_data['created']
        
        # Add to database
        # Fix: Initialize items if not present
        if 'items' not in self.materials:
            self.materials['items'] = {}
            
        self.materials['items'][material_id] = material_data
        self._save_database(self.material_db_file, self.materials)
        
        # Save material-specific file
        material_file = os.path.join(self.material_dir, f"{material_id}.json")
        with open(material_file, 'w') as f:
            json.dump(material_data, f, indent=2)
        
        return material_id
    
    def update_material(self, material_id: str, material_data: Dict[str, Any]) -> bool:
        """
        Update an existing material profile.
        
        Args:
            material_id: ID of the material profile to update
            material_data: Updated material profile data
            
        Returns:
            Success status
        """
        # Fix: Initialize items if not present
        if 'items' not in self.materials:
            self.materials['items'] = {}
            
        if material_id not in self.materials['items']:
            return False
        
        # Preserve creation date
        created = self.materials['items'][material_id].get('created', datetime.now().isoformat())
        
        # Update metadata
        material_data['id'] = material_id
        material_data['created'] = created
        material_data['modified'] = datetime.now().isoformat()
        
        # Update in database
        self.materials['items'][material_id] = material_data
        self._save_database(self.material_db_file, self.materials)
        
        # Update material-specific file
        material_file = os.path.join(self.material_dir, f"{material_id}.json")
        with open(material_file, 'w') as f:
            json.dump(material_data, f, indent=2)
        
        return True
    
    def get_material(self, material_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a material profile by ID.
        
        Args:
            material_id: ID of the material profile
            
        Returns:
            Material profile data or None if not found
        """
        # Fix: Initialize items if not present
        if 'items' not in self.materials:
            self.materials['items'] = {}
            
        return self.materials['items'].get(material_id)
    
    def get_all_materials(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all material profiles.
        
        Returns:
            Dictionary of material profiles
        """
        # Fix: Initialize items if not present
        if 'items' not in self.materials:
            self.materials['items'] = {}
            
        return self.materials['items']
    
    def delete_material(self, material_id: str) -> bool:
        """
        Delete a material profile.
        
        Args:
            material_id: ID of the material profile to delete
            
        Returns:
            Success status
        """
        # Fix: Initialize items if not present
        if 'items' not in self.materials:
            self.materials['items'] = {}
            
        if material_id not in self.materials['items']:
            return False
        
        # Remove from database
        del self.materials['items'][material_id]
        self._save_database(self.material_db_file, self.materials)
        
        # Remove material-specific file
        material_file = os.path.join(self.material_dir, f"{material_id}.json")
        if os.path.exists(material_file):
            os.remove(material_file)
        
        return True
    
    # Process profile methods
    
    def add_process(self, process_data: Dict[str, Any]) -> str:
        """
        Add a new process profile.
        
        Args:
            process_data: Process profile data
            
        Returns:
            ID of the new process profile
        """
        # Generate unique ID if not provided
        process_id = process_data.get('id', str(uuid.uuid4()))
        
        # Add metadata
        process_data['id'] = process_id
        process_data['created'] = datetime.now().isoformat()
        process_data['modified'] = process_data['created']
        
        # Add to database
        # Fix: Initialize items if not present
        if 'items' not in self.processes:
            self.processes['items'] = {}
            
        self.processes['items'][process_id] = process_data
        self._save_database(self.process_db_file, self.processes)
        
        # Save process-specific file
        process_file = os.path.join(self.process_dir, f"{process_id}.json")
        with open(process_file, 'w') as f:
            json.dump(process_data, f, indent=2)
        
        return process_id
    
    def update_process(self, process_id: str, process_data: Dict[str, Any]) -> bool:
        """
        Update an existing process profile.
        
        Args:
            process_id: ID of the process profile to update
            process_data: Updated process profile data
            
        Returns:
            Success status
        """
        # Fix: Initialize items if not present
        if 'items' not in self.processes:
            self.processes['items'] = {}
            
        if process_id not in self.processes['items']:
            return False
        
        # Preserve creation date
        created = self.processes['items'][process_id].get('created', datetime.now().isoformat())
        
        # Update metadata
        process_data['id'] = process_id
        process_data['created'] = created
        process_data['modified'] = datetime.now().isoformat()
        
        # Update in database
        self.processes['items'][process_id] = process_data
        self._save_database(self.process_db_file, self.processes)
        
        # Update process-specific file
        process_file = os.path.join(self.process_dir, f"{process_id}.json")
        with open(process_file, 'w') as f:
            json.dump(process_data, f, indent=2)
        
        return True
    
    def get_process(self, process_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a process profile by ID.
        
        Args:
            process_id: ID of the process profile
            
        Returns:
            Process profile data or None if not found
        """
        # Fix: Initialize items if not present
        if 'items' not in self.processes:
            self.processes['items'] = {}
            
        return self.processes['items'].get(process_id)
    
    def get_all_processes(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all process profiles.
        
        Returns:
            Dictionary of process profiles
        """
        # Fix: Initialize items if not present
        if 'items' not in self.processes:
            self.processes['items'] = {}
            
        return self.processes['items']
    
    def delete_process(self, process_id: str) -> bool:
        """
        Delete a process profile.
        
        Args:
            process_id: ID of the process profile to delete
            
        Returns:
            Success status
        """
        # Fix: Initialize items if not present
        if 'items' not in self.processes:
            self.processes['items'] = {}
            
        if process_id not in self.processes['items']:
            return False
        
        # Remove from database
        del self.processes['items'][process_id]
        self._save_database(self.process_db_file, self.processes)
        
        # Remove process-specific file
        process_file = os.path.join(self.process_dir, f"{process_id}.json")
        if os.path.exists(process_file):
            os.remove(process_file)
        
        return True
