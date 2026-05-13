#!/usr/bin/env python3
"""
Isomer System Status & Quick Launch Helper
Shows system status and helps launch the application
"""

import os
import sys
import subprocess
import platform

def print_header():
    """Print welcome header"""
    print("\n" + "="*60)
    print("🎥 ISOMER - AI Surveillance System")
    print("="*60)
    print("Real-time object detection, motion detection & analytics")
    print("="*60 + "\n")

def check_prerequisites():
    """Check if Python and Node.js are installed"""
    print("📋 Checking prerequisites...\n")
    
    issues = []
    
    # Check Python
    try:
        result = subprocess.run([sys.executable, '--version'], 
                              capture_output=True, text=True)
        python_version = result.stdout.strip() or result.stderr.strip()
        print(f"✅ Python: {python_version}")
    except:
        issues.append("Python not found - please install Python 3.8+")
        print("❌ Python: NOT FOUND")
    
    # Check Node.js
    try:
        result = subprocess.run(['node', '--version'], 
                              capture_output=True, text=True)
        node_version = result.stdout.strip()
        print(f"✅ Node.js: {node_version}")
    except:
        issues.append("Node.js not found - please install Node.js 16+")
        print("❌ Node.js: NOT FOUND")
    
    # Check npm
    try:
        result = subprocess.run(['npm', '--version'], 
                              capture_output=True, text=True)
        npm_version = result.stdout.strip()
        print(f"✅ npm: {npm_version}")
    except:
        issues.append("npm not found - install with Node.js")
        print("❌ npm: NOT FOUND")
    
    print()
    return issues

def print_system_info():
    """Print system information"""
    print("💻 System Information:")
    print(f"   OS: {platform.system()} {platform.release()}")
    print(f"   Architecture: {platform.machine()}")
    print()

def print_quick_start():
    """Print quick start instructions"""
    print("🚀 QUICK START (Choose one):\n")
    
    system = platform.system()
    
    if system == "Windows":
        print("1️⃣  Automated (Recommended):")
        print("   → Run: start.bat")
        print("\n2️⃣  Manual:")
        print("   Terminal 1: cd backend && python app.py")
        print("   Terminal 2: cd frontend && npm run dev")
    else:  # macOS/Linux
        print("1️⃣  Automated (Recommended):")
        print("   → Run: chmod +x start.sh && ./start.sh")
        print("\n2️⃣  Manual:")
        print("   Terminal 1: cd backend && python app.py")
        print("   Terminal 2: cd frontend && npm run dev")
    
    print("\n3️⃣  Using Docker:")
    print("   → Run: docker-compose up --build")
    print()

def print_urls():
    """Print access URLs"""
    print("🌐 ACCESS URLS:\n")
    print("   Dashboard: http://localhost:3000")
    print("   Backend API: http://localhost:5000")
    print("   API Docs: http://localhost:5000/api/health")
    print()

def print_next_steps():
    """Print next steps"""
    print("📖 DOCUMENTATION:\n")
    print("   Quick Start: QUICKSTART.md (5 minutes)")
    print("   Full Setup: INSTALLATION.md (detailed)")
    print("   API Docs: API_DOCUMENTATION.md")
    print("   Development: DEVELOPMENT.md")
    print("   Features: FEATURES.md")
    print()

def print_features():
    """Print key features"""
    print("✨ KEY FEATURES:\n")
    print("   ✓ Real-time video streaming (30+ FPS)")
    print("   ✓ YOLOv8 AI object detection")
    print("   ✓ Optical flow motion detection")
    print("   ✓ Intrusion detection with alerts")
    print("   ✓ Modern analytics dashboard")
    print("   ✓ Detection history & export")
    print("   ✓ GPU acceleration ready")
    print()

def print_troubleshooting():
    """Print troubleshooting info"""
    print("🔧 TROUBLESHOOTING:\n")
    
    print("❓ Port already in use?")
    system = platform.system()
    if system == "Windows":
        print("   > netstat -ano | findstr :5000")
        print("   > taskkill /PID <PID> /F")
    else:
        print("   > lsof -i :5000")
        print("   > kill -9 <PID>")
    
    print("\n❓ Module not found?")
    print("   > pip install --upgrade -r backend/requirements.txt")
    print("   > npm install --no-save frontend/")
    
    print("\n❓ Still having issues?")
    print("   > python test_setup.py  # Run diagnostics")
    print("   > See DEVELOPMENT.md for debugging tips")
    print()

def main():
    """Main function"""
    print_header()
    print_system_info()
    
    # Check prerequisites
    issues = check_prerequisites()
    
    if issues:
        print("\n⚠️  ISSUES FOUND:\n")
        for issue in issues:
            print(f"   • {issue}")
        print("\nPlease fix these issues before starting.")
        return
    
    print("✅ All prerequisites met!\n")
    
    print_quick_start()
    print_urls()
    print_features()
    print_next_steps()
    print_troubleshooting()
    
    print("="*60)
    print("Ready to start? Choose option 1, 2, or 3 above")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
