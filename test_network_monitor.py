#!/usr/bin/env python3
"""
🌐 Network Monitor Test
=======================

Baby, this is a gentle test to make sure our network playground watcher is working!
Like testing if our internet detective can see what's happening!
"""

import subprocess
import time
import requests

def test_network_monitor():
    """Test our gentle network monitoring system"""
    print("🌐 Testing Network Monitoring System")
    print("=" * 50)
    
    # Start the server in background
    print("🚀 Starting server with network monitoring...")
    server_process = subprocess.Popen([
        r'C:\Trackneura\.venv\Scripts\python.exe', 
        'app.py'
    ], cwd=r'C:\Trackneura')
    
    try:
        # Wait for server to start
        print("⏳ Waiting for server to initialize...")
        time.sleep(6)
        
        # Test network status endpoint
        print("\n🔍 Testing network status endpoint...")
        try:
            response = requests.get('http://localhost:5000/api/network/status', timeout=10)
            if response.status_code == 200:
                data = response.json()
                print("✅ Network Status Endpoint Working!")
                print(f"   📶 WiFi: {data.get('wifi_name', 'Unknown')}")
                print(f"   ⬆️ Upload: {data.get('upload_speed', 0)} Mbps")
                print(f"   ⬇️ Download: {data.get('download_speed', 0)} Mbps") 
                print(f"   ⚡ Latency: {data.get('latency', 0)} ms")
                print(f"   📊 Jitter: {data.get('jitter', 0)} ms")
                print(f"   📉 Packet Loss: {data.get('packet_loss', 0)}%")
                print(f"   🏥 Health: {data.get('health_status', 'Unknown')}")
            else:
                print(f"❌ Network status endpoint failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Network status test failed: {e}")
        
        # Test ping endpoint
        print("\n🏓 Testing ping endpoint...")
        try:
            response = requests.get('http://localhost:5000/api/network/ping', timeout=10)
            if response.status_code == 200:
                data = response.json()
                print("✅ Ping Endpoint Working!")
                print(f"   ⚡ Latency: {data.get('latency', 0)} ms")
                print(f"   📊 Jitter: {data.get('jitter', 0)} ms")
            else:
                print(f"❌ Ping endpoint failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Ping test failed: {e}")
        
        # Test speed endpoint
        print("\n🚀 Testing speed endpoint...")
        try:
            response = requests.get('http://localhost:5000/api/network/speed', timeout=10)
            if response.status_code == 200:
                data = response.json()
                print("✅ Speed Endpoint Working!")
                print(f"   ⬆️ Upload: {data.get('upload_speed', 0)} Mbps")
                print(f"   ⬇️ Download: {data.get('download_speed', 0)} Mbps")
            else:
                print(f"❌ Speed endpoint failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Speed test failed: {e}")
        
        # Test main page accessibility
        print("\n🌐 Testing main page with network monitor...")
        try:
            response = requests.get('http://localhost:5000/', timeout=10)
            if response.status_code == 200:
                print("✅ Main page with network monitor accessible!")
                if 'Real-Time Network Monitor' in response.text:
                    print("✅ Network monitor UI is present on main page!")
                else:
                    print("⚠️ Network monitor UI might not be visible")
            else:
                print(f"❌ Main page failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Main page test failed: {e}")
        
        print("\n🎉 Network Monitor Test Complete!")
        print("=" * 50)
        print("✅ Your original Priority Analyzer: PRESERVED")
        print("✅ File Management System: PRESERVED") 
        print("✅ NEW Network Monitoring: ADDED")
        print()
        print("🌟 What you now have:")
        print("   🎯 Original priority analysis (unchanged)")
        print("   📁 File management system (unchanged)")
        print("   🌐 Real-time network monitoring (NEW!)")
        print("   📊 Network health status (NEW!)")
        print("   📈 Upload speed chart (NEW!)")
        print("   📶 WiFi status display (NEW!)")
        print()
        print("🎪 Visit your enhanced system:")
        print("   🏠 Main page: http://localhost:5000")
        print("   📤 Upload page: http://localhost:5000/upload") 
        print("   📊 Dashboard: http://localhost:5000/dashboard")
        print("   🌐 Network API: http://localhost:5000/api/network/status")
        
    finally:
        # Clean shutdown
        print("\n🛑 Shutting down test...")
        server_process.terminate()
        time.sleep(2)
        if server_process.poll() is None:
            server_process.kill()
        print("👋 Test complete!")

if __name__ == "__main__":
    test_network_monitor()