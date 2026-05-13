# API Documentation

Complete reference for all Isomer backend APIs.

## Base URL

```
http://localhost:5000/api
```

## 📹 Video Routes

### Upload Video

**Endpoint:** `POST /video/upload`

Upload a video file for processing.

**Request:**
```bash
curl -X POST http://localhost:5000/api/video/upload \
  -F "file=@video.mp4"
```

**Response:**
```json
{
  "success": true,
  "filename": "20240513_120000_video.mp4",
  "filepath": "uploads/20240513_120000_video.mp4",
  "message": "File uploaded successfully",
  "timestamp": "2024-05-13T12:00:00"
}
```

**Status Codes:**
- `200` - Upload successful
- `400` - No file provided or invalid format
- `500` - Server error

---

### List Videos

**Endpoint:** `GET /video/list`

Get all uploaded videos.

**Request:**
```bash
curl http://localhost:5000/api/video/list
```

**Response:**
```json
{
  "videos": [
    {
      "filename": "20240513_120000_video.mp4",
      "filepath": "uploads/20240513_120000_video.mp4",
      "size": 1048576,
      "modified_time": "2024-05-13T12:00:00"
    }
  ]
}
```

---

### Delete Video

**Endpoint:** `DELETE /video/delete/<filename>`

Delete a video file.

**Request:**
```bash
curl -X DELETE http://localhost:5000/api/video/delete/video.mp4
```

**Response:**
```json
{
  "success": true,
  "message": "Video deleted"
}
```

---

## 🎯 Detection Routes

### Detection History

**Endpoint:** `GET /detection/history`

Get detection history with pagination.

**Query Parameters:**
- `limit` (int, default=50) - Number of records
- `offset` (int, default=0) - Pagination offset

**Request:**
```bash
curl "http://localhost:5000/api/detection/history?limit=10&offset=0"
```

**Response:**
```json
{
  "success": true,
  "total": 1500,
  "count": 10,
  "detections": [
    {
      "id": 1,
      "timestamp": "2024-05-13T12:30:45",
      "frame_id": "frame_001",
      "objects": [
        {
          "class_name": "person",
          "confidence": 0.95,
          "x": 100,
          "y": 150,
          "width": 200,
          "height": 300
        }
      ],
      "confidence": 0.95,
      "image_path": "captures/frame_001.jpg"
    }
  ]
}
```

---

### Detection Statistics

**Endpoint:** `GET /detection/statistics`

Get aggregated detection statistics.

**Request:**
```bash
curl http://localhost:5000/api/detection/statistics
```

**Response:**
```json
{
  "success": true,
  "total_detections": 1500,
  "recent_detections": 125,
  "class_distribution": {
    "person": 850,
    "car": 400,
    "truck": 150,
    "bicycle": 100
  },
  "most_detected": "person"
}
```

---

### Save Detection

**Endpoint:** `POST /detection/save`

Manually save a detection record.

**Request Body:**
```json
{
  "frame_id": "frame_001",
  "objects_detected": [
    {
      "class_name": "person",
      "confidence": 0.95,
      "x": 100,
      "y": 150,
      "width": 200,
      "height": 300
    }
  ],
  "confidence_score": 0.95,
  "image_path": "captures/frame_001.jpg"
}
```

**Response:**
```json
{
  "success": true,
  "detection_id": 1,
  "timestamp": "2024-05-13T12:30:45"
}
```

---

### Clear Detections

**Endpoint:** `DELETE /detection/clear`

Delete all detection records (admin only).

**Request:**
```bash
curl -X DELETE http://localhost:5000/api/detection/clear
```

**Response:**
```json
{
  "success": true,
  "deleted_count": 1500,
  "message": "1500 detection records deleted"
}
```

---

## 🚨 Alert Routes

### Get All Alerts

**Endpoint:** `GET /alert/all`

Get all alerts with optional filtering.

**Query Parameters:**
- `alert_type` - Filter by type (intrusion, motion, unknown_object)
- `severity` - Filter by severity (low, medium, high)
- `acknowledged` - Filter by status (true/false)
- `limit` - Number of records (default=100)
- `offset` - Pagination offset (default=0)

**Request:**
```bash
curl "http://localhost:5000/api/alert/all?severity=high&limit=20"
```

**Response:**
```json
{
  "success": true,
  "total": 50,
  "count": 20,
  "alerts": [
    {
      "id": 1,
      "timestamp": "2024-05-13T12:45:00",
      "type": "intrusion",
      "location": "zone_1",
      "severity": "high",
      "message": "Person detected in restricted zone",
      "image_path": "captures/intrusion_001.jpg",
      "acknowledged": false
    }
  ]
}
```

---

### Get Active Alerts

**Endpoint:** `GET /alert/active`

Get only unacknowledged alerts.

**Request:**
```bash
curl http://localhost:5000/api/alert/active
```

**Response:**
```json
{
  "success": true,
  "count": 3,
  "alerts": [
    {
      "id": 1,
      "timestamp": "2024-05-13T12:45:00",
      "type": "intrusion",
      "severity": "high",
      "message": "Person detected in restricted zone",
      "location": "zone_1"
    }
  ]
}
```

---

### Create Alert

**Endpoint:** `POST /alert/create`

Create a new alert.

**Request Body:**
```json
{
  "alert_type": "intrusion",
  "location": "zone_1",
  "severity": "high",
  "message": "Person detected in restricted zone",
  "image_path": "captures/intrusion_001.jpg"
}
```

