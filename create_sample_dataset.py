import pandas as pd
import numpy as np

def create_sample_dataset():
    """Create a sample dataset.xlsx for training if one doesn't exist"""
    
    # Sample data
    data = {
        'filename': [
            'emergency_report.pdf', 'urgent_document.docx', 'critical_analysis.xlsx',
            'presentation.pptx', 'meeting_notes.txt', 'project_plan.pdf',
            'design_mockup.psd', 'logo_design.ai', 'banner_graphic.eps',
            'profile_photo.jpg', 'team_picture.png', 'screenshot.gif',
            'training_video.mp4', 'conference_call.avi', 'demo_recording.mov',
            'background_music.mp3', 'voice_memo.wav', 'podcast_episode.flac',
            'project_backup.zip', 'source_code.tar.gz', 'database_dump.7z',
            'readme.txt', 'config.json', 'data_export.csv'
        ],
        'file_size': [
            2048000, 1536000, 3072000,  # Emergency/urgent files
            5120000, 1024000, 2560000,  # Regular documents
            52428800, 31457280, 41943040,  # Graphic files
            4194304, 2097152, 1048576,  # Images
            104857600, 209715200, 157286400,  # Videos
            8388608, 4194304, 16777216,  # Audio files
            20971520, 10485760, 31457280,  # Archives
            8192, 4096, 65536  # Small text files
        ],
        'priority': [
            'emergency', 'emergency', 'emergency',  # High priority
            'text', 'text', 'text',  # Text documents
            'graphic_heavy', 'graphic_heavy', 'graphic_heavy',  # Graphics
            'image', 'image', 'image',  # Images
            'video', 'video', 'video',  # Videos
            'audio', 'audio', 'audio',  # Audio
            'archive', 'archive', 'archive',  # Archives
            'other', 'other', 'other'  # Others
        ]
    }
    
    df = pd.DataFrame(data)
    df.to_excel('dataset.xlsx', index=False)
    print("Sample dataset.xlsx created successfully!")
    print(f"Dataset contains {len(df)} samples")
    print("\nDataset preview:")
    print(df.head(10))

if __name__ == "__main__":
    create_sample_dataset()