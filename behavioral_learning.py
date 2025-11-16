# 🧠 Behavioral Learning System - The Memory Master of Our Playground!
# This is like having a super smart teacher who remembers every kid's behavior and gets better at helping them!

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score
import joblib
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json
from dataclasses import dataclass, asdict

from smart_priority_config import *
from smart_priority_engine import FileMetrics, ChunkMetrics

@dataclass
class TransferHistory:
    """A memory of how each transfer went (like a report card) 📚"""
    file_id: str
    filename: str
    file_size: int
    file_type: str
    user_priority: int
    time_sensitive: str
    network_condition: str
    chunk_size: int
    start_time: datetime
    end_time: datetime
    success: bool
    actual_speed: float  # bytes per second
    error_count: int
    retry_count: int
    final_priority_score: float
    wait_time: float  # seconds
    total_time: float  # seconds

@dataclass
class PredictionFeatures:
    """All the features we use to make smart predictions 🔮"""
    file_size: float
    file_type_encoded: int
    user_priority: int
    time_sensitive_encoded: int
    network_condition_encoded: int
    chunk_size: float
    hour_of_day: int
    day_of_week: int
    recent_error_rate: float
    recent_avg_speed: float
    file_extension_encoded: int
    historical_success_rate: float

class BehavioralLearningSystem:
    """The amazing learning brain that gets smarter with every transfer! 🧠✨"""
    
    def __init__(self, model_dir: str = "behavioral_models"):
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        
        # Our smart models (like different types of intelligence)
        self.speed_predictor = RandomForestRegressor(n_estimators=100, random_state=42)
        self.success_predictor = GradientBoostingClassifier(n_estimators=100, random_state=42)
        self.priority_optimizer = RandomForestRegressor(n_estimators=100, random_state=42)
        
        # Feature processors (like translators for different languages)
        self.feature_scaler = StandardScaler()
        self.file_type_encoder = LabelEncoder()
        self.time_sensitive_encoder = LabelEncoder()
        self.network_encoder = LabelEncoder()
        self.extension_encoder = LabelEncoder()
        
        # Our memory storage (like a diary of all transfers)
        self.transfer_history: List[TransferHistory] = []
        self.models_trained = False
        
        # Performance tracking
        self.model_performance = {
            'speed_prediction_accuracy': 0.0,
            'success_prediction_accuracy': 0.0,
            'priority_optimization_score': 0.0,
            'last_training_time': None,
            'training_samples': 0
        }
        
        print("🧠 Behavioral Learning System initialized! Ready to get smarter! ✨")
    
    def record_transfer(self, file_metrics: FileMetrics, chunk: ChunkMetrics, 
                       success: bool, actual_speed: float, error_count: int,
                       retry_count: int, priority_score: float, 
                       start_time: datetime, end_time: datetime):
        """Remember how a transfer went (like writing in our diary) 📝"""
        
        wait_time = 0.0  # Would calculate from queue waiting time in real implementation
        total_time = (end_time - start_time).total_seconds()
        
        history_record = TransferHistory(
            file_id=file_metrics.file_id,
            filename=file_metrics.filename,
            file_size=file_metrics.file_size,
            file_type=file_metrics.file_type.value,
            user_priority=file_metrics.user_priority.value,
            time_sensitive=file_metrics.time_sensitive,
            network_condition=file_metrics.network_condition.value,
            chunk_size=chunk.chunk_size,
            start_time=start_time,
            end_time=end_time,
            success=success,
            actual_speed=actual_speed,
            error_count=error_count,
            retry_count=retry_count,
            final_priority_score=priority_score,
            wait_time=wait_time,
            total_time=total_time
        )
        
        self.transfer_history.append(history_record)
        
        # Keep memory manageable (like cleaning out old diary entries)
        if len(self.transfer_history) > 10000:
            # Keep only the most recent 8000 records
            self.transfer_history = self.transfer_history[-8000:]
        
        print(f"📝 Recorded transfer: {file_metrics.filename} - {'✅' if success else '❌'}")
        
        # Trigger retraining if we have enough new data
        if len(self.transfer_history) % 50 == 0 and len(self.transfer_history) >= 100:
            print("🎓 Enough new data collected! Time to learn more!")
            self.train_models()
    
    def prepare_features(self, file_metrics: FileMetrics, chunk: ChunkMetrics, 
                        current_time: datetime = None) -> PredictionFeatures:
        """Convert file info into features our AI can understand 🔄"""
        
        if current_time is None:
            current_time = datetime.now()
        
        # Calculate recent performance metrics
        recent_transfers = [h for h in self.transfer_history 
                          if h.end_time > current_time - timedelta(hours=1)]
        
        recent_error_rate = 0.0
        recent_avg_speed = 0.0
        
        if recent_transfers:
            recent_error_rate = sum(1 for h in recent_transfers if not h.success) / len(recent_transfers)
            successful_transfers = [h for h in recent_transfers if h.success]
            if successful_transfers:
                recent_avg_speed = np.mean([h.actual_speed for h in successful_transfers])
        
        # Calculate historical success rate for similar files
        similar_files = [h for h in self.transfer_history 
                        if h.file_type == file_metrics.file_type.value and
                        abs(h.file_size - file_metrics.file_size) < file_metrics.file_size * 0.5]
        
        historical_success_rate = 1.0
        if similar_files:
            historical_success_rate = sum(1 for h in similar_files if h.success) / len(similar_files)
        
        # Get file extension
        file_extension = os.path.splitext(file_metrics.filename)[1].lower()
        
        return PredictionFeatures(
            file_size=float(file_metrics.file_size),
            file_type_encoded=self._safe_encode(self.file_type_encoder, file_metrics.file_type.value),
            user_priority=file_metrics.user_priority.value,
            time_sensitive_encoded=self._safe_encode(self.time_sensitive_encoder, file_metrics.time_sensitive),
            network_condition_encoded=self._safe_encode(self.network_encoder, file_metrics.network_condition.value),
            chunk_size=float(chunk.chunk_size),
            hour_of_day=current_time.hour,
            day_of_week=current_time.weekday(),
            recent_error_rate=recent_error_rate,
            recent_avg_speed=recent_avg_speed,
            file_extension_encoded=self._safe_encode(self.extension_encoder, file_extension),
            historical_success_rate=historical_success_rate
        )
    
    def _safe_encode(self, encoder: LabelEncoder, value: str) -> int:
        """Safely encode a value, handling new unseen values 🛡️"""
        try:
            return encoder.transform([value])[0]
        except ValueError:
            # New value not seen during training - use most common class
            if hasattr(encoder, 'classes_') and len(encoder.classes_) > 0:
                return 0  # Use first class as default
            else:
                return 0
    
    def train_models(self):
        """Train our AI models to get smarter! 🎓"""
        
        if len(self.transfer_history) < 20:
            print("📚 Not enough data to train models yet (need at least 20 samples)")
            return
        
        print(f"🎓 Training models with {len(self.transfer_history)} samples...")
        
        # Prepare training data
        features_list = []
        speed_targets = []
        success_targets = []
        priority_targets = []
        
        for history in self.transfer_history:
            # Recreate file metrics for feature extraction
            file_metrics = FileMetrics(
                file_id=history.file_id,
                filename=history.filename,
                file_size=history.file_size,
                file_type=FileType(history.file_type),
                user_priority=UserPriority(history.user_priority),
                time_sensitive=history.time_sensitive,
                upload_start_time=history.start_time,
                network_condition=NetworkCondition(history.network_condition)
            )
            
            chunk = ChunkMetrics(
                chunk_id=f"{history.file_id}_chunk_0",
                file_id=history.file_id,
                chunk_number=0,
                chunk_size=history.chunk_size
            )
            
            features = self.prepare_features(file_metrics, chunk, history.start_time)
            features_list.append(features)
            
            # Targets for different models
            speed_targets.append(history.actual_speed)
            success_targets.append(1 if history.success else 0)
            priority_targets.append(history.final_priority_score)
        
        # Convert to arrays
        feature_arrays = self._features_to_arrays(features_list)
        
        if len(feature_arrays) == 0:
            print("❌ No valid features extracted for training")
            return
        
        # Fit encoders first
        self._fit_encoders(features_list)
        
        # Re-encode features with fitted encoders
        feature_arrays = self._features_to_arrays(features_list)
        
        # Scale features
        X_scaled = self.feature_scaler.fit_transform(feature_arrays)
        
        # Split data for training and validation
        test_size = min(0.3, max(0.1, len(X_scaled) * 0.2))
        
        try:
            # Train speed predictor
            X_train, X_test, y_speed_train, y_speed_test = train_test_split(
                X_scaled, speed_targets, test_size=test_size, random_state=42
            )
            
            self.speed_predictor.fit(X_train, y_speed_train)
            speed_pred = self.speed_predictor.predict(X_test)
            speed_accuracy = 1 - (mean_squared_error(y_speed_test, speed_pred) / np.var(y_speed_test))
            speed_accuracy = max(0, speed_accuracy)  # Ensure non-negative
            
            # Train success predictor
            X_train, X_test, y_success_train, y_success_test = train_test_split(
                X_scaled, success_targets, test_size=test_size, random_state=42
            )
            
            self.success_predictor.fit(X_train, y_success_train)
            success_pred = self.success_predictor.predict(X_test)
            success_accuracy = accuracy_score(y_success_test, success_pred)
            
            # Train priority optimizer
            X_train, X_test, y_priority_train, y_priority_test = train_test_split(
                X_scaled, priority_targets, test_size=test_size, random_state=42
            )
            
            self.priority_optimizer.fit(X_train, y_priority_train)
            priority_pred = self.priority_optimizer.predict(X_test)
            priority_accuracy = 1 - (mean_squared_error(y_priority_test, priority_pred) / np.var(y_priority_test))
            priority_accuracy = max(0, priority_accuracy)  # Ensure non-negative
            
            # Update performance metrics
            self.model_performance.update({
                'speed_prediction_accuracy': speed_accuracy,
                'success_prediction_accuracy': success_accuracy,
                'priority_optimization_score': priority_accuracy,
                'last_training_time': datetime.now(),
                'training_samples': len(self.transfer_history)
            })
            
            self.models_trained = True
            
            print(f"🎓 Models trained successfully!")
            print(f"   Speed Prediction Accuracy: {speed_accuracy:.3f}")
            print(f"   Success Prediction Accuracy: {success_accuracy:.3f}")
            print(f"   Priority Optimization Score: {priority_accuracy:.3f}")
            
            # Save models
            self.save_models()
            
        except Exception as e:
            print(f"❌ Error training models: {e}")
    
    def _fit_encoders(self, features_list: List[PredictionFeatures]):
        """Fit our encoders with all the data 🔧"""
        
        file_types = []
        time_sensitives = []
        network_conditions = []
        extensions = []
        
        for history in self.transfer_history:
            file_types.append(history.file_type)
            time_sensitives.append(history.time_sensitive)
            network_conditions.append(history.network_condition)
            
            extension = os.path.splitext(history.filename)[1].lower()
            extensions.append(extension)
        
        # Fit encoders
        if file_types:
            self.file_type_encoder.fit(file_types)
        if time_sensitives:
            self.time_sensitive_encoder.fit(time_sensitives)
        if network_conditions:
            self.network_encoder.fit(network_conditions)
        if extensions:
            self.extension_encoder.fit(extensions)
    
    def _features_to_arrays(self, features_list: List[PredictionFeatures]) -> np.ndarray:
        """Convert our features to arrays AI can work with 🔢"""
        
        if not features_list:
            return np.array([])
        
        arrays = []
        for features in features_list:
            array = [
                features.file_size,
                features.file_type_encoded,
                features.user_priority,
                features.time_sensitive_encoded,
                features.network_condition_encoded,
                features.chunk_size,
                features.hour_of_day,
                features.day_of_week,
                features.recent_error_rate,
                features.recent_avg_speed,
                features.file_extension_encoded,
                features.historical_success_rate
            ]
            arrays.append(array)
        
        return np.array(arrays)
    
    def predict_transfer_speed(self, file_metrics: FileMetrics, chunk: ChunkMetrics) -> float:
        """Predict how fast a transfer will be 🔮"""
        
        if not self.models_trained:
            # Use simple heuristic
            base_speeds = {
                NetworkCondition.EXCELLENT: 50 * 1024 * 1024,
                NetworkCondition.GOOD: 20 * 1024 * 1024,
                NetworkCondition.FAIR: 10 * 1024 * 1024,
                NetworkCondition.POOR: 2 * 1024 * 1024,
                NetworkCondition.CRITICAL: 512 * 1024
            }
            return base_speeds.get(file_metrics.network_condition, 10 * 1024 * 1024)
        
        features = self.prepare_features(file_metrics, chunk)
        feature_array = self._features_to_arrays([features])
        
        if len(feature_array) == 0:
            return 10 * 1024 * 1024  # Default 10 MB/s
        
        feature_scaled = self.feature_scaler.transform(feature_array)
        predicted_speed = self.speed_predictor.predict(feature_scaled)[0]
        
        # Ensure reasonable bounds
        return max(100 * 1024, min(predicted_speed, 100 * 1024 * 1024))  # 100KB/s to 100MB/s
    
    def predict_success_probability(self, file_metrics: FileMetrics, chunk: ChunkMetrics) -> float:
        """Predict how likely a transfer is to succeed 🎯"""
        
        if not self.models_trained:
            # Use simple heuristic based on file size and network
            if file_metrics.network_condition == NetworkCondition.CRITICAL:
                return 0.6
            elif file_metrics.file_size > 100 * 1024 * 1024:
                return 0.8
            else:
                return 0.9
        
        features = self.prepare_features(file_metrics, chunk)
        feature_array = self._features_to_arrays([features])
        
        if len(feature_array) == 0:
            return 0.8  # Default 80% success rate
        
        feature_scaled = self.feature_scaler.transform(feature_array)
        success_prob = self.success_predictor.predict_proba(feature_scaled)[0]
        
        return success_prob[1] if len(success_prob) > 1 else 0.8
    
    def optimize_priority_score(self, file_metrics: FileMetrics, chunk: ChunkMetrics, 
                               base_priority: float) -> float:
        """Use AI to optimize the priority score 🎯"""
        
        if not self.models_trained:
            return base_priority  # No optimization without training
        
        features = self.prepare_features(file_metrics, chunk)
        feature_array = self._features_to_arrays([features])
        
        if len(feature_array) == 0:
            return base_priority
        
        feature_scaled = self.feature_scaler.transform(feature_array)
        optimized_priority = self.priority_optimizer.predict(feature_scaled)[0]
        
        # Blend with base priority (don't change too drastically)
        final_priority = base_priority * 0.7 + optimized_priority * 0.3
        
        return max(1.0, min(final_priority, 200.0))  # Keep in reasonable range
    
    def get_insights(self) -> dict:
        """Get smart insights about transfer patterns 📊"""
        
        if len(self.transfer_history) < 10:
            return {"message": "Not enough data for insights yet"}
        
        insights = {}
        
        # Success rate by file type
        type_success = {}
        for file_type in FileType:
            type_transfers = [h for h in self.transfer_history if h.file_type == file_type.value]
            if type_transfers:
                success_rate = sum(1 for h in type_transfers if h.success) / len(type_transfers)
                type_success[file_type.value] = {
                    'success_rate': success_rate,
                    'total_transfers': len(type_transfers),
                    'avg_speed': np.mean([h.actual_speed for h in type_transfers if h.success])
                }
        
        insights['file_type_performance'] = type_success
        
        # Network condition analysis
        network_performance = {}
        for condition in NetworkCondition:
            condition_transfers = [h for h in self.transfer_history 
                                 if h.network_condition == condition.value]
            if condition_transfers:
                success_rate = sum(1 for h in condition_transfers if h.success) / len(condition_transfers)
                network_performance[condition.value] = {
                    'success_rate': success_rate,
                    'total_transfers': len(condition_transfers),
                    'avg_speed': np.mean([h.actual_speed for h in condition_transfers if h.success])
                }
        
        insights['network_performance'] = network_performance
        
        # Time-based patterns
        hour_performance = {}
        for hour in range(24):
            hour_transfers = [h for h in self.transfer_history if h.start_time.hour == hour]
            if hour_transfers:
                success_rate = sum(1 for h in hour_transfers if h.success) / len(hour_transfers)
                hour_performance[hour] = {
                    'success_rate': success_rate,
                    'total_transfers': len(hour_transfers)
                }
        
        insights['hourly_performance'] = hour_performance
        
        # Model performance
        insights['model_performance'] = self.model_performance.copy()
        
        return insights
    
    def save_models(self):
        """Save our trained models (like keeping our smart books) 💾"""
        
        if not self.models_trained:
            print("⚠️ No trained models to save")
            return
        
        try:
            # Save models
            joblib.dump(self.speed_predictor, os.path.join(self.model_dir, 'speed_predictor.pkl'))
            joblib.dump(self.success_predictor, os.path.join(self.model_dir, 'success_predictor.pkl'))
            joblib.dump(self.priority_optimizer, os.path.join(self.model_dir, 'priority_optimizer.pkl'))
            
            # Save encoders and scalers
            joblib.dump(self.feature_scaler, os.path.join(self.model_dir, 'feature_scaler.pkl'))
            joblib.dump(self.file_type_encoder, os.path.join(self.model_dir, 'file_type_encoder.pkl'))
            joblib.dump(self.time_sensitive_encoder, os.path.join(self.model_dir, 'time_sensitive_encoder.pkl'))
            joblib.dump(self.network_encoder, os.path.join(self.model_dir, 'network_encoder.pkl'))
            joblib.dump(self.extension_encoder, os.path.join(self.model_dir, 'extension_encoder.pkl'))
            
            # Save history and metadata
            history_data = [asdict(h) for h in self.transfer_history]
            # Convert datetime objects to strings
            for record in history_data:
                record['start_time'] = record['start_time'].isoformat()
                record['end_time'] = record['end_time'].isoformat()
            
            with open(os.path.join(self.model_dir, 'transfer_history.json'), 'w') as f:
                json.dump(history_data, f, indent=2)
            
            with open(os.path.join(self.model_dir, 'model_metadata.json'), 'w') as f:
                metadata = self.model_performance.copy()
                if metadata['last_training_time']:
                    metadata['last_training_time'] = metadata['last_training_time'].isoformat()
                json.dump(metadata, f, indent=2)
            
            print(f"💾 Behavioral learning models saved to {self.model_dir}")
            
        except Exception as e:
            print(f"❌ Error saving models: {e}")
    
    def load_models(self):
        """Load our previously trained models (like reading our smart books) 📖"""
        
        try:
            model_files = [
                'speed_predictor.pkl', 'success_predictor.pkl', 'priority_optimizer.pkl',
                'feature_scaler.pkl', 'file_type_encoder.pkl', 'time_sensitive_encoder.pkl',
                'network_encoder.pkl', 'extension_encoder.pkl'
            ]
            
            # Check if all model files exist
            if not all(os.path.exists(os.path.join(self.model_dir, f)) for f in model_files):
                print("📝 No complete model set found, starting fresh!")
                return False
            
            # Load models
            self.speed_predictor = joblib.load(os.path.join(self.model_dir, 'speed_predictor.pkl'))
            self.success_predictor = joblib.load(os.path.join(self.model_dir, 'success_predictor.pkl'))
            self.priority_optimizer = joblib.load(os.path.join(self.model_dir, 'priority_optimizer.pkl'))
            
            # Load encoders and scalers
            self.feature_scaler = joblib.load(os.path.join(self.model_dir, 'feature_scaler.pkl'))
            self.file_type_encoder = joblib.load(os.path.join(self.model_dir, 'file_type_encoder.pkl'))
            self.time_sensitive_encoder = joblib.load(os.path.join(self.model_dir, 'time_sensitive_encoder.pkl'))
            self.network_encoder = joblib.load(os.path.join(self.model_dir, 'network_encoder.pkl'))
            self.extension_encoder = joblib.load(os.path.join(self.model_dir, 'extension_encoder.pkl'))
            
            # Load history
            history_file = os.path.join(self.model_dir, 'transfer_history.json')
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    history_data = json.load(f)
                
                self.transfer_history = []
                for record in history_data:
                    record['start_time'] = datetime.fromisoformat(record['start_time'])
                    record['end_time'] = datetime.fromisoformat(record['end_time'])
                    self.transfer_history.append(TransferHistory(**record))
            
            # Load metadata
            metadata_file = os.path.join(self.model_dir, 'model_metadata.json')
            if os.path.exists(metadata_file):
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                
                if metadata.get('last_training_time'):
                    metadata['last_training_time'] = datetime.fromisoformat(metadata['last_training_time'])
                
                self.model_performance.update(metadata)
            
            self.models_trained = True
            print(f"📖 Behavioral learning models loaded from {self.model_dir}")
            print(f"   History: {len(self.transfer_history)} records")
            print(f"   Last training: {self.model_performance.get('last_training_time', 'Unknown')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            return False

# 🎪 Demo function
def demo_behavioral_learning():
    """Show how our learning system gets smarter! 🧠✨"""
    
    print("🧠 Welcome to the Behavioral Learning System Demo!")
    print("=" * 60)
    
    # Create learning system
    learning_system = BehavioralLearningSystem("demo_models")
    
    # Try to load existing models
    learning_system.load_models()
    
    # Generate some sample transfer history
    print("📚 Generating sample transfer history...")
    
    sample_files = [
        ("emergency_doc.pdf", FileType.EMERGENCY, 5*1024*1024, UserPriority.CRITICAL),
        ("video_file.mp4", FileType.VIDEO, 200*1024*1024, UserPriority.NORMAL),
        ("backup.zip", FileType.ARCHIVE, 50*1024*1024, UserPriority.LOW),
        ("presentation.pptx", FileType.DOCUMENT, 25*1024*1024, UserPriority.HIGH),
        ("photo.jpg", FileType.IMAGE, 10*1024*1024, UserPriority.NORMAL),
    ]
    
    # Simulate transfers
    for i in range(30):  # Generate 30 sample transfers
        filename, file_type, size, priority = sample_files[i % len(sample_files)]
        
        file_metrics = FileMetrics(
            file_id=f"file_{i}",
            filename=f"{i}_{filename}",
            file_size=size + (i * 1024 * 1024),  # Vary sizes
            file_type=file_type,
            user_priority=priority,
            time_sensitive="normal",
            upload_start_time=datetime.now() - timedelta(hours=i),
            network_condition=list(NetworkCondition)[i % len(NetworkCondition)]
        )
        
        chunk = ChunkMetrics(
            chunk_id=f"chunk_{i}",
            file_id=file_metrics.file_id,
            chunk_number=0,
            chunk_size=min(5*1024*1024, size)
        )
        
        # Simulate transfer results
        success = np.random.random() > 0.2  # 80% success rate
        speed = np.random.uniform(1*1024*1024, 20*1024*1024)  # 1-20 MB/s
        error_count = 0 if success else np.random.randint(1, 4)
        retry_count = error_count
        priority_score = 50 + np.random.uniform(-20, 20)
        start_time = datetime.now() - timedelta(hours=i, minutes=30)
        end_time = start_time + timedelta(seconds=size/speed)
        
        learning_system.record_transfer(
            file_metrics, chunk, success, speed, error_count,
            retry_count, priority_score, start_time, end_time
        )
    
    print(f"📚 Generated {len(learning_system.transfer_history)} transfer records")
    
    # Make some predictions
    print("\n🔮 Making smart predictions...")
    
    test_file = FileMetrics(
        file_id="test_file",
        filename="test_document.pdf",
        file_size=15*1024*1024,
        file_type=FileType.DOCUMENT,
        user_priority=UserPriority.HIGH,
        time_sensitive="urgent",
        upload_start_time=datetime.now(),
        network_condition=NetworkCondition.GOOD
    )
    
    test_chunk = ChunkMetrics(
        chunk_id="test_chunk",
        file_id="test_file",
        chunk_number=0,
        chunk_size=5*1024*1024
    )
    
    predicted_speed = learning_system.predict_transfer_speed(test_file, test_chunk)
    success_prob = learning_system.predict_success_probability(test_file, test_chunk)
    optimized_priority = learning_system.optimize_priority_score(test_file, test_chunk, 75.0)
    
    print(f"   Predicted Speed: {predicted_speed / (1024*1024):.2f} MB/s")
    print(f"   Success Probability: {success_prob:.2%}")
    print(f"   Optimized Priority: {optimized_priority:.2f} (was 75.0)")
    
    # Show insights
    print("\n📊 Smart insights from our learning:")
    insights = learning_system.get_insights()
    
    if 'file_type_performance' in insights:
        print("   File Type Performance:")
        for file_type, perf in insights['file_type_performance'].items():
            print(f"     {file_type}: {perf['success_rate']:.1%} success, "
                  f"{perf['avg_speed']/(1024*1024):.1f} MB/s avg")
    
    if 'network_performance' in insights:
        print("   Network Performance:")
        for condition, perf in insights['network_performance'].items():
            print(f"     {condition}: {perf['success_rate']:.1%} success, "
                  f"{perf['avg_speed']/(1024*1024):.1f} MB/s avg")
    
    # Save models
    learning_system.save_models()
    
    print("\n✨ Behavioral Learning System demo complete! We're getting smarter! 🎉")

if __name__ == "__main__":
    demo_behavioral_learning()