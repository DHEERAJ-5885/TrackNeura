#!/usr/bin/env python3
"""
🎪 Smart File Transfer System Launcher
======================================

This script starts the intelligent priority-based file transfer system
with machine learning capabilities and beautiful web dashboard.

Usage:
    python run_smart_system.py

Features:
- 🧠 AI-powered priority analysis  
- 🔄 Dynamic queue management
- 🌐 Network adaptation
- 📊 Real-time dashboard
- 📚 Behavioral learning
"""

import os
import sys
import time

def print_banner():
    """Display startup banner"""
    banner = """
    🎪 ════════════════════════════════════════════════════════════════
    🎪   SMART FILE TRANSFER SYSTEM - INTELLIGENT PRIORITY ENGINE
    🎪 ════════════════════════════════════════════════════════════════
    🎪 
    🎪   🧠 AI-Powered Priority Analysis    📊 Real-time Dashboard
    🎪   🔄 Dynamic Queue Management        🌐 Network Adaptation  
    🎪   📚 Behavioral Learning System     ⚡ High Performance
    🎪 
    🎪 ════════════════════════════════════════════════════════════════
    """
    print(banner)

def main():
    """Main entry point"""
    try:
        print_banner()
        print("🚀 Starting Smart File Transfer System...")
        
        # Import and run the Flask app
        from smart_file_transfer_system import app
        
        print("✅ System components initialized successfully!")
        print("🌐 Starting web server...")
        print()
        print("📊 Dashboard: http://localhost:5001")
        print("🔌 API Base:  http://localhost:5001/api")
        print()
        print("🎯 Ready to receive files! Press Ctrl+C to stop.")
        print("═" * 60)
        
        # Run the Flask app
        app.run(
            host='0.0.0.0',
            port=5001,
            debug=False,  # Set to False for production-like behavior
            threaded=True
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested by user...")
        print("🧹 Cleaning up system resources...")
        print("👋 Smart File Transfer System stopped. Goodbye!")
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ System startup failed: {e}")
        print("💡 Check your Python environment and dependencies")
        sys.exit(1)

if __name__ == "__main__":
    main()