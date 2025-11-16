#!/usr/bin/env python3
"""
🩺 Auto-Healing Upload Test Server
Simple test server to validate the healing upload functionality
"""

from flask import Flask, request, jsonify, render_template
import os
import json
import uuid
import hashlib
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1GB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload_chunk', methods=['POST'])
def upload_chunk():
    """Handle chunked file uploads with healing magic"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'})
        
        file = request.files['file']
        chunk_number = int(request.form.get('chunk_number', 0))
        total_chunks = int(request.form.get('total_chunks', 1))
        upload_id = request.form.get('upload_id')
        checksum = request.form.get('checksum')
        chunk_size = int(request.form.get('chunk_size', 0))
        
        if not upload_id:
            return jsonify({'success': False, 'error': 'No upload ID provided'})
        
        # Create upload directory
        upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], upload_id)
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save chunk
        chunk_path = os.path.join(upload_dir, f'chunk_{chunk_number:06d}')
        file.save(chunk_path)
        
        # Verify chunk checksum
        if checksum:
            with open(chunk_path, 'rb') as f:
                chunk_data = f.read()
                calculated_checksum = hashlib.md5(chunk_data).hexdigest()
                
                if calculated_checksum != checksum:
                    os.remove(chunk_path)  # Remove corrupted chunk
                    return jsonify({
                        'success': False, 
                        'error': 'Chunk corruption detected',
                        'expected_checksum': checksum,
                        'actual_checksum': calculated_checksum
                    })
        
        # Save metadata
        metadata_path = os.path.join(upload_dir, 'metadata.json')
        metadata = {}
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
        
        metadata.update({
            'upload_id': upload_id,
            'total_chunks': total_chunks,
            'last_chunk': chunk_number,
            'timestamp': datetime.now().isoformat(),
            f'chunk_{chunk_number}': {
                'checksum': checksum,
                'size': chunk_size,
                'uploaded_at': datetime.now().isoformat()
            }
        })
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Chunk {chunk_number}/{total_chunks-1} uploaded for {upload_id}")
        
        return jsonify({
            'success': True,
            'chunk_number': chunk_number,
            'checksum': calculated_checksum if checksum else None,
            'message': f'Chunk {chunk_number} uploaded successfully'
        })
        
    except Exception as e:
        print(f"💔 Upload chunk error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/check_chunks/<upload_id>')
def check_chunks(upload_id):
    """Check which chunks already exist for an upload"""
    try:
        upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], upload_id)
        
        if not os.path.exists(upload_dir):
            return jsonify({'success': True, 'existing_chunks': []})
        
        # Find existing chunk files
        existing_chunks = []
        for filename in os.listdir(upload_dir):
            if filename.startswith('chunk_'):
                try:
                    chunk_number = int(filename.split('_')[1])
                    existing_chunks.append(chunk_number)
                except ValueError:
                    continue
        
        existing_chunks.sort()
        
        print(f"🔍 Found {len(existing_chunks)} existing chunks for {upload_id}")
        
        return jsonify({
            'success': True,
            'existing_chunks': existing_chunks
        })
        
    except Exception as e:
        print(f"💔 Check chunks error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/complete_upload/<upload_id>')
def complete_upload(upload_id):
    """Complete a chunked upload by assembling chunks"""
    try:
        upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], upload_id)
        
        if not os.path.exists(upload_dir):
            return jsonify({'success': False, 'error': 'Upload not found'})
        
        # Load metadata
        metadata_path = os.path.join(upload_dir, 'metadata.json')
        if not os.path.exists(metadata_path):
            return jsonify({'success': False, 'error': 'Upload metadata not found'})
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        total_chunks = metadata.get('total_chunks', 0)
        
        # Check if all chunks exist
        missing_chunks = []
        for i in range(total_chunks):
            chunk_path = os.path.join(upload_dir, f'chunk_{i:06d}')
            if not os.path.exists(chunk_path):
                missing_chunks.append(i)
        
        if missing_chunks:
            return jsonify({
                'success': False,
                'error': f'Missing chunks: {missing_chunks}',
                'missing_chunks': missing_chunks
            })
        
        # Assemble file (in a real app, you'd do this properly)
        print(f"🎉 Upload {upload_id} completed with {total_chunks} chunks!")
        
        return jsonify({
            'success': True,
            'message': f'Upload completed successfully with {total_chunks} chunks',
            'upload_id': upload_id
        })
        
    except Exception as e:
        print(f"💔 Complete upload error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/dashboard')
def dashboard():
    """Simple dashboard for testing"""
    return f"""
    <h1>🎉 Healing Upload Test Complete!</h1>
    <p>Your files have been uploaded with healing magic!</p>
    <p><a href="/">Upload More Files</a></p>
    """

if __name__ == '__main__':
    print("🩺 Starting Auto-Healing Upload Test Server...")
    print("📡 Server will be available at: http://localhost:5000")
    print("🔧 Upload endpoint: /upload_chunk")
    print("🔍 Check chunks: /check_chunks/<upload_id>")
    print("✅ Complete upload: /complete_upload/<upload_id>")
    
    app.run(debug=True, host='0.0.0.0', port=5000)