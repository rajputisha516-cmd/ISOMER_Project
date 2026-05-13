# Isomer Project Structure

```
Isomer/
│
├── frontend/                          # React.js frontend application
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx            # Top navigation bar
│   │   │   ├── Sidebar.jsx           # Left sidebar navigation
│   │   │   ├── VideoStream.jsx       # Live video player
│   │   │   ├── AlertPanel.jsx        # Active alerts display
│   │   │   └── StatsCard.jsx         # Statistics cards
│   │   │
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx         # Main dashboard page
│   │   │   ├── Analytics.jsx         # Analytics & insights page
│   │   │   ├── History.jsx           # Detection history page
│   │   │   └── Settings.jsx          # Settings page
│   │   │
│   │   ├── services/
│   │   │   └── api.js                # API client with axios
│   │   │
│   │   ├── App.jsx                   # Root component
│   │   ├── main.jsx                  # Entry point
│   │   └── index.css                 # Global styles
│   │
│   ├── public/                        # Static assets
│   ├── package.json                   # Node dependencies
│   ├── vite.config.js                 # Vite configuration
│   ├── tailwind.config.js             # Tailwind configuration
│   ├── postcss.config.js              # PostCSS configuration
│   ├── index.html                     # HTML template
│   └── .gitignore
│
├── backend/                           # Flask backend application
│   ├── app.py                         # Main Flask application
│   │
│   ├── routes/
│   │   ├── video_routes.py            # Video upload/management APIs
│   │   ├── detection_routes.py        # Detection history APIs
│   │   ├── alert_routes.py            # Alert management APIs
│   │   ├── history_routes.py          # History & export APIs
│   │   └── __init__.py
│   │
│   ├── models/
│   │   └── __init__.py                # Database models (imported from utils)
│   │
│   ├── utils/
│   │   ├── config.py                  # Configuration settings
│   │   ├── database.py                # SQLAlchemy models & DB init
│   │   ├── logger.py                  # Logging configuration
│   │   └── __init__.py
│   │
│   ├── motion_detection/
│   │   ├── detector.py                # Optical flow motion detection
│   │   └── __init__.py
│   │
│   ├── video_processing/
│   │   ├── processor.py               # YOLOv8 video processing
│   │   └── __init__.py
│   │
│   ├── requirements.txt               # Python dependencies
│   ├── .env                          # Environment configuration
│   └── .gitignore
│
├── ai_model/                          # AI model utilities
│   ├── inference.py                   # YOLOv8 inference pipeline
│   └── __init__.py
│
├── README.md                          # Complete documentation
├── INSTALLATION.md                    # Installation guide
└── PROJECT_STRUCTURE.md              # This file

```

## File Descriptions

### Frontend Files

**Components:**
- `Navbar.jsx` - Top navigation with status indicators
- `Sidebar.jsx` - Navigation menu with collapsed state
- `VideoStream.jsx` - Canvas-based video player
- `AlertPanel.jsx` - Real-time alert notifications
- `StatsCard.jsx` - Reusable statistics display

**Pages:**
- `Dashboard.jsx` - Main surveillance interface
- `Analytics.jsx` - Charts and trend analysis
- `History.jsx` - Searchable detection history
- `Settings.jsx` - Configuration and uploads

**Services:**
- `api.js` - Axios instance with interceptors

### Backend Files

**Routes:**
- `video_routes.py` - Upload, list, delete videos
- `detection_routes.py` - Get and save detection records
- `alert_routes.py` - Create and acknowledge alerts
- `history_routes.py` - Export and analytics data

**Core Modules:**
- `app.py` - Flask app, SocketIO, main logic
- `config.py` - All configuration parameters
- `database.py` - SQLAlchemy models
- `detector.py` - Farneback optical flow implementation
- `processor.py` - YOLOv8 segmentation pipeline

### AI Model Files

- `inference.py` - Model loading and inference utilities

## Key Technologies in Each File

### Frontend
- **React 18** - All .jsx files
- **React Router** - Page navigation in App.jsx
- **Tailwind CSS** - Styling in index.css and all components
- **Recharts** - Analytics.jsx graphs
- **Socket.IO** - Real-time in VideoStream.jsx, AlertPanel.jsx
- **Axios** - API calls via services/api.js

### Backend
- **Flask** - app.py and all route files
- **Flask-SocketIO** - Real-time communication in app.py
- **SQLAlchemy** - ORM models in database.py
- **OpenCV** - Video processing in processor.py and detector.py
- **YOLOv8** - Model loading in processor.py
- **NumPy** - Array operations throughout

### Database
- **SQLite** - Default database (surveillance.db)
- Tables: Detection, Alert, MotionData, Zone, Statistics

## API Endpoints Structure

All endpoints follow REST conventions:

```
/api/video/        - Video management
/api/detection/    - Detection records
/api/alert/        - Alert management
/api/history/      - Historical data
```

## Component Hierarchy

```
App
├── Navbar
├── Sidebar
└── Routes
    ├── Dashboard
    │   ├── VideoStream
    │   ├── AlertPanel
    │   └── StatsCard (x4)
    ├── Analytics
    │   └── Recharts components
    ├── History
    │   └── Detection/Alert tables
    └── Settings
        └── Configuration forms
```

## Data Flow

1. **Frontend** sends requests to Backend API via Axios
2. **Backend** processes requests and sends responses
3. **Real-time updates** via WebSocket from Backend
4. **Database** stores all data in SQLite
5. **Frontend** displays data and allows user interactions

## Extension Points

Easy to add:
- New detection models (replace processor.py)
- Additional API endpoints (new files in routes/)
- New UI pages (new files in pages/)
- Database models (new classes in database.py)
- Detection algorithms (new files in motion_detection/)

---

For detailed implementation info, see README.md
