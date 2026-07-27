import cv2
import numpy as np
import handtracker as ht
import time
import autopy as ap

#SMOOTHING VARIABLES
smoothing=3
prev_x,prev_y=0,0
curr_x,curr_y=0,0

#FPS VARIABLES
prev_time=0
current_time=0

#CAPTURE SIZE
cap_width=640
cap_height=480

cap=cv2.VideoCapture(0)
cap.set(3,cap_width)
cap.set(4,cap_height)    

tracker=ht.handTracker()

#PXLS REDUCED
redn_h=65
redn_w=50

#INNER FRAME SIZE
reduced_width=cap_width-redn_w
reduced_height=cap_height-redn_h

#SCREEN SIZE
screen_width,screen_height=ap.screen.size()

time.sleep(5) #5 second dealy to laod up Fruit Ninja
while True:
    success,img = cap.read()

    img,position=tracker.findFinger(img)

    #POSITION VARIABLES
    if len(position)!=0:
        # print(position)
        x=position[0][0] #both wrt capture size
        y=position[0][1]

        x_i=np.interp(x,(redn_w,cap_width-redn_w),(0,screen_width)) #both mapped from innerframe to screen size
        y_i=np.interp(y,(redn_h,cap_height-redn_h),(0,screen_height))

        # print(x_i,y_i)

    #FPS
    current_time=time.time()
    fps=1/(current_time-prev_time)
    prev_time=current_time
    cv2.putText(img,str(int(fps)),(10,40),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

    #INNER FRAME VISUALIZATION
    cv2.rectangle(img,(redn_w,redn_h),(reduced_width,reduced_height),(255,0,255),2)

    
    #MOUSE CONTROL
    if len(position)!=0 and x_i>0 and y_i>0:
        smooth_x=prev_x+(x_i-prev_x)/smoothing #Exponential smoothing formula
        smooth_y=prev_y+(y_i-prev_y)/smoothing
        prev_x,prev_y=smooth_x,smooth_y
        
        ap.mouse.move(smooth_x,smooth_y)
        ap.mouse.toggle(button=ap.mouse.Button.LEFT,down=True)
    cv2.imshow("Mirrored Capture",img)

    #TERMINATOR
    if cv2.waitKey(1)==ord('q'):
        break