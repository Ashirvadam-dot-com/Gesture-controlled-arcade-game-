import cv2
import mediapipe as mp
import numpy as np
import time 
import math
from pycaw.pycaw import AudioUtilities


cap=cv2.VideoCapture(0)
cap.set(3,640) # width
cap.set(4,400) # height

mp_hands=mp.solutions.hands
mp_drawing_tools=mp.solutions.drawing_utils
mp_drawing_styles=mp.solutions.drawing_styles



hands=mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

landmark_style=mp_drawing_tools.DrawingSpec(
    color=(255,255,255),
    thickness=-1,
    circle_radius=5 )

connection_style=mp_drawing_tools.DrawingSpec(
    color=(255,0,0),
    thickness=2)


ctime=0
ptime=0

#creating a landmarks list
def get_landmarks_list(hand_landmarks,img):
    h,w,c=img.shape
    landmarks_list=[]
    
    for id, lm in enumerate(hand_landmarks.landmark):
        cx=int(lm.x*w)
        cy=int(lm.y*h)
        landmarks_list.append([id,cx,cy])
    return landmarks_list



# setting pycaw variables
devices=AudioUtilities.GetSpeakers()
volume=devices.EndpointVolume
volRange=volume.GetVolumeRange()
Volume_range=volRange[:2]
minVol,maxVol=Volume_range
vol_per=0
volume.SetMasterVolumeLevel(0,None)




while True:
    isTrue, frame=cap.read()
    img=cv2.flip(frame,1)
    rgb_img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    
    
    # fps counter
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img,f"FPS={int(fps)}",(50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,0),2)
    # volume bar wala rectangle
    cv2.rectangle(img,(50,70),(70,200),(255,0,0),2)
    # passing into mp
    results=hands.process(rgb_img)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing_tools.draw_landmarks(
                img,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                landmark_style,
                connection_style)
            
            h,w,c=img.shape

            lm_list=get_landmarks_list(hand_landmarks,img)
            # circling the index finger
            index_tip=lm_list[8]
            index_x=index_tip[1]
            index_y=index_tip[2]
            cv2.circle(img,(index_x,index_y),10,(0,255,0),-1)
            
            # circling the thumb
            thumb_tip=lm_list[4]
            thumb_x=thumb_tip[1]
            thumb_y=thumb_tip[2]
            cv2.circle(img,(thumb_x, thumb_y),10,(0,255,0),-1)
            cv2.line(img,(index_x,index_y),(thumb_x,thumb_y),(0,255,0),3)
            
            # printing the coordinates of index and thumb
            coordinates=[[index_x,index_y],[thumb_x,thumb_y]]
            
            
            # dist=(np.abs(coordinates[0][1]-coordinates[1][1]),np.abs(coordinates[0][0]-coordinates[1][0]))
            dist=math.hypot(index_x-thumb_x,index_y-thumb_y)
            # print(int(dist))
            # min distance --> 20 --> 30
            # max distance --> 200 --> 160
            if int(dist)<30:
                cv2.circle(img,(((index_x+thumb_x))//2,((index_y+thumb_y)//2)),13,(0,0,255),-1)
            else :
                cv2.circle(img,(((index_x+thumb_x))//2,((index_y+thumb_y)//2)),13,(0,255,0),-1)
            
            
            vol=np.interp(dist,[30,160],[minVol,maxVol])
            vol_bar=np.interp(vol,[-65,0],[200,70])
            vol_per=np.interp(vol,[-65,0],[0,100])
            Vol_bar=int(vol_bar)
            cv2.rectangle(img,(50,Vol_bar),(70,200),(255,0,0),-1)
            cv2.putText(img,f"vol={int(vol_per) } %",(40,240),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(255,0,0),2)
            volume.SetMasterVolumeLevel(vol,None)
            
               
    cv2.imshow("hands",img)
    
    if cv2.waitKey(1) & 0xFF==ord("q"):
        break
       




