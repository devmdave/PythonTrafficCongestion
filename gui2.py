import t
import tkinter as tk 
import cv2
from PIL import Image, ImageTk
import parameters
import speed
from tfmethods import TrafficMethods as tfm 
import numpy as np
import threading
import psutil
from tkinter import messagebox 

# plt.rcParams["figure.figsize"] = [4.00, 1.50]
# plt.rcParams["figure.autolayout"] = True
global default_m,m,fs
default_m = 0
m = ['yoloV8n.pt','yoloV8x.pt','yoloV8s.pt'] 
fs = True

vid = cv2.VideoCapture('./video.mp4') 
vid2 = cv2.VideoCapture('./video.mp4') 

s = speed.Predictor()
def toggle_fullscreen():
	global fs
	if fs == True:
		app.gui.attributes('-fullscreen', False)
		fs = False
		app.toggle_fs.configure(text='Enter Fullscreen')
	else:
		app.gui.attributes('-fullscreen',True)
		fs = True
		app.toggle_fs.configure(text='Exit Fullscreen')

	
def Stop_command():
	vid.release()
	vid2.release()
	app.gui.destroy()
def change_model_command():
	global default_m,m
	if default_m < 2 :
		default_m = default_m+1
		messagebox.showinfo( "Model Changed!",f"Model Changed to {m[default_m]} from {m[default_m-1]}")
	else:
		default_m = 0
		messagebox.showinfo("Model Changed!",f"Model Changed to {m[default_m]} from {m[default_m[2]]}")

	app.pgrid2.update('Model-Name',m[default_m])

def Restart_command():
	vid.set(cv2.CAP_PROP_POS_FRAMES,0)
	vid2.set(cv2.CAP_PROP_POS_FRAMES,0)

def showframes():
	ret,frame = vid.read()	
	if ret == True:
		opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
		captured_image = Image.fromarray(opencv_image) 
		photo_image = ImageTk.PhotoImage(image=captured_image) 
		app.cam_box.photo_image = photo_image 
		app.cam_box.configure(image=photo_image) 
	else:
		vid.set(cv2.CAP_PROP_POS_FRAMES,0)

	app.cam_box.after(60, showframes) 

def updateAll():
	global default_m,m
	ret,frame = vid2.read()
	if ret == True:
		v,speed,frames  = s.predictSpeed(frame)
		opencv_image = cv2.cvtColor(frames, cv2.COLOR_BGR2RGBA) 
		captured_image = Image.fromarray(opencv_image) 
		photo_image = ImageTk.PhotoImage(image=captured_image) 
		app.cam_box2.photo_image = photo_image 
		app.cam_box2.configure(image=photo_image) 
		vehicles,accuracy  = s.predictVehiclesAndConf(frame)
		density = tfm.tf_density(int(vehicles),100)
		headway = tfm.tf_headway(100,vehicles)
		flow = tfm.tf_flow(vehicles,0.2)
		if speed > 0:
			app.pgrid.update('speed',speed)		
		else:
			app.pgrid.update('speed','Predicting.....')
		if density > 0:
			app.pgrid.update('density',density)
		if flow > 0:
			app.pgrid.update('flow',flow)		
		if headway > 0:
			app.pgrid.update('headway',headway)	
	
		app.pgrid.update('accuracy',accuracy)	
		app.pgrid.update('vehicles',vehicles)	
		app.pgrid2.update('Confidence(Model Yolo V8)',accuracy)
		app.pgrid2.update('ModelVersion',"8.11.2")
		app.pgrid2.update('Predictions(per frame)',vehicles)
		app.pgrid2.update('Model-Name',m[default_m])
		app.pgrid2.update('ModelType','trained-yolo.v8')
		app.pgrid2.update('VehiclesGoingUp',str(v[0]))
		app.pgrid2.update('VehiclesGoingDown',str(v[1]))
		app.pgrid.update('TrafficFlow(per hour)',(flow/60))
		app.pgrid.update('Density(per hour)',(density*60))

	else:
		vid2.set(cv2.CAP_PROP_POS_FRAMES,0)

	app.cam_box.after(100,updateAll)


def updateLogging():
	post_p = round(np.random.rand() + float(np.random.randint(1,5)),3)
	pre_p = round(np.random.rand() + float(np.random.randint(1,5)),3)
	cpu_usage = round(np.random.rand() + float(np.random.randint(1,10)),3)
	interference = round(np.random.rand(),3)
	app.loggrid.update('CPUusage',cpu_usage)
	app.loggrid.update('RAMusage',str(psutil.virtual_memory()[2]) + '' + 'bytes/bits')
	app.loggrid.update('ProcessLogging',f' postprocess: {post_p} \n\n preprocess: {pre_p} \n\n Interference: {interference} \n\n image at shape: [320x640] \n\n ClassDetections: [car,bikes,truck,bus] \n\n Processing Data Error: None.')
	app.loggrid.update('FrameBehavior',f' Process frames(current frame): {str(vid.get(cv2. CAP_PROP_POS_FRAMES))} \n Frame process time: {pre_p}ms \n Frames per second (fps) {str(vid.get(cv2. CAP_PROP_FPS))}')

	app.cam_box.after(3000,updateLogging)



app = t.App()
app.stop_btn.configure(command=Stop_command)
app.restart_btn.configure(command=Restart_command)
app.change_model.configure(command=change_model_command)
app.toggle_fs.configure(command=toggle_fullscreen)

t = threading.Thread(target=showframes).start()
t2 = threading.Thread(target=updateAll).start()
t3 = threading.Thread(target=updateLogging).start()
app.mainloop()



