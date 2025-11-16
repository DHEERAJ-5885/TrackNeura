# 🚀 TrackNeura - Intelligent File Management System

A comprehensive Flask-based platform featuring intelligent file management, real-time AI assistance, and live WiFi discovery capabilities.

## ✨ Key Features

- **🤖 Real AI Chatbot**: Powered by Google's Gemini AI for intelligent conversations
- **📶 Live WiFi Finder**: Real-time WiFi hotspot discovery with interactive maps
- **🧠 Smart File Management**: ML-enhanced priority analysis and auto-healing uploads
- **🌐 Network Monitoring**: Real-time connection status and performance tracking
- **🔄 Auto-Healing System**: Automatic error detection and recovery for uploads
- **📊 Priority Engine**: Smart file prioritization using machine learning
- **🎪 Dynamic Scheduling**: Intelligent queue management for optimal performance
- **🏥 Behavioral Learning**: System learns from user patterns to improve performance

## Priority Levels

1. **Emergency files** (Priority 1) - Files containing keywords like "emergency", "urgent", "critical", "alert"
2. **Graphic-heavy files** (Priority 2) - .psd, .ai, .svg, .eps, .indd, .sketch
3. **Video files** (Priority 3) - .mp4, .avi, .mov, .wmv, .flv, .webm
4. **Image files** (Priority 4) - .jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp
5. **Text files** (Priority 5) - .txt, .doc, .docx, .pdf, .rtf, .odt
6. **Audio files** (Priority 6) - .mp3, .wav, .flac, .aac, .ogg
7. **Archive files** (Priority 7) - .zip, .rar, .7z, .tar, .gz
8. **Other files** (Priority 8) - All other file types

## Installation

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Access the web interface at `http://localhost:5000`

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t priority-analyzer .
```

2. Run the container:
```bash
docker run -p 5000:5000 priority-analyzer
```

## API Endpoints

### POST /api/analyze
Upload and analyze multiple files.

**Request**: Multipart form data with `files` field containing multiple files

**Response**:
```json
{
  "upload_id": "uuid",
  "total_files": 3,
  "files": [
    {
      "filename": "emergency_report.pdf",
      "category": "emergency",
      "priority_level": 1,
      "file_size": 1024,
      "chunk_size": 524288,
      "file_id": "uuid",
      "upload_time": "2025-11-15T10:30:00"
    }
  ]
}
```

### GET /api/priority/{upload_id}
Get priority information for all files in an upload.

**Response**:
```json
{
  "upload_id": "uuid",
  "files": [...],
  "priority_queue": [...]
}
```

### GET /api/chunk/{upload_id}/{file_id}
Get chunking information for a specific file.

**Response**:
```json
{
  "file_id": "uuid",
  "filename": "document.pdf",
  "total_size": 1048576,
  "chunk_size": 524288,
  "total_chunks": 2,
  "priority_level": 5,
  "category": "text"
}
```

### GET /api/chunk/{upload_id}/{file_id}/{chunk_number}
Get a specific chunk of a file.

**Response**:
```json
{
  "chunk_number": 0,
  "chunk_size": 524288,
  "data": "hex_encoded_data",
  "is_last_chunk": false
}
```

### GET /api/status
Health check endpoint.

**Response**:
```json
{
  "status": "active",
  "service": "priority-analyzer",
  "version": "1.0.0"
}
```

## Testing

Run the test script to verify API functionality:

```bash
python test_api.py
```

## Integration with Chunking Microservice

This microservice is designed to work with a separate chunking microservice. The chunking service can:

1. Call `/api/analyze` to upload and analyze files
2. Use `/api/priority/{upload_id}` to get the priority queue
3. Process files in priority order using `/api/chunk/{upload_id}/{file_id}` for metadata
4. Retrieve actual file chunks using `/api/chunk/{upload_id}/{file_id}/{chunk_number}`

## 📶 WiFi Finder Setup

### 🔑 Get API Keys

1. **Google Maps API** (Required for WiFi discovery):
   - Visit: https://console.cloud.google.com/apis/credentials
   - Enable: Maps JavaScript API, Places API, Geocoding API
   - Copy your API key

2. **OpenWiFiMap API** (Optional for crowdsourced data):
   - Register at: https://openwifimap.net/api
   - Get your API key

3. **PM-WANI API** (Optional for India's public WiFi):
   - Register with PM-WANI providers

### ⚙️ Environment Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys:
```bash
# Required for AI Chatbot
GEMINI_API_KEY=your_gemini_api_key_here

# Required for WiFi Finder
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here

# Optional for enhanced WiFi data
OPENWIFIMAP_API_KEY=your_openwifimap_api_key_here
PMWANI_API_KEY=your_pmwani_api_key_here
```

### 🧪 Test WiFi Finder

```bash
# Test the WiFi service
curl -X POST http://localhost:5000/api/wifi/nearby \
  -H "Content-Type: application/json" \
  -d '{"lat": 26.9124, "lng": 75.7873, "radiusMeters": 800}'

# Check service status
curl http://localhost:5000/api/wifi/status
```

## File Structure

```
Trackneura/
├── app.py                     # Main Flask application
├── wifi_service.py            # WiFi discovery service
├── wifi_routes.py             # WiFi API endpoints
├── gemini_client.py           # AI chatbot client
├── ai_routes.py               # AI API endpoints
├── requirements.txt           # Python dependencies
├── .env.example               # Environment configuration template
├── static/js/
│   ├── GeminiChatAssistant.js # AI chatbot frontend
│   └── WiFiFinder.js          # WiFi finder frontend
├── templates/                 # HTML templates
└── uploads/                   # File upload directory
```

## 🌐 API Endpoints

### WiFi Finder APIs
- `POST /api/wifi/nearby` - Find WiFi hotspots near location
- `GET /api/wifi/status` - Check WiFi service status
- `GET /api/wifi/test` - Test WiFi service functionality

### AI Chatbot APIs
- `POST /api/ai/chat` - Chat with Gemini AI
- `GET /api/ai/status` - Check AI service status

## Security & Privacy

- **Location Privacy**: Location data is only used for WiFi discovery and cached for 30 seconds
- **API Key Security**: All external API keys are stored server-side, never exposed to frontend
- **Rate Limiting**: Built-in rate limiting prevents API abuse
- **Secure File Handling**: Files stored with secure filenames using `werkzeug.utils.secure_filename`
- File uploads are limited to 100MB by default
- Upload directories are created with proper permissions
- File paths are validated to prevent directory traversal attacks