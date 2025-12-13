# Traffic Flow Analysis

Real-time vehicle detection and traffic parameter analysis using YOLOv8 and Flask.

## Features

- **Vehicle Detection**: YOLOv8-based detection for cars, trucks, buses, and motorcycles
- **Speed Tracking**: Calculates vehicle speeds using dual detection lines
- **Traffic Metrics**: Real-time computation of density, flow rate, headway, and vehicle counts
- **Live Dashboard**: Web-based UI with streaming video feed and metrics updates
- **Directional Counting**: Tracks vehicles moving up and down

## Tech Stack

- **Detection**: YOLOv8 (Ultralytics)
- **Backend**: Flask
- **Processing**: OpenCV, NumPy
- **Frontend**: Vanilla JavaScript, CSS

## Installation

### Using uv (recommended)

```bash
uv sync
``` Static assets in `static/`, templates in `templates/`
- Video files and YOLO models in root directory


### Using pip

```bash
pip install -e .
```

## Usage

1. Start the Flask server:

```bash
python main.py
```

2. Open your browser to `http://localhost:5000`

3. The system will:
   - Load the YOLOv8 model (`yolov8n.pt`)
   - Process the video file (`video3.mp4`)
   - Stream detection results to the web interface
   - Update metrics every second

## Configuration

Edit constants in `main.py`:

```python
VIDEO_PATH = "video3.mp4"          # Video file path
MODEL_PATH = "yolov8n.pt"          # YOLO model (yolov8n.pt or yolov8s.pt)
FRAME_WIDTH = 1020                 # Processing width
FRAME_HEIGHT = 500                 # Processing height
ROAD_LENGTH = 100                  # Road segment length (meters)
DISTANCE_BETWEEN_LINES = 10        # Distance between detection lines (meters)
```

## Project Structure

```
PythonTrafficCongestion/
├── main.py              # Flask app with YOLOv8 detection
├── static/
│   ├── script.js        # Frontend JavaScript
│   └── style.css        # UI styles
├── templates/
│   └── index.html       # Web interface
├── video3.mp4           # Input video
├── yolov8n.pt           # YOLO model weights
└── pyproject.toml       # Dependencies
```

## Metrics Explained

- **Vehicles**: Current vehicle count in frame
- **Speed**: Average speed (km/h) from recent measurements
- **Accuracy**: Mean detection confidence score
- **FPS**: Processing frame rate
- **Density**: Vehicles per meter (vehicles/road_length)
- **Flow Rate**: Vehicle throughput
- **Headway**: Average spacing between vehicles (meters)
- **Up/Down Count**: Directional vehicle counts

## Requirements

- Python 3.12+
- OpenCV
- Flask
- Ultralytics YOLOv8
- NumPy

## License

MIT
