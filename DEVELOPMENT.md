# Development Setup & Tips

## Development Environment Setup

### VS Code Extensions Recommended

```
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- Flask (ms-python.flask)
- ES7+ React/Redux/React-Native snippets (dsznajder.es7-react-js-snippets)
- Tailwind CSS IntelliSense (bradlc.vscode-tailwindcss)
- Prettier (esbenp.prettier-vscode)
- ESLint (dbaeumer.vscode-eslint)
```

### Hot Reload Development

#### Backend (Flask)
```bash
cd backend
source venv/bin/activate
FLASK_ENV=development python app.py
```

The Flask app automatically reloads on code changes when `DEBUG=True` in .env

#### Frontend (React)
```bash
cd frontend
npm run dev
```

Vite provides instant hot reload for React components

### Code Formatting

```bash
# Backend (Python)
cd backend
source venv/bin/activate
black .  # Format code
flake8 . # Lint code

# Frontend (JavaScript)
cd frontend
npm run format  # Prettier formatting
npm run lint    # ESLint checking
```

## Database Management

### View Database in SQLite

```bash
# Using SQLite CLI
sqlite3 backend/surveillance.db

# List tables
.tables

# View schema
.schema

# Query example
SELECT * FROM detections LIMIT 10;
```

### Database Migrations (if needed)

```bash
# In backend directory with venv activated
flask db init
flask db migrate
flask db upgrade
```

## API Testing

### Using curl

```bash
# Get active alerts
curl http://localhost:5000/api/alert/active

# Get detection statistics
curl http://localhost:5000/api/detection/statistics

# Get dashboard stats
curl http://localhost:5000/api/history/dashboard-stats

# Export CSV
curl http://localhost:5000/api/history/export/csv -o data.csv
```

### Using Postman

Import endpoints:
- `http://localhost:5000/api/video/upload` (POST)
- `http://localhost:5000/api/alert/active` (GET)
- `http://localhost:5000/api/detection/statistics` (GET)

### Using Python

```python
import requests

# Get stats
response = requests.get('http://localhost:5000/api/history/dashboard-stats')
print(response.json())

# Upload video
with open('video.mp4', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:5000/api/video/upload', files=files)
```

## Model Development

### Testing YOLOv8 Locally

```bash
cd backend
python -c "
from video_processing.processor import VideoProcessor
processor = VideoProcessor()

import cv2
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

if ret:
    output, detections = processor.process_frame(frame)
    print(f'Detected: {len(detections)} objects')
    print(detections)
"
```

### Custom Model Training

```python
from ultralytics import YOLO

# Load pretrained model
model = YOLO('yolov8n-seg.pt')

# Train on custom dataset
results = model.train(
    data='path/to/dataset.yaml',
    epochs=50,
    imgsz=640,
    batch=16,
    device=0  # GPU ID
)

# Use custom model
model = YOLO('runs/detect/train/weights/best.pt')
results = model.predict('test_image.jpg')
```

## Performance Profiling

### Backend Profiling

```python
# Add to app.py
from werkzeug.middleware.profiler import ProfilerMiddleware
app = ProfilerMiddleware(app)
```

### Memory Usage

```bash
# Monitor memory
watch -n 1 'ps aux | grep python'

# Profile with memory_profiler
pip install memory-profiler
python -m memory_profiler app.py
```

### Frontend Performance

```javascript
// In console
performance.getEntriesByType('navigation')
performance.getEntriesByType('resource')
```

## Debugging

### Backend Debugging

```python
# Add breakpoints in VS Code
# Set breakpoint with Ctrl+Shift+B

# Or use pdb
import pdb; pdb.set_trace()
```

### Frontend Debugging

```javascript
// React DevTools
// Redux DevTools
// Chrome DevTools Network/Console/Performance

// Console logging
console.log('Detection data:', detectionData)
console.table(detections)
```

## Common Development Issues

### Port Conflicts

```bash
# Kill process on port 5000
lsof -i :5000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Kill process on port 3000
lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### Dependency Issues

```bash
# Clear pip cache
pip cache purge

# Reinstall requirements
pip install --upgrade -r requirements.txt

# Clear npm cache
npm cache clean --force
npm install
```

### CUDA Issues

```bash
# Check CUDA
nvcc --version
nvidia-smi

# Force CPU mode
# In config.py: DEVICE = 'cpu'
```

## Testing

### Backend Tests

```bash
cd backend
source venv/bin/activate
pytest tests/

# With coverage
pytest --cov=. tests/
```

### Frontend Tests

```bash
cd frontend
npm test

# With coverage
npm test -- --coverage
```

## Creating a Test Video

```python
import cv2
import numpy as np

# Create synthetic video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('test_video.mp4', fourcc, 30.0, (640, 480))

for i in range(150):  # 5 seconds at 30fps
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    # Add random rectangles to simulate objects
    cv2.rectangle(frame, (100 + i, 100), (200 + i, 200), (0, 255, 0), -1)
    out.write(frame)

out.release()
```

## Documentation Generation

```bash
# Backend
pip install sphinx
cd backend
sphinx-quickstart docs

# Frontend
npm install -g typedoc
```

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
git add .
git commit -m "Add new feature"

# Push and create PR
git push origin feature/new-feature
```

---

Happy developing! 🚀
