"""
History and data export routes
"""

from flask import Blueprint, request, jsonify, send_file
from datetime import datetime, timedelta
from utils.database import db, Detection, Alert, MotionData
import os
import csv
from io import StringIO, BytesIO
import zipfile

bp = Blueprint('history', __name__, url_prefix='/api/history')

@bp.route('/detections', methods=['GET'])
def get_detection_history():
    """
    Get detection history with date filtering
    
    Args (query params):
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        limit: Number of records to return
    
    Returns:
        JSON with detection history
    """
    try:
        # Parse date filters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        limit = request.args.get('limit', 500, type=int)
        
        query = Detection.query
        
        if start_date:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Detection.timestamp >= start)
        
        if end_date:
            end = datetime.strptime(end_date, '%Y-%m-%d')
            end = end.replace(hour=23, minute=59, second=59)
            query = query.filter(Detection.timestamp <= end)
        
        detections = query.order_by(Detection.timestamp.desc()).limit(limit).all()
        
        return jsonify({
            'success': True,
            'count': len(detections),
            'detections': [
                {
                    'id': d.id,
                    'timestamp': d.timestamp.isoformat(),
                    'frame_id': d.frame_id,
                    'objects_detected': d.objects_detected,
                    'confidence_score': d.confidence_score,
                    'image_path': d.image_path
                }
                for d in detections
            ]
        }), 200
    
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/alerts', methods=['GET'])
def get_alert_history():
    """
    Get alert history with date filtering
    
    Args (query params):
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        severity: Filter by severity
        limit: Number of records to return
    
    Returns:
        JSON with alert history
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        severity = request.args.get('severity')
        limit = request.args.get('limit', 500, type=int)
        
        query = Alert.query
        
        if start_date:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Alert.timestamp >= start)
        
        if end_date:
            end = datetime.strptime(end_date, '%Y-%m-%d')
            end = end.replace(hour=23, minute=59, second=59)
            query = query.filter(Alert.timestamp <= end)
        
        if severity:
            query = query.filter_by(severity=severity)
        
        alerts = query.order_by(Alert.timestamp.desc()).limit(limit).all()
        
        return jsonify({
            'success': True,
            'count': len(alerts),
            'alerts': [
                {
                    'id': a.id,
                    'timestamp': a.timestamp.isoformat(),
                    'alert_type': a.alert_type,
                    'location': a.location,
                    'severity': a.severity,
                    'message': a.message,
                    'acknowledged': a.acknowledged
                }
                for a in alerts
            ]
        }), 200
    
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/export/csv', methods=['GET'])
def export_to_csv():
    """
    Export detection and alert history as CSV
    
    Returns:
        CSV file download
    """
    try:
        # Get data
        detections = Detection.query.all()
        alerts = Alert.query.all()
        
        # Create CSV in memory
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        
        # Write detections
        writer.writerow(['DETECTIONS'])
        writer.writerow(['Timestamp', 'Frame ID', 'Objects', 'Confidence', 'Image Path'])
        for d in detections:
            writer.writerow([
                d.timestamp.isoformat(),
                d.frame_id,
                str(d.objects_detected),
                d.confidence_score,
                d.image_path
            ])
        
        writer.writerow([])
        
        # Write alerts
        writer.writerow(['ALERTS'])
        writer.writerow(['Timestamp', 'Type', 'Location', 'Severity', 'Message', 'Acknowledged'])
        for a in alerts:
            writer.writerow([
                a.timestamp.isoformat(),
                a.alert_type,
                a.location,
                a.severity,
                a.message,
                a.acknowledged
            ])
        
        # Convert to bytes
        csv_bytes = BytesIO(csv_buffer.getvalue().encode())
        csv_bytes.seek(0)
        
        return send_file(
            csv_bytes,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'surveillance_history_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/daily-summary', methods=['GET'])
def get_daily_summary():
    """
    Get daily summary statistics
    
    Returns:
        JSON with daily statistics
    """
    try:
        # Get data for last 7 days
        today = datetime.utcnow().date()
        summary = []
        
        for i in range(7):
            date = today - timedelta(days=i)
            start = datetime.combine(date, datetime.min.time())
            end = datetime.combine(date, datetime.max.time())
            
            detection_count = Detection.query.filter(
                Detection.timestamp.between(start, end)
            ).count()
            
            alert_count = Alert.query.filter(
                Alert.timestamp.between(start, end)
            ).count()
            
            intrusion_count = Alert.query.filter(
                Alert.alert_type == 'intrusion',
                Alert.timestamp.between(start, end)
            ).count()
            
            summary.append({
                'date': date.isoformat(),
                'detections': detection_count,
                'alerts': alert_count,
                'intrusions': intrusion_count
            })
        
        return jsonify({
            'success': True,
            'summary': summary
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/dashboard-stats', methods=['GET'])
def get_dashboard_stats():
    """
    Get comprehensive dashboard statistics
    
    Returns:
        JSON with all dashboard metrics
    """
    try:
        total_detections = Detection.query.count()
        total_alerts = Alert.query.count()
        active_alerts = Alert.query.filter_by(acknowledged=False).count()
        
        # Last 24 hours
        twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
        detections_24h = Detection.query.filter(
            Detection.timestamp >= twenty_four_hours_ago
        ).count()
        alerts_24h = Alert.query.filter(
            Alert.timestamp >= twenty_four_hours_ago
        ).count()
        
        return jsonify({
            'success': True,
            'total_detections': total_detections,
            'total_alerts': total_alerts,
            'active_alerts': active_alerts,
            'detections_24h': detections_24h,
            'alerts_24h': alerts_24h,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
