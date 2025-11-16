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
