#!/usr/bin/env python3
"""🌐 Simple Browser Opener"""
import webbrowser
import time
import subprocess
import sys

print("🌐 Opening your enhanced system in browser...")
print("✨ Your system includes:")
print("   🎯 Original Priority Analyzer (preserved)")
print("   📁 File Management System (preserved)")  
print("   🌐 NEW: Real-time Network Monitor")
print()

# Wait a moment for server
time.sleep(3)

# Try to open in browser
try:
    print("🚀 Opening http://127.0.0.1:5000 in your browser...")
    webbrowser.open("http://127.0.0.1:5000")
    print("✅ Browser should open now!")
    print()
    print("🌟 If browser doesn't open, manually visit:")
    print("   http://127.0.0.1:5000")
    print("   or")
    print("   http://localhost:5000")
    print()
    print("📚 What you'll see:")
    print("   🎯 Your original Priority Analyzer")
    print("   🌐 Real-time Network Monitor dashboard")
    print("   📤 Links to Upload and Dashboard pages")
    print("   📊 Live network statistics every second")
    
except Exception as e:
    print(f"⚠️ Could not auto-open browser: {e}")
    print("Please manually open: http://127.0.0.1:5000")

print()
print("💡 If you see 'can't reach page':")
print("   1. Wait 10 seconds and refresh")
print("   2. Check that the server terminal is still running")
print("   3. Try http://localhost:5000 instead")
print("   4. Check Windows Firewall/antivirus settings")