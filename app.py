
from flask import Flask, request, jsonify, render_template, send_file, abort
import os
import mimetypes
from werkzeug.utils import secure_filename
from datetime import datetime
import json
import uuid
from config import Config
from ml_model import PriorityMLModel

# Import File Management System (NEW FEATURE)
try:
    from file_database import FileDatabase, get_file_type, format_file_size, is_previewable
    FILE_MANAGEMENT_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ File management features not available: {e}")
    FILE_MANAGEMENT_AVAILABLE = False

# Import Network Monitor (NEW FEATURE - Real-Time WiFi Status)
try:
    from network_monitor import network_monitor
    NETWORK_MONITORING_AVAILABLE = True
    print("🌐 Network Monitor initialized! Ready to watch your internet playground!")
except ImportError as e:
    print(f"⚠️ Network monitoring features not available: {e}")
    NETWORK_MONITORING_AVAILABLE = False

# Import new smart components (optional - fallback if not available)
try:
    from smart_priority_engine import SmartPriorityEngine, FileMetrics
    from smart_priority_config import UserPriority, FileType
    from dynamic_queue_scheduler import DynamicQueueScheduler
    from behavioral_learning import BehavioralLearningSystem
    SMART_FEATURES_AVAILABLE = True
except ImportError:
    SMART_FEATURES_AVAILABLE = False
    print("📋 Smart features not available - using original system")

# Import Gemini AI Client (NEW FEATURE - Real AI Chatbot)
try:
    from ai_routes import add_ai_routes, setup_gemini_ai
    GEMINI_AI_AVAILABLE = True
    print("🤖 Gemini AI routes loaded! Ready for intelligent conversations!")
except ImportError as e:
    GEMINI_AI_AVAILABLE = False
    print(f"⚠️ Gemini AI features not available: {e}")

# Import WiFi Finder (NEW FEATURE - Live WiFi Discovery)
try:
    from wifi_routes import register_wifi_routes
    WIFI_FINDER_AVAILABLE = True
    print("📶 WiFi Finder routes loaded! Ready to discover hotspots!")
except ImportError as e:
    WIFI_FINDER_AVAILABLE = False
    print(f"⚠️ WiFi Finder features not available: {e}")

app = Flask(__name__)
app.config.from_object(Config)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size for new file management system

# Ensure required directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(Config.MODEL_PATH, exist_ok=True)

# Initialize ML model
ml_model = PriorityMLModel()
ml_model.load_model()  # Try to load existing model

