import cv2
import mediapipe as mp
import numpy as np
import time
import math

mp_hands=mp.solutions.hands
mp_drawing_tools=mp.solutions.drawing_utils

hands=mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5  
)

landmarks_styles=mp_drawing_tools.DrawingSpec(
    color=(255,255,255),
    thickness=-1,
    circle_radius=4    
)

connection_style=mp_drawing_tools.DrawingSpec(
    color=(255,0,0),
    thickness=3
)

def get_coordinates(img,hand_lanmarks):
    h,w,c=img.shape
    landmarks_list=[]
    
    for id,lm in enumerate(hand_lanmarks.landmark):
        cx,cy=int(lm.x*w),int(lm.y*h)
        landmarks_list.append([id,cx,cy])
    return landmarks_list

cap=cv2.VideoCapture(0)


def finger_0reo_righthand(lm_list):
    tips=[8,12,16,20] # except thumb
    
    thumb_x,thumb_y=lm_list[4][1:] 
    index_x,index_y=lm_list[8][1:]     
    distance=int(math.hypot(thumb_x-index_x,thumb_y-index_y))
    
    Orientation=[]
    
    Orientation.append(1 if lm_list[3][1]>lm_list[4][1] else 0)
    for tip in tips :
        Orientation.append(1 if lm_list[tip][2]<lm_list[tip-2][2] else 0)
        
    # orientation list has been created with 0's and 1's 
    
    if Orientation==[0,0,0,0,0]:
        return "FIST"
    if Orientation==[1,1,1,1,1]:
        return "OPEN PALM"
    if Orientation==[0,1,0,0,0]:
        return "POINTING"
    if Orientation==[0,1,1,0,0]:
        return "PEACE"
    if Orientation==[1,0,1,1,1]  and distance <40 :
        return "PINCH"

while True:
    isTrue,frame=cap.read()
    
    img=cv2.flip(frame,1)
    rgb_img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    cv2.rectangle(img,(0,0),((int(img.shape[1]//5))+40,int(img.shape[0]//5)-40),(0,0,0),-1)
    
    results=hands.process(rgb_img)
    
    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            mp_drawing_tools.draw_landmarks(
                img,
                hand_landmark,
                mp_hands.HAND_CONNECTIONS,
                landmarks_styles,
                connection_style
            )
            
            lm_list=get_coordinates(img,hand_landmark)
            # index_tip,index_pip=lm_list[8],lm_list[6]

            # thumb_x,thumb_y=lm_list[4][1:] 
            # index_x,index_y=lm_list[8][1:]
            
            # distance=math.hypot(thumb_x-index_x,thumb_y-index_y)
            
            # print(distance)
            
            Oreo=finger_0reo_righthand(lm_list)
            cv2.putText(img,Oreo,(20,60),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(0,255,0),2)  
            
            print(Oreo)             
    else :
        cv2.putText(img,"NONE",(20,60),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(0,0,255),2)
        
    cv2.imshow("hand_tracking",img)
    
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
    