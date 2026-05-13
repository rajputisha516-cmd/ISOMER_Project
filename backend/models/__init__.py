"""
Backend models package - SQLAlchemy models
"""

from utils.database import db, Detection, Alert, MotionData, Zone, Statistics

__all__ = ['Detection', 'Alert', 'MotionData', 'Zone', 'Statistics']
