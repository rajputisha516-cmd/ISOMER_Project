"""
Database initialization and utilities
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

def init_db(app):
    """Initialize database with the Flask app"""
    db.init_app(app)
    with app.app_context():
        db.create_all()

def get_db():
    """Get database instance"""
    return db

# ============================================================================
# DATABASE MODELS
# ============================================================================

class Detection(db.Model):
    """Store detection records"""
    __tablename__ = 'detections'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    frame_id = db.Column(db.String(50))
    objects_detected = db.Column(db.JSON)  # List of detected objects
    confidence_score = db.Column(db.Float)
    image_path = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<Detection {self.id}>'

class Alert(db.Model):
    """Store intrusion alerts"""
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    alert_type = db.Column(db.String(50))  # intrusion, motion, unknown_object
    location = db.Column(db.String(255))
    severity = db.Column(db.String(20))  # low, medium, high
    message = db.Column(db.Text)
    image_path = db.Column(db.String(255))
    acknowledged = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Alert {self.id}>'

class MotionData(db.Model):
    """Store motion detection data"""
    __tablename__ = 'motion_data'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    motion_detected = db.Column(db.Boolean)
    motion_intensity = db.Column(db.Float)  # 0-1
    motion_vectors = db.Column(db.JSON)
    
    def __repr__(self):
        return f'<MotionData {self.id}>'

class Zone(db.Model):
    """Store intrusion detection zones"""
    __tablename__ = 'zones'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    coordinates = db.Column(db.JSON)  # Polygon coordinates
    enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Zone {self.name}>'

class Statistics(db.Model):
    """Store system statistics"""
    __tablename__ = 'statistics'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    total_detections = db.Column(db.Integer, default=0)
    total_alerts = db.Column(db.Integer, default=0)
    average_fps = db.Column(db.Float)
    uptime_seconds = db.Column(db.Integer)
    
    def __repr__(self):
        return f'<Statistics {self.id}>'
