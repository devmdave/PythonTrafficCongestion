import cv2
import pandas as pd
from ultralytics import YOLO
from tracker import*

model=YOLO('yolov8n.pt')



def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        colorsBGR = [x, y]
        print(colorsBGR)
        

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

# cap=cv2.VideoCapture('video.mp4')
cap=cv2.VideoCapture('video3.mp4')


my_file = open("./splitcode/coco.txt", "r")
data = my_file.read()
class_list = data.split("\n") 
#print(class_list)

count=0
prev_vhcount = 0
total_vh_count = 0
# vh_count = 0

tracker=Tracker()

cy1=322
cy2=368
offset=6

while True:    
    ret,frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 3 != 0:
        continue
    frame=cv2.resize(frame,(1020,500))
    results=model.predict(frame)
    a=results[0].boxes.data
    px=pd.DataFrame(a).astype("float")
    list=[]
    cv2.line(frame,(5,400),(1010,400),(255,255,255),1)
    vh_count = 0
    for index,row in px.iterrows():
        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])
        d=int(row[5])
        cv2.rectangle(frame, (x1,y1), (x2,y2), (255,0,0), 2) 
        list.append([x1,y1,x2,y2])
        if (y1 > 450) or (y2 > 450):
            vh_count = vh_count+1
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,0,255), 2) 
    print('vhcount is '+ str(vh_count))
    
    
    cv2.imshow("RGB", frame)

    if cv2.waitKey(50)&0xFF==27:
        break

cap.release()
cv2.destroyAllWindows()

