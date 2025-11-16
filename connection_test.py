#!/usr/bin/env python3
"""
🔍 Simple Connection Test
========================
Quick test to see if the server is responding
"""

import requests
import time

def test_connection():
    """Test basic connection to the server"""
    try:
        print("🔍 Testing connection to http://localhost:5000...")
        response = requests.get('http://localhost:5000', timeout=10)
        print(f"✅ Server is responding! Status Code: {response.status_code}")
        
        # Test API status
        try:
            api_response = requests.get('http://localhost:5000/api/status', timeout=10)
            if api_response.status_code == 200:
                data = api_response.json()
                print(f"✅ API Status: {data.get('status', 'unknown')}")
                print(f"✅ ML Model: {'Trained' if data.get('ml_model_trained') else 'Not Trained'}")
            else:
                print(f"⚠️ API Status Code: {api_response.status_code}")
        except Exception as e:
            print(f"⚠️ API test failed: {e}")
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - server may not be running")
        return False
    except requests.exceptions.Timeout:
        print("❌ Connection timeout - server is not responding")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🎪 Connection Test")
    print("=" * 30)
    
    # Give server time to start
    print("⏳ Waiting for server...")
    time.sleep(3)
    
    if test_connection():
        print("\n🎉 SUCCESS! Your system is working!")
        print("🌐 Visit: http://localhost:5000")
        print("📤 Upload: http://localhost:5000/upload")
        print("📊 Dashboard: http://localhost:5000/dashboard")
    else:
        print("\n⚠️ Server connection failed. Check if app.py is running.")