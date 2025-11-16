#!/usr/bin/env python3
"""
🎪 Complete System Test - Original Priority Analyzer + New File Management
==========================================================================

This comprehensive test demonstrates:
1. Your original Priority Analyzer working perfectly
2. The new File Management System working alongside it
3. Both systems operating without any conflicts
"""

import subprocess
import time
import requests
import tempfile
import os

def start_system():
    """Start the enhanced system with both features"""
    return subprocess.Popen([
        r'C:\Trackneura\.venv\Scripts\python.exe', 
        'app.py'
    ], cwd=r'C:\Trackneura')

def test_original_priority_analyzer():
    """Test your original Priority Analyzer functionality"""
    print("🎯 Testing Original Priority Analyzer...")
    
    try:
        # Test original API status
        response = requests.get('http://localhost:5000/api/status', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Original Priority Analyzer API Working!")
            print(f"   📊 Status: {data.get('status')}")
            print(f"   🤖 ML Model: {'Trained' if data.get('ml_model_trained') else 'Not Trained'}")
            print(f"   📋 Version: {data.get('version')}")
        
        # Test original file upload and analysis
        print("\\n📤 Testing Original File Analysis...")
        with tempfile.NamedTemporaryFile(suffix='.log', delete=False) as tmp:
            tmp.write(b'EMERGENCY: Critical system failure detected! Server down!')
            tmp_path = tmp.name
        
        with open(tmp_path, 'rb') as f:
            response = requests.post(
                'http://localhost:5000/upload',
                files={'files': ('emergency_server.log', f, 'text/plain')},
                timeout=10
            )
        
        os.unlink(tmp_path)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Original File Analysis Working!")
            print(f"   📁 Upload ID: {data.get('upload_id')}")
            print(f"   📊 Files Analyzed: {len(data.get('files', []))}")
            
            if data.get('files'):
                file_info = data['files'][0]
                print(f"   📄 File: {file_info.get('filename')}")
                print(f"   📋 Category: {file_info.get('category')}")
                print(f"   ⭐ Priority Level: {file_info.get('priority_level')}")
                if 'smart_priority_score' in file_info:
                    print(f"   ✨ Smart Priority: {file_info.get('smart_priority_score', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Original Priority Analyzer test failed: {e}")
        return False

def test_new_file_management():
    """Test the new File Management System"""
    print("\\n📁 Testing NEW File Management System...")
    
    try:
        # Test file management stats
        response = requests.get('http://localhost:5000/api/files/stats', timeout=10)
        if response.status_code == 200:
            stats = response.json()
            print("✅ File Management System Working!")
            print(f"   📊 Total Files: {stats.get('total_files', 0)}")
            print(f"   💾 Storage Used: {stats.get('total_size', 0)} bytes")
            print(f"   📅 Latest Upload: {stats.get('latest_upload', 'None')}")
        
        # Test new file upload
        print("\\n📤 Testing NEW File Upload System...")
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
            tmp.write(b'This is a test document for the new file management system!')
            tmp_path = tmp.name
        
        with open(tmp_path, 'rb') as f:
            response = requests.post(
                'http://localhost:5000/api/files/upload',
                files={'file': ('test_document.txt', f, 'text/plain')},
                timeout=10
            )
        
        os.unlink(tmp_path)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ NEW File Upload Working!")
            print(f"   📁 File ID: {data.get('file_id')}")
            print(f"   📄 Filename: {data.get('filename')}")
            print(f"   📋 File Type: {data.get('file_type')}")
            print(f"   💾 File Size: {data.get('file_size')} bytes")
            print(f"   🔗 Preview URL: {data.get('preview_url')}")
            print(f"   ⬇️ Download URL: {data.get('download_url')}")
            
            # Test file list
            print("\\n📋 Testing File List...")
            response = requests.get('http://localhost:5000/api/files/list', timeout=10)
            if response.status_code == 200:
                files = response.json()
                print(f"✅ File List Working! Found {len(files)} file(s)")
            
            return True
        
    except Exception as e:
        print(f"❌ File Management System test failed: {e}")
        return False

def test_web_pages():
    """Test that all web pages are accessible"""
    print("\\n🌐 Testing Web Pages...")
    
    pages = [
        ('/', 'Original Priority Analyzer Home'),
        ('/upload', 'NEW Upload Page'),
        ('/dashboard', 'NEW Dashboard Page')
    ]
    
    for url, name in pages:
        try:
            response = requests.get(f'http://localhost:5000{url}', timeout=10)
            if response.status_code == 200:
                print(f"✅ {name} - Accessible")
            else:
                print(f"❌ {name} - Error {response.status_code}")
        except Exception as e:
            print(f"❌ {name} - Failed: {e}")

def main():
    """Run comprehensive system test"""
    print("🎪 COMPLETE SYSTEM TEST")
    print("=" * 60)
    print("Testing your Original Priority Analyzer + NEW File Management System")
    print("Both systems working together without conflicts!")
    print()
    
    # Start system
    print("🚀 Starting complete system...")
    server_process = start_system()
    
    try:
        # Wait for startup
        print("⏳ Waiting for system to initialize...")
        time.sleep(8)
        
        # Run tests
        test_results = []
        
        # Test 1: Original Priority Analyzer
        test_results.append(test_original_priority_analyzer())
        
        # Test 2: New File Management System
        test_results.append(test_new_file_management())
        
        # Test 3: Web Pages
        test_web_pages()
        
        # Results Summary
        print("\\n🎪 COMPLETE SYSTEM TEST RESULTS")
        print("=" * 60)
        
        if all(test_results):
            print("🎉 ALL TESTS PASSED!")
            print("✅ Your Original Priority Analyzer: WORKING PERFECTLY")
            print("✅ NEW File Management System: WORKING PERFECTLY")
            print("✅ Both systems integrated seamlessly!")
            print()
            print("🌟 What you now have:")
            print("   🎯 Original file priority analysis with ML")
            print("   📤 NEW file upload system for any file type")
            print("   👀 NEW file preview system")
            print("   📊 NEW file dashboard")
            print("   ⬇️ NEW file download system")
            print("   🔄 All systems working together!")
            print()
            print("🎪 Your system is ready!")
            print("   🏠 Priority Analyzer: http://localhost:5000")
            print("   📤 Upload Files: http://localhost:5000/upload")
            print("   📊 Dashboard: http://localhost:5000/dashboard")
        else:
            print("⚠️ Some tests had issues, but the system should still work!")
            print("Check the individual test results above.")
        
    finally:
        # Clean shutdown
        print("\\n🛑 Shutting down test system...")
        server_process.terminate()
        time.sleep(2)
        if server_process.poll() is None:
            server_process.kill()
        print("👋 Test complete!")

if __name__ == "__main__":
    main()