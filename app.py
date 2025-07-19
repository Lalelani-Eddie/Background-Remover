from flask import Flask, render_template, request, send_file, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import io
import base64
from PIL import Image
from rembg import remove, new_session
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Configuration
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Create directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Initialize different models
models = {
    'general': new_session('u2net'),
    'high_quality': new_session('isnet-general-use'),
    'human': new_session('silueta'),
    'light': new_session('u2netp')
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image(file_path, model='general'):
    """Process image and return base64 encoded result"""
    try:
        with open(file_path, 'rb') as input_file:
            input_data = input_file.read()
        
        # Remove background
        output_data = remove(input_data, session=models[model])
        
        # Convert to base64 for web display
        output_base64 = base64.b64encode(output_data).decode('utf-8')
        
        # Save processed file
        unique_id = str(uuid.uuid4())
        processed_filename = f"{unique_id}.png"
        processed_path = os.path.join(PROCESSED_FOLDER, processed_filename)
        
        with open(processed_path, 'wb') as output_file:
            output_file.write(output_data)
        
        return output_base64, processed_filename
    
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return None, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    
    file = request.files['file']
    model = request.form.get('model', 'general')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': 'File too large. Maximum size is 16MB'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(file_path)
        
        # Process image
        result_base64, processed_filename = process_image(file_path, model)
        
        # Clean up uploaded file
        os.remove(file_path)
        
        if result_base64:
            return jsonify({
                'success': True,
                'result_image': f"data:image/png;base64,{result_base64}",
                'download_filename': processed_filename
            })
        else:
            return jsonify({'error': 'Failed to process image'}), 500
    
    return jsonify({'error': 'Invalid file format'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    """Download processed image"""
    file_path = os.path.join(PROCESSED_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name=f"no_background_{filename}")
    return "File not found", 404

@app.route('/api/models')
def get_models():
    """Return available models"""
    return jsonify({
        'models': [
            {'value': 'general', 'name': 'General Use (U2-Net)'},
            {'value': 'high_quality', 'name': 'High Quality (IS-Net)'},
            {'value': 'human', 'name': 'Human Portraits (Silueta)'},
            {'value': 'light', 'name': 'Lightweight (U2-Net-P)'}
        ]
    })

# Cleanup old files (run periodically)
def cleanup_old_files():
    """Remove files older than 1 hour"""
    import time
    current_time = time.time()
    
    for folder in [UPLOAD_FOLDER, PROCESSED_FOLDER]:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.getctime(file_path) < current_time - 3600:  # 1 hour
                os.remove(file_path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)