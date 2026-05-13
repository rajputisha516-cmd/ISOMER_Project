"""
Video upload and streaming routes
"""

from flask import Blueprint, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from utils.config import Config
import cv2
import base64
import threading
import time

bp = Blueprint('video', __name__, url_prefix='/api/video')

ALLOWED_EXTENSIONS = Config.ALLOWED_EXTENSIONS

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['POST'])
def upload_video():
    """
    Upload video file
    
    Returns:
        JSON with upload status and file path
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': f'File type not allowed. Allowed: {ALLOWED_EXTENSIONS}'}), 400
    
    try:
        # Create uploads directory if not exists
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        
        # Generate unique filename
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'filepath': filepath,
            'message': 'File uploaded successfully',
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/analyze', methods=['POST'])
def analyze_video():
    """
    Analyze uploaded video file for object detection and alerts
    
    Expected JSON:
    {
        "filename": "video_filename.mp4"
    }
    
    Returns:
        JSON with analysis results including detections, alerts, and statistics
    """
    data = request.get_json()
    
    if not data or 'filename' not in data:
        return jsonify({'error': 'Filename is required'}), 400
    
    filename = data['filename']
    filepath = os.path.join(Config.UPLOAD_FOLDER, secure_filename(filename))
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    if not allowed_file(filename):
        return jsonify({'error': f'File type not allowed. Allowed: {ALLOWED_EXTENSIONS}'}), 400
    
    try:
        # Initialize processors
        from motion_detection.detector import MotionDetector
        from video_processing.processor import VideoProcessor
        
        video_processor = VideoProcessor(Config.MODEL_NAME)
        motion_detector = MotionDetector()
        
        # Open video file
        capture = cv2.VideoCapture(filepath)
        if not capture.isOpened():
            return jsonify({'error': 'Could not open video file'}), 500
        
        # Get video properties
        frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = capture.get(cv2.CAP_PROP_FPS)
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Analysis results
        all_detections = []
        all_alerts = []
        frame_results = []
        
        frame_index = 0
        consecutive_failures = 0
        cached_detections = []
        
        # Process video frames
        while True:
            ok, frame = capture.read()
            
            if not ok or frame is None:
                consecutive_failures += 1
                if consecutive_failures >= 10:  # Allow more failures for video files
                    break
                time.sleep(0.01)
                continue
            
            consecutive_failures = 0
            frame_index += 1
            
            # Resize frame to match streaming configuration
            frame = cv2.resize(frame, (Config.VIDEO_FRAME_WIDTH, Config.VIDEO_FRAME_HEIGHT))
            
            try:
                # Process frame (same logic as stream_video)
                motion_frame, motion_data = motion_detector.detect(frame)
                should_run_detection = (
                    frame_index == 1
                    or frame_index % Config.DETECTION_INTERVAL == 0
                    or not cached_detections
                )
                if should_run_detection:
                    annotated_frame, cached_detections = video_processor.process_frame(frame)
                else:
                    annotated_frame = video_processor.annotate_frame(frame, cached_detections)
            except Exception as exc:
                # Continue processing other frames if one fails
                print(f"Frame processing failed at frame {frame_index}: {exc}")
                continue
            
            combined_frame = cv2.addWeighted(annotated_frame, 0.7, motion_frame, 0.3, 0)
            intrusion_alert = motion_detector.check_intrusion(cached_detections)
            
            # Store detection data for this frame
            frame_detections = []
            for det in cached_detections:
                frame_detections.append({
                    "class_name": det["class_name"],
                    "confidence": det["confidence"],
                    "x": det["x"],
                    "y": det["y"],
                    "width": det["width"],
                    "height": det["height"]
                })
            
            all_detections.extend(frame_detections)
            
            # Check for alerts
            if intrusion_alert.get("should_alert"):
                alert_data = {
                    "type": "intrusion",
                    "message": (
                        f"{len(intrusion_alert['objects_in_zone'])} person(s) detected "
                        "inside the intrusion zone"
                    ),
                    "timestamp": datetime.now().isoformat(),
                    "frame_number": frame_index,
                    "objects_in_zone": len(intrusion_alert['objects_in_zone'])
                }
                all_alerts.append(alert_data)
            
            # Store frame result (every 30th frame to avoid too much data)
            if frame_index % 30 == 0:
                encoded, buffer = cv2.imencode(
                    ".jpg",
                    combined_frame,
                    [int(cv2.IMWRITE_JPEG_QUALITY), Config.STREAM_JPEG_QUALITY],
                )
                if encoded:
                    frame_b64 = base64.b64encode(buffer).decode("ascii")
                    frame_results.append({
                        "frame": frame_b64,
                        "detections": frame_detections,
                        "motion_data": motion_data,
                        "intrusion_alert": intrusion_alert,
                        "frame_number": frame_index,
                        "timestamp": datetime.now().isoformat()
                    })
            
            # Break if we've processed enough frames (limit to prevent timeout)
            if frame_index >= 300:  # Process max 300 frames (~10 seconds at 30fps)
                break
        
        capture.release()
        motion_detector.reset()
        
        # Calculate statistics
        detection_counts = {}
        for det in all_detections:
            class_name = det["class_name"]
            detection_counts[class_name] = detection_counts.get(class_name, 0) + 1
        
        # Prepare result
        result = {
            'success': True,
            'filename': filename,
            'analysis': {
                'total_frames_processed': frame_index,
                'total_detections': len(all_detections),
                'total_alerts': len(all_alerts),
                'detection_counts': detection_counts,
                'alerts': all_alerts[:10],  # Limit to first 10 alerts
                'sample_frames': frame_results[:5],  # First 5 sampled frames
                'video_properties': {
                    'width': width,
                    'height': height,
                    'fps': fps,
                    'duration_seconds': frame_count / fps if fps > 0 else 0
                }
            },
            'message': f'Video analyzed successfully. Processed {frame_index} frames.',
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/list', methods=['GET'])
def list_videos():
    """
    List all uploaded videos
    
    Returns:
        JSON with list of video files
    """
    try:
        if not os.path.exists(Config.UPLOAD_FOLDER):
            return jsonify({'videos': []}), 200
        
        videos = []
        for filename in os.listdir(Config.UPLOAD_FOLDER):
            if allowed_file(filename):
                filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
                file_size = os.path.getsize(filepath)
                file_mtime = os.path.getmtime(filepath)
                
                videos.append({
                    'filename': filename,
                    'filepath': filepath,
                    'size': file_size,
                    'modified_time': datetime.fromtimestamp(file_mtime).isoformat()
                })
        
        return jsonify({'videos': videos}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/delete/<filename>', methods=['DELETE'])
def delete_video(filename):
    """
    Delete a video file
    
    Args:
        filename: Name of file to delete
    
    Returns:
        JSON with deletion status
    """
    try:
        filepath = os.path.join(Config.UPLOAD_FOLDER, secure_filename(filename))
        
        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({'success': True, 'message': 'Video deleted'}), 200
        else:
            return jsonify({'error': 'File not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
