#!/usr/bin/env python3
"""
Script to train the ML model on dataset.xlsx
"""

import sys
import os
from ml_model import PriorityMLModel
from config import Config

def main():
    """Train the priority prediction model"""
    print("Starting model training...")
    
    # Check if dataset exists
    if not os.path.exists(Config.DATASET_PATH):
        print(f"Dataset file not found: {Config.DATASET_PATH}")
        print("Please make sure 'dataset.xlsx' is in the root directory")
        return False
    
    # Initialize the ML model
    ml_model = PriorityMLModel()
    
    # Train the model
    success = ml_model.train_model(Config.DATASET_PATH)
    
    if success:
        print("\n✅ Model training completed successfully!")
        print(f"Model saved to: {Config.MODEL_PATH}")
        return True
    else:
        print("\n❌ Model training failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)