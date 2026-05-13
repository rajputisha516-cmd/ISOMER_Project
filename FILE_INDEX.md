# 📑 Isomer Project File Index

Quick reference for all files in the Isomer surveillance system.

## 📄 Documentation Files (Read These First!)

| File | Purpose | Read Time |
|------|---------|-----------|
| [QUICKSTART.md](QUICKSTART.md) | 5-minute quick setup guide | 5 min |
| [README.md](README.md) | Complete documentation | 20 min |
| [INSTALLATION.md](INSTALLATION.md) | Detailed installation guide | 10 min |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Development tips & debugging | 15 min |
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | Complete API reference | 20 min |
| [FEATURES.md](FEATURES.md) | All features list | 5 min |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Code organization | 10 min |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | High-level overview | 10 min |
| [COMPLETION_CHECKLIST.md](COMPLETION_CHECKLIST.md) | Deliverables checklist | 5 min |

---

## 🚀 Quick Start Files

| File | Purpose | Command |
|------|---------|---------|
| [start.bat](start.bat) | Windows auto-launcher | `start.bat` |
| [start.sh](start.sh) | Unix auto-launcher | `./start.sh` |
| [status.py](status.py) | System status checker | `python status.py` |
| [test_setup.py](test_setup.py) | Setup verification | `python test_setup.py` |

---

## 🐳 Container & Deployment

| File | Purpose |
|------|---------|
| [docker-compose.yml](docker-compose.yml) | Docker Compose configuration |
| [backend/Dockerfile](backend/Dockerfile) | Backend container image |
| [frontend/Dockerfile](frontend/Dockerfile) | Frontend container image |

---

## 🧠 Backend (Flask + AI)

### Main Application
| File | Purpose | Lines |
|------|---------|-------|
| [backend/app.py](backend/app.py) | Main Flask app, SocketIO server | 250 |

### Routes (API Endpoints)
| File | Purpose | Endpoints |
|------|---------|-----------|
| [backend/routes/video_routes.py](backend/routes/video_routes.py) | Video management | 3 endpoints |
| [backend/routes/detection_routes.py](backend/routes/detection_routes.py) | Detection APIs | 5 endpoints |
| [backend/routes/alert_routes.py](backend/routes/alert_routes.py) | Alert management | 6 endpoints |
| [backend/routes/history_routes.py](backend/routes/history_routes.py) | History & export | 6 endpoints |

### Configuration & Database
| File | Purpose | Contains |
|------|---------|----------|
| [backend/utils/config.py](backend/utils/config.py) | Configuration settings | 40+ settings |
| [backend/utils/database.py](backend/utils/database.py) | SQLAlchemy models | 5 database models |
| [backend/utils/logger.py](backend/utils/logger.py) | Logging setup | Logger configuration |

### AI & Processing
| File | Purpose | Algorithm |
|------|---------|-----------|
| [backend/video_processing/processor.py](backend/video_processing/processor.py) | YOLOv8 detection | Object detection & segmentation |
| [backend/motion_detection/detector.py](backend/motion_detection/detector.py) | Motion detection | Farneback optical flow |
| [ai_model/inference.py](ai_model/inference.py) | Model inference | Model loading & inference |

### Configuration
| File | Purpose |
|------|---------|
| [backend/.env](backend/.env) | Environment variables |
| [backend/.env.example](backend/.env.example) | Example config (all options) |
| [backend/requirements.txt](backend/requirements.txt) | Python dependencies |

---

## ⚛️ Frontend (React.js)

### Pages
| File | Purpose | Features |
|------|---------|----------|
| [frontend/src/pages/Dashboard.jsx](frontend/src/pages/Dashboard.jsx) | Main dashboard | Live video, stats, alerts |
| [frontend/src/pages/Analytics.jsx](frontend/src/pages/Analytics.jsx) | Analytics page | Charts, trends, statistics |
| [frontend/src/pages/History.jsx](frontend/src/pages/History.jsx) | History page | Searchable tables, export |
| [frontend/src/pages/Settings.jsx](frontend/src/pages/Settings.jsx) | Settings page | Configuration, uploads |

