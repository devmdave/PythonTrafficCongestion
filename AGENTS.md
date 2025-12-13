# Agent Guidelines for PythonTrafficCongestion

## Build/Run/Test Commands
- **Run app**: `python main.py` (starts Flask server on http://localhost:5000)
- **Install deps**: `uv sync` or `pip install -e .`
- **No test suite**: No tests currently exist in this project

## Code Style & Conventions

### Python (main.py)
- **Imports**: Standard library first, then third-party (cv2, numpy, flask, ultralytics), alphabetically within groups
- **Formatting**: 4-space indentation, max line length ~88 chars, double quotes for strings
- **Types**: No type hints used in this codebase
- **Naming**: snake_case for functions/variables, PascalCase for classes (e.g., `Tracker`)
- **Docstrings**: Brief one-line docstrings in triple quotes for functions/classes
- **Error handling**: Minimal - use exceptions for critical failures (e.g., video loading)
- **Global state**: Uses global variables (`model`, `cap`, `metrics`) with thread locks for Flask

### JavaScript (static/script.js)
- **Style**: camelCase naming, async/await for API calls, JSDoc comments for functions
- **Formatting**: 4-space indentation, single quotes for strings

### Project Structure
- Single-file Flask app (`main.py`) with YOLOv8 vehicle detection
- Static assets in `static/`, templates in `templates/`
- Video files and YOLO models in root directory
