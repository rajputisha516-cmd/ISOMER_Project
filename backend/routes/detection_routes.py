"""
Detection and inference routes
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from utils.database import db, Detection

bp = Blueprint('detection', __name__, url_prefix='/api/detection')

@bp.route('/history', methods=['GET'])
def get_detection_history():
    """
    Get detection history with pagination
    
    Args (query params):
        limit: Number of records to return (default: 50)
        offset: Offset for pagination (default: 0)
    
    Returns:
        JSON with detection history
    """
    try:
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        detections = Detection.query.order_by(
            Detection.timestamp.desc()
        ).limit(limit).offset(offset).all()
        
        total = Detection.query.count()
        
        return jsonify({
            'success': True,
            'total': total,
            'count': len(detections),
            'detections': [
                {
                    'id': d.id,
                    'timestamp': d.timestamp.isoformat(),
                    'objects': d.objects_detected,
                    'confidence': d.confidence_score,
                    'image_path': d.image_path
                }
                for d in detections
            ]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/statistics', methods=['GET'])
def get_detection_statistics():
    """
    Get detection statistics for dashboard
    
    Returns:
        JSON with aggregated detection data
    """
    try:
        total_detections = Detection.query.count()
        
        # Get unique class names
        detections = Detection.query.all()
        class_counts = {}
        
        for detection in detections:
            if detection.objects_detected:
                for obj in detection.objects_detected:
                    class_name = obj.get('class_name', 'unknown')
                    class_counts[class_name] = class_counts.get(class_name, 0) + 1
        
        # Get recent detections (last hour)
        from datetime import timedelta
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        recent_count = Detection.query.filter(
            Detection.timestamp >= one_hour_ago
        ).count()
        
        return jsonify({
            'success': True,
            'total_detections': total_detections,
            'recent_detections': recent_count,
            'class_distribution': class_counts,
            'most_detected': max(class_counts.items(), key=lambda x: x[1])[0] if class_counts else 'N/A'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/save', methods=['POST'])
def save_detection():
    """
    Save detection record to database
    
    Request body:
        {
            'frame_id': str,
            'objects_detected': list,
            'confidence_score': float,
            'image_path': str
        }
    
    Returns:
        JSON with saved detection
    """
    try:
        data = request.get_json()
        
        detection = Detection(
            frame_id=data.get('frame_id'),
            objects_detected=data.get('objects_detected'),
            confidence_score=data.get('confidence_score'),
            image_path=data.get('image_path'),
            timestamp=datetime.utcnow()
        )
        
        db.session.add(detection)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'detection_id': detection.id,
            'timestamp': detection.timestamp.isoformat()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/clear', methods=['DELETE'])
def clear_detections():
    """
    Clear all detection records (admin only)
    
    Returns:
        JSON with operation status
    """
    try:
        count = Detection.query.count()
        Detection.query.delete()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'deleted_count': count,
            'message': f'{count} detection records deleted'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
