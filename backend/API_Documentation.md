# EdgeSafe Backend API Documentation

---

## GET /

### Purpose:
Check if the API is running

### Response: 
{
  "message": "EdgeSafe API running"
}

## GET /events

### Purpose:
Retrieve all logged detection events

### Query Parameters:
- `detected`: Filter by detection result 
- `source`: Filter by camera source
- `limit`: Limit num. of results

### Response:
[
  {
    "id": 1,
    "model_name": "YOLO",
    "inference_ms": 10,
    "timestamp": "2026-04-15T10:30:00.123456",
    "confidence": 0.91,
    "detected": true,
    "source": "CAM 1",
    "image_path": "images/test1.jpg"
  },
  {
    "id": 2,
    "model_name": "YOLOv11n",
    "inference_ms": 12,
    "timestamp": "2026-04-15T10:30:01.456789",
    "confidence": 0.87,
    "detected": true,
    "source": "CAM 2",
    "image_path": "images/test2.jpg"
  }
]

## GET /events/{event_id}

### Purpose:
Retrieve a specific detection event by ID

### Path Parameters:
- `event_id`: The ID of the event to retrieve

### Response (Success):
{
  "id": 1,
  "model_name": "YOLO",
  "inference_ms": 10,
  "timestamp": "2026-04-15T10:30:00.123456",
  "confidence": 0.91,
  "detected": true,
  "source": "CAM 1",
  "image_path": "images/test1.jpg"
}

### Response (Not Found):
{
  "detail": "Event not found"
}

## Database Schema

### detection_events Table:
- `id` (INTEGER PRIMARY KEY): Unique event identifier
- `model_name` (TEXT): ML model used 
- `inference_ms` (INTEGER): Inference time in milliseconds
- `timestamp` (TEXT): timestamp
- `confidence` (REAL): Detection confidence (0.0-1.0)
- `detected` (BOOLEAN): Whether firearm was detected
- `source` (TEXT): Camera source identifier
- `image_path` (TEXT): Path to processed image