import t
import tkinter as tk 
from graphmodule import *
import cv2
from PIL import Image, ImageTk
import parameters
import speed
from tfmethods import TrafficMethods as tfm 
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib import pyplot as plt, animation
import numpy as np
import threading


plt.rcParams["figure.figsize"] = [4.00, 1.50]
plt.rcParams["figure.autolayout"] = True


vid = cv2.VideoCapture('./video.mp4') 
total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
global accuracy_record,headway_record,vehicle_record
accuracy_record = []
vehicle_record = []
headway_record = []

p = speed.Predictor()


	
def open_camera():
	global accuracy_record,vehicle_record,headway_record

	_, frame = vid.read()
	new_frame,s = p.predictSpeed(frame)
	opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
	# Capture the latest frame and transform to image
	captured_image = Image.fromarray(opencv_image)
	captured_image2 = Image.fromarray(new_frame)
	# Convert captured image to photoimage
	photo_image = ImageTk.PhotoImage(image=captured_image)
	photo_image2 = ImageTk.PhotoImage(image=captured_image2)
	# Displaying photoimage in the label
	app.lbl_camera_fr.photo_image = photo_image
	app.lbl_resultfr_fr.photo_image = photo_image2
	# Configure image in the label
	app.lbl_camera_fr.configure(image=photo_image)
	app.lbl_resultfr_fr.configure(image=photo_image2)
	
	vh_count = p.predictVehicles(frame)
	accuracy = p.predictAccuracy()
	density = tfm.tf_density(int(vh_count),100)
	headway = tfm.tf_headway(100,vh_count)
	flow = tfm.tf_flow(vh_count,s)
    
	# params.update('speed',int(s),50)
	# params.update('vehicles',int(vh_count),20)
	# params.update('accuracy',round(float(accuracy),3),0.253)
	# params.update('density',float(density),0.9)
	# params.update('headway',round(float(headway),3),0.99)
	# params.update('flow',round(float(flow),3),0.99)
	# params.update('bidirectional','yes',range=False)
	# params.update('roadbreadth',100.0,range=False)
	# params.update('calibratedpixelvalues',3.6,range=False)

	max_accuracy = str(accuracy)
	max_vehicles_per_hour = vh_count*60*60

	max_flow = round(float(flow),3)* int(s)
	max_speed = int(s) * headway

	# predicted_params.update('ConfidenceOfModel',max_accuracy,range=False)	
	# predicted_params.update('MaxSpeedofTraffic',max_speed,range=False)	
	# predicted_params.update('MaxFlowofTraffic',max_flow,range=False)	
	# predicted_params.update('MaxVehiclesPredictedPerHour',max_vehicles_per_hour,range=False)	
	# predicted_params.update('TotalFrames',total_frames,range=False)	
	new_frame = cv2.resize(new_frame,(600,300))
	frame = cv2.resize(frame,(600,300))
    

	# Repeat the same process after every 10 seconds

	app.lbl_camera_fr.after(1, open_camera)

app = t.App()
open_camera()
app.mainloop()



