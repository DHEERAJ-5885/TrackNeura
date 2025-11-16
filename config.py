import os

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000
    
    # File Upload Settings
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    
    # ML Model settings
    MODEL_PATH = 'models'
    DATASET_PATH = 'dataset.xlsx'
    MODEL_FILE = 'priority_model.pkl'
    SCALER_FILE = 'feature_scaler.pkl'
    LABEL_ENCODER_FILE = 'label_encoder.pkl'
    
    # Priority categories
    PRIORITY_CATEGORIES = [
        'emergency',
        'graphic_heavy', 
        'video',
        'image',
        'text',
        'audio',
        'archive',
        'other'
    ]
    
    # Feature extraction settings
    FEATURE_COLUMNS = [
        'file_size',
        'file_extension_encoded',
        'filename_length',
        'has_emergency_keywords',
        'creation_time_hour',
        'file_type_category'
    ]

# Priority Rules Configuration
PRIORITY_RULES = {
    'emergency_keywords': ['emergency', 'urgent', 'critical', 'alert', 'immediate', 'asap'],
    'file_extensions': {
        'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.ico'],
        'text': ['.txt', '.doc', '.docx', '.pdf', '.rtf', '.odt', '.md', '.csv'],
        'graphic_heavy': ['.psd', '.ai', '.svg', '.eps', '.indd', '.sketch', '.fig'],
        'video': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv', '.m4v'],
        'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
        'archive': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz']
    }
}

# Chunk Size Configuration (in bytes)
CHUNK_SIZES = {
    'emergency': 512 * 1024,      # 512KB - fastest processing
    'text': 1024 * 1024,          # 1MB
    'image': 2 * 1024 * 1024,     # 2MB
    'audio': 4 * 1024 * 1024,     # 4MB
    'archive': 8 * 1024 * 1024,   # 8MB
    'video': 16 * 1024 * 1024,    # 16MB
    'graphic_heavy': 32 * 1024 * 1024,  # 32MB
    'other': 1024 * 1024          # 1MB
}