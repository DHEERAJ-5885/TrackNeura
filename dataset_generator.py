# 📚 Training Dataset Generator - Creating Smart Examples for Our AI!
# This creates perfect example data to teach our system how to be super smart!

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
from typing import List, Dict, Tuple
import json

from smart_priority_config import *

class DatasetGenerator:
    """The master creator of training examples! 🎨📊"""
    
    def __init__(self):
        self.file_extensions = {
            FileType.EMERGENCY: ['.pdf', '.doc', '.docx', '.txt'],
            FileType.DOCUMENT: ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
            FileType.IMAGE: ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
            FileType.VIDEO: ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm'],
            FileType.AUDIO: ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
            FileType.ARCHIVE: ['.zip', '.rar', '.7z', '.tar', '.gz'],
            FileType.CODE: ['.py', '.js', '.html', '.css', '.java', '.cpp']
        }
        
        self.filename_patterns = {
            FileType.EMERGENCY: [
                'emergency_report', 'urgent_document', 'critical_analysis', 
                'alert_notification', 'priority_memo', 'immediate_action',
                'crisis_management', 'asap_request', 'deadline_urgent'
            ],
            FileType.DOCUMENT: [
                'report', 'document', 'presentation', 'proposal', 'contract',
                'manual', 'guide', 'specification', 'analysis', 'summary'
            ],
            FileType.IMAGE: [
                'photo', 'image', 'picture', 'screenshot', 'diagram',
                'chart', 'graphic', 'logo', 'banner', 'thumbnail'
            ],
            FileType.VIDEO: [
                'video', 'movie', 'clip', 'recording', 'tutorial',
                'presentation', 'conference', 'training', 'demo'
            ],
            FileType.AUDIO: [
                'audio', 'music', 'sound', 'recording', 'podcast',
                'interview', 'meeting', 'call', 'voicemail'
            ],
            FileType.ARCHIVE: [
                'backup', 'archive', 'package', 'bundle', 'compressed',
                'data_export', 'source_code', 'project_files'
            ],
            FileType.CODE: [
                'source', 'code', 'script', 'program', 'application',
                'website', 'api', 'function', 'module', 'library'
            ]
        }
        
        print("📚 Dataset Generator ready to create amazing training data! ✨")
    
    def generate_realistic_filename(self, file_type: FileType) -> str:
        """Create realistic filenames that match each file type 📝"""
        
        base_names = self.filename_patterns.get(file_type, ['file'])
        extensions = self.file_extensions.get(file_type, ['.dat'])
        
        base_name = random.choice(base_names)
        extension = random.choice(extensions)
        
        # Add some variation
        if random.random() < 0.3:  # 30% chance of adding number
            base_name += f"_{random.randint(1, 999)}"
        
        if random.random() < 0.2:  # 20% chance of adding version
            base_name += f"_v{random.randint(1, 9)}"
        
        if random.random() < 0.1:  # 10% chance of adding date
            date_str = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y%m%d")
            base_name += f"_{date_str}"
        
        return f"{base_name}{extension}"
    
    def generate_realistic_file_size(self, file_type: FileType) -> int:
        """Generate realistic file sizes for each type 📏"""
        
        # Base size ranges for each file type (in bytes)
        size_ranges = {
            FileType.EMERGENCY: (1024, 50 * 1024 * 1024),      # 1KB - 50MB
            FileType.DOCUMENT: (1024, 100 * 1024 * 1024),      # 1KB - 100MB
            FileType.IMAGE: (10 * 1024, 50 * 1024 * 1024),     # 10KB - 50MB
            FileType.VIDEO: (1024 * 1024, 2 * 1024 * 1024 * 1024),  # 1MB - 2GB
            FileType.AUDIO: (100 * 1024, 200 * 1024 * 1024),   # 100KB - 200MB
            FileType.ARCHIVE: (1024, 1 * 1024 * 1024 * 1024),  # 1KB - 1GB
            FileType.CODE: (1024, 10 * 1024 * 1024),           # 1KB - 10MB
            FileType.OTHER: (1024, 100 * 1024 * 1024)          # 1KB - 100MB
        }
        
        min_size, max_size = size_ranges.get(file_type, (1024, 10 * 1024 * 1024))
        
        # Use log-normal distribution for more realistic size distribution
        log_min = np.log(min_size)
        log_max = np.log(max_size)
        log_size = np.random.uniform(log_min, log_max)
        
        return int(np.exp(log_size))
    
    def generate_transfer_performance(self, file_size: int, file_type: FileType, 
                                    network_condition: NetworkCondition, 
                                    user_priority: UserPriority) -> Dict:
        """Generate realistic transfer performance data 📊"""
        
        # Base network speeds (bytes per second)
        base_speeds = {
            NetworkCondition.EXCELLENT: 50 * 1024 * 1024,
            NetworkCondition.GOOD: 20 * 1024 * 1024,
            NetworkCondition.FAIR: 10 * 1024 * 1024,
            NetworkCondition.POOR: 2 * 1024 * 1024,
            NetworkCondition.CRITICAL: 512 * 1024
        }
        
        base_speed = base_speeds[network_condition]
        
        # Add file type complexity factors
        complexity_factors = {
            FileType.EMERGENCY: 0.9,    # Simpler processing
            FileType.DOCUMENT: 0.95,    # Easy text
            FileType.CODE: 0.95,        # Text-based
            FileType.IMAGE: 1.0,        # Standard
            FileType.AUDIO: 1.05,       # Slight compression overhead
            FileType.VIDEO: 1.2,        # More complex
            FileType.ARCHIVE: 1.15,     # Compression considerations
            FileType.OTHER: 1.0
        }
        
        complexity = complexity_factors.get(file_type, 1.0)
        effective_speed = base_speed / complexity
        
        # Add random variation (±30%)
        speed_variation = np.random.uniform(0.7, 1.3)
        actual_speed = effective_speed * speed_variation
        
        # Calculate transfer time
        base_transfer_time = file_size / actual_speed
        
        # Success probability based on conditions
        success_base_rates = {
            NetworkCondition.EXCELLENT: 0.98,
            NetworkCondition.GOOD: 0.95,
            NetworkCondition.FAIR: 0.90,
            NetworkCondition.POOR: 0.75,
            NetworkCondition.CRITICAL: 0.60
        }
        
        base_success_rate = success_base_rates[network_condition]
        
        # Larger files have slightly lower success rates
        size_penalty = min(0.1, file_size / (1024 * 1024 * 1024))  # Max 10% penalty for 1GB+
        success_rate = base_success_rate - size_penalty
        
        # Higher priority gets slight boost
        priority_boost = (user_priority.value - 3) * 0.02  # ±4% based on priority
        success_rate += priority_boost
        
        success = np.random.random() < success_rate
        
        # Generate error and retry counts
        if success:
            error_count = 0
            retry_count = 0
            actual_transfer_time = base_transfer_time * np.random.uniform(0.9, 1.1)
        else:
            error_count = np.random.randint(1, 5)
            retry_count = error_count
            actual_transfer_time = base_transfer_time * np.random.uniform(1.5, 3.0)
        
        return {
            'success': success,
            'actual_speed': actual_speed,
            'transfer_time': actual_transfer_time,
            'error_count': error_count,
            'retry_count': retry_count,
            'wait_time': np.random.uniform(0, 300)  # 0-5 minutes wait
        }
    
    def calculate_optimal_priority(self, file_type: FileType, file_size: int,
                                 user_priority: UserPriority, time_sensitive: str,
                                 network_condition: NetworkCondition) -> float:
        """Calculate what the optimal priority should be 🎯"""
        
        # Start with base file type score
        base_scores = {
            FileType.EMERGENCY: 100,
            FileType.DOCUMENT: 80,
            FileType.CODE: 75,
            FileType.IMAGE: 60,
            FileType.AUDIO: 50,
            FileType.VIDEO: 30,
            FileType.ARCHIVE: 20,
            FileType.OTHER: 40
        }
        
        score = base_scores.get(file_type, 40)
        
        # Size factor (smaller files get slight boost)
        if file_size < 1024 * 1024:  # < 1MB
            score *= 1.2
        elif file_size < 10 * 1024 * 1024:  # < 10MB
            score *= 1.1
        elif file_size > 100 * 1024 * 1024:  # > 100MB
            score *= 0.9
        
        # User priority factor
        priority_multipliers = {
            UserPriority.CRITICAL: 1.4,
            UserPriority.HIGH: 1.2,
            UserPriority.NORMAL: 1.0,
            UserPriority.LOW: 0.8,
            UserPriority.DEFERRED: 0.6
        }
        score *= priority_multipliers[user_priority]
        
        # Time sensitivity
        time_multipliers = {
            'immediate': 1.8,
            'urgent': 1.4,
            'normal': 1.0,
            'flexible': 0.8,
            'background': 0.5
        }
        score *= time_multipliers.get(time_sensitive, 1.0)
        
        # Network condition adaptation
        if network_condition in [NetworkCondition.POOR, NetworkCondition.CRITICAL]:
            if file_size < 10 * 1024 * 1024:  # Boost small files on poor networks
                score *= 1.3
            else:  # Reduce large files on poor networks
                score *= 0.7
        
        return max(1.0, min(score, 200.0))  # Keep in reasonable range
    
    def generate_comprehensive_dataset(self, num_samples: int = 1000) -> pd.DataFrame:
        """Generate a comprehensive training dataset! 📊✨"""
        
        print(f"🎨 Generating {num_samples} comprehensive training samples...")
        
        data = []
        
        for i in range(num_samples):
            # Choose file type (with emergency files being rarer)
            file_type_weights = [0.05, 0.25, 0.15, 0.20, 0.10, 0.15, 0.08, 0.02]
            file_type = np.random.choice(list(FileType), p=file_type_weights)
            
            # Generate basic file properties
            filename = self.generate_realistic_filename(file_type)
            file_size = self.generate_realistic_file_size(file_type)
            
            # Choose other properties
            user_priority = np.random.choice(list(UserPriority))
            network_condition = np.random.choice(list(NetworkCondition))
            
            # Time sensitivity based on file type and user priority
            if file_type == FileType.EMERGENCY:
                time_sensitive = np.random.choice(['immediate', 'urgent'], p=[0.7, 0.3])
            elif user_priority in [UserPriority.CRITICAL, UserPriority.HIGH]:
                time_sensitive = np.random.choice(['urgent', 'normal'], p=[0.6, 0.4])
            else:
                time_sensitive = np.random.choice(['normal', 'flexible', 'background'], p=[0.5, 0.3, 0.2])
            
            # Generate timestamp (within last 30 days)
            upload_time = datetime.now() - timedelta(
                days=np.random.randint(0, 30),
                hours=np.random.randint(0, 24),
                minutes=np.random.randint(0, 60)
            )
            
            # Calculate optimal priority
            optimal_priority = self.calculate_optimal_priority(
                file_type, file_size, user_priority, time_sensitive, network_condition
            )
            
            # Generate performance data
            performance = self.generate_transfer_performance(
                file_size, file_type, network_condition, user_priority
            )
            
            # Create chunk information
            chunk_size = min(file_size, np.random.choice([
                1*1024*1024, 2*1024*1024, 4*1024*1024, 8*1024*1024, 16*1024*1024
            ]))  # 1MB, 2MB, 4MB, 8MB, 16MB chunks
            
            # Add context tags
            context_tags = []
            if file_type == FileType.EMERGENCY:
                context_tags.extend(['critical', 'deadline'])
            if user_priority == UserPriority.CRITICAL:
                context_tags.append('high_priority')
            if time_sensitive in ['immediate', 'urgent']:
                context_tags.append('time_critical')
            
            sample = {
                'file_id': f'file_{i:06d}',
                'filename': filename,
                'file_size': file_size,
                'file_type': file_type.value,
                'user_priority': user_priority.value,
                'time_sensitive': time_sensitive,
                'network_condition': network_condition.value,
                'chunk_size': chunk_size,
                'upload_time': upload_time.isoformat(),
                'optimal_priority': optimal_priority,
                'success': performance['success'],
                'actual_speed': performance['actual_speed'],
                'transfer_time': performance['transfer_time'],
                'error_count': performance['error_count'],
                'retry_count': performance['retry_count'],
                'wait_time': performance['wait_time'],
                'context_tags': ','.join(context_tags),
                'hour_of_day': upload_time.hour,
                'day_of_week': upload_time.weekday(),
                'file_extension': os.path.splitext(filename)[1].lower()
            }
            
            data.append(sample)
            
            if (i + 1) % 100 == 0:
                print(f"   Generated {i + 1}/{num_samples} samples...")
        
        df = pd.DataFrame(data)
        print(f"✅ Generated complete dataset with {len(df)} samples!")
        
        return df
    
    def create_file_priority_dataset(self, num_samples: int = 500) -> pd.DataFrame:
        """Create a focused dataset for file priority prediction 🎯"""
        
        print(f"🎯 Creating file priority dataset with {num_samples} samples...")
        
        data = []
        
        for i in range(num_samples):
            file_type = np.random.choice(list(FileType))
            filename = self.generate_realistic_filename(file_type)
            file_size = self.generate_realistic_file_size(file_type)
            user_priority = np.random.choice(list(UserPriority))
            time_sensitive = np.random.choice(['immediate', 'urgent', 'normal', 'flexible', 'background'])
            
            # Calculate priority score
            priority_score = self.calculate_optimal_priority(
                file_type, file_size, user_priority, time_sensitive, NetworkCondition.GOOD
            )
            
            data.append({
                'filename': filename,
                'file_size': file_size,
                'file_type': file_type.value,
                'user_priority': user_priority.value,
                'time_sensitive': time_sensitive,
                'priority_score': priority_score,
                'file_extension': os.path.splitext(filename)[1].lower()
            })
        
        return pd.DataFrame(data)
    
    def create_network_performance_dataset(self, num_samples: int = 300) -> pd.DataFrame:
        """Create a dataset focused on network performance patterns 🌐"""
        
        print(f"🌐 Creating network performance dataset with {num_samples} samples...")
        
        data = []
        
        for i in range(num_samples):
            network_condition = np.random.choice(list(NetworkCondition))
            file_type = np.random.choice(list(FileType))
            file_size = self.generate_realistic_file_size(file_type)
            
            performance = self.generate_transfer_performance(
                file_size, file_type, network_condition, UserPriority.NORMAL
            )
            
            data.append({
                'network_condition': network_condition.value,
                'file_type': file_type.value,
                'file_size': file_size,
                'predicted_speed': performance['actual_speed'],
                'success_probability': 1.0 if performance['success'] else 0.0,
                'transfer_time': performance['transfer_time'],
                'error_count': performance['error_count']
            })
        
        return pd.DataFrame(data)
    
    def save_datasets(self, output_dir: str = "training_datasets"):
        """Save all our beautiful datasets! 💾"""
        
        os.makedirs(output_dir, exist_ok=True)
        
        print("💾 Creating and saving comprehensive training datasets...")
        
        # Generate different datasets
        datasets = {
            'comprehensive_dataset.csv': self.generate_comprehensive_dataset(1000),
            'file_priority_dataset.csv': self.create_file_priority_dataset(500),
            'network_performance_dataset.csv': self.create_network_performance_dataset(300),
            'small_test_dataset.csv': self.generate_comprehensive_dataset(100)
        }
        
        # Save datasets
        for filename, dataset in datasets.items():
            filepath = os.path.join(output_dir, filename)
            dataset.to_csv(filepath, index=False)
            print(f"   Saved {filename}: {len(dataset)} samples")
        
        # Create dataset documentation
        doc = {
            'datasets': {
                'comprehensive_dataset.csv': {
                    'description': 'Complete dataset with all features for training the full system',
                    'samples': len(datasets['comprehensive_dataset.csv']),
                    'features': list(datasets['comprehensive_dataset.csv'].columns),
                    'use_case': 'Training comprehensive ML models for priority, speed, and success prediction'
                },
                'file_priority_dataset.csv': {
                    'description': 'Focused dataset for file priority prediction',
                    'samples': len(datasets['file_priority_dataset.csv']),
                    'features': list(datasets['file_priority_dataset.csv'].columns),
                    'use_case': 'Training priority scoring models'
                },
                'network_performance_dataset.csv': {
                    'description': 'Network condition and performance patterns',
                    'samples': len(datasets['network_performance_dataset.csv']),
                    'features': list(datasets['network_performance_dataset.csv'].columns),
                    'use_case': 'Training network adaptation and speed prediction'
                },
                'small_test_dataset.csv': {
                    'description': 'Smaller dataset for quick testing and development',
                    'samples': len(datasets['small_test_dataset.csv']),
                    'features': list(datasets['small_test_dataset.csv'].columns),
                    'use_case': 'Development and testing'
                }
            },
            'file_types': [ft.value for ft in FileType],
            'network_conditions': [nc.value for nc in NetworkCondition],
            'user_priorities': [up.value for up in UserPriority],
            'generation_time': datetime.now().isoformat(),
            'generator_version': '1.0'
        }
        
        with open(os.path.join(output_dir, 'dataset_documentation.json'), 'w') as f:
            json.dump(doc, f, indent=2)
        
        print(f"📚 All datasets saved to {output_dir}/")
        print("✨ Ready to train the smartest file transfer system ever! 🚀")
        
        return datasets

