# Isomer - AI-Powered Smart Surveillance & Intrusion Detection System

A production-ready, full-stack intelligent surveillance system built with modern web technologies and advanced AI/Deep Learning models. Real-time video processing with YOLOv8 segmentation, motion detection using optical flow, and comprehensive intrusion detection with alerts.

## 🎯 Project Overview

Isomer is a complete surveillance solution that combines:

- **Real-time video streaming** from webcams or video files
- **YOLOv8 AI segmentation** for advanced object detection
- **Farneback optical flow** for motion detection
- **Intrusion zone detection** with customizable alerts
- **Modern web dashboard** for monitoring and analytics
- **Complete REST API** for programmatic access
- **WebSocket real-time updates** for live notifications

## ✨ Key Features

### 1. Video Processing
- Real-time webcam streaming at 30+ FPS
- Support for video file uploads
- Configurable frame resolution and quality
- Automatic frame optimization for processing

### 2. AI Object Detection
- YOLOv8 nano segmentation model
- Detects: persons, vehicles, animals, and more
- Segmentation masks for pixel-perfect detection
- Confidence-based filtering
- GPU acceleration support

### 3. Motion Detection
- Farneback optical flow algorithm
- Visualized motion vectors
- Motion intensity measurement
- Region-based motion extraction
- Configurable sensitivity

### 4. Intrusion Detection
- Custom polygon zone definition
- Real-time zone violation detection
- Instant alert generation
- Snapshot capture on intrusion

### 5. Alert System
- Categorized alerts (intrusion, motion, unknown objects)
- Severity levels (low, medium, high)
- Alert acknowledgment system
- Real-time WebSocket notifications
- Email integration ready

### 6. Dashboard & Analytics
- Live video feed with overlays
- Real-time statistics and metrics
- 7-day historical trends
- Detection and alert distributions
- FPS counter and performance metrics

### 7. Data Management
- SQLite database for persistence
- Detection history storage
- Alert logging
- CSV export functionality
- Configurable data retention

## 🏗️ Architecture

```
Frontend (React)          Backend (Flask)           AI Models (PyTorch)
├── Dashboard            ├── Video Processing       ├── YOLOv8 Segmentation
├── Analytics            ├── Motion Detection       ├── Optical Flow
├── History              ├── Intrusion Detection    └── Model Inference
└── Settings             ├── REST APIs
                        ├── WebSocket Server
                        └── SQLite Database
```

## 📋 Tech Stack

### Frontend
- **React 18** - UI framework
- **React Router** - Navigation
- **Tailwind CSS** - Modern styling with glassmorphism
- **Recharts** - Analytics and data visualization
- **Socket.IO Client** - Real-time communication
- **Axios** - HTTP client
- **Vite** - Fast build tool

### Backend
- **Flask 2.3** - Web framework
- **Flask-SocketIO** - Real-time bidirectional communication
- **Flask-SQLAlchemy** - ORM database
- **OpenCV 4.8** - Computer vision and video processing
- **NumPy** - Numerical computing

### AI/Deep Learning
- **PyTorch** - Deep learning framework
- **Ultralytics YOLOv8** - Object detection and segmentation
- **scikit-image** - Image processing utilities

## 🚀 Getting Started

### Prerequisites

- Python 3.8+ (for backend)
- Node.js 16+ (for frontend)
- Git
- 4GB RAM minimum (8GB+ recommended with GPU)
- NVIDIA GPU (optional but recommended for real-time processing)

### Backend Setup

1. **Clone or navigate to the backend directory:**

```bash
cd backend
```

2. **Create a Python virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

4. **Download YOLOv8 model (automatic on first run):**

The model will be downloaded automatically when the application first starts. Alternatively, download manually:

```bash
python -c "from ultralytics import YOLO; YOLO('yolov8n-seg.pt')"
```

5. **Create environment file:**

```bash
cp .env .env.local
# Edit .env.local with your settings
```

6. **Run the backend server:**

```bash
python app.py
```

The backend will start on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**

```bash
cd frontend
```

2. **Install dependencies:**

```bash
npm install
```

3. **Create environment file:**

```bash
echo "VITE_API_URL=http://localhost:5000" > .env.local
```

4. **Start development server:**

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 🔧 Configuration

### Backend Configuration (backend/utils/config.py)

```python
# Detection Settings
CONFIDENCE_THRESHOLD = 0.5  # Object detection confidence
NMS_THRESHOLD = 0.45        # Non-Maximum Suppression
MOTION_THRESHOLD = 0.1      # Motion detection sensitivity

# Model Settings
MODEL_NAME = 'yolov8n-seg'  # YOLOv8 model variant
CLASSES_TO_DETECT = ['person', 'car', 'truck', 'bus']

# Video Settings
VIDEO_FRAME_WIDTH = 640
VIDEO_FRAME_HEIGHT = 480
VIDEO_FPS = 30
```

### Frontend Configuration

Edit `frontend/.env.local`:

```
VITE_API_URL=http://localhost:5000
VITE_SOCKET_URL=http://localhost:5000
```

## 📡 API Endpoints

### Video Management

```
POST   /api/video/upload          - Upload video file
GET    /api/video/list            - List uploaded videos
DELETE /api/video/delete/<name>   - Delete video
```

### Detection

```
GET    /api/detection/history     - Detection history
GET    /api/detection/statistics  - Detection statistics
POST   /api/detection/save        - Save detection record
DELETE /api/detection/clear       - Clear detections
```

### Alerts

