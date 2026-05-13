"""
Alert management routes
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from utils.database import db, Alert

bp = Blueprint('alert', __name__, url_prefix='/api/alert')

@bp.route('/all', methods=['GET'])
def get_all_alerts():
    """
    Get all alerts with optional filtering
    
    Args (query params):
        alert_type: Filter by alert type (intrusion, motion, unknown_object)
        severity: Filter by severity (low, medium, high)
        acknowledged: Filter by acknowledged status (true/false)
        limit: Number of records to return
        offset: Offset for pagination
    
    Returns:
        JSON with alerts list
    """
    try:
        query = Alert.query
        
        # Apply filters
        alert_type = request.args.get('alert_type')
        severity = request.args.get('severity')
        acknowledged = request.args.get('acknowledged')
        
        if alert_type:
            query = query.filter_by(alert_type=alert_type)
        if severity:
            query = query.filter_by(severity=severity)
        if acknowledged:
            acknowledged_bool = acknowledged.lower() == 'true'
            query = query.filter_by(acknowledged=acknowledged_bool)
        
        # Pagination
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        alerts = query.order_by(Alert.timestamp.desc()).limit(limit).offset(offset).all()
        total = query.count()
        
        return jsonify({
            'success': True,
            'total': total,
            'count': len(alerts),
            'alerts': [
                {
                    'id': a.id,
                    'timestamp': a.timestamp.isoformat(),
                    'type': a.alert_type,
                    'location': a.location,
                    'severity': a.severity,
                    'message': a.message,
                    'image_path': a.image_path,
                    'acknowledged': a.acknowledged
                }
                for a in alerts
            ]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/active', methods=['GET'])
def get_active_alerts():
    """
    Get unacknowledged (active) alerts
    
    Returns:
        JSON with active alerts
    """
    try:
        alerts = Alert.query.filter_by(acknowledged=False).order_by(
            Alert.timestamp.desc()
        ).all()
        
        return jsonify({
            'success': True,
            'count': len(alerts),
            'alerts': [
                {
                    'id': a.id,
                    'timestamp': a.timestamp.isoformat(),
                    'type': a.alert_type,
                    'severity': a.severity,
                    'message': a.message,
                    'location': a.location
                }
                for a in alerts
            ]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/create', methods=['POST'])
def create_alert():
    """
    Create a new alert
    
    Request body:
        {
            'alert_type': str,  # intrusion, motion, unknown_object
            'location': str,
            'severity': str,    # low, medium, high
            'message': str,
            'image_path': str (optional)
        }
    
    Returns:
        JSON with created alert
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['alert_type', 'location', 'severity', 'message']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        alert = Alert(
            alert_type=data['alert_type'],
            location=data['location'],
            severity=data['severity'],
            message=data['message'],
            image_path=data.get('image_path'),
            timestamp=datetime.utcnow(),
            acknowledged=False
        )
        
        db.session.add(alert)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'alert_id': alert.id,
            'timestamp': alert.timestamp.isoformat()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/acknowledge/<int:alert_id>', methods=['PUT'])
def acknowledge_alert(alert_id):
    """
    Mark alert as acknowledged
    
    Args:
        alert_id: ID of alert to acknowledge
    
    Returns:
        JSON with updated alert
    """
    try:
        alert = Alert.query.get(alert_id)
        
        if not alert:
            return jsonify({'error': 'Alert not found'}), 404
        
        alert.acknowledged = True
        db.session.commit()
        
        return jsonify({
            'success': True,
            'alert_id': alert.id,
            'acknowledged': alert.acknowledged
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/statistics', methods=['GET'])
def get_alert_statistics():
    """
    Get alert statistics
    
    Returns:
        JSON with aggregated alert data
    """
    try:
        total_alerts = Alert.query.count()
        active_alerts = Alert.query.filter_by(acknowledged=False).count()
        
        # Count by severity
        severity_counts = {}
        for severity in ['low', 'medium', 'high']:
            count = Alert.query.filter_by(severity=severity).count()
            severity_counts[severity] = count
        
        # Count by type
        type_counts = {}
        for alert_type in ['intrusion', 'motion', 'unknown_object']:
            count = Alert.query.filter_by(alert_type=alert_type).count()
            type_counts[alert_type] = count
        
        return jsonify({
            'success': True,
            'total_alerts': total_alerts,
            'active_alerts': active_alerts,
            'severity_distribution': severity_counts,
            'type_distribution': type_counts
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
