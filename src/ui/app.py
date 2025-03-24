"""
Orca Slicer Settings Generator - Web Application
Main Flask application for the web interface
"""

import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

# Import AI and Profile components
from ..ai import AIManager
from ..profiles import ProfileManager

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'data', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize components
data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
ai_manager = AIManager(data_dir=data_dir)
profile_manager = ProfileManager(data_dir=data_dir)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'json', 'ini', 'cfg', 'txt'}

def allowed_file(filename):
    """Check if file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

# Printer profile routes

@app.route('/printers')
def list_printers():
    """List all printer profiles."""
    printers = profile_manager.get_all_printer_profiles()
    return render_template('printers/list.html', printers=printers)

@app.route('/printers/new', methods=['GET', 'POST'])
def new_printer():
    """Create a new printer profile."""
    if request.method == 'POST':
        # Process form data
        name = request.form.get('name')
        vendor = request.form.get('vendor')
        model = request.form.get('model')
        bed_width = float(request.form.get('bed_width', 220))
        bed_depth = float(request.form.get('bed_depth', 220))
        max_height = float(request.form.get('max_height', 250))
        nozzle_diameter = float(request.form.get('nozzle_diameter', 0.4))
        is_direct_drive = request.form.get('is_direct_drive') == 'on'
        printer_type = request.form.get('printer_type', 'cartesian')
        use_klipper = request.form.get('use_klipper') == 'on'
        template_id = request.form.get('template_id')
        
        # Create printer profile
        printer_id = profile_manager.create_printer_profile(
            name=name,
            vendor=vendor,
            model=model,
            bed_size=[bed_width, bed_depth],
            max_height=max_height,
            nozzle_diameter=nozzle_diameter,
            is_direct_drive=is_direct_drive,
            printer_type=printer_type,
            use_klipper=use_klipper,
            template_id=template_id if template_id else None
        )
        
        return redirect(url_for('view_printer', printer_id=printer_id))
    
    # GET request - show form
    templates = profile_manager.get_printer_templates()
    return render_template('printers/new.html', templates=templates)

@app.route('/printers/<printer_id>')
def view_printer(printer_id):
    """View a printer profile."""
    printer = profile_manager.get_printer_profile(printer_id)
    if not printer:
        return render_template('error.html', message="Printer profile not found"), 404
    
    return render_template('printers/view.html', printer=printer)

@app.route('/printers/<printer_id>/edit', methods=['GET', 'POST'])
def edit_printer(printer_id):
    """Edit a printer profile."""
    printer = profile_manager.get_printer_profile(printer_id)
    if not printer:
        return render_template('error.html', message="Printer profile not found"), 404
    
    if request.method == 'POST':
        # Process form data
        printer['name'] = request.form.get('name')
        printer['vendor'] = request.form.get('vendor')
        printer['model'] = request.form.get('model')
        bed_width = float(request.form.get('bed_width', 220))
        bed_depth = float(request.form.get('bed_depth', 220))
        printer['bed_size'] = [bed_width, bed_depth]
        printer['bed_shape'] = [[0, 0], [bed_width, 0], [bed_width, bed_depth], [0, bed_depth]]
        printer['max_print_height'] = float(request.form.get('max_height', 250))
        printer['nozzle_diameter'] = float(request.form.get('nozzle_diameter', 0.4))
        printer['direct_drive'] = request.form.get('is_direct_drive') == 'on'
        printer['printer_type'] = request.form.get('printer_type', 'cartesian')
        printer['use_klipper'] = request.form.get('use_klipper') == 'on'
        
        # Update printer profile
        profile_manager.update_printer_profile(printer_id, printer)
        
        return redirect(url_for('view_printer', printer_id=printer_id))
    
    # GET request - show form
    return render_template('printers/edit.html', printer=printer)

@app.route('/printers/<printer_id>/delete', methods=['POST'])
def delete_printer(printer_id):
    """Delete a printer profile."""
    profile_manager.delete_printer_profile(printer_id)
    return redirect(url_for('list_printers'))

@app.route('/printers/import', methods=['GET', 'POST'])
def import_printer():
    """Import a printer profile from Orca Slicer format."""
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            return render_template('error.html', message="No file part"), 400
        
        file = request.files['file']
        if file.filename == '':
            return render_template('error.html', message="No selected file"), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Import profile
            printer_id = profile_manager.import_profile_from_orca(filepath, 'printer')
            if printer_id:
                return redirect(url_for('view_printer', printer_id=printer_id))
            else:
                return render_template('error.html', message="Failed to import printer profile"), 400
    
    # GET request - show form
    return render_template('printers/import.html')

@app.route('/printers/<printer_id>/export')
def export_printer(printer_id):
    """Export a printer profile to Orca Slicer format."""
    printer = profile_manager.get_printer_profile(printer_id)
    if not printer:
        return render_template('error.html', message="Printer profile not found"), 404
    
    # Create export filename
    filename = f"{printer['vendor']}_{printer['model']}.json"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Export profile
    if profile_manager.export_profile_to_orca(printer_id, 'printer', filepath):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    else:
        return render_template('error.html', message="Failed to export printer profile"), 400

# Material profile routes

@app.route('/materials')
def list_materials():
    """List all material profiles."""
    materials = profile_manager.get_all_material_profiles()
    return render_template('materials/list.html', materials=materials)

@app.route('/materials/new', methods=['GET', 'POST'])
def new_material():
    """Create a new material profile."""
    if request.method == 'POST':
        # Process form data
        name = request.form.get('name')
        vendor = request.form.get('vendor')
        material_type = request.form.get('material_type')
        color = request.form.get('color', '#FFFFFF')
        diameter = float(request.form.get('diameter', 1.75))
        temp_min = float(request.form.get('temp_min', 190))
        temp_max = float(request.form.get('temp_max', 220))
        bed_temp_min = float(request.form.get('bed_temp_min', 50))
        bed_temp_max = float(request.form.get('bed_temp_max', 60))
        template_id = request.form.get('template_id')
        
        # Create material profile
        material_id = profile_manager.create_material_profile(
            name=name,
            vendor=vendor,
            material_type=material_type,
            color=color,
            diameter=diameter,
            temp_range=[temp_min, temp_max],
            bed_temp_range=[bed_temp_min, bed_temp_max],
            template_id=template_id if template_id else None
        )
        
        return redirect(url_for('view_material', material_id=material_id))
    
    # GET request - show form
    templates = profile_manager.get_material_templates()
    return render_template('materials/new.html', templates=templates)

@app.route('/materials/<material_id>')
def view_material(material_id):
    """View a material profile."""
    material = profile_manager.get_material_profile(material_id)
    if not material:
        return render_template('error.html', message="Material profile not found"), 404
    
    return render_template('materials/view.html', material=material)

@app.route('/materials/<material_id>/edit', methods=['GET', 'POST'])
def edit_material(material_id):
    """Edit a material profile."""
    material = profile_manager.get_material_profile(material_id)
    if not material:
        return render_template('error.html', message="Material profile not found"), 404
    
    if request.method == 'POST':
        # Process form data
        material['name'] = request.form.get('name')
        material['vendor'] = request.form.get('vendor')
        material['type'] = request.form.get('material_type')
        material['color'] = request.form.get('color', '#FFFFFF')
        material['diameter'] = float(request.form.get('diameter', 1.75))
        material['temp_range_min'] = float(request.form.get('temp_min', 190))
        material['temp_range_max'] = float(request.form.get('temp_max', 220))
        material['bed_temp_range_min'] = float(request.form.get('bed_temp_min', 50))
        material['bed_temp_range_max'] = float(request.form.get('bed_temp_max', 60))
        
        # Update material profile
        profile_manager.update_material_profile(material_id, material)
        
        return redirect(url_for('view_material', material_id=material_id))
    
    # GET request - show form
    return render_template('materials/edit.html', material=material)

@app.route('/materials/<material_id>/delete', methods=['POST'])
def delete_material(material_id):
    """Delete a material profile."""
    profile_manager.delete_material_profile(material_id)
    return redirect(url_for('list_materials'))

@app.route('/materials/import', methods=['GET', 'POST'])
def import_material():
    """Import a material profile from Orca Slicer format."""
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            return render_template('error.html', message="No file part"), 400
        
        file = request.files['file']
        if file.filename == '':
            return render_template('error.html', message="No selected file"), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Import profile
            material_id = profile_manager.import_profile_from_orca(filepath, 'material')
            if material_id:
                return redirect(url_for('view_material', material_id=material_id))
            else:
                return render_template('error.html', message="Failed to import material profile"), 400
    
    # GET request - show form
    return render_template('materials/import.html')

@app.route('/materials/<material_id>/export')
def export_material(material_id):
    """Export a material profile to Orca Slicer format."""
    material = profile_manager.get_material_profile(material_id)
    if not material:
        return render_template('error.html', message="Material profile not found"), 404
    
    # Create export filename
    filename = f"{material['vendor']}_{material['type']}.json"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Export profile
    if profile_manager.export_profile_to_orca(material_id, 'material', filepath):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    else:
        return render_template('error.html', message="Failed to export material profile"), 400

# Process profile routes

@app.route('/processes')
def list_processes():
    """List all process profiles."""
    processes = profile_manager.get_all_process_profiles()
    return render_template('processes/list.html', processes=processes)

@app.route('/processes/new', methods=['GET', 'POST'])
def new_process():
    """Create a new process profile."""
    if request.method == 'POST':
        # Process form data
        name = request.form.get('name')
        printer_id = request.form.get('printer_id')
        material_id = request.form.get('material_id')
        nozzle_size = float(request.form.get('nozzle_size', 0.4))
        
        # Get print requirements
        print_requirements = {
            'purpose': request.form.get('purpose', 'visual'),
            'surface_quality_importance': int(request.form.get('quality_importance', 3)),
            'strength_importance': int(request.form.get('strength_importance', 3)),
            'speed_importance': int(request.form.get('speed_importance', 3)),
            'material_usage_importance': int(request.form.get('material_importance', 3))
        }
        
        # Generate process profile
        process_id = profile_manager.generate_process_profile(
            name=name,
            printer_id=printer_id,
            material_id=material_id,
            nozzle_size=nozzle_size,
            print_requirements=print_requirements
        )
        
        return redirect(url_for('view_process', process_id=process_id))
    
    # GET request - show form
    printers = profile_manager.get_all_printer_profiles()
    materials = profile_manager.get_all_material_profiles()
    return render_template('processes/new.html', printers=printers, materials=materials)

@app.route('/processes/<process_id>')
def view_process(process_id):
    """View a process profile."""
    process = profile_manager.get_process_profile(process_id)
    if not process:
        return render_template('error.html', message="Process profile not found"), 404
    
    # Get related printer and material
    printer = profile_manager.get_printer_profile(process.get('printer_id', ''))
    material = profile_manager.get_material_profile(process.get('material_id', ''))
    
    return render_template('processes/view.html', process=process, printer=printer, material=material)

@app.route('/processes/<process_id>/optimize', methods=['GET', 'POST'])
def optimize_process(process_id):
    """Optimize a process profile."""
    process = profile_manager.get_process_profile(process_id)
    if not process:
        return render_template('error.html', message="Process profile not found"), 404
    
    if request.method == 'POST':
        # Get print requirements
        print_requirements = {
            'purpose': request.form.get('purpose', 'visual'),
            'surface_quality_importance': int(request.form.get('quality_importance', 3)),
            'strength_importance': int(request.form.get('strength_importance', 3)),
            'speed_importance': int(request.form.get('speed_importance', 3)),
            'material_usage_importance': int(request.form.get('material_importance', 3))
        }
        
        # Optimize process profile
        new_process_id = profile_manager.optimize_process_profile(process_id, print_requirements)
        
        return redirect(url_for('view_process', process_id=new_process_id))
    
    # GET request - show form
    return render_template('processes/optimize.html', process=process)

@app.route('/processes/<process_id>/delete', methods=['POST'])
def delete_process(process_id):
    """Delete a process profile."""
    profile_manager.delete_process_profile(process_id)
    return redirect(url_for('list_processes'))

@app.route('/processes/import', methods=['GET', 'POST'])
def import_process():
    """Import a process profile from Orca Slicer format."""
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            return render_template('error.html', message="No file part"), 400
        
        file = request.files['file']
        if file.filename == '':
            return render_template('error.html', message="No selected file"), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Import profile
            process_id = profile_manager.import_profile_from_orca(filepath, 'process')
            if process_id:
                return redirect(url_for('view_process', process_id=process_id))
            else:
                return render_template('error.html', message="Failed to import process profile"), 400
    
    # GET request - show form
    return render_template('processes/import.html')

@app.route('/processes/<process_id>/export')
def export_process(process_id):
    """Export a process profile to Orca Slicer format."""
    process = profile_manager.get_process_profile(process_id)
    if not process:
        return render_template('error.html', message="Process profile not found"), 404
    
    # Create export filename
    filename = f"{process['name'].replace(' ', '_')}.json"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Export profile
    if profile_manager.export_profile_to_orca(process_id, 'process', filepath):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    else:
        return render_template('error.html', message="Failed to export process profile"), 400

@app.route('/processes/compare', methods=['GET', 'POST'])
def compare_processes():
    """Compare two process profiles."""
    if request.method == 'POST':
        process_id_1 = request.form.get('process_id_1')
        process_id_2 = request.form.get('process_id_2')
        
        # Compare profiles
        comparison = profile_manager.compare_process_profiles(process_id_1, process_id_2)
        
        # Get process profiles
        process_1 = profile_manager.get_process_profile(process_id_1)
        process_2 = profile_manager.get_process_profile(process_id_2)
        
        return render_template('processes/comparison.html', 
                              comparison=comparison, 
                              process_1=process_1, 
                              process_2=process_2)
    
    # GET request - show form
    processes = profile_manager.get_all_process_profiles()
    return render_template('processes/compare.html', processes=processes)

# Settings recommendation routes

@app.route('/recommend')
def recommend_settings():
    """Recommend settings based on printer and material."""
    printers = profile_manager.get_all_printer_profiles()
    materials = profile_manager.get_all_material_profiles()
    return render_template('recommend/index.html', printers=printers, materials=materials)

@app.route('/recommend/result', methods=['POST'])
def recommend_result():
    """Show recommended settings."""
    printer_id = request.form.get('printer_id')
    material_id = request.form.get('material_id')
    nozzle_size = float(request.form.get('nozzle_size', 0.4))
    
    # Get print requirements
    print_requirements = {
        'purpose': request.form.get('purpose', 'visual'),
        'surface_quality_importance': int(request.form.get('quality_importance', 3)),
        'strength_importance': int(request.form.get('strength_importance', 3)),
        'speed_importance': int(request.form.get('speed_importance', 3)),
        'material_usage_importance': int(request.form.get('material_importance', 3))
    }
    
    # Generate process profile
    process_id = profile_manager.generate_process_profile(
        name="Recommended Settings",
        printer_id=printer_id,
        material_id=material_id,
        nozzle_size=nozzle_size,
        print_requirements=print_requirements
    )
    
    return redirect(url_for('view_process', process_id=process_id))

# Help and information routes

@app.route('/help')
def help_index():
    """Show help index."""
    return render_template('help/index.html')

@app.route('/help/settings')
def help_settings():
    """Show settings help."""
    return render_template('help/settings.html')

@app.route('/help/klipper')
def help_klipper():
    """Show Klipper help."""
    return render_template('help/klipper.html')

@app.route('/help/printing')
def help_printing():
    """Show 3D printing help."""
    return render_template('help/printing.html')

@app.route('/help/about')
def help_about():
    """Show about page."""
    return render_template('help/about.html')

# API routes for AJAX calls

@app.route('/api/setting/explain', methods=['POST'])
def api_explain_setting():
    """Explain a setting value."""
    data = request.json
    setting_name = data.get('setting_name')
    setting_value = data.get('setting_value')
    context = data.get('context', {})
    
    explanation = ai_manager.explain_setting(setting_name, setting_value, context)
    return jsonify(explanation)

@app.route('/api/printer/templates', methods=['GET'])
def api_printer_templates():
    """Get printer templates."""
    templates = profile_manager.get_printer_templates()
    return jsonify(templates)

@app.route('/api/material/templates', methods=['GET'])
def api_material_templates():
    """Get material templates."""
    templates = profile_manager.get_material_templates()
    return jsonify(templates)

@app.route('/api/process/templates', methods=['GET'])
def api_process_templates():
    """Get process templates."""
    templates = profile_manager.get_process_templates()
    return jsonify(templates)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
