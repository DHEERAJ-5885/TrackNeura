"""
🗃️ File Management Database
===========================

This module handles all database operations for the new Upload & File Management System.
It works alongside your existing Priority Analyzer without interfering with it.
"""

import sqlite3
import os
from typing import Dict, List, Optional
from datetime import datetime
import uuid

class FileDatabase:
    """Simple database manager for uploaded files"""
    
    def __init__(self, db_path: str = "file_management.db"):
        """Initialize the file database"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create the files table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create files table for the new upload system
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS uploaded_files (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                original_filename TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                file_type TEXT NOT NULL,
                mime_type TEXT,
                upload_date TEXT NOT NULL,
                file_path TEXT NOT NULL,
                download_url TEXT NOT NULL,
                preview_url TEXT NOT NULL,
                user_id TEXT DEFAULT 'default_user',
                description TEXT,
                is_active INTEGER DEFAULT 1
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_file_metadata(self, file_info: Dict) -> str:
        """Save file metadata to database and return the file ID"""
        file_id = str(uuid.uuid4())
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO uploaded_files 
            (id, filename, original_filename, file_size, file_type, mime_type, 
             upload_date, file_path, download_url, preview_url, user_id, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            file_id,
            file_info['filename'],
            file_info['original_filename'],
            file_info['file_size'],
            file_info['file_type'],
            file_info.get('mime_type', ''),
            file_info['upload_date'],
            file_info['file_path'],
            file_info['download_url'],
            file_info['preview_url'],
            file_info.get('user_id', 'default_user'),
            file_info.get('description', '')
        ))
        
        conn.commit()
        conn.close()
        
        return file_id
    
    def get_file_by_id(self, file_id: str) -> Optional[Dict]:
        """Get file information by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, filename, original_filename, file_size, file_type, mime_type,
                   upload_date, file_path, download_url, preview_url, user_id, description
            FROM uploaded_files 
            WHERE id = ? AND is_active = 1
        ''', (file_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'filename': row[1],
                'original_filename': row[2],
                'file_size': row[3],
                'file_type': row[4],
                'mime_type': row[5],
                'upload_date': row[6],
                'file_path': row[7],
                'download_url': row[8],
                'preview_url': row[9],
                'user_id': row[10],
                'description': row[11]
            }
        return None
    
    def get_all_files(self, user_id: str = None) -> List[Dict]:
        """Get all files, optionally filtered by user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute('''
                SELECT id, filename, original_filename, file_size, file_type, mime_type,
                       upload_date, file_path, download_url, preview_url, user_id, description
                FROM uploaded_files 
                WHERE user_id = ? AND is_active = 1
                ORDER BY upload_date DESC
            ''', (user_id,))
        else:
            cursor.execute('''
                SELECT id, filename, original_filename, file_size, file_type, mime_type,
                       upload_date, file_path, download_url, preview_url, user_id, description
                FROM uploaded_files 
                WHERE is_active = 1
                ORDER BY upload_date DESC
            ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        files = []
        for row in rows:
            files.append({
                'id': row[0],
                'filename': row[1],
                'original_filename': row[2],
                'file_size': row[3],
                'file_type': row[4],
                'mime_type': row[5],
                'upload_date': row[6],
                'file_path': row[7],
                'download_url': row[8],
                'preview_url': row[9],
                'user_id': row[10],
                'description': row[11]
            })
        
        return files
    
    def get_file_stats(self, user_id: str = None) -> Dict:
        """Get file statistics for dashboard"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute('''
                SELECT COUNT(*), SUM(file_size), MAX(upload_date)
                FROM uploaded_files 
                WHERE user_id = ? AND is_active = 1
            ''', (user_id,))
        else:
            cursor.execute('''
                SELECT COUNT(*), SUM(file_size), MAX(upload_date)
                FROM uploaded_files 
                WHERE is_active = 1
            ''')
        
        row = cursor.fetchone()
        conn.close()
        
        return {
            'total_files': row[0] or 0,
            'total_size': row[1] or 0,
            'latest_upload': row[2] or 'No uploads yet'
        }
    
    def delete_file(self, file_id: str) -> bool:
        """Soft delete a file (mark as inactive)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE uploaded_files 
            SET is_active = 0 
            WHERE id = ?
        ''', (file_id,))
        
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return affected > 0

# Helper functions for file operations
def get_file_type(filename: str) -> str:
    """Determine file type from filename"""
    ext = os.path.splitext(filename.lower())[1]
    
    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']:
        return 'image'
    elif ext in ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']:
        return 'video'
    elif ext in ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a']:
        return 'audio'
    elif ext in ['.pdf']:
        return 'pdf'
    elif ext in ['.doc', '.docx', '.txt', '.rtf', '.odt']:
        return 'document'
    elif ext in ['.xls', '.xlsx', '.csv', '.ods']:
        return 'spreadsheet'
    elif ext in ['.ppt', '.pptx', '.odp']:
        return 'presentation'
    elif ext in ['.zip', '.rar', '.7z', '.tar', '.gz']:
        return 'archive'
    else:
        return 'other'

def format_file_size(size_bytes: int) -> str:
    """Convert bytes to human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def is_previewable(file_type: str) -> bool:
    """Check if file type can be previewed"""
    return file_type in ['image', 'video', 'audio', 'pdf']