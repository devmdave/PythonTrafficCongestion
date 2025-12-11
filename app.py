"""
Traffic Flow Analysis - Vehicle detection and tracking with YOLOv8
"""

from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
from ultralytics import YOLO
import time
from threading import Lock
from collections import deque

app = Flask(__name__)

# Config
VIDEO_PATH = 'video3.mp4'
MODEL_PATH = 'yolov8n.pt'
FRAME_WIDTH = 1020
FRAME_HEIGHT = 500
ROAD_LENGTH = 100  # meters
DISTANCE_BETWEEN_LINES = 10  # meters

# Global state
model = None
cap = None
metrics = {
    'speed': 0, 'vehicles': 0, 'accuracy': 0,
    'density': 0, 'headway': 0, 'flow': 0,
    'vehicles_up': 0, 'vehicles_down': 0, 'fps': 0
}
lock = Lock()


class Tracker:
    """Simple vehicle tracker with ID assignment"""
    
    def __init__(self, cy1=322, cy2=368, offset=6):
        self.centers = {}
        self.next_id = 0
        self.down_times = {}
        self.up_times = {}
        self.counted_down = set()
        self.counted_up = set()
        self.cy1 = cy1
        self.cy2 = cy2
        self.offset = offset
        self.recent_speeds = deque(maxlen=30)  # Keep last 30 speeds
    
    def update(self, boxes):
        """Update tracking and return objects with IDs"""
        tracked = []
        
        for box in boxes:
            x1, y1, x2, y2 = box
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            
            # Find existing track
            matched_id = None
            min_dist = 40
            
            for obj_id, (px, py) in self.centers.items():
                dist = ((cx - px)**2 + (cy - py)**2)**0.5
                if dist < min_dist:
                    matched_id = obj_id
                    min_dist = dist
            
            # Assign ID
            if matched_id is None:
                matched_id = self.next_id
                self.next_id += 1
            
            self.centers[matched_id] = (cx, cy)
            tracked.append((x1, y1, x2, y2, matched_id, cx, cy))
        
        # Cleanup old tracks
        active_ids = {t[4] for t in tracked}
        self.centers = {k: v for k, v in self.centers.items() if k in active_ids}
        
        return tracked
    
    def calc_speed(self, obj_id, cy):
        """Calculate speed when vehicle crosses lines"""
        speed = None
        
        # Downward movement
        if self.cy1 - self.offset < cy < self.cy1 + self.offset:
            if obj_id not in self.down_times:
                self.down_times[obj_id] = time.time()
        
        elif self.cy2 - self.offset < cy < self.cy2 + self.offset:
            if obj_id in self.down_times and obj_id not in self.counted_down:
                elapsed = time.time() - self.down_times[obj_id]
                if elapsed > 0:
                    speed = (DISTANCE_BETWEEN_LINES / elapsed) * 3.6  # km/h
                    self.counted_down.add(obj_id)
                    self.recent_speeds.append(speed)
        
        # Upward movement
        if self.cy2 - self.offset < cy < self.cy2 + self.offset:
            if obj_id not in self.up_times:
                self.up_times[obj_id] = time.time()
        
        elif self.cy1 - self.offset < cy < self.cy1 + self.offset:
            if obj_id in self.up_times and obj_id not in self.counted_up:
                elapsed = time.time() - self.up_times[obj_id]
                if elapsed > 0:
                    speed = (DISTANCE_BETWEEN_LINES / elapsed) * 3.6
                    self.counted_up.add(obj_id)
                    self.recent_speeds.append(speed)
        
        return speed
    
    def get_avg_speed(self):
        """Get average from recent speeds"""
        return np.mean(self.recent_speeds) if self.recent_speeds else 0


tracker = Tracker()


def init_model():
    """Load YOLO model"""
    global model
    model = YOLO(MODEL_PATH)
    model.fuse()  # Optimize for inference
    print(f"Model loaded: {MODEL_PATH}")


def init_video():
    """Setup video capture"""
    global cap
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        raise Exception(f"Cannot open video: {VIDEO_PATH}")
    print(f"Video loaded: {VIDEO_PATH}")


def process_frame(frame):
    """Detect, track, and calculate metrics"""
    start = time.time()
    
    # Resize
    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
    
    # Detect vehicles
    results = model(frame, verbose=False)[0]
    
    # Filter vehicle classes (car, truck, bus, motorcycle)
    vehicle_ids = {2, 3, 5, 7}
    boxes = []
    
    for box in results.boxes:
        if int(box.cls) in vehicle_ids:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            boxes.append((x1, y1, x2, y2))
    
    # Track
    tracked = tracker.update(boxes)
    
    # Process each vehicle
    for x1, y1, x2, y2, obj_id, cx, cy in tracked:
        # Draw box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f'{obj_id}', (x1, y1-8), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Check speed
        speed = tracker.calc_speed(obj_id, cy)
        if speed:
            cv2.putText(frame, f'{int(speed)}km/h', (x2-50, y2-8), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
    
    # Draw detection lines
    cv2.line(frame, (274, tracker.cy1), (814, tracker.cy1), (255, 255, 255), 2)
    cv2.line(frame, (177, tracker.cy2), (927, tracker.cy2), (255, 255, 255), 2)
    
    # Calculate metrics
    vehicle_count = len(tracked)
    avg_speed = tracker.get_avg_speed()
    accuracy = float(results.boxes.conf.mean()) if len(results.boxes) > 0 else 0
    density = vehicle_count / ROAD_LENGTH
    headway = ROAD_LENGTH / vehicle_count if vehicle_count > 0 else 0
    flow = vehicle_count  # Simplified
    fps = 1.0 / (time.time() - start)
    
    # Update global state
    with lock:
        metrics.update({
            'speed': round(avg_speed, 1),
            'vehicles': vehicle_count,
            'accuracy': round(accuracy, 2),
            'density': round(density, 3),
            'headway': round(headway, 2),
            'flow': round(flow, 2),
            'vehicles_up': len(tracker.counted_up),
            'vehicles_down': len(tracker.counted_down),
            'fps': round(fps, 1)
        })
    
    # Overlay info
    info = [
        f'Vehicles: {vehicle_count}',
        f'Speed: {int(avg_speed)} km/h',
        f'Down: {len(tracker.counted_down)} | Up: {len(tracker.counted_up)}',
        f'FPS: {fps:.1f}'
    ]
    
    for i, text in enumerate(info):
        cv2.putText(frame, text, (10, 28 + i*28), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    return frame


def gen_frames():
    """Stream video frames"""
    while True:
        ret, frame = cap.read()
        
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop
            continue
        
        processed = process_frame(frame)
        
        # Encode
        _, buffer = cv2.imencode('.jpg', processed, 
                                 [cv2.IMWRITE_JPEG_QUALITY, 85])
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + 
               buffer.tobytes() + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/metrics')
def get_metrics():
    with lock:
        return jsonify(metrics)


@app.route('/restart')
def restart():
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    print("Loading model...")
    init_model()
    
    print("Loading video...")
    init_video()
    
    print("Starting server on http://localhost:5000")
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
