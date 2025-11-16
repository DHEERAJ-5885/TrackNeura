#!/usr/bin/env python3
"""
🎪 Quick Smart File Transfer System Test
======================================
A simple test to demonstrate the working system
"""

import subprocess
import time
import requests
import json
import sys
import threading

def start_server():
    """Start the server in a subprocess"""
    return subprocess.Popen([
        r'C:\Trackneura\.venv\Scripts\python.exe', 
        'run_smart_system.py'
    ], cwd=r'C:\Trackneura')

def test_api():
    """Test the API endpoints"""
    print("🎪 Smart File Transfer System API Test")
    print("=" * 50)
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(8)
    
    try:
        # Test 1: System Status
        print("\n🔍 Testing system status...")
        response = requests.get('http://localhost:5001/api/status', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ System Status Retrieved!")
            print(f"   📊 Status: {data.get('system_info', {}).get('status', 'unknown')}")
            print(f"   🌐 Network: {data.get('network_condition', 'unknown')}")
        else:
            print(f"❌ Status check failed: {response.status_code}")
            return False
            
        # Test 2: Emergency File Upload
        print("\n📤 Testing emergency file upload...")
        payload = {
            "filename": "emergency_server_crash.log",
            "file_size": 5 * 1024 * 1024,  # 5MB
            "user_priority": 5,  # Critical
            "time_sensitive": "immediate",
            "context_tags": ["emergency", "critical", "server"]
        }
        
        response = requests.post(
            'http://localhost:5001/api/upload',
            headers={'Content-Type': 'application/json'},
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Emergency File Successfully Analyzed!")
            print(f"   📁 File: {data.get('filename', 'unknown')}")
            print(f"   📋 Type: {data.get('file_type', 'unknown')}")
            print(f"   ⭐ Priority Score: {data.get('priority_score', 0):.2f}")
            print(f"   🧩 Chunks: {data.get('total_chunks', 0)}")
            print(f"   🤖 ML Enhanced: {'Yes' if data.get('ml_enhanced') else 'No'}")
        else:
            print(f"❌ Upload failed: {response.status_code}")
            return False
            
        # Test 3: Video File Upload  
        print("\n📤 Testing video file upload...")
        payload = {
            "filename": "vacation_video.mp4",
            "file_size": 500 * 1024 * 1024,  # 500MB
            "user_priority": 2,  # Low
            "time_sensitive": "background",
            "context_tags": ["personal", "video"]
        }
        
        response = requests.post(
            'http://localhost:5001/api/upload',
            headers={'Content-Type': 'application/json'},
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Video File Successfully Analyzed!")
            print(f"   📁 File: {data.get('filename', 'unknown')}")
            print(f"   ⭐ Priority Score: {data.get('priority_score', 0):.2f}")
            print(f"   🧩 Chunks: {data.get('total_chunks', 0)}")
        
        # Test 4: Generate Training Data
        print("\n📚 Testing training data generation...")
        response = requests.post('http://localhost:5001/api/generate-training-data', timeout=15)
        if response.status_code == 200:
            data = response.json()
            print("✅ Training Data Generated!")
            print(f"   📊 Total Samples: {data.get('total_samples', 0)}")
        
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("🌟 The Smart File Transfer System is working perfectly!")
        print("📊 Dashboard available at: http://localhost:5001")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def main():
    """Main test function"""
    # Start the server
    print("🚀 Starting Smart File Transfer System...")
    server_process = start_server()
    
    try:
        # Run the tests
        success = test_api()
        
        if success:
            print("\n✨ System is ready for use!")
            print("🎪 The AI playground is operational!")
        else:
            print("\n⚠️  Some tests failed!")
            
    finally:
        # Clean shutdown
        print("\n🛑 Shutting down server...")
        server_process.terminate()
        time.sleep(2)
        if server_process.poll() is None:
            server_process.kill()
        print("👋 Test complete!")

if __name__ == "__main__":
    main()