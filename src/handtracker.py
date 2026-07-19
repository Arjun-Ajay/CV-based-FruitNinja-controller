import cv2
import mediapipe as mp
import time

class handTracker():
    def __init__(self,mode=False,maxHands=1,modelComp=1,detectionConf=0.5,trackingConf=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.modelComp=modelComp
        self.detectionConf=detectionConf
        self.trackingConf=trackingConf
        
        self.mpHands=mp.solutions.hands

        self.hands=self.mpHands.Hands(
                    static_image_mode=self.mode,
                    max_num_hands=self.maxHands,
                    model_complexity=self.modelComp,
                    min_detection_confidence=self.detectionConf,
                    min_tracking_confidence=self.trackingConf) 

        self.mpDraw=mp.solutions.drawing_utils

    def findFinger(self,img):
            pos=[]
            img = cv2.flip(img, 1)
            imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

            res=self.hands.process(imgRGB)
            
            if res.multi_hand_landmarks:
                #print("Hand Detected")
                for  handLms in res.multi_hand_landmarks:
                    for id,lm in enumerate(handLms.landmark):
                        if id==8:
                            h,w=1080,1920
                            cx,cy=int(lm.x*w),int(lm.y*h)
                            pos.append([id,cx,cy])
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
            return img,pos

def main():
    prev_time=0
    current_time=0

    cap=cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)         #NOTE: FPS DEPENDS ON THESE. EXPERIMENT LATER!!!
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

    tracker=handTracker()

    while True:
        success,img = cap.read()
        img,position=tracker.findFinger(img)

        current_time=time.time()
        fps=1/(current_time-prev_time)
        prev_time=current_time
        cv2.putText(img,str(int(fps)),(10,40),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

        if len(position)!=0:print(position)
        cv2.imshow("Mirrored Capture",img)
    
        if cv2.waitKey(1)==ord('q'):
            break


if __name__=="__main__":
    main()