"""
Flask application for Traffic Flow Congestion Analysis
Real-time vehicle detection and traffic parameter analysis using YOLOv8
"""

from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
from ultralytics import YOLO
import time
from collections import defaultdict
import threading
import json

app = Flask(__name__)

# Global variables
model = None
video_capture = None
current_metrics = {
    'speed': 0,
    'vehicles': 0,
    'accuracy': 0,
    'density': 0,
    'headway': 0,
    'flow': 0,
    'vehicles_up': 0,
    'vehicles_down': 0,
    'fps': 0
}
lock = threading.Lock()

# Tracker class for vehicle tracking
class VehicleTracker:
    def __init__(self):
        self.center_points = {}
        self.id_count = 0
        self.vh_down = {}
        self.vh_up = {}
        self.counter_down = []
        self.counter_up = []
        self.cy1 = 322  # Line 1 for speed detection
        self.cy2 = 368  # Line 2 for speed detection
        self.offset = 6
        
    def update(self, objects_rect):
        """Update tracked objects and assign IDs"""
        objects_bbs_ids = []
        
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + w) // 2
            cy = (y + h) // 2
            
            same_object_detected = False
            for obj_id, pt in self.center_points.items():
                dist = np.sqrt((cx - pt[0])**2 + (cy - pt[1])**2)
                
                if dist < 35:
                    self.center_points[obj_id] = (cx, cy)
                    objects_bbs_ids.append([x, y, w, h, obj_id])
                    same_object_detected = True
                    break
            
            if not same_object_detected:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1
        
        # Clean up unused IDs
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center
        
        self.center_points = new_center_points.copy()
        return objects_bbs_ids

# Traffic calculation utilities
class TrafficMetrics:
    @staticmethod
    def calculate_density(vehicles, road_length):
        """Calculate traffic density (vehicles per unit length)"""
        return vehicles / road_length if road_length > 0 else 0
    
    @staticmethod
    def calculate_flow(vehicles, time_interval):
        """Calculate traffic flow (vehicles per unit time)"""
        return vehicles / time_interval if time_interval > 0 else 0
    
    @staticmethod
    def calculate_headway(road_length, vehicles):
        """Calculate average headway (space between vehicles)"""
        return road_length / vehicles if vehicles > 0 else 0
    
    @staticmethod
    def calculate_speed(flow, density):
        """Calculate average speed"""
        return flow / density if density > 0 else 0

# Initialize tracker
tracker = VehicleTracker()

def initialize_model(model_path='yolov8n.pt'):
    """Initialize YOLO model"""
    global model
    model = YOLO(model_path)
    return model

def initialize_video(video_path='video.mp4'):
    """Initialize video capture"""
    global video_capture
    video_capture = cv2.VideoCapture(video_path)
    return video_capture

