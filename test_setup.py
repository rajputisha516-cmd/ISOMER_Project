"""
Utility script to test backend connectivity and model loading
Run this to verify your setup is correct
"""

import requests
import json
from datetime import datetime

def test_backend_health():
    """Test if backend is running"""
    try:
        response = requests.get('http://localhost:5000/api/health')
        if response.status_code == 200:
            print("✅ Backend is running")
            print(json.dumps(response.json(), indent=2))
            return True
    except Exception as e:
        print(f"❌ Backend not responding: {e}")
        return False

def test_detection_endpoint():
    """Test detection API"""
    try:
        response = requests.get('http://localhost:5000/api/detection/statistics')
        if response.status_code == 200:
            print("\n✅ Detection API working")
            print(json.dumps(response.json(), indent=2))
            return True
    except Exception as e:
        print(f"❌ Detection API error: {e}")
        return False

def test_alert_endpoint():
    """Test alert API"""
    try:
        response = requests.get('http://localhost:5000/api/alert/active')
        if response.status_code == 200:
            print("\n✅ Alert API working")
            print(f"   Active alerts: {response.json().get('count', 0)}")
            return True
    except Exception as e:
        print(f"❌ Alert API error: {e}")
        return False

def test_history_endpoint():
    """Test history API"""
    try:
        response = requests.get('http://localhost:5000/api/history/dashboard-stats')
        if response.status_code == 200:
            print("\n✅ History API working")
            data = response.json()
            print(f"   Total detections: {data.get('total_detections', 0)}")
            print(f"   Total alerts: {data.get('total_alerts', 0)}")
            print(f"   Active alerts: {data.get('active_alerts', 0)}")
            return True
    except Exception as e:
        print(f"❌ History API error: {e}")
        return False

def test_yolo_model():
    """Test if YOLO model loads"""
    try:
        print("\n🔄 Testing YOLO model loading...")
        from ultralytics import YOLO
        model = YOLO('yolov8n-seg.pt')
        print("✅ YOLO model loaded successfully")
        return True
    except Exception as e:
        print(f"❌ YOLO model failed: {e}")
        print("   Run: python -c \"from ultralytics import YOLO; YOLO('yolov8n-seg.pt')\"")
        return False

def test_opencv():
    """Test if OpenCV is installed"""
    try:
        import cv2
        print(f"✅ OpenCV {cv2.__version__} installed")
        
        # Test webcam
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ Webcam accessible")
            cap.release()
        else:
            print("⚠️  Webcam not accessible")
        return True
    except Exception as e:
        print(f"❌ OpenCV error: {e}")
        return False

def main():
    print("=" * 50)
    print("Isomer System Health Check")
    print("=" * 50)
    
    results = []
    
    # Test connections
    print("\n🌐 Backend Connectivity Tests:")
    results.append(("Backend Health", test_backend_health()))
    results.append(("Detection API", test_detection_endpoint()))
    results.append(("Alert API", test_alert_endpoint()))
    results.append(("History API", test_history_endpoint()))
    
    # Test components
    print("\n🤖 Component Tests:")
    results.append(("YOLO Model", test_yolo_model()))
    results.append(("OpenCV", test_opencv()))
    
    # Summary
    print("\n" + "=" * 50)
    print("Summary:")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<30} {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All systems ready!")
    else:
        print("\n⚠️  Some tests failed. Check the output above.")
    
    print("=" * 50)

if __name__ == '__main__':
    main()