### Components
| File | Purpose | Used In |
|------|---------|---------|
| [frontend/src/components/Navbar.jsx](frontend/src/components/Navbar.jsx) | Top navigation | All pages |
| [frontend/src/components/Sidebar.jsx](frontend/src/components/Sidebar.jsx) | Left sidebar | All pages |
| [frontend/src/components/VideoStream.jsx](frontend/src/components/VideoStream.jsx) | Video player | Dashboard |
| [frontend/src/components/AlertPanel.jsx](frontend/src/components/AlertPanel.jsx) | Alert display | Dashboard |
| [frontend/src/components/StatsCard.jsx](frontend/src/components/StatsCard.jsx) | Stat cards | Dashboard, Analytics |

### Services & Configuration
| File | Purpose |
|------|---------|
| [frontend/src/services/api.js](frontend/src/services/api.js) | API client (Axios) |
| [frontend/src/App.jsx](frontend/src/App.jsx) | Root component |
| [frontend/src/main.jsx](frontend/src/main.jsx) | Entry point |
| [frontend/src/index.css](frontend/src/index.css) | Global styles |

### Configuration
| File | Purpose |
|------|---------|
| [frontend/package.json](frontend/package.json) | npm dependencies |
| [frontend/vite.config.js](frontend/vite.config.js) | Vite build config |
| [frontend/tailwind.config.js](frontend/tailwind.config.js) | Tailwind CSS config |
| [frontend/postcss.config.js](frontend/postcss.config.js) | PostCSS config |
| [frontend/index.html](frontend/index.html) | HTML template |
| [frontend/.env.example](frontend/.env.example) | Example config |

---

## 📊 Data & Models

### Database Models (in backend/utils/database.py)
- **Detection** - Stores detected objects
- **Alert** - Stores intrusion/motion alerts
- **MotionData** - Stores motion information
- **Zone** - Stores intrusion zones
- **Statistics** - Stores system stats

### AI Models
- **YOLOv8n-seg** - Object detection & segmentation
- **Farneback Optical Flow** - Motion detection

---

## 🔧 Configuration Reference

### Backend Configuration
Location: `backend/.env` (or .env.example)
- Flask settings
- Database URI
- Model configuration
- Detection thresholds
- GPU/CPU settings
- Logging configuration

### Frontend Configuration
Location: `frontend/.env.local` (or .env.example)
- API URL
- Socket URL
- Development settings

---

## 📚 How to Use This Index

### I want to...

**Get started quickly:**
→ Read [QUICKSTART.md](QUICKSTART.md)

