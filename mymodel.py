import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tracker import*
import time
from math import dist

my_file = open("./splitcode/coco.txt", "r")
data = my_file.read()
class_list = data.split("\n") 
offset=6
counter1=[]
class Predictor:
    def __init__(self,cv2obj,dimensions=(500,500)):
        self.frame = None
        self.cv2 = cv2obj
        self.dimensions = dimensions
        self.tracker = Tracker()
        self.count = 0
        self.counter=[]
        self.vh_down={}
        self.vh_up={}
        self.cy1=322
        self.cy2=368
        self.pt_model = None
        self.model = None

    def init_Model(self,path_to_model=None):
        if self.pt_model == None and path_to_model == None:
            self.pt_model = 'yolov8s.pt'
        elif path_to_model != None:
            self.pt_model = path_to_model

        self.model=YOLO(self.pt_model)
    class Speed:
        def __init__(self):
            pass

        def predictSpeed(self,frame):
            self.frame = frame
            
            if self.model == None:
                self.init_Model()
            else:
                results=self.model.predict(self.frame)

                a=results[0].boxes.data
                px=pd.DataFrame(a).astype("float")
                list=[]
                for index,row in px.iterrows():
                    x1=int(row[0])
                    y1=int(row[1])
                    x2=int(row[2])
                    y2=int(row[3])
                    d=int(row[5])
                    c=class_list[d]
                    if 'car' in c:
                        list.append([x1,y1,x2,y2])
                bbox_id=self.tracker.update(list)
                for bbox in bbox_id:
                    x3,y3,x4,y4,id=bbox
                    cx=int(x3+x4)//2
                    cy=int(y3+y4)//2
                    self.cv2.circle(self.frame,(cx,cy),4,(0,0,255),-1)

                    if self.cy1<(cy+offset) and self.cy1 > (cy-offset):
                        self.vh_down[id]=time.time()

                    if id in self.vh_down:
                        if self.cy2<(cy+offset) and self.cy2 > (cy-offset):
                            elapsed_time=time.time() - self.vh_down[id]
                            if self.counter.count(id)==0:
                                self.counter.append(id)
                                distance = 10 # meters
                                a_speed_ms = distance / elapsed_time
                                a_speed_kh = a_speed_ms * 3.6
                                self.cv2.circle(self.frame,(cx,cy),4,(0,0,255),-1)
                                print("speed: "+str(a_speed_kh))
                                self.cv2.putText(self.frame,str(id),(x3,y3),self.cv2.FONT_HERSHEY_COMPLEX,0.6,(255,255,255),1)
                                self.cv2.putText(self.frame,str(int(a_speed_kh))+'Km/h',(x4,y4 ),self.cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)

    #               logic of detecting scrolling vehicles
                    if self.cy2<(cy+offset) and self.cy2 > (cy-offset):
                        self.vh_up[id]=time.time()
                    
                    if id in self.vh_up:
                        if self.cy1<(cy+offset) and self.cy1 > (cy-offset):
                            elapsed1_time=time.time() - self.vh_up[id]

                            if counter1.count(id)==0:
                                counter1.append(id)      
                                distance1 = 10 # meters
                                a_speed_ms1 = distance1 / elapsed1_time
                                a_speed_kh1 = a_speed_ms1 * 3.6
                                self.cv2.circle(self.frame,(cx,cy),4,(0,0,255),-1)
                                print("speed: "+ str(a_speed_kh1))
                                self.cv2.putText(self.frame,str(id),(x3,y3),self.cv2.FONT_HERSHEY_COMPLEX,0.6,(255,255,255),1)
                                self.cv2.putText(self.frame,str(int(a_speed_kh1))+'Km/h',(x4,y4),self.cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)

            return self.frame
            