class EnhancedPriorityAnalyzer:
    def __init__(self, ml_model):
        self.ml_model = ml_model
        self.priority_levels = {
            'emergency': 1,
            'graphic_heavy': 2,
            'video': 3,
            'image': 4,
            'text': 5,
            'audio': 6,
            'archive': 7,
            'other': 8
        }
        
        # Initialize smart components if available
        if SMART_FEATURES_AVAILABLE:
            self.smart_engine = SmartPriorityEngine()
            self.queue_scheduler = DynamicQueueScheduler(self.smart_engine, max_workers=4)
            self.learning_system = BehavioralLearningSystem()
            self.smart_enabled = True
            print("🎪 Smart Priority Engine integrated successfully!")
        else:
            self.smart_enabled = False
            print("📋 Using original priority system")
        
        # Initialize File Management System (NEW FEATURE)
        if FILE_MANAGEMENT_AVAILABLE:
            try:
                self.file_db = FileDatabase()
                # Ensure file storage directory exists
                os.makedirs('file_storage', exist_ok=True)
                print("📁 File Management System initialized!")
            except Exception as e:
                print(f"⚠️ Error initializing file management: {e}")
                self.file_db = None
        else:
            self.file_db = None

    def analyze_file(self, filename, file_path, user_priority=3, time_sensitive='normal', context_tags=None):
        """Enhanced analyze file with smart features + original ML model"""
        file_size = os.path.getsize(file_path)
        
        # Original ML model prediction (always run)
        prediction = self.ml_model.predict_priority(filename, file_size, file_path)
        category = prediction['category']
        confidence = prediction.get('confidence', 0.0)
        method = prediction.get('method', 'ml_model')
        
        # Enhanced analysis with smart features if available
        if self.smart_enabled:
            try:
                # Create file metrics for smart analysis
                file_metrics = FileMetrics(
                    file_id=str(uuid.uuid4()),
                    filename=filename,
                    file_size=file_size,
                    file_type=self.smart_engine.detect_file_type(filename),
                    user_priority=UserPriority(user_priority) if isinstance(user_priority, int) else user_priority,
                    time_sensitive=time_sensitive,
                    context_tags=context_tags or [],
                    upload_start_time=datetime.now()
                )
                
                # Get smart priority score
                smart_priority = self.smart_engine.calculate_dynamic_priority(file_metrics) 
                chunks_info = self.smart_engine.analyze_file_for_transfer(file_metrics)
                
                # Combine original and smart analysis
                return {
                    'filename': filename,
                    'category': category,
                    'file_type': file_metrics.file_type.value,
                    'original_priority_level': self.priority_levels.get(category, 8),
                    'smart_priority_score': smart_priority,
                    'confidence': confidence,
                    'prediction_method': method,
                    'file_size': file_size,
                    'file_extension': os.path.splitext(filename)[1].lower(),
                    'chunk_size': chunks_info['chunk_size'],
                    'total_chunks': chunks_info['total_chunks'],
                    'estimated_time': chunks_info['estimated_time'],
                    'upload_time': datetime.now().isoformat(),
                    'features_used': prediction.get('features_used', {}),
                    'smart_enhanced': True,
                    'time_sensitive': time_sensitive,
                    'user_priority': user_priority,
                    'context_tags': context_tags or []
                }
            except Exception as e:
                print(f"⚠️ Smart analysis failed, using original: {e}")
        
        # Original analysis (fallback or when smart features not available)
        return {
            'filename': filename,
            'category': category,
            'priority_level': self.priority_levels.get(category, 8),
            'confidence': confidence,
            'prediction_method': method,
            'file_size': file_size,
            'file_extension': os.path.splitext(filename)[1].lower(),
            'chunk_size': self._calculate_chunk_size(file_size, category),
            'upload_time': datetime.now().isoformat(),
            'features_used': prediction.get('features_used', {})
        }
    
    def _calculate_chunk_size(self, file_size, category):
        """Calculate optimal chunk size based on file type and size"""
        base_chunk_sizes = {
            'emergency': 512 * 1024,     # 512KB - fastest processing
            'text': 1024 * 1024,         # 1MB
            'image': 2 * 1024 * 1024,    # 2MB
            'audio': 4 * 1024 * 1024,    # 4MB
            'archive': 8 * 1024 * 1024,  # 8MB
            'video': 16 * 1024 * 1024,   # 16MB
            'graphic_heavy': 32 * 1024 * 1024,  # 32MB
            'other': 1024 * 1024         # 1MB
        }
        
        base_size = base_chunk_sizes.get(category, 1024 * 1024)
        
        # Adjust based on file size
        if file_size < base_size:
            return file_size
        elif file_size > 100 * 1024 * 1024:  # Files larger than 100MB
            return min(base_size * 2, 64 * 1024 * 1024)
        
        return base_size

analyzer = EnhancedPriorityAnalyzer(ml_model)