**Understand the architecture:**
→ Read [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

**Learn the API:**
→ Read [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

**Set up properly:**
→ Read [INSTALLATION.md](INSTALLATION.md)

**Develop/extend the system:**
→ Read [DEVELOPMENT.md](DEVELOPMENT.md)

**See all features:**
→ Read [FEATURES.md](FEATURES.md)

**Debug an issue:**
→ Check [DEVELOPMENT.md](DEVELOPMENT.md) Troubleshooting section

**Deploy to production:**
→ Read [INSTALLATION.md](INSTALLATION.md) Deployment section

**Understand the code:**
→ Check code comments and docstrings in each file

---

## 📁 File Organization by Type

### Python Files (Backend)
```
backend/
├── app.py                          (Main application)
├── routes/
│   ├── video_routes.py
│   ├── detection_routes.py
│   ├── alert_routes.py
│   └── history_routes.py
├── utils/
│   ├── config.py
│   ├── database.py
│   └── logger.py
├── motion_detection/
│   └── detector.py
├── video_processing/
│   └── processor.py
├── requirements.txt
└── .env (and .env.example)

ai_model/
└── inference.py
```

### JavaScript Files (Frontend)
```
frontend/
├── src/
│   ├── pages/
│   │   ├── Dashboard.jsx
│   │   ├── Analytics.jsx
│   │   ├── History.jsx
│   │   └── Settings.jsx
│   ├── components/
│   │   ├── Navbar.jsx
│   │   ├── Sidebar.jsx
│   │   ├── VideoStream.jsx
│   │   ├── AlertPanel.jsx
│   │   └── StatsCard.jsx
│   ├── services/
│   │   └── api.js
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
└── Configuration files
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── postcss.config.js
    └── index.html
```

### Configuration & Scripts
```
Root/
├── docker-compose.yml
├── start.bat (Windows)
├── start.sh (Unix)
├── status.py (System status)
└── test_setup.py (Diagnostics)
```

### Documentation
```
Root/
├── README.md (Complete guide)
├── QUICKSTART.md (5-min setup)
├── INSTALLATION.md (Detailed setup)
├── DEVELOPMENT.md (Dev guide)
├── API_DOCUMENTATION.md (API reference)
├── FEATURES.md (Features list)
├── PROJECT_STRUCTURE.md (Code org)
├── PROJECT_SUMMARY.md (Overview)
├── COMPLETION_CHECKLIST.md (Deliverables)
└── FILE_INDEX.md (This file)
```

---

## 🎯 File Statistics

| Metric | Count |
|--------|-------|
| Total Files | 55+ |
| Python Files | 15 |
| JavaScript Files | 12 |
| Documentation Files | 10 |
| Configuration Files | 6 |
| Container Files | 3 |
| Script Files | 3 |
| Lines of Code | 5000+ |
| API Endpoints | 20+ |
| Database Tables | 5 |
| Pages | 4 |
| Components | 5 |

---

## 💡 Quick Navigation

### I need to modify...

**Video processing:**
→ `backend/video_processing/processor.py`

**Motion detection:**
→ `backend/motion_detection/detector.py`

**Database:**
→ `backend/utils/database.py`

**API endpoints:**
→ `backend/routes/*.py`

**Frontend UI:**
→ `frontend/src/pages/*.jsx`

**Styling:**
→ `frontend/src/index.css`

**Configuration:**
→ `backend/.env` or `frontend/.env.local`

---

## 🔗 File Dependencies

### Backend Dependencies
```
app.py
├── routes/* (all route files)
├── utils/config.py
├── utils/database.py
├── utils/logger.py
├── video_processing/processor.py
└── motion_detection/detector.py
    ├── PyTorch
    ├── OpenCV
    └── NumPy
```

### Frontend Dependencies
```
App.jsx
├── pages/* (all page files)
├── components/* (all components)
├── services/api.js
├── Tailwind CSS
├── Recharts
└── Socket.IO
```

---

## 🚀 Execution Flow

1. **Start Backend**: `python backend/app.py`
2. **Start Frontend**: `npm -C frontend run dev`
3. **Access Dashboard**: http://localhost:3000
4. **Backend Processes**: 
   - Captures video frames
   - Runs AI detection
   - Detects motion
   - Checks intrusions
   - Sends to frontend via WebSocket
5. **Frontend Updates**:
   - Displays video stream
   - Shows detections
   - Displays alerts
   - Updates analytics

---

## 📞 File Reading Order

For complete understanding, read in this order:

1. **QUICKSTART.md** - Get running (5 min)
2. **README.md** - Understand project (20 min)
3. **PROJECT_STRUCTURE.md** - Understand code org (10 min)
4. **API_DOCUMENTATION.md** - Learn APIs (20 min)
5. **FEATURES.md** - See all capabilities (5 min)
6. **DEVELOPMENT.md** - For development work (15 min)
7. **Code Files** - Deep dive as needed (varies)

---

## ✅ All Files Created

- ✅ 55+ files
- ✅ 5000+ lines of code
- ✅ 10 documentation files
- ✅ Complete frontend
- ✅ Complete backend
- ✅ AI models ready
- ✅ Docker support
- ✅ Deployment ready

---

**Last Updated**: May 2024  
**Version**: 1.0.0  
**Status**: ✅ Complete
