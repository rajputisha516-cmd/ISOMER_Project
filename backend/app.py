"""
Flask backend for the AI-powered smart surveillance system.
"""

import base64
import os
import threading
import time
from datetime import datetime

import cv2
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room

from motion_detection.detector import MotionDetector
from routes import alert_routes, detection_routes, history_routes, video_routes
from utils.config import Config
from utils.database import init_db
from video_processing.processor import VideoProcessor

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize Socket.IO for real-time communication
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

for directory in (
    Config.INSTANCE_DIR,
    Config.ULTRALYTICS_CONFIG_DIR,
    Config.UPLOAD_FOLDER,
    Config.CAPTURE_DIR,
    Config.HISTORY_DIR,
    Config.LOG_DIR,
):
    os.makedirs(directory, exist_ok=True)

# Initialize database
init_db(app)

# Initialize video processor and motion detector
video_processor = VideoProcessor(Config.MODEL_NAME)
motion_detector = MotionDetector()

# Global variables for video streaming
stream_lock = threading.Lock()
stream_thread = None
streaming_active = False
current_source = None
current_frame = None
detection_data = None


# ============================================================================
# INITIALIZATION
# ============================================================================

def initialize_directories():
    """Create required directories if they do not exist."""
    for directory in (
        Config.UPLOAD_FOLDER,
        Config.CAPTURE_DIR,
        Config.HISTORY_DIR,
        Config.LOG_DIR,
        Config.INSTANCE_DIR,
        Config.ULTRALYTICS_CONFIG_DIR,
    ):
        os.makedirs(directory, exist_ok=True)


def normalize_source(source):
    """Normalize incoming stream sources."""
    if isinstance(source, str):
        stripped = source.strip()
        if stripped.isdigit():
            return int(stripped)
        return stripped
    return source


def set_stream_state(active, source=None):
    """Update stream state under lock."""
    global streaming_active, current_source
    with stream_lock:
        streaming_active = active
        current_source = source if active else None


def is_streaming():
    """Return whether the stream should keep running."""
    with stream_lock:
        return streaming_active


def emit_stream_error(message):
    """Broadcast a stream error to connected clients."""
    print(f"Stream error: {message}")
    socketio.emit(
        "stream_error",
        {
            "message": message,
            "timestamp": datetime.now().isoformat(),
        },
    )


def open_video_source(source):
    """Open a webcam or file source with Windows-friendly fallbacks."""
    normalized_source = normalize_source(source)

    if isinstance(normalized_source, int) and os.name == "nt":
        for backend in (cv2.CAP_DSHOW, cv2.CAP_MSMF):
            capture = cv2.VideoCapture(normalized_source, backend)
            if capture.isOpened():
                capture.set(cv2.CAP_PROP_FRAME_WIDTH, Config.VIDEO_FRAME_WIDTH)
                capture.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.VIDEO_FRAME_HEIGHT)
                capture.set(cv2.CAP_PROP_FPS, Config.VIDEO_FPS)
                capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                return capture
            capture.release()

    capture = cv2.VideoCapture(normalized_source)
    if capture.isOpened():
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, Config.VIDEO_FRAME_WIDTH)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.VIDEO_FRAME_HEIGHT)
        capture.set(cv2.CAP_PROP_FPS, Config.VIDEO_FPS)
        capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    return capture


# ============================================================================
# SOCKET.IO EVENTS
# ============================================================================

@socketio.on("connect")
def handle_connect():
    """Handle client connection."""
    print(f"Client connected: {request.sid}")
    emit(
        "connection_response",
        {
            "data": "Connected to surveillance server",
            "streaming": is_streaming(),
        },
    )


@socketio.on("disconnect")
def handle_disconnect():
    """Handle client disconnection."""
    print(f"Client disconnected: {request.sid}")


@socketio.on("join")
def on_join(data):
    """Client joins a room for receiving updates."""
    room = (data or {}).get("room", "surveillance")
    join_room(room)
    emit("message", {"data": f"Joined room {room}"})


@socketio.on("start_stream")
def handle_start_stream(data):
    """Start video streaming."""
    global stream_thread, streaming_active, current_source

    source = normalize_source((data or {}).get("source", 0))

    with stream_lock:
        already_running = streaming_active and stream_thread and stream_thread.is_alive()
        if already_running:
            emit(
                "stream_started",
                {
                    "status": "Stream already running",
                    "source": current_source,
                },
            )
            return

        streaming_active = True
        current_source = source
        motion_detector.reset()
        stream_thread = threading.Thread(target=stream_video, args=(source,), daemon=True)
        stream_thread.start()