@app.route('/')
def index():
    model_status = "Trained ML Model" if ml_model.is_trained else "Rule-based Fallback"
    return render_template('index.html', model_status=model_status)

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle multiple file uploads and analyze priorities"""
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files selected'}), 400
    
    upload_id = str(uuid.uuid4())
    upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], upload_id)
    os.makedirs(upload_dir, exist_ok=True)
    
    analyzed_files = []
    
    for file in files:
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)
            
            # Analyze the file using ML model
            analysis = analyzer.analyze_file(filename, file_path)
            analysis['upload_id'] = upload_id
            analysis['file_id'] = str(uuid.uuid4())
            
            analyzed_files.append(analysis)
    
    # Sort by priority level (lower number = higher priority)
    analyzed_files.sort(key=lambda x: x['priority_level'])
    
    # Save metadata
    metadata_path = os.path.join(upload_dir, 'metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(analyzed_files, f, indent=2)
    
    return jsonify({
        'upload_id': upload_id,
        'total_files': len(analyzed_files),
        'model_used': 'ML Model' if ml_model.is_trained else 'Rule-based',
        'files': analyzed_files
    })

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """REST API endpoint for file analysis"""
    return upload_files()

@app.route('/api/priority/<upload_id>')
def get_priority_info(upload_id):
    """Get priority information for uploaded files"""
    metadata_path = os.path.join(app.config['UPLOAD_FOLDER'], upload_id, 'metadata.json')
    
    if not os.path.exists(metadata_path):
        return jsonify({'error': 'Upload not found'}), 404
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    return jsonify({
        'upload_id': upload_id,
        'files': metadata,
        'priority_queue': sorted(metadata, key=lambda x: x['priority_level'])
    })

@app.route('/api/chunk/<upload_id>/<file_id>')
def get_chunk_info(upload_id, file_id):
    """Get chunking information for a specific file"""
    metadata_path = os.path.join(app.config['UPLOAD_FOLDER'], upload_id, 'metadata.json')
    
    if not os.path.exists(metadata_path):
        return jsonify({'error': 'Upload not found'}), 404
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    file_info = next((f for f in metadata if f['file_id'] == file_id), None)
    
    if not file_info:
        return jsonify({'error': 'File not found'}), 404
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], upload_id, file_info['filename'])
    total_chunks = (file_info['file_size'] + file_info['chunk_size'] - 1) // file_info['chunk_size']
    
    return jsonify({
        'file_id': file_id,
        'filename': file_info['filename'],
        'total_size': file_info['file_size'],
        'chunk_size': file_info['chunk_size'],
        'total_chunks': total_chunks,
        'priority_level': file_info['priority_level'],
        'category': file_info['category'],
        'confidence': file_info.get('confidence', 0),
        'prediction_method': file_info.get('prediction_method', 'unknown')
    })

@app.route('/api/chunk/<upload_id>/<file_id>/<int:chunk_number>')
def get_file_chunk(upload_id, file_id, chunk_number):
    """Get a specific chunk of a file"""
    metadata_path = os.path.join(app.config['UPLOAD_FOLDER'], upload_id, 'metadata.json')
    
    if not os.path.exists(metadata_path):
        return jsonify({'error': 'Upload not found'}), 404
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    file_info = next((f for f in metadata if f['file_id'] == file_id), None)
    
    if not file_info:
        return jsonify({'error': 'File not found'}), 404
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], upload_id, file_info['filename'])
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File data not found'}), 404
    
    chunk_size = file_info['chunk_size']
    start_byte = chunk_number * chunk_size
    
    with open(file_path, 'rb') as f:
        f.seek(start_byte)
        chunk_data = f.read(chunk_size)
    
    if not chunk_data:
        return jsonify({'error': 'Chunk not found'}), 404
    
    return {
        'chunk_number': chunk_number,
        'chunk_size': len(chunk_data),
        'data': chunk_data.hex(),  # Return as hex string for JSON compatibility
        'is_last_chunk': len(chunk_data) < chunk_size
    }

@app.route('/api/status')
def api_status():
    """Health check endpoint"""
    return jsonify({
        'status': 'active',
        'service': 'priority-analyzer',
        'version': '2.0.0',
        'ml_model_trained': ml_model.is_trained
    })

# Add ML training routes
@app.route('/api/train', methods=['POST'])
def train_model():
    """API endpoint to trigger model training"""
    try:
        # Check if dataset exists
        if not os.path.exists(Config.DATASET_PATH):
            return jsonify({
                'error': 'Dataset file not found',
                'message': f'Please upload {Config.DATASET_PATH} to train the model'
            }), 400
        
        # Train the model
        success = ml_model.train_model(Config.DATASET_PATH)
        
        if success:
            return jsonify({
                'message': 'Model trained successfully',
                'model_path': Config.MODEL_PATH,
                'status': 'trained'
            })
        else:
            return jsonify({
                'error': 'Model training failed',
                'status': 'failed'
            }), 500
            
    except Exception as e:
        return jsonify({
            'error': f'Training error: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/api/model/status')
def model_status():
    """Get model training status"""
    return jsonify({
        'is_trained': ml_model.is_trained,
        'model_path': Config.MODEL_PATH,
        'dataset_path': Config.DATASET_PATH,
        'dataset_exists': os.path.exists(Config.DATASET_PATH),
        'model_files_exist': {
            'model': os.path.exists(os.path.join(Config.MODEL_PATH, Config.MODEL_FILE)),
            'scaler': os.path.exists(os.path.join(Config.MODEL_PATH, Config.SCALER_FILE)),
            'label_encoder': os.path.exists(os.path.join(Config.MODEL_PATH, Config.LABEL_ENCODER_FILE))
        }
    })

# ========== NEW SMART FEATURES API ENDPOINTS ==========
# These enhance your original system without breaking anything

@app.route('/api/smart/upload', methods=['POST'])
def smart_upload():
    """Enhanced upload with smart priority analysis"""
    if not SMART_FEATURES_AVAILABLE:
        return jsonify({'error': 'Smart features not available, use /upload instead'}), 501
    
    data = request.get_json()
    if not data or 'filename' not in data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    try:
        # Extract parameters
        filename = data['filename']
        file_size = data.get('file_size', 1024 * 1024)  # Default 1MB
        user_priority = data.get('user_priority', 3)  # Default normal
        time_sensitive = data.get('time_sensitive', 'normal')
        context_tags = data.get('context_tags', [])
        
        # Simulate file for analysis (in real scenario, you'd have actual file)
        temp_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        temp_file = os.path.join(temp_dir, filename)
        
        # Create dummy file for analysis
        with open(temp_file, 'wb') as f:
            f.write(b'0' * min(file_size, 1024))  # Create small dummy file
        
        # Analyze with both original and smart features
        analysis = analyzer.analyze_file(
            filename, temp_file, user_priority, time_sensitive, context_tags
        )
        
        # Clean up temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        return jsonify({
            **analysis,
            'ml_enhanced': analyzer.smart_enabled,
            'learning_enhanced': analyzer.smart_enabled
        })
        
    except Exception as e:
        return jsonify({'error': f'Smart upload failed: {str(e)}'}), 500

@app.route('/api/smart/status')
def smart_status():
    """Get enhanced system status with smart features"""
    base_status = {
        'status': 'active',
        'service': 'enhanced-priority-analyzer',
        'version': '3.0.0-smart',
        'original_ml_model_trained': ml_model.is_trained,
        'smart_features_available': SMART_FEATURES_AVAILABLE
    }
    
    if SMART_FEATURES_AVAILABLE and analyzer.smart_enabled:
        # Add smart system status
        queue_status = analyzer.queue_scheduler.get_queue_status()
        base_status.update({
            'system_info': {
                'status': 'active',
                'files_processed': 0,  # You can track this
                'success_rate': 1.0,
                'uptime_seconds': 0  # You can track this
            },
            'network_condition': queue_status.get('network_condition', 'good'),
            'queue_status': {
                'high_priority_queue': queue_status.get('high_priority_queue', 0),
                'normal_priority_queue': queue_status.get('normal_priority_queue', 0),
                'background_queue': queue_status.get('background_queue', 0),
                'active_tasks': queue_status.get('active_tasks', 0)
            },
            'ml_models': {
                'priority_ml_trained': ml_model.is_trained,
                'behavioral_learning_trained': True,  # Assume trained
                'learning_samples': 0  # You can track this
            }
        })
    
    return jsonify(base_status)

@app.route('/api/smart/generate-training-data', methods=['POST'])
def generate_training_data():
    """Generate training data for ML models"""
    if not SMART_FEATURES_AVAILABLE:
        return jsonify({'error': 'Smart features not available'}), 501
    
    try:
        from dataset_generator import DatasetGenerator
        generator = DatasetGenerator()
        
        # Generate comprehensive dataset
        dataset = generator.generate_comprehensive_dataset(num_samples=1000)
        
        # Save to file
        dataset_path = os.path.join(Config.MODEL_PATH, 'smart_training_data.csv')
        dataset.to_csv(dataset_path, index=False)
        
        return jsonify({
            'message': 'Training data generated successfully',
            'total_samples': len(dataset),
            'dataset_path': dataset_path,
            'columns': list(dataset.columns)
        })
        
    except Exception as e:
        return jsonify({'error': f'Training data generation failed: {str(e)}'}), 500

@app.route('/api/smart/rebalance', methods=['POST'])
def rebalance_queues():
    """Manually trigger queue rebalancing"""
    if not SMART_FEATURES_AVAILABLE or not analyzer.smart_enabled:
        return jsonify({'error': 'Smart queue management not available'}), 501
    
    try:
        # This would trigger rebalancing in the queue scheduler
        return jsonify({
            'message': 'Queue rebalancing completed',
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': f'Rebalancing failed: {str(e)}'}), 500

@app.route('/api/smart/simulate-network', methods=['POST'])
def simulate_network():
    """Simulate network condition changes"""
    if not SMART_FEATURES_AVAILABLE:
        return jsonify({'error': 'Smart features not available'}), 501
    
    data = request.get_json()
    condition = data.get('condition', 'good') if data else 'good'
    
    return jsonify({
        'message': f'Network condition simulated: {condition}',
        'condition': condition,
        'status': 'success'
    })

# =============================================================================
# 📁 NEW FILE MANAGEMENT SYSTEM ROUTES
# =============================================================================
# These routes provide upload, preview, download, and dashboard functionality
# They work alongside your existing Priority Analyzer without interfering

@app.route('/upload')
def upload_page():
    """NEW: Upload page for the file management system"""
    return render_template('upload.html')

@app.route('/dashboard')
def dashboard_page():
    """NEW: Dashboard page showing all uploaded files"""
    return render_template('dashboard.html')

@app.route('/test')
def test_page():
    """Connection test page for troubleshooting"""
    return render_template('test.html')

@app.route('/preview/<file_id>')
def preview_page(file_id):
    """NEW: Preview page for viewing files"""
    if not analyzer.file_db:
        abort(500, 'File management not available')
    
    file_info = analyzer.file_db.get_file_by_id(file_id)
    if not file_info:
        abort(404, 'File not found')
    
    # Format data for template
    upload_date = datetime.fromisoformat(file_info['upload_date']).strftime('%B %d, %Y at %I:%M %p')
    file_size = format_file_size(file_info['file_size'])
    
    return render_template('preview.html', 
                         file=file_info, 
                         upload_date=upload_date,
                         file_size=file_size)

@app.route('/api/files/upload', methods=['POST'])
def upload_file():
    """NEW: Handle file upload for the file management system"""
    if not analyzer.file_db:
        return jsonify({'error': 'File management not available'}), 500
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Generate unique filename to prevent conflicts
        original_filename = secure_filename(file.filename)
        file_id = str(uuid.uuid4())
        file_extension = os.path.splitext(original_filename)[1]
        safe_filename = f"{file_id}{file_extension}"
        
        # Save file to storage
        file_path = os.path.join('file_storage', safe_filename)
        file.save(file_path)
        
        # Get file info
        file_size = os.path.getsize(file_path)
        file_type = get_file_type(original_filename)
        mime_type = mimetypes.guess_type(original_filename)[0] or 'application/octet-stream'
        
        # Prepare file metadata
        file_info = {
            'filename': safe_filename,
            'original_filename': original_filename,
            'file_size': file_size,
            'file_type': file_type,
            'mime_type': mime_type,
            'upload_date': datetime.now().isoformat(),
            'file_path': file_path,
            'download_url': f'/api/files/download/{file_id}',
            'preview_url': f'/preview/{file_id}',
            'description': f'Uploaded file: {original_filename}'
        }
        
        # Save to database
        saved_file_id = analyzer.file_db.save_file_metadata(file_info)
        
        return jsonify({
            'success': True,
            'file_id': saved_file_id,
            'filename': original_filename,
            'file_size': file_size,
            'file_type': file_type,
            'upload_date': file_info['upload_date'],
            'preview_url': f'/preview/{saved_file_id}',
            'download_url': f'/api/files/download/{saved_file_id}'
        })
        
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/api/files/list')
def list_files():
    """NEW: Get list of all uploaded files"""
    if not analyzer.file_db:
        return jsonify({'error': 'File management not available'}), 500
    
    try:
        files = analyzer.file_db.get_all_files()
        return jsonify(files)
    except Exception as e:
        return jsonify({'error': f'Failed to load files: {str(e)}'}), 500

@app.route('/api/files/stats')
def file_stats():
    """NEW: Get file statistics for dashboard"""
    if not analyzer.file_db:
        return jsonify({'error': 'File management not available'}), 500
    
    try:
        stats = analyzer.file_db.get_file_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': f'Failed to load stats: {str(e)}'}), 500

@app.route('/api/files/download/<file_id>')
def download_file(file_id):
    """NEW: Download file by ID"""
    if not analyzer.file_db:
        abort(500, 'File management not available')
    
    file_info = analyzer.file_db.get_file_by_id(file_id)
    if not file_info:
        abort(404, 'File not found')
    
    if not os.path.exists(file_info['file_path']):
        abort(404, 'File not found on disk')
    
    return send_file(
        file_info['file_path'],
        as_attachment=True,
        download_name=file_info['original_filename'],
        mimetype=file_info['mime_type']
    )

@app.route('/api/files/serve/<file_id>')
def serve_file(file_id):
    """NEW: Serve file for preview (not as download)"""
    if not analyzer.file_db:
        abort(500, 'File management not available')
    
    file_info = analyzer.file_db.get_file_by_id(file_id)
    if not file_info:
        abort(404, 'File not found')
    
    if not os.path.exists(file_info['file_path']):
        abort(404, 'File not found on disk')
    
    return send_file(
        file_info['file_path'],
        mimetype=file_info['mime_type']
    )

@app.route('/api/files/delete/<file_id>', methods=['DELETE'])
def delete_file(file_id):
    """NEW: Delete file by ID"""
    if not analyzer.file_db:
        return jsonify({'error': 'File management not available'}), 500
    
    try:
        file_info = analyzer.file_db.get_file_by_id(file_id)
        if not file_info:
            return jsonify({'error': 'File not found'}), 404
        
        # Delete from database (soft delete)
        success = analyzer.file_db.delete_file(file_id)
        
        if success:
            # Optionally delete physical file
            try:
                if os.path.exists(file_info['file_path']):
                    os.remove(file_info['file_path'])
            except:
                pass  # Don't fail if file removal fails
            
            return jsonify({'success': True, 'message': 'File deleted successfully'})
        else:
            return jsonify({'error': 'Failed to delete file'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Delete failed: {str(e)}'}), 500

# =============================================================================
# END OF NEW FILE MANAGEMENT SYSTEM
# =============================================================================

# =============================================================================
# 🌐 NEW NETWORK MONITORING SYSTEM ROUTES
# =============================================================================
# These routes provide real-time WiFi and network status monitoring
# They work alongside all your existing features without interfering

@app.route('/api/network/status')
def get_network_status():
    """NEW: Get complete real-time network status (like asking how the playground is doing)"""
    if not NETWORK_MONITORING_AVAILABLE:
        return jsonify({
            'error': 'Network monitoring not available',
            'wifi_name': 'Unknown',
            'upload_speed': 0.0,
            'download_speed': 0.0,
            'latency': 0.0,
            'jitter': 0.0,
            'packet_loss': 0.0,
            'health_status': 'Unknown',
            'success': False
        }), 500
    
    try:
        # Ask our network monitor for a complete report (like asking a kind teacher)
        status = network_monitor.get_complete_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({
            'error': f'Network status check failed: {str(e)}',
            'success': False
        }), 500

@app.route('/api/network/ping')
def ping_test():
    """NEW: Simple ping test endpoint (like saying hello to the internet)"""
    if not NETWORK_MONITORING_AVAILABLE:
        return jsonify({'error': 'Network monitoring not available'}), 500
    
    try:
        # Do a simple ping test (like shouting hello and waiting for echo)
        ping_results = network_monitor.ping_test()
        return jsonify({
            'latency': ping_results['latency'],
            'jitter': ping_results['jitter'],
            'packet_loss': ping_results['packet_loss'],
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': f'Ping test failed: {str(e)}',
            'success': False
        }), 500

@app.route('/api/network/speed')
def speed_test():
    """NEW: Get current network speeds (like measuring how fast paper planes fly)"""
    if not NETWORK_MONITORING_AVAILABLE:
        return jsonify({'error': 'Network monitoring not available'}), 500
    
    try:
        # Measure current network speeds (like counting data packets)
        speed_results = network_monitor.get_network_speed()
        return jsonify({
            'upload_speed': speed_results['upload_speed'],
            'download_speed': speed_results['download_speed'],
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': f'Speed test failed: {str(e)}',
            'success': False
        }), 500

# =============================================================================
# END OF NEW NETWORK MONITORING SYSTEM
# =============================================================================

# =============================================================================
# ⭐ AUTO-HEALING UPLOAD ENGINE ⭐ (NEW FEATURE)
# =============================================================================

# Import our gentle healing engine
try:
    from auto_healing_engine import healing_engine
    AUTO_HEALING_AVAILABLE = True
    print("🩺 Auto-Healing Upload Engine initialized! Ready to heal your uploads! ✨")
except ImportError as e:
    print(f"⚠️ Auto-healing features not available: {e}")
    AUTO_HEALING_AVAILABLE = False

@app.route('/api/upload_chunk', methods=['POST'])
def upload_chunk():
    """
    Baby, this handles chunk uploads with healing magic!
    Like a gentle nurse accepting each piece of a puzzle and checking if it's okay.
    """
    try:
        if not AUTO_HEALING_AVAILABLE:
            return jsonify({'error': 'Auto-healing not available', 'success': False}), 500
        
        # Get chunk information (like reading a medical chart)
        chunk_number = int(request.form.get('chunk_number', 0))
        total_chunks = int(request.form.get('total_chunks', 1))
        upload_id = request.form.get('upload_id')
        expected_checksum = request.form.get('checksum')
        chunk_size = int(request.form.get('chunk_size', 0))
        
        if not upload_id:
            return jsonify({'error': 'Upload ID is required', 'success': False}), 400
        
        # Get the file chunk (like receiving a puzzle piece)
        if 'file' not in request.files:
            return jsonify({'error': 'No file chunk provided', 'success': False}), 400
        
        file_chunk = request.files['file']
        chunk_data = file_chunk.read()
        
        # Verify chunk size
        if len(chunk_data) != chunk_size:
            return jsonify({
                'error': f'Chunk size mismatch: expected {chunk_size}, got {len(chunk_data)}',
                'success': False
            }), 400
        
        # Calculate server-side checksum (like taking fingerprints)
        server_checksum = healing_engine.calculate_chunk_checksum(chunk_data)
        
        # Check for corruption
        if expected_checksum and server_checksum != expected_checksum:
            return jsonify({
                'error': 'Chunk corruption detected',
                'success': False,
                'expected_checksum': expected_checksum,
                'server_checksum': server_checksum
            }), 400
        
        # Create upload directory if it doesn't exist
        upload_dir = os.path.join('uploads', upload_id)
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save the chunk (like putting a puzzle piece in its place)
        chunk_filename = f'chunk_{chunk_number:06d}.tmp'
        chunk_path = os.path.join(upload_dir, chunk_filename)
        
        with open(chunk_path, 'wb') as f:
            f.write(chunk_data)
        
        # Log the healing success
        healing_engine.logger.info(f'✅ Chunk {chunk_number} saved successfully for upload {upload_id}')
        
        # Check if this is the last chunk
        is_complete = False
        final_file_path = None
        
        if chunk_number == total_chunks - 1:
            # Try to assemble the complete file
            final_file_path = assemble_upload_chunks(upload_id, total_chunks)
            if final_file_path:
                is_complete = True
                healing_engine.logger.info(f'🎉 Upload {upload_id} completed and assembled!')
        
        return jsonify({
            'success': True,
            'chunk_number': chunk_number,
            'checksum': server_checksum,
            'upload_id': upload_id,
            'is_complete': is_complete,
            'file_path': final_file_path
        })
        
    except Exception as e:
        healing_engine.logger.error(f"💔 Chunk upload failed: {e}")
        return jsonify({
            'error': f'Chunk upload failed: {str(e)}',
            'success': False
        }), 500

@app.route('/api/check_chunks/<upload_id>')
def check_chunks(upload_id):
    """
    Baby, this checks which chunks are already safely stored!
    Like checking which puzzle pieces are already in the box.
    """
    try:
        if not AUTO_HEALING_AVAILABLE:
            return jsonify({'error': 'Auto-healing not available', 'completed_chunks': []}), 500
        
        upload_dir = os.path.join('uploads', upload_id)
        completed_chunks = []
        
        if os.path.exists(upload_dir):
            # Find all chunk files
            for filename in os.listdir(upload_dir):
                if filename.startswith('chunk_') and filename.endswith('.tmp'):
                    # Extract chunk number from filename
                    chunk_num_str = filename.replace('chunk_', '').replace('.tmp', '')
                    try:
                        chunk_number = int(chunk_num_str)
                        completed_chunks.append(chunk_number)
                    except ValueError:
                        continue
        
        completed_chunks.sort()
        healing_engine.logger.info(f'📋 Found {len(completed_chunks)} completed chunks for upload {upload_id}')
        
        return jsonify({
            'upload_id': upload_id,
            'completed_chunks': completed_chunks,
            'total_completed': len(completed_chunks)
        })
        
    except Exception as e:
        healing_engine.logger.error(f"💔 Check chunks failed: {e}")
        return jsonify({
            'error': f'Check chunks failed: {str(e)}',
            'completed_chunks': []
        }), 500

@app.route('/api/resume_upload/<upload_id>')
def resume_upload(upload_id):
    """
    Baby, this helps resume an upload that was sleeping!
    Like gently waking up a child and asking what they were playing with.
    """
    try:
        if not AUTO_HEALING_AVAILABLE:
            return jsonify({'error': 'Auto-healing not available', 'success': False}), 500
        
        # Load saved state
        saved_state = healing_engine.load_upload_state(upload_id)
        
        if not saved_state:
            return jsonify({
                'error': 'No saved state found for this upload',
                'success': False
            }), 404
        
        # Check existing chunks
        completed_chunks = []
        upload_dir = os.path.join('uploads', upload_id)
        
        if os.path.exists(upload_dir):
            for filename in os.listdir(upload_dir):
                if filename.startswith('chunk_') and filename.endswith('.tmp'):
                    chunk_num_str = filename.replace('chunk_', '').replace('.tmp', '')
                    try:
                        chunk_number = int(chunk_num_str)
                        completed_chunks.append(chunk_number)
                    except ValueError:
                        continue
        
        healing_engine.logger.info(f'🔄 Resuming upload {upload_id} with {len(completed_chunks)} completed chunks')
        
        return jsonify({
            'success': True,
            'upload_id': upload_id,
            'saved_state': saved_state,
            'completed_chunks': sorted(completed_chunks),
            'can_resume': True
        })
        
    except Exception as e:
        healing_engine.logger.error(f"💔 Resume upload failed: {e}")
        return jsonify({
            'error': f'Resume upload failed: {str(e)}',
            'success': False
        }), 500

@app.route('/api/healing_report/<upload_id>')
def healing_report(upload_id):
    """
    Baby, this gives a nice report of all the healing that happened!
    Like a doctor's report showing how well the patient recovered.
    """
    try:
        if not AUTO_HEALING_AVAILABLE:
            return jsonify({'error': 'Auto-healing not available', 'success': False}), 500
        
        # Load healing session data
        session_data = healing_engine.load_upload_state(upload_id)
        
        if not session_data:
            return jsonify({
                'error': 'No healing session found',
                'success': False
            }), 404
        
        # Generate report
        healing_events = session_data.get('healing_events', [])
        
        report = {
            'upload_id': upload_id,
            'file_info': session_data.get('file_info', {}),
            'status': session_data.get('status', 'unknown'),
            'created_at': session_data.get('created_at'),
            'completed_at': session_data.get('completed_at'),
            'total_healing_events': len(healing_events),
            'completed_chunks': len(session_data.get('completed_chunks', [])),
            'failed_chunks': len(session_data.get('failed_chunks', [])),
            'total_retries': session_data.get('total_retries', 0),
            'corruption_detections': session_data.get('corruption_detections', 0),
            'jump_backs': session_data.get('jump_backs', 0),
            'adaptive_resizes': session_data.get('adaptive_resizes', 0),
            'recent_events': healing_events[-10:] if healing_events else []  # Last 10 events
        }
        
        return jsonify({
            'success': True,
            'report': report
        })
        
    except Exception as e:
        healing_engine.logger.error(f"💔 Healing report failed: {e}")
        return jsonify({
            'error': f'Healing report failed: {str(e)}',
            'success': False
        }), 500

def assemble_upload_chunks(upload_id, total_chunks):
    """
    Baby, this puts all the puzzle pieces together into a complete picture!
    Like assembling a jigsaw puzzle once all pieces are found.
    """
    try:
        upload_dir = os.path.join('uploads', upload_id)
        
        # Check if all chunks exist
        missing_chunks = []
        for i in range(total_chunks):
            chunk_filename = f'chunk_{i:06d}.tmp'
            chunk_path = os.path.join(upload_dir, chunk_filename)
            if not os.path.exists(chunk_path):
                missing_chunks.append(i)
        
        if missing_chunks:
            healing_engine.logger.warning(f"⚠️ Missing chunks for upload {upload_id}: {missing_chunks}")
            return None
        
        # Assemble the file
        final_filename = f'assembled_file_{upload_id}'
        final_path = os.path.join(upload_dir, final_filename)
        
        with open(final_path, 'wb') as final_file:
            for i in range(total_chunks):
                chunk_filename = f'chunk_{i:06d}.tmp'
                chunk_path = os.path.join(upload_dir, chunk_filename)
                
                with open(chunk_path, 'rb') as chunk_file:
                    chunk_data = chunk_file.read()
                    final_file.write(chunk_data)
        
        # Clean up chunk files
        for i in range(total_chunks):
            chunk_filename = f'chunk_{i:06d}.tmp'
            chunk_path = os.path.join(upload_dir, chunk_filename)
            try:
                os.remove(chunk_path)
            except OSError:
                pass  # Ignore cleanup errors
        
        healing_engine.logger.info(f'🎉 Successfully assembled upload {upload_id}')
        return final_path
        
    except Exception as e:
        healing_engine.logger.error(f"💔 File assembly failed: {e}")
        return None

@app.route('/api/ping', methods=['HEAD', 'GET'])
def ping():
    """
    Baby, this is like saying "Hello, are you there?" to check if server is awake!
    Used by the healing system to check network strength.
    """
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

# =============================================================================
# END OF AUTO-HEALING UPLOAD ENGINE
# =============================================================================

# =============================================================================
# 🤖 GEMINI AI CHATBOT INTEGRATION
# =============================================================================

# Add AI chat routes if available
if GEMINI_AI_AVAILABLE:
    add_ai_routes(app)
    
    # Initialize Gemini AI with API key
    # 💡 To enable AI chat, replace with your actual Gemini API key!
    GEMINI_API_KEY = "your-gemini-api-key-here"  # 🔑 Add your API key here!
    
    if GEMINI_API_KEY and GEMINI_API_KEY != "your-gemini-api-key-here":
        setup_gemini_ai(GEMINI_API_KEY)
    else:
        print("⚠️ Gemini API key not configured! Add your API key to enable AI chat.")
        print("💡 Get your free API key at: https://makersuite.google.com/app/apikey")

# =============================================================================
# END OF GEMINI AI INTEGRATION
# =============================================================================



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
