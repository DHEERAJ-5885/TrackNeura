#!/usr/bin/env python3
"""
🌐 Simple Connectivity Test
==========================

Baby, this checks if your server is working and you can reach it!
"""

import requests
import time
import webbrowser
import sys

def test_connectivity():
    """Test if our server is reachable"""
    print("🌐 Testing Your Enhanced System Connectivity")
    print("=" * 50)
    
    # Test different URLs
    urls_to_test = [
        ("Main Priority Analyzer", "http://127.0.0.1:5000/"),
        ("Upload Page", "http://127.0.0.1:5000/upload"),
        ("Dashboard", "http://127.0.0.1:5000/dashboard"),
        ("Network Status API", "http://127.0.0.1:5000/api/network/status"),
        ("System Status API", "http://127.0.0.1:5000/api/status"),
    ]
    
    print("⏳ Waiting 2 seconds for server to be ready...")
    time.sleep(2)
    
    all_working = True
    
    for name, url in urls_to_test:
        try:
            print(f"\n🔍 Testing {name}...")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {name}: WORKING (Status: {response.status_code})")
                
                # Check if it has expected content
                if url.endswith('/'):  # Main page
                    if 'Priority Analyzer' in response.text:
                        print("   📊 Priority Analyzer content: FOUND")
                    if 'Network Monitor' in response.text:
                        print("   🌐 Network Monitor content: FOUND")
            else:
                print(f"❌ {name}: ERROR (Status: {response.status_code})")
                all_working = False
                
        except requests.exceptions.ConnectError:
            print(f"❌ {name}: CONNECTION REFUSED - Server might not be running")
            all_working = False
        except requests.exceptions.Timeout:
            print(f"❌ {name}: TIMEOUT - Server too slow")
            all_working = False
        except Exception as e:
            print(f"❌ {name}: ERROR - {e}")
            all_working = False
    
    print(f"\n{'=' * 50}")
    
    if all_working:
        print("🎉 ALL SYSTEMS WORKING!")
        print("✅ Your server is running perfectly!")
        print("\n🌟 You can now access:")
        print("   🏠 Main page: http://127.0.0.1:5000")
        print("   📤 Upload: http://127.0.0.1:5000/upload")
        print("   📊 Dashboard: http://127.0.0.1:5000/dashboard")
        
        # Try to open browser
        try:
            print("\n🌐 Opening your system in browser...")
            webbrowser.open("http://127.0.0.1:5000")
            print("✅ Browser opened! Check your web browser!")
        except Exception as e:
            print(f"⚠️ Could not auto-open browser: {e}")
            print("   Please manually open: http://127.0.0.1:5000")
    else:
        print("⚠️ Some issues detected!")
        print("💡 Try these solutions:")
        print("   1. Make sure the server is running (check terminal)")
        print("   2. Try refreshing your browser")
        print("   3. Try http://localhost:5000 instead")
        print("   4. Check if antivirus/firewall is blocking")
    
    return all_working

if __name__ == "__main__":
    test_connectivity()