# 🎪 Demo and generation function
def generate_all_training_data():
    """Generate all training datasets for our smart system! 🎨"""
    
    print("🎪 Welcome to the Training Dataset Generator!")
    print("=" * 60)
    
    generator = DatasetGenerator()
    datasets = generator.save_datasets()
    
    # Show some sample data
    print("\n📊 Sample from comprehensive dataset:")
    print(datasets['comprehensive_dataset.csv'].head())
    
    print("\n📈 Dataset statistics:")
    comp_dataset = datasets['comprehensive_dataset.csv']
    
    print(f"   Total samples: {len(comp_dataset)}")
    print(f"   File types distribution:")
    for file_type, count in comp_dataset['file_type'].value_counts().items():
        print(f"     {file_type}: {count} ({count/len(comp_dataset)*100:.1f}%)")
    
    print(f"   Network conditions:")
    for condition, count in comp_dataset['network_condition'].value_counts().items():
        print(f"     {condition}: {count} ({count/len(comp_dataset)*100:.1f}%)")
    
    print(f"   Success rate: {comp_dataset['success'].mean():.1%}")
    print(f"   Average file size: {comp_dataset['file_size'].mean()/1024/1024:.1f} MB")
    print(f"   Average priority score: {comp_dataset['optimal_priority'].mean():.1f}")
    
    print("\n🎉 Training data generation complete! Your AI will be super smart! 🧠✨")

if __name__ == "__main__":
    generate_all_training_data()