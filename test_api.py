import requests
import json

# Test the Priority Analyzer API
BASE_URL = 'http://localhost:5000'

def test_status():
    """Test the health check endpoint"""
    response = requests.get(f'{BASE_URL}/api/status')
    print("Status:", response.json())

def test_model_status():
    """Test model status endpoint"""
    response = requests.get(f'{BASE_URL}/api/model/status')
    result = response.json()
    print("Model Status:", json.dumps(result, indent=2))

def test_file_upload():
    """Test file upload and analysis"""
    # Create sample files for testing
    files = [
        ('files', ('emergency_report.pdf', b'Sample emergency file content', 'application/pdf')),
        ('files', ('image.jpg', b'Sample image content', 'image/jpeg')),
        ('files', ('document.txt', b'Sample text content', 'text/plain')),
        ('files', ('graphics.psd', b'Sample graphics content', 'application/octet-stream')),
    ]
    
    response = requests.post(f'{BASE_URL}/api/analyze', files=files)
    result = response.json()
    print("Upload Result:", json.dumps(result, indent=2))
    
    return result.get('upload_id')

def test_priority_info(upload_id):
    """Test getting priority information"""
    response = requests.get(f'{BASE_URL}/api/priority/{upload_id}')
    result = response.json()
    print("Priority Info:", json.dumps(result, indent=2))
    
    return result['files'][0]['file_id'] if result['files'] else None

def test_chunk_info(upload_id, file_id):
    """Test getting chunk information"""
    response = requests.get(f'{BASE_URL}/api/chunk/{upload_id}/{file_id}')
    result = response.json()
    print("Chunk Info:", json.dumps(result, indent=2))

if __name__ == '__main__':
    print("Testing Priority Analyzer API...")
    
    # Test status
    test_status()
    
    # Test model status
    test_model_status()
    
    # Test file upload
    upload_id = test_file_upload()
    
    if upload_id:
        # Test priority info
        file_id = test_priority_info(upload_id)
        
        if file_id:
            # Test chunk info
            test_chunk_info(upload_id, file_id)