@socketio.on("stop_stream")
def handle_stop_stream():
    """Stop video streaming."""
    set_stream_state(False)
    motion_detector.reset()
    emit("stream_stopped", {"status": "Stream stopped"})


@socketio.on("set_intrusion_zone")
def handle_set_intrusion_zone(data):
    """Set intrusion detection zone."""
    zone = (data or {}).get("zone")
    motion_detector.set_intrusion_zone(zone)
    socketio.emit("zone_set", {"zone": zone})


# ============================================================================
# VIDEO STREAMING
# ============================================================================

def stream_video(source):
    """
    Capture video frames, process them, and emit them to connected clients.

    Args:
        source: Video source (0 for webcam or a file path)
    """
    global current_frame, detection_data

    set_stream_state(True, source)
    capture = open_video_source(source)

    if not capture.isOpened():
        set_stream_state(False)
        emit_stream_error(f"Could not open video source: {source}")
        socketio.emit("stream_stopped", {"status": "Stream stopped", "source": source})
        return

    socketio.emit(
        "stream_started",
        {
            "status": "Stream started",
            "source": source,
        },
    )

    consecutive_failures = 0
    frames_in_window = 0
    window_started_at = time.perf_counter()
    latest_fps = 0.0
    frame_index = 0
    cached_detections = []

    try:
        while is_streaming():
            ok, frame = capture.read()

            if not ok or frame is None:
                consecutive_failures += 1
                if consecutive_failures >= 5:
                    emit_stream_error(f"Unable to read frames from video source: {source}")
                    break
                time.sleep(0.1)
                continue

            consecutive_failures = 0
            frame_index += 1
            frame = cv2.resize(frame, (Config.VIDEO_FRAME_WIDTH, Config.VIDEO_FRAME_HEIGHT))

            try:
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
                emit_stream_error(f"Frame processing failed: {exc}")
                break

            combined_frame = cv2.addWeighted(annotated_frame, 0.7, motion_frame, 0.3, 0)
            intrusion_alert = motion_detector.check_intrusion(cached_detections)

            frames_in_window += 1
            elapsed = time.perf_counter() - window_started_at
            if elapsed >= 1:
                latest_fps = frames_in_window / elapsed
                frames_in_window = 0
                window_started_at = time.perf_counter()

            cv2.putText(
                combined_frame,
                f"FPS: {latest_fps:.1f}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

            encoded, buffer = cv2.imencode(
                ".jpg",
                combined_frame,
                [int(cv2.IMWRITE_JPEG_QUALITY), Config.STREAM_JPEG_QUALITY],
            )
            if not encoded:
                continue

            frame_b64 = base64.b64encode(buffer).decode("ascii")
            timestamp = datetime.now().isoformat()

            current_frame = frame_b64
            detection_data = {
                "detections": cached_detections,
                "motion_data": motion_data,
                "intrusion_alert": intrusion_alert,
                "timestamp": timestamp,
                "fps": round(latest_fps, 1),
            }

            socketio.emit(
                "video_frame",
                {
                    "frame": frame_b64,
                    "frame_encoding": "base64",
                    "detections": cached_detections,
                    "motion_data": motion_data,
                    "intrusion_alert": intrusion_alert,
                    "fps": round(latest_fps, 1),
                    "timestamp": timestamp,
                },
            )

            if intrusion_alert.get("should_alert"):
                socketio.emit(
                    "alert_triggered",
                    {
                        "type": "intrusion",
                        "message": (
                            f"{len(intrusion_alert['objects_in_zone'])} person(s) detected "
                            "inside the intrusion zone"
                        ),
                        "timestamp": timestamp,
                    },
                )

    finally:
        capture.release()
        motion_detector.reset()
        set_stream_state(False)
        socketio.emit("stream_stopped", {"status": "Stream stopped", "source": source})


# ============================================================================
# REGISTER BLUEPRINTS
# ============================================================================

app.register_blueprint(video_routes.bp)
app.register_blueprint(detection_routes.bp)
app.register_blueprint(alert_routes.bp)
app.register_blueprint(history_routes.bp)


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return (
        jsonify(
            {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "streaming": is_streaming(),
            }
        ),
        200,
    )


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    initialize_directories()
    socketio.run(
        app,
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", 5000)),
        debug=Config.DEBUG,
        use_reloader=False,
        allow_unsafe_werkzeug=True,
    )