**Response:**
```json
{
  "success": true,
  "alert_id": 1,
  "timestamp": "2024-05-13T12:45:00"
}
```

---

### Acknowledge Alert

**Endpoint:** `PUT /alert/acknowledge/<alert_id>`

Mark an alert as acknowledged.

**Request:**
```bash
curl -X PUT http://localhost:5000/api/alert/acknowledge/1
```

**Response:**
```json
{
  "success": true,
  "alert_id": 1,
  "acknowledged": true
}
```

---

### Alert Statistics

**Endpoint:** `GET /alert/statistics`

Get alert statistics.

**Request:**
```bash
curl http://localhost:5000/api/alert/statistics
```

**Response:**
```json
{
  "success": true,
  "total_alerts": 150,
  "active_alerts": 5,
  "severity_distribution": {
    "low": 50,
    "medium": 60,
    "high": 40
  },
  "type_distribution": {
    "intrusion": 80,
    "motion": 50,
    "unknown_object": 20
  }
}
```

---

## 📊 History Routes

### Detection History

**Endpoint:** `GET /history/detections`

Get detection history with date filtering.

**Query Parameters:**
- `start_date` - Format: YYYY-MM-DD
- `end_date` - Format: YYYY-MM-DD
- `limit` - Number of records (default=500)

**Request:**
```bash
curl "http://localhost:5000/api/history/detections?start_date=2024-05-10&end_date=2024-05-13"
```

---

### Alert History

**Endpoint:** `GET /history/alerts`

Get alert history with date filtering.

**Query Parameters:**
- `start_date` - Format: YYYY-MM-DD
- `end_date` - Format: YYYY-MM-DD
- `severity` - Filter by severity
- `limit` - Number of records (default=500)

**Request:**
```bash
curl "http://localhost:5000/api/history/alerts?severity=high"
```

---

### Export to CSV

**Endpoint:** `GET /history/export/csv`

Export all data as CSV file.

**Request:**
```bash
curl http://localhost:5000/api/history/export/csv -o data.csv
```

---

### Daily Summary

**Endpoint:** `GET /history/daily-summary`

Get 7-day summary statistics.

**Request:**
```bash
curl http://localhost:5000/api/history/daily-summary
```

**Response:**
```json
{
  "success": true,
  "summary": [
    {
      "date": "2024-05-13",
      "detections": 145,
      "alerts": 12,
      "intrusions": 3
    },
    {
      "date": "2024-05-12",
      "detections": 132,
      "alerts": 8,
      "intrusions": 1
    }
  ]
}
```

---

### Dashboard Statistics

**Endpoint:** `GET /history/dashboard-stats`

Get comprehensive dashboard statistics.

**Request:**
```bash
curl http://localhost:5000/api/history/dashboard-stats
```

**Response:**
```json
{
  "success": true,
  "total_detections": 1500,
  "total_alerts": 150,
  "active_alerts": 5,
  "detections_24h": 145,
  "alerts_24h": 12,
  "timestamp": "2024-05-13T12:30:45"
}
```

---

## 💚 Health Check

### System Health

**Endpoint:** `GET /health`

Check system health status.

**Request:**
```bash
curl http://localhost:5000/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-05-13T12:30:45",
  "streaming": true
}
```

---

## 🔌 WebSocket Events

### Connection

**Event:** `connect`

**Response:**
```json
{
  "data": "Connected to surveillance server"
}
```

---

### Join Room

**Event:** `join`

**Emit:**
```javascript
socket.emit('join', { room: 'surveillance' })
```

---

### Start Stream

**Event:** `start_stream`

**Emit:**
```javascript
socket.emit('start_stream', { source: 0 })  // 0 = webcam
socket.emit('start_stream', { source: 'path/to/video.mp4' })
```

**Response:**
```json
{
  "status": "Stream started"
}
```

---

### Stop Stream

**Event:** `stop_stream`

**Emit:**
```javascript
socket.emit('stop_stream')
```

**Response:**
```json
{
  "status": "Stream stopped"
}
```

---

### Video Frame

**Event:** `video_frame`

**Receive:**
```javascript
socket.on('video_frame', (data) => {
  // data.frame - processed frame (hex)
  // data.detections - detected objects
  // data.motion_data - motion information
  // data.intrusion_alert - intrusion detection
  // data.fps - frames per second
  // data.timestamp - frame timestamp
})
```

---

### Set Intrusion Zone

**Event:** `set_intrusion_zone`

**Emit:**
```javascript
socket.emit('set_intrusion_zone', {
  zone: [[100, 100], [500, 100], [500, 500], [100, 500]]
})
```

**Response:**
```json
{
  "zone": [[100, 100], [500, 100], [500, 500], [100, 500]]
}
```

---

## Error Responses

### 400 Bad Request

```json
{
  "error": "Invalid request parameters"
}
```

### 404 Not Found

```json
{
  "error": "Resource not found"
}
```

### 500 Server Error

```json
{
  "error": "Internal server error"
}
```

---

## Rate Limiting

No rate limiting currently implemented. Consider adding for production.

## Authentication

Currently no authentication. Implement JWT tokens for production.

## CORS

Enabled for `localhost:3000`. Update `app.py` for production.

---

**Last Updated:** May 2024  
**API Version:** 1.0.0
