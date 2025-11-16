import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
import mimetypes
from datetime import datetime
import re
from config import Config

class PriorityMLModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.extension_encoder = LabelEncoder()
        self.is_trained = False
        self.feature_columns = Config.FEATURE_COLUMNS
        
        # Emergency keywords for feature extraction
        self.emergency_keywords = [
            'emergency', 'urgent', 'critical', 'alert', 'asap', 'priority',
            'immediate', 'rush', 'crisis', 'important', 'deadline'
        ]
        
        # File type mappings
        self.file_type_mapping = {
            'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'],
            'document': ['.txt', '.doc', '.docx', '.pdf', '.rtf', '.odt', '.csv', '.xlsx'],
            'video': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv'],
            'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
            'archive': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c'],
            'graphic': ['.psd', '.ai', '.eps', '.indd', '.sketch', '.fig']
        }
    
    def load_and_prepare_dataset(self, dataset_path=None):
        """Load dataset and prepare features for training"""
        if dataset_path is None:
            dataset_path = Config.DATASET_PATH
            
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"Dataset file not found: {dataset_path}")
        
        # Load the Excel file
        try:
            df = pd.read_excel(dataset_path)
            print(f"Dataset loaded successfully with {len(df)} rows")
            print(f"Columns found: {list(df.columns)}")
            
            # Display first few rows to understand the structure
            print("\nFirst 5 rows of the dataset:")
            print(df.head())
            
            return df
            
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return None
    
    def extract_features(self, filename, file_size, file_path=None):
        """Extract features from file information"""
        features = {}
        
        # Basic file information
        features['file_size'] = file_size
        features['filename_length'] = len(filename)
        
        # File extension
        file_ext = os.path.splitext(filename)[1].lower()
        features['file_extension'] = file_ext
        
        # Emergency keywords detection
        filename_lower = filename.lower()
        features['has_emergency_keywords'] = int(any(
            keyword in filename_lower for keyword in self.emergency_keywords
        ))
        
        # Time-based features (if file exists)
        if file_path and os.path.exists(file_path):
            creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
            features['creation_time_hour'] = creation_time.hour
        else:
            features['creation_time_hour'] = datetime.now().hour
        
        # File type category
        file_type = 'other'
        for category, extensions in self.file_type_mapping.items():
            if file_ext in extensions:
                file_type = category
                break
        features['file_type_category'] = file_type
        
        return features
    
    def prepare_training_data(self, df):
        """Prepare the dataset for training"""
        # Check if required columns exist
        required_columns = ['filename', 'file_size', 'priority']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"Missing required columns: {missing_columns}")
            print("Available columns:", list(df.columns))
            
            # Try to map common column names
            column_mapping = {
                'file_name': 'filename',
                'size': 'file_size',
                'priority_level': 'priority',
                'category': 'priority'
            }
            
            for old_name, new_name in column_mapping.items():
                if old_name in df.columns and new_name in missing_columns:
                    df = df.rename(columns={old_name: new_name})
                    print(f"Mapped column '{old_name}' to '{new_name}'")
        
        # Extract features for each file
        feature_data = []
        
        for idx, row in df.iterrows():
            try:
                filename = str(row['filename'])
                file_size = int(row['file_size']) if pd.notna(row['file_size']) else 0
                
                # Extract features
                features = self.extract_features(filename, file_size)
                features['priority'] = row['priority']
                
                feature_data.append(features)
                
            except Exception as e:
                print(f"Error processing row {idx}: {e}")
                continue
        
        # Convert to DataFrame
        feature_df = pd.DataFrame(feature_data)
        
        # Encode categorical features
        if len(feature_df) > 0:
            # Encode file extensions
            feature_df['file_extension_encoded'] = self.extension_encoder.fit_transform(
                feature_df['file_extension'].astype(str)
            )
            
            # Encode file type categories
            feature_df['file_type_encoded'] = pd.Categorical(
                feature_df['file_type_category']
            ).codes
            
            print(f"Prepared {len(feature_df)} samples for training")
            print(f"Features: {list(feature_df.columns)}")
            
        return feature_df
    
    def train_model(self, dataset_path=None):
        """Train the ML model on the dataset"""
        # Load and prepare data
        df = self.load_and_prepare_dataset(dataset_path)
        if df is None:
            return False
        
        # Prepare training data
        feature_df = self.prepare_training_data(df)
        
        if len(feature_df) == 0:
            print("No valid training data found")
            return False
        
        # Prepare features and target
        feature_columns = [
            'file_size', 'filename_length', 'has_emergency_keywords',
            'creation_time_hour', 'file_extension_encoded', 'file_type_encoded'
        ]
        
        X = feature_df[feature_columns]
        y = feature_df['priority']
        
        # Encode target labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Split the data (reduce test size for small datasets)
        test_size = min(0.3, max(0.1, len(X) * 0.2))  # Adaptive test size
        if len(X) < 20:
            # For very small datasets, don't stratify
            X_train, X_test, y_train, y_test = train_test_split(
                X, y_encoded, test_size=test_size, random_state=42
            )
        else:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y_encoded, test_size=test_size, random_state=42, stratify=y_encoded
            )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train the model
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=10,
            min_samples_split=5
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate the model
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Model trained successfully!")
        print(f"Accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(
            y_test, y_pred, 
            target_names=self.label_encoder.classes_
        ))
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nFeature Importance:")
        print(feature_importance)
        
        self.is_trained = True
        
        # Save the model
        self.save_model()
        
        return True
    
    def predict_priority(self, filename, file_size, file_path=None):
        """Predict priority for a single file"""
        if not self.is_trained and not self.load_model():
            # Fallback to rule-based prediction
            return self._rule_based_prediction(filename, file_size)
        
        # Extract features
        features = self.extract_features(filename, file_size, file_path)
        
        # Prepare feature vector
        feature_vector = np.array([[
            features['file_size'],
            features['filename_length'],
            features['has_emergency_keywords'],
            features['creation_time_hour'],
            self._encode_extension(features['file_extension']),
            self._encode_file_type(features['file_type_category'])
        ]])
        
        # Scale features
        feature_vector_scaled = self.scaler.transform(feature_vector)
        
        # Make prediction
        prediction = self.model.predict(feature_vector_scaled)[0]
        probability = self.model.predict_proba(feature_vector_scaled)[0]
        
        # Convert back to category
        priority_category = self.label_encoder.inverse_transform([prediction])[0]
        confidence = max(probability)
        
        return {
            'category': priority_category,
            'confidence': confidence,
            'features_used': features
        }
    
    def _encode_extension(self, extension):
        """Encode file extension, handling unseen extensions"""
        try:
            return self.extension_encoder.transform([extension])[0]
        except:
            return 0  # Default for unseen extensions
    
    def _encode_file_type(self, file_type):
        """Encode file type category"""
        type_mapping = {
            'image': 0, 'document': 1, 'video': 2, 'audio': 3,
            'archive': 4, 'code': 5, 'graphic': 6, 'other': 7
        }
        return type_mapping.get(file_type, 7)
    
    def _rule_based_prediction(self, filename, file_size):
        """Fallback rule-based prediction when ML model is not available"""
        features = self.extract_features(filename, file_size)
        
        # Rule-based logic
        if features['has_emergency_keywords']:
            return {'category': 'emergency', 'confidence': 0.9, 'method': 'rule_based'}
        elif features['file_type_category'] == 'graphic':
            return {'category': 'graphic_heavy', 'confidence': 0.8, 'method': 'rule_based'}
        elif features['file_type_category'] == 'video':
            return {'category': 'video', 'confidence': 0.8, 'method': 'rule_based'}
        elif features['file_type_category'] == 'image':
            return {'category': 'image', 'confidence': 0.8, 'method': 'rule_based'}
        elif features['file_type_category'] == 'document':
            return {'category': 'text', 'confidence': 0.8, 'method': 'rule_based'}
        else:
            return {'category': 'other', 'confidence': 0.7, 'method': 'rule_based'}
    
    def save_model(self):
        """Save the trained model and encoders"""
        os.makedirs(Config.MODEL_PATH, exist_ok=True)
        
        if self.model:
            joblib.dump(self.model, os.path.join(Config.MODEL_PATH, Config.MODEL_FILE))
            joblib.dump(self.scaler, os.path.join(Config.MODEL_PATH, Config.SCALER_FILE))
            joblib.dump(self.label_encoder, os.path.join(Config.MODEL_PATH, Config.LABEL_ENCODER_FILE))
            joblib.dump(self.extension_encoder, os.path.join(Config.MODEL_PATH, 'extension_encoder.pkl'))
            
            print("Model saved successfully!")
    
    def load_model(self):
        """Load the trained model and encoders"""
        try:
            model_path = os.path.join(Config.MODEL_PATH, Config.MODEL_FILE)
            scaler_path = os.path.join(Config.MODEL_PATH, Config.SCALER_FILE)
            label_encoder_path = os.path.join(Config.MODEL_PATH, Config.LABEL_ENCODER_FILE)
            extension_encoder_path = os.path.join(Config.MODEL_PATH, 'extension_encoder.pkl')
            
            if all(os.path.exists(path) for path in [model_path, scaler_path, label_encoder_path]):
                self.model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path)
                self.label_encoder = joblib.load(label_encoder_path)
                self.extension_encoder = joblib.load(extension_encoder_path)
                self.is_trained = True
                print("Model loaded successfully!")
                return True
        except Exception as e:
            print(f"Error loading model: {e}")
        
        return False