def process_frame(frame):
    """Process a single frame with YOLO detection and tracking"""
    global tracker, current_metrics
    
    start_time = time.time()
    
    # Resize frame
    frame_resized = cv2.resize(frame, (1020, 500))
    
    # Run YOLO detection
    results = model(frame_resized)
    
    # Extract detections
    detections = results[0].boxes.data.cpu().numpy()
    
    # Filter for vehicles (car, truck, bus, motorcycle)
    vehicle_classes = [2, 3, 5, 7]  # COCO class IDs
    vehicle_boxes = []
    
    for detection in detections:
        x1, y1, x2, y2, conf, cls = detection
        if int(cls) in vehicle_classes:
            vehicle_boxes.append([int(x1), int(y1), int(x2), int(y2)])
    
    # Update tracker
    tracked_objects = tracker.update(vehicle_boxes)
    
    # Calculate speed and direction
    speeds = []
    for bbox in tracked_objects:
        x3, y3, x4, y4, obj_id = bbox
        cx = (x3 + x4) // 2
        cy = (y3 + y4) // 2
        
        # Draw bounding box
        cv2.rectangle(frame_resized, (x3, y3), (x4, y4), (0, 255, 0), 2)
        cv2.putText(frame_resized, f'ID:{obj_id}', (x3, y3-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        # Speed detection (going down)
        if tracker.cy1 < (cy + tracker.offset) and tracker.cy1 > (cy - tracker.offset):
            tracker.vh_down[obj_id] = time.time()
        
        if obj_id in tracker.vh_down:
            if tracker.cy2 < (cy + tracker.offset) and tracker.cy2 > (cy - tracker.offset):
                elapsed_time = time.time() - tracker.vh_down[obj_id]
                if obj_id not in tracker.counter_down:
                    tracker.counter_down.append(obj_id)
                    distance = 10  # meters
                    speed_ms = distance / elapsed_time if elapsed_time > 0 else 0
                    speed_kmh = speed_ms * 3.6
                    speeds.append(speed_kmh)
                    cv2.putText(frame_resized, f'{int(speed_kmh)} km/h', (x4, y4), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        # Speed detection (going up)
        if tracker.cy2 < (cy + tracker.offset) and tracker.cy2 > (cy - tracker.offset):
            tracker.vh_up[obj_id] = time.time()
        
        if obj_id in tracker.vh_up:
            if tracker.cy1 < (cy + tracker.offset) and tracker.cy1 > (cy - tracker.offset):
                elapsed_time = time.time() - tracker.vh_up[obj_id]
                if obj_id not in tracker.counter_up:
                    tracker.counter_up.append(obj_id)
                    distance = 10  # meters
                    speed_ms = distance / elapsed_time if elapsed_time > 0 else 0
                    speed_kmh = speed_ms * 3.6
                    speeds.append(speed_kmh)
    
    # Draw detection lines
    cv2.line(frame_resized, (274, tracker.cy1), (814, tracker.cy1), (255, 255, 255), 2)
    cv2.line(frame_resized, (177, tracker.cy2), (927, tracker.cy2), (255, 255, 255), 2)
    
    # Calculate metrics
    avg_speed = np.mean(speeds) if speeds else 0
    vehicle_count = len(tracked_objects)
    accuracy = float(results[0].boxes.conf.mean()) if len(results[0].boxes.conf) > 0 else 0
    
    road_length = 100  # meters
    density = TrafficMetrics.calculate_density(vehicle_count, road_length)
    headway = TrafficMetrics.calculate_headway(road_length, vehicle_count)
    flow = TrafficMetrics.calculate_flow(vehicle_count, 1)  # per second
    
    # Calculate FPS
    fps = 1.0 / (time.time() - start_time)
    
    # Update global metrics
    with lock:
        current_metrics.update({
            'speed': round(avg_speed, 2),
            'vehicles': vehicle_count,
            'accuracy': round(accuracy, 3),
            'density': round(density, 3),
            'headway': round(headway, 3),
            'flow': round(flow, 3),
            'vehicles_up': len(tracker.counter_up),
            'vehicles_down': len(tracker.counter_down),
            'fps': round(fps, 1)
        })
    
    # Add metrics overlay
    y_offset = 30
    metrics_text = [
        f'Vehicles: {vehicle_count}',
        f'Speed: {int(avg_speed)} km/h',
        f'Down: {len(tracker.counter_down)} | Up: {len(tracker.counter_up)}',
        f'FPS: {fps:.1f}'
    ]
    
    for i, text in enumerate(metrics_text):
        cv2.putText(frame_resized, text, (10, y_offset + i*30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    return frame_resized

def generate_frames():
    """Generate video frames for streaming"""
    global video_capture
    
    while True:
        success, frame = video_capture.read()
        
        if not success:
            # Loop video
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        
        # Process frame
        processed_frame = process_frame(frame)
        
        # Encode frame
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/metrics')
def get_metrics():
    """Get current traffic metrics"""
    with lock:
        return jsonify(current_metrics)

@app.route('/restart')
def restart_video():
    """Restart video from beginning"""
    global video_capture
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
    return jsonify({'status': 'success', 'message': 'Video restarted'})

if __name__ == '__main__':
    # Initialize
    print("Initializing YOLO model...")
    initialize_model('yolov8n.pt')
    
    print("Initializing video capture...")
    initialize_video('video.mp4')
    
    print("Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
