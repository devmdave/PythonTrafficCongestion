🚦 Traffic Flow Congestion
Real-time vehicle detection, traffic parameter analysis, and live UI visualization using YOLOv8 and Python.

Welcome to Traffic Flow Congestion—a computer vision-powered system that monitors traffic in real time, counts vehicles, and computes congestion metrics with a sleek, responsive UI. Built for urban insights, automation demos, and smart city prototypes.

📸 Features
🔍 Vehicle Detection: Uses Ultralytics YOLOv8 for high-speed, high-accuracy object detection.

📊 Traffic Metrics: Computes congestion parameters like vehicle count, density, and flow rate.

🖥️ Live Dashboard: Real-time UI built with PyQt5 to visualize traffic stats and detection overlays.

⚙️ Modular Design: Clean architecture with separate modules for detection, data processing, and UI rendering.

🧠 Tech Stack
Component	Technology Used
Detection Model	YOLOv8 (Ultralytics)
UI Framework	PyQt5
Data Handling	pandas, JSON
Visualization	OpenCV, Matplotlib
Language	Python 3.x
🚀 Getting Started
1. Clone the repo
bash
git clone https://github.com/devmdave/PythonTrafficCongestion.git
cd PythonTrafficCongestion
2. Set up virtual environment
bash
python -m venv venv
source venv/Scripts/activate  # On Windows
3. Install dependencies
bash
pip install -r requirements.txt
4. Run the project
bash
python main.py
📂 Project Structure
Code
├── main.py              # Entry point
├── detect.py            # YOLOv8 detection logic
├── graphmodule.py       # Traffic metric visualization
├── gui.py / gui2.py     # Real-time UI modules
├── mymodel.py           # Model loading and inference
├── labels.xml           # Class labels
├── requirements.txt     # Dependencies
└── README.md            # You're here!
🎯 Use Cases
Smart city traffic monitoring

Real-time congestion analytics

Automation and control system demos

Educational CV projects

🙋‍♂️ About the Author
Hi, I'm Madhav Dave—an ECE student passionate about embedded systems, automation, and computer vision. I build real-world tools that blend hardware and software into seamless, user-friendly experiences.

Connect with me on LinkedIn or explore more of my work!

📬 Feedback & Contributions
Feel free to fork, star ⭐, or open issues. Suggestions and improvements are always welcome!
