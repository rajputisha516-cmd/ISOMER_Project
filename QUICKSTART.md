# Isomer - Quick Start Guide

Get the AI Surveillance System up and running in minutes!

## 🚀 Prerequisites

- Python 3.8+ → Download from [python.org](https://www.python.org/downloads/)
- Node.js 16+ → Download from [nodejs.org](https://nodejs.org/)
- Git → Download from [git-scm.com](https://git-scm.com/)

Verify installations:
```bash
python --version
node --version
npm --version
```

## ⚡ Quick Start (5 minutes)

### Option 1: Automated Start Script

**Windows:**
```bash
start.bat
```

**macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```

This will:
1. Set up Python virtual environment
2. Install dependencies
3. Start backend on http://localhost:5000
4. Start frontend on http://localhost:3000

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 🎯 First Steps

1. Open http://localhost:3000 in your browser
2. You should see the Isomer dashboard
3. Click "Start Stream" button
4. Allow webcam permission when prompted
5. Watch as the system starts detecting objects!

## 📊 What You Can Do Now

- **Dashboard**: See live video with object detection overlays
- **Analytics**: View detection trends and statistics
- **History**: Browse all past detections and alerts
- **Settings**: Adjust detection thresholds and upload videos

## 🎥 Using Uploaded Videos

1. Go to Settings page
2. Upload an MP4, AVI, or MOV video file
3. System will process it frame-by-frame
4. View detections in History

## 🛠️ Troubleshooting

### Port Already in Use?
```bash
# Windows - find process using port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### Module Not Found?
```bash
# Reinstall dependencies
cd backend
pip install --upgrade -r requirements.txt

cd ../frontend
npm install
```

### Still Not Working?
Check the logs:
- Backend: Check terminal for Python errors
- Frontend: Check browser console (F12)
- Database: Check if `surveillance.db` file exists

## 📚 Next Steps

1. Read full [README.md](README.md) for complete documentation
2. Check [DEVELOPMENT.md](DEVELOPMENT.md) for development tips
3. Review [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for code organization
4. Explore [INSTALLATION.md](INSTALLATION.md) for advanced setup

## 🔧 Common Tasks

### Change Detection Sensitivity
Settings → Confidence Threshold (lower = more detections)

### Define Intrusion Zone
Dashboard → Set custom polygon zone

### Export Detection Data
History → Click "Export CSV"

### View System Health
Dashboard → Check top-right status indicators

## 📈 Performance Tips

- Use GPU if available (CUDA)
- Lower video resolution for faster processing
- Close other applications
- Use model variant: yolov8n-seg (nano) < yolov8s-seg (small)

## 🌐 Access from Other Devices

Change backend URL in `frontend/.env.local`:
```
VITE_API_URL=http://YOUR_COMPUTER_IP:5000
VITE_SOCKET_URL=http://YOUR_COMPUTER_IP:5000
```

## 🚢 Deployment

When ready for production:

**Docker:**
```bash
docker-compose up --build
```

**Vercel + Render:**
See [INSTALLATION.md](INSTALLATION.md) deployment section

## 📞 Need Help?

- Check [README.md](README.md) for detailed docs
- Review error messages in terminal
- Check browser console (F12)
- See [DEVELOPMENT.md](DEVELOPMENT.md) for debugging

## ✅ Checklist

- [ ] Python installed
- [ ] Node.js installed
- [ ] Backend running (http://localhost:5000)
- [ ] Frontend running (http://localhost:3000)
- [ ] Webcam working
- [ ] Dashboard shows live video
- [ ] Objects being detected

🎉 You're all set! Enjoy using Isomer!

---

**Version**: 1.0.0  
**Last Updated**: May 2024
