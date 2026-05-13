"""
Configuration settings for the surveillance system.
"""

import os
from datetime import timedelta
from pathlib import Path


def _sqlite_uri(path):
    """Build a SQLite URI from a filesystem path."""
    return f"sqlite:///{path.as_posix()}"


class Config:
    """Application configuration."""

    BASE_DIR = Path(__file__).resolve().parent.parent
    INSTANCE_DIR = BASE_DIR / "instance"
    ULTRALYTICS_CONFIG_DIR = BASE_DIR / ".ultralytics"

    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-change-in-production")
    DEBUG = os.environ.get("DEBUG", "true").lower() == "true"
    TESTING = False

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI",
        _sqlite_uri(INSTANCE_DIR / "surveillance.db"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Upload settings
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB
    UPLOAD_FOLDER = str(BASE_DIR / "uploads")
    ALLOWED_EXTENSIONS = {"mp4", "avi", "mov", "flv", "wmv"}

    # Video settings
    VIDEO_FRAME_WIDTH = int(os.environ.get("VIDEO_FRAME_WIDTH", 640))
    VIDEO_FRAME_HEIGHT = int(os.environ.get("VIDEO_FRAME_HEIGHT", 480))
    VIDEO_FPS = int(os.environ.get("VIDEO_FPS", 60))
    STREAM_JPEG_QUALITY = int(os.environ.get("STREAM_JPEG_QUALITY", 75))

    # Detection settings
    CONFIDENCE_THRESHOLD = 0.5
    NMS_THRESHOLD = 0.45

    # Motion detection
    MOTION_THRESHOLD = 0.1
    OPTICAL_FLOW_SCALE = 0.5

    # Intrusion detection
    INTRUSION_COOLDOWN = 5  # seconds

    # Directories
    CAPTURE_DIR = str(BASE_DIR / "captures")
    HISTORY_DIR = str(BASE_DIR / "history")
    LOG_DIR = str(BASE_DIR / "logs")

    # Logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Model settings
    MODEL_NAME = os.environ.get("MODEL_NAME", "yolov8n-seg")
    MODEL_WEIGHTS_PATH = str(BASE_DIR / f"{MODEL_NAME}.pt")
    MODEL_CONFIDENCE = float(os.environ.get("MODEL_CONFIDENCE", 0.5))
    INFERENCE_IMAGE_SIZE = int(os.environ.get("INFERENCE_IMAGE_SIZE", 320))
    DETECTION_INTERVAL = max(1, int(os.environ.get("DETECTION_INTERVAL", 3)))
    MAX_DETECTIONS = int(os.environ.get("MAX_DETECTIONS", 20))
    DRAW_SEGMENTATION_MASKS = os.environ.get(
        "DRAW_SEGMENTATION_MASKS",
        "false",
    ).lower() == "true"
    CLASSES_TO_DETECT = ["person", "car", "truck", "bus", "bicycle", "motorcycle"]