```
GET    /api/alert/all             - All alerts
GET    /api/alert/active          - Active (unacknowledged) alerts
POST   /api/alert/create          - Create alert
PUT    /api/alert/acknowledge/<id> - Acknowledge alert
GET    /api/alert/statistics      - Alert statistics
```

### History & Export

```
GET    /api/history/detections    - Detection history
GET    /api/history/alerts        - Alert history
GET    /api/history/export/csv    - Export as CSV
GET    /api/history/daily-summary - 7-day summary
GET    /api/history/dashboard-stats - Dashboard metrics
```

### Health Check

```
GET    /api/health                - System health status
```

## 🔌 WebSocket Events

### Client → Server

```javascript
// Start video streaming
socket.emit('start_stream', { source: 0 })  // 0 = webcam, or file path

// Stop streaming
socket.emit('stop_stream')

// Set intrusion zone
socket.emit('set_intrusion_zone', { zone: [[x1,y1], [x2,y2], ...] })

// Join room for updates
socket.emit('join', { room: 'surveillance' })
```

### Server → Client

```javascript
// Video frame with detection data
socket.on('video_frame', (data) => {
  // data.frame - processed video frame (hex)
  // data.detections - detected objects
  // data.motion_data - motion information
  // data.intrusion_alert - intrusion detection
  // data.fps - frames per second
})

// Stream events
socket.on('stream_started', (data) => {})
socket.on('stream_stopped', (data) => {})

// Zone updates
socket.on('zone_set', (data) => {})
```

## 📊 Database Schema

### Models

**Detection**
- id: Integer (Primary Key)
- timestamp: DateTime
- frame_id: String
- objects_detected: JSON (list of detections)
- confidence_score: Float
- image_path: String

**Alert**
- id: Integer (Primary Key)
- timestamp: DateTime
- alert_type: String (intrusion, motion, unknown_object)
- location: String
- severity: String (low, medium, high)
- message: Text
- image_path: String
- acknowledged: Boolean

**MotionData**
- id: Integer (Primary Key)
- timestamp: DateTime
- motion_detected: Boolean
- motion_intensity: Float (0-1)
- motion_vectors: JSON

**Zone**
- id: Integer (Primary Key)
- name: String
- coordinates: JSON (polygon points)
- enabled: Boolean

**Statistics**
- id: Integer (Primary Key)
- timestamp: DateTime
- total_detections: Integer
- total_alerts: Integer
- average_fps: Float
- uptime_seconds: Integer

## 🎓 Usage Examples

### Starting Video Stream

```bash
# In the dashboard, click "Start Stream"
# Or via curl:
curl -X POST http://localhost:5000/api/video/upload \
  -F "file=@video.mp4"
```

### Checking Active Alerts

```bash
curl http://localhost:5000/api/alert/active
```

### Exporting Data

```bash
curl http://localhost:5000/api/history/export/csv \
  -o surveillance_data.csv
```

### Getting Dashboard Stats

```bash
curl http://localhost:5000/api/history/dashboard-stats
```

## 🚢 Deployment

### Frontend Deployment (Vercel)

1. Push frontend to GitHub
2. Import repository in Vercel
3. Set environment variables
4. Deploy

```bash
npm run build
```

### Backend Deployment (Render/Railway)

1. Create account on Render or Railway
2. Connect GitHub repository
3. Set environment variables
4. Deploy

**Environment Variables:**
```
FLASK_ENV=production
SECRET_KEY=<your-secret-key>
DATABASE_URL=<database-connection-string>
```

### Docker Deployment

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=sqlite:///surveillance.db
    volumes:
      - ./data:/app/data

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://backend:5000

networks:
  default:
    name: surveillance-network
```

## 🔒 Security Considerations

1. **Change secret key in production**
2. **Use HTTPS in production**
3. **Implement authentication for API**
4. **Validate all user inputs**
5. **Use environment variables for sensitive data**
6. **Implement rate limiting**
7. **Enable CORS only for trusted origins**
8. **Regular security audits**

## 🐛 Troubleshooting

### CUDA Out of Memory
- Reduce model size (e.g., yolov8n instead of yolov8l)
- Reduce video resolution
- Disable GPU acceleration

### WebSocket Connection Issues
- Check firewall settings
- Verify backend is running
- Check CORS configuration
- Ensure correct API URL in frontend

### Model Download Issues
```bash
# Manual model download
python -c "from ultralytics import YOLO; YOLO('yolov8n-seg.pt')"
```

### Database Errors
```bash
# Reset database
rm backend/surveillance.db
python backend/app.py
```

## 📈 Performance Optimization

1. **GPU Acceleration**: Use CUDA-enabled GPU
2. **Model Quantization**: Use smaller YOLOv8 variants
3. **Frame Batching**: Process multiple frames together
4. **Caching**: Cache results for redundant detections
5. **Database Indexing**: Add indexes on frequently queried fields
6. **CDN**: Use CDN for frontend assets

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

MIT License - See LICENSE file for details

## 📧 Support

For issues and questions:
- Create an issue on GitHub
- Email: support@example.com
- Documentation: https://docs.example.com

## 🙏 Acknowledgments

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [OpenCV](https://opencv.org/)
- [Flask](https://flask.palletsprojects.com/)
- [React](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)

## 🗺️ Roadmap

- [ ] Multi-camera support
- [ ] Face blur/recognition
- [ ] Telegram bot integration
- [ ] Email alerts
- [ ] Heatmap generation
- [ ] Advanced object tracking
- [ ] Cloud storage integration
- [ ] Mobile app (React Native)
- [ ] Advanced analytics
- [ ] Custom model training

---

**Version**: 1.0.0  
**Last Updated**: May 2024  
**Maintained by**: Isomer Team
