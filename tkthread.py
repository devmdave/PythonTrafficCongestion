import tkinter 
import threading
import time
import cv2
from PIL import Image,ImageTk

vid = cv2.VideoCapture('./video.mp4') 
frame = cv2.imread('tfimage.webp')
def update():
	# Capture the video frame by frame 
	_, frame = vid.read() 

	# Convert image from one color space to other 
	opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 

	# Capture the latest frame and transform to image 
	captured_image = Image.fromarray(opencv_image) 

	# Convert captured image to photoimage 
	photo_image = ImageTk.PhotoImage(image=captured_image) 

	# Displaying photoimage in the label 
	lbl.photo_image = photo_image 

	# Configure image in the label 
	lbl.configure(image=photo_image) 

	# Repeat the same process after every 10 seconds 
	lbl.after(10, update) 


win = tkinter.Tk()
lbl = tkinter.Label(win,text='its not in thread now.')
lbl.grid(row=0,column=0,sticky='nsew')
lbl = tkinter.Label(win,text='its not in thread now.')
lbl.grid(row=1,column=1,sticky='nsew')
lbl = tkinter.Label(win,text='its not in thread now.')
lbl.grid(row=2,column=2,sticky='nsew')

t = threading.Thread(target=update).start()
win.mainloop()
