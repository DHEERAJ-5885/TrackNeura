# 🎪 Smart Priority File Transfer System Configuration
# Think of this as the rulebook for our magical playground!

import os
from dataclasses import dataclass
from typing import Dict, List, Tuple
from enum import Enum

class FileType(Enum):
    """Different types of kids (files) in our playground"""
    EMERGENCY = "emergency"      # The kid who scraped their knee - needs immediate attention!
    DOCUMENT = "document"        # The studious kid with homework
    IMAGE = "image"             # The artist kid with drawings
    VIDEO = "video"             # The movie-maker kid with big projects
    AUDIO = "audio"             # The musician kid with songs
    ARCHIVE = "archive"         # The collector kid with treasure boxes
    CODE = "code"               # The programmer kid with cool inventions
    OTHER = "other"             # All the other wonderful kids

class NetworkCondition(Enum):
    """How strong our playground's internet connection is"""
    EXCELLENT = "excellent"     # Super fast highway - everyone can zoom!
    GOOD = "good"              # Nice smooth road
    FAIR = "fair"              # Bumpy path, need to be careful
    POOR = "poor"              # Muddy trail, only small steps work
    CRITICAL = "critical"      # Almost broken bridge, emergency only!

class UserPriority(Enum):
    """How important each kid thinks their turn is"""
    CRITICAL = 5    # "I REALLY REALLY need this now!"
    HIGH = 4        # "This is super important!"
    NORMAL = 3      # "Regular importance, please"
    LOW = 2         # "Whenever you can, thanks"
    DEFERRED = 1    # "No rush at all"

@dataclass
class SmartPriorityConfig:
    """The master rulebook for our playground supervisor"""
    
    # 🎯 Base scoring weights (how much each factor matters)
    WEIGHTS = {
        'file_size': 0.15,          # Smaller kids often go first
        'file_type': 0.20,          # Emergency kids get priority
        'time_sensitive': 0.25,     # Urgent homework comes first
        'network_strength': 0.15,   # Match kid size to road condition
        'failure_history': 0.10,    # Kids who struggled before get help
        'user_priority': 0.10,      # Listen to how important they say it is
        'predicted_difficulty': 0.05 # Smart guess of how hard it'll be
    }
    
    # 📏 File size categories (like shirt sizes for kids)
    SIZE_CATEGORIES = {
        'tiny': (0, 1024 * 1024),           # 0-1MB: Like a small toy
        'small': (1024 * 1024, 10 * 1024 * 1024),    # 1-10MB: Like a book
        'medium': (10 * 1024 * 1024, 100 * 1024 * 1024), # 10-100MB: Like a backpack
        'large': (100 * 1024 * 1024, 1024 * 1024 * 1024), # 100MB-1GB: Like a suitcase
        'huge': (1024 * 1024 * 1024, float('inf'))   # 1GB+: Like a moving truck
    }
    
    # 🏆 Type priority scores (some kids naturally go first)
    TYPE_SCORES = {
        FileType.EMERGENCY: 100,    # Always first - like a hurt kid
        FileType.DOCUMENT: 80,      # Important homework
        FileType.CODE: 75,          # Cool inventions need care
        FileType.IMAGE: 60,         # Pretty pictures
        FileType.AUDIO: 50,         # Nice songs
        FileType.VIDEO: 30,         # Big movies take time
        FileType.ARCHIVE: 20,       # Treasure boxes can wait
        FileType.OTHER: 40          # Fair chance for everyone else
    }
    
    # ⏰ Time sensitivity multipliers
    TIME_MULTIPLIERS = {
        'immediate': 2.0,    # "Right now!" - double priority
        'urgent': 1.5,       # "Very soon please" - boost priority
        'normal': 1.0,       # "Regular timing" - normal priority
        'flexible': 0.8,     # "Whenever works" - slightly lower
        'background': 0.5    # "No rush at all" - half priority
    }
    
    # 🌐 Network adaptation rules
    NETWORK_RULES = {
        NetworkCondition.EXCELLENT: {'max_concurrent': 10, 'chunk_size': 32*1024*1024},
        NetworkCondition.GOOD: {'max_concurrent': 6, 'chunk_size': 16*1024*1024},
        NetworkCondition.FAIR: {'max_concurrent': 4, 'chunk_size': 8*1024*1024},
        NetworkCondition.POOR: {'max_concurrent': 2, 'chunk_size': 4*1024*1024},
        NetworkCondition.CRITICAL: {'max_concurrent': 1, 'chunk_size': 1*1024*1024}
    }
    
    # 🔄 Learning system parameters
    LEARNING_CONFIG = {
        'success_boost': 1.1,       # Reward files that completed well
        'failure_penalty': 0.9,     # Help files that struggled
        'adaptation_rate': 0.1,     # How fast we learn new patterns
        'memory_decay': 0.95,       # Gradually forget very old patterns
        'min_history_samples': 5    # Need at least this many examples to learn
    }
    
    # 📊 Chunk priority rules (inside each file)
    CHUNK_RULES = {
        'metadata_boost': 2.0,      # File headers are super important
        'beginning_boost': 1.5,     # Start of file often crucial
        'ending_boost': 1.2,        # End of file sometimes important
        'middle_penalty': 0.9,      # Middle chunks can wait a bit
        'error_recovery_boost': 3.0 # If chunk failed, really boost it
    }

# 🎨 File type detection patterns
FILE_PATTERNS = {
    FileType.EMERGENCY: [
        'emergency', 'urgent', 'critical', 'alert', 'asap', 'immediate',
        'priority', 'rush', 'crisis', 'important', 'deadline'
    ],
    FileType.DOCUMENT: ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
    FileType.IMAGE: ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],
    FileType.VIDEO: ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv'],
    FileType.AUDIO: ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
    FileType.ARCHIVE: ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
    FileType.CODE: ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.go']
}

# 🎯 Default configuration instance
DEFAULT_CONFIG = SmartPriorityConfig()