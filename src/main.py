import cv2
import numpy as np
import handtracker as ht
import time
import autopy as ap

prev_time=0
current_time=0

cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)    

tracker=ht.handTracker()

while True:
    success,img = cap.read()
    img,position=tracker.findFinger(img)

    current_time=time.time()
    fps=1/(current_time-prev_time)
    prev_time=current_time
    cv2.putText(img,str(int(fps)),(10,40),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

    if len(position)!=0 and position[0][0]>0 and position[0][1]>0:
        #print(position)
        ap.mouse.move(position[0][0],position[0][1])
    cv2.imshow("Mirrored Capture",img)

    if cv2.waitKey(1)==ord('q'):
        break