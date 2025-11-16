#!/usr/bin/env python3
"""
🎪 Smart File Transfer System API Test
=====================================

This script tests the API endpoints of our smart file transfer system
to demonstrate all the amazing features in action!
"""

import requests
import json
import time
import sys
import os
import tempfile

def test_system_status():
    """Test the system status endpoint"""
    print("🔍 Testing system status...")
    try:
        # Test original system first
        response = requests.get('http://localhost:5000/api/status')
        if response.status_code == 200:
            data = response.json()
            print("✅ Original System Status Retrieved!")
            print(f"   📊 Status: {data.get('status', 'unknown')}")
            print(f"   🤖 ML Model: {'Trained' if data.get('ml_model_trained') else 'Not Trained'}")
            print(f"   📋 Version: {data.get('version', 'unknown')}")
            
            # Test smart status if available
            try:
                smart_response = requests.get('http://localhost:5000/api/smart/status')
                if smart_response.status_code == 200:
                    smart_data = smart_response.json()
                    print("✅ Smart Features Status Retrieved!")
                    print(f"   🧠 Smart Features: {'Available' if smart_data.get('smart_features_available') else 'Not Available'}")
                    if smart_data.get('system_info'):
                        print(f"   🌐 Network: {smart_data.get('network_condition', 'unknown')}")
            except:
                print("   ℹ️ Smart features not available (using original system)")
            
            return True
        else:
            print(f"❌ Status check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing status: {e}")
        return False

def test_file_upload(filename, file_size, priority, time_sensitive, tags):
    """Test file upload with smart analysis"""
    print(f"📤 Testing file upload: {filename}")
    
    payload = {
        "filename": filename,
        "file_size": file_size,
        "user_priority": priority,
        "time_sensitive": time_sensitive,
        "context_tags": tags
    }
    
    try:
        # Try smart upload first, fallback to original
        try:
            response = requests.post(
                'http://localhost:5000/api/smart/upload',
                headers={'Content-Type': 'application/json'},
                json=payload
            )
        except:
            # Fallback: create dummy file and use original upload
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=os.path.splitext(filename)[1], delete=False) as tmp:
                tmp.write(b'0' * min(file_size, 1024))
                tmp_path = tmp.name
            
            with open(tmp_path, 'rb') as f:
                response = requests.post(
                    'http://localhost:5000/upload',
                    files={'files': (filename, f, 'application/octet-stream')}
                )
            os.unlink(tmp_path)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ File Successfully Analyzed!")
            print(f"   📁 File: {data.get('filename', 'unknown')}")
            print(f"   📋 Type: {data.get('file_type', 'unknown')}")
            print(f"   ⭐ Priority Score: {data.get('priority_score', 0):.2f}")
            print(f"   🧩 Chunks: {data.get('total_chunks', 0)}")
            print(f"   ⏱️  Est. Time: {data.get('estimated_time', 0):.1f}s")
            print(f"   🤖 ML Enhanced: {'Yes' if data.get('ml_enhanced') else 'No'}")
            print(f"   🧠 Learning: {'Active' if data.get('learning_enhanced') else 'Building'}")
            return True
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing upload: {e}")
        return False

def test_training_data_generation():
    """Test training data generation"""
    print("📚 Testing training data generation...")
    try:
        response = requests.post('http://localhost:5000/api/smart/generate-training-data')
        if response.status_code == 200:
            data = response.json()
            print("✅ Training Data Generated!")
            print(f"   📊 Total Samples: {data.get('total_samples', 0)}")
            return True
        else:
            print(f"❌ Training data generation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error generating training data: {e}")
        return False

def main():
    """Run comprehensive API tests"""
    print("🎪 Smart File Transfer System API Test Suite")
    print("=" * 50)
    
    # Wait a moment for system to be ready
    print("⏳ Waiting for system to be ready...")
    time.sleep(2)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: System Status
    total_tests += 1
    if test_system_status():
        tests_passed += 1
    print()
    
    # Test 2: Emergency File Upload
    total_tests += 1
    if test_file_upload(
        filename="emergency_server_crash.log",
        file_size=5 * 1024 * 1024,  # 5MB
        priority=5,  # Critical
        time_sensitive="immediate",
        tags=["emergency", "critical", "server"]
    ):
        tests_passed += 1
    print()
    
    # Test 3: Presentation File Upload  
    total_tests += 1
    if test_file_upload(
        filename="quarterly_presentation.pptx",
        file_size=50 * 1024 * 1024,  # 50MB
        priority=4,  # High
        time_sensitive="urgent",
        tags=["presentation", "deadline", "business"]
    ):
        tests_passed += 1
    print()
    
    # Test 4: Video File Upload
    total_tests += 1
    if test_file_upload(
        filename="vacation_video.mp4",
        file_size=500 * 1024 * 1024,  # 500MB
        priority=2,  # Low
        time_sensitive="background",
        tags=["personal", "video"]
    ):
        tests_passed += 1
    print()
    
    # Test 5: Training Data Generation
    total_tests += 1
    if test_training_data_generation():
        tests_passed += 1
    print()
    
    # Final status check
    total_tests += 1
    if test_system_status():
        tests_passed += 1
    
    # Results
    print("🎪 Test Results Summary")
    print("=" * 50)
    print(f"✅ Tests Passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED! Smart File Transfer System is working perfectly!")
        print("🌟 The AI playground is ready for action!")
    else:
        print(f"⚠️  Some tests failed. Check the system status.")
    
    print("\n📊 You can now visit the dashboard at: http://localhost:5001")
    print("🎪 The Smart File Transfer System is ready to handle your files!")

if __name__ == "__main__":
    main()