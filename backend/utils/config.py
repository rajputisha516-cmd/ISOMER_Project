"""
Configuration settings for the surveillance system
"""

import os
from datetime import timedelta

class Config:
    """Base configuration"""
    
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    DEBUG = True
    TESTING = False
    
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///surveillance.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Upload settings
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'flv', 'wmv'}
    
    # Video settings
    VIDEO_FRAME_WIDTH = int(os.environ.get('VIDEO_FRAME_WIDTH', 640))
    VIDEO_FRAME_HEIGHT = int(os.environ.get('VIDEO_FRAME_HEIGHT', 480))
    VIDEO_FPS = int(os.environ.get('VIDEO_FPS', 60))  # Increased from 30 to 60 for smoother streaming
    STREAM_JPEG_QUALITY = int(os.environ.get('STREAM_JPEG_QUALITY', 75))  # Increased quality for better visuals

    # Detection settings
    CONFIDENCE_THRESHOLD = 0.5
    NMS_THRESHOLD = 0.45
    
    # Motion detection
    MOTION_THRESHOLD = 0.1
    OPTICAL_FLOW_SCALE = 0.5
    
    # Intrusion detection
    INTRUSION_COOLDOWN = 5  # seconds
    
    # Directories
    CAPTURE_DIR = 'captures'
    HISTORY_DIR = 'history'
    LOG_DIR = 'logs'
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Model settings
    MODEL_NAME = os.environ.get('MODEL_NAME') or 'yolov8n-seg'
    MODEL_CONFIDENCE = float(os.environ.get('MODEL_CONFIDENCE', 0.5))
    INFERENCE_IMAGE_SIZE = int(os.environ.get('INFERENCE_IMAGE_SIZE', 320))
    DETECTION_INTERVAL = max(1, int(os.environ.get('DETECTION_INTERVAL', 3)))
    MAX_DETECTIONS = int(os.environ.get('MAX_DETECTIONS', 20))
    DRAW_SEGMENTATION_MASKS = os.environ.get('DRAW_SEGMENTATION_MASKS', 'false').lower() == 'true'
    CLASSES_TO_DETECT = ['person', 'car', 'truck', 'bus', 'bicycle', 'motorcycle']
