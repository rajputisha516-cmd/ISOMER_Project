# Installation and Setup Guide

## Quick Start (Development)

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git
- 8GB RAM (recommended)

### Step 1: Clone/Extract Project

```bash
cd Isomer
```

### Step 2: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env .env.local  # Windows
cp .env .env.local    # macOS/Linux

# Start server
python app.py
```

Backend will run on http://localhost:5000

### Step 3: Frontend Setup

```bash
# In a new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on http://localhost:3000

## Accessing the Application

1. Open browser: http://localhost:3000
2. Start with Dashboard tab
3. Click "Start Stream" to begin surveillance
4. View detections, alerts, and analytics

## Common Issues & Solutions

### Port Already in Use
```bash
# Kill process on port 5000 (Flask)
lsof -i :5000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Kill process on port 3000 (React)
lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### CUDA/GPU Issues
If you encounter GPU-related errors:

1. Update your GPU drivers
2. Edit backend/utils/config.py:
   ```python
   DEVICE = 'cpu'  # Force CPU mode
   ```

### Model Download Issues
If YOLOv8 model fails to download:

```bash
python -c "from ultralytics import YOLO; YOLO('yolov8n-seg.pt')"
```

## Production Deployment

### Using Docker

```bash
# Build and run
docker-compose up --build

# Access
http://localhost:3000
```

### Using Vercel (Frontend) + Render (Backend)

1. **Backend (Render)**
   - Connect GitHub repository
   - Set Python version: 3.9
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
   - Add environment variables

2. **Frontend (Vercel)**
   - Connect GitHub repository
   - Framework: React
   - Build command: `npm run build`
   - Output directory: `dist`
   - Environment: `VITE_API_URL=<render-url>`

## Testing

### Backend Testing
```bash
cd backend
pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

## Key Directories

```
backend/
├── app.py              # Main Flask app
├── routes/            # API route handlers
├── models/            # Database models
├── utils/             # Configuration & utilities
├── motion_detection/  # Motion detection module
├── video_processing/  # Video processing with YOLOv8
└── requirements.txt   # Python dependencies

frontend/
├── src/
│   ├── components/    # React components
│   ├── pages/        # Page components
│   ├── services/     # API services
│   ├── App.jsx       # Main app
│   └── index.css     # Tailwind styles
├── package.json      # Dependencies
└── vite.config.js   # Build config

ai_model/
└── inference.py      # Model inference utilities
```

## Default Credentials & Settings

- **Backend API**: http://localhost:5000
- **Frontend**: http://localhost:3000
- **Database**: SQLite (surveillance.db)
- **Default Model**: YOLOv8 Nano Segmentation
- **Confidence Threshold**: 0.5
- **Motion Threshold**: 0.1

## Useful Commands

```bash
# Backend
python app.py                  # Start server
pip freeze > requirements.txt  # Update dependencies

# Frontend
npm run dev       # Development
npm run build     # Production build
npm run preview   # Preview build

# Database
sqlite3 surveillance.db        # Direct DB access
```

## Next Steps

1. Configure detection thresholds in Settings
2. Define intrusion zones
3. Set up email alerts (optional)
4. Monitor analytics dashboard
5. Export detection history as needed

## Documentation

See README.md for complete documentation.
