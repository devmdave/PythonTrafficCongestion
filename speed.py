import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tracker import*
import time
from math import dist
import os
import psutil


class Predictor():
    def __init__(self):
        self.model=YOLO('yolov8n.pt')
        my_file = open("./splitcode/coco.txt", "r")
        data = my_file.read()
        self.class_list = data.split("\n") 
        self.cy1=322
        self.cy2=368
        self.offset=6
        self.vh_down={}
        self.counter=[]
        self.vh_up={}
        self.conf = 0
        self.counter1=[]
        self.tracker=Tracker()

    def predictVehiclesAndConf(self,fr):
        frame=cv2.resize(fr,(1020,500))
        results=self.model.predict(frame)
        a=results[0].boxes.data
        self.conf = results[0].boxes.conf[0]
        vh_count = results[0].__len__()
        return vh_count,self.conf


    def predictSpeed(self,fr):
        speed = 0
        frame=cv2.resize(fr,(1020,500))
        results=self.model.predict(frame)
        a=results[0].boxes.boxes
        px=pd.DataFrame(a).astype("float")
        list=[]
        for index,row in px.iterrows():
            x1=int(row[0])
            y1=int(row[1])
            x2=int(row[2])
            y2=int(row[3])
            d=int(row[5])
            c=self.class_list[d]
            if 'car' in c:
                list.append([x1,y1,x2,y2])
        bbox_id=self.tracker.update(list)
        for bbox in bbox_id:
            x3,y3,x4,y4,id=bbox
            cx=int(x3+x4)//2
            cy=int(y3+y4)//2
            
            cv2.rectangle(frame,(x3,y3),(x4,y4),(0,0,255),2)
            


            if self.cy1<(cy+self.offset) and self.cy1 > (cy-self.offset):
                self.vh_down[id]=time.time()
            if id in self.vh_down:
            
                if self.cy2<(cy+self.offset) and self.cy2 > (cy-self.offset):
                    
                    elapsed_time=time.time() - self.vh_down[id]
                    if self.counter.count(id)==0:
                        self.counter.append(id)
                        distance = 10 # meters
                        a_speed_ms = distance / elapsed_time
                        a_speed_kh = a_speed_ms * 3.6
                        speed = a_speed_kh
                        cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                        cv2.putText(frame,str(id),(x3,y3),cv2.FONT_HERSHEY_COMPLEX,0.6,(255,255,255),1)
                        cv2.putText(frame,str(int(a_speed_kh))+'Km/h',(x4,y4 ),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)

                    
            #####going UP#####     
            if self.cy2<(cy+self.offset) and self.cy2 > (cy-self.offset):
                self.vh_up[id]=time.time()
            if id in self.vh_up:
                if self.cy1<(cy+self.offset) and self.cy1 > (cy-self.offset):
                    elapsed1_time=time.time() - self.vh_up[id]
                    if self.counter1.count(id)==0:
                        self.counter1.append(id)      
                        distance1 = 10 # meters
                        a_speed_ms1 = distance1 / elapsed1_time
                        a_speed_kh1 = a_speed_ms1 * 3.6
                        speed = a_speed_kh
                        # cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                        # cv2.putText(frame,str(id),(x3,y3),cv2.FONT_HERSHEY_COMPLEX,0.6,(255,255,255),1)
                        # cv2.putText(frame,str(int(a_speed_kh1))+'Km/h',(x4,y4),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)

        # cv2.line(frame,(274,self.cy1),(814,self.cy1),(255,255,255),1)
        # cv2.putText(frame,('L1'),(277,320),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
        # cv2.line(frame,(177,self.cy2),(927,self.cy2),(255,255,255),1)
        # cv2.putText(frame,('L2'),(182,367),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
        d=(len(self.counter))
        u=(len(self.counter1))
        # cv2.putText(frame,('goingdown:-')+str(d),(60,90),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
        # cv2.putText(frame,('goingup:-')+str(u),(60,130),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
        return (d,u),speed,cv2.resize(results[0].plot(labels=False),(400,400))

    





