import cv2
import time
from Gestures import finger_oreo_hand
from mediapipe_setup import (mp_hands,
                             mp_drawing_tools,
                             hands,
                             landmarks_styles,
                             connection_style,
                             get_coordinates)
from pinichDurationANDfiring import (pinch,fire)


cap=cv2.VideoCapture(0)
ctime=0
ptime=0
start_time,duration=0,0
Start_time,Duration=0,0
while True:
    isTrue,frame=cap.read()
    
    img=cv2.flip(frame,1)
    rgb_img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    
    # left region
    cv2.rectangle(img,(0,0),((int(img.shape[1]//5)-30),int(img.shape[0]//5)-40),(0,0,0),-1)
    cv2.putText(img,"LEFT HAND",(10,30),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,0),2)
    
    
    # right region
    cv2.rectangle(img,(1050,0),((int(img.shape[1]//5))+1040,int(img.shape[0]//5)-40),(0,0,0),-1)
    cv2.putText(img,"RIGHT HAND",(1050,30),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,0),2)
    
    # fps 
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img,f"FPS : {int(fps)}",(int(img.shape[1]//2),int(img.shape[0])-10),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255),2)
    
    
    Oreo_R ='NONE'
    Oreo_L ='NONE'
    
    results=hands.process(rgb_img)
    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmark,handedness in zip(results.multi_hand_landmarks,results.multi_handedness):
            mp_drawing_tools.draw_landmarks(
                img,
                hand_landmark,
                mp_hands.HAND_CONNECTIONS,
                landmarks_styles,
                connection_style
            )
            hand_label=handedness.classification[0].label

            lm_list=get_coordinates(img,hand_landmark)
            
            # right hand side
            if hand_label =="Right":
                Oreo_R=finger_oreo_hand(lm_list,hand_label)
                
            if hand_label=="Left":
                Oreo_L=finger_oreo_hand(lm_list,hand_label)
    start_time,duration,Oreo_R=pinch(img,Oreo_R,ctime,start_time,duration)
    Start_time,Duration=fire(img,Oreo_R,Oreo_L,ctime,Start_time,Duration)
                
    if Oreo_R=='NONE':
        cv2.putText(img,"NONE",(1050,90),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,255),2)
    else :
        cv2.putText(img,Oreo_R,(1050,90),cv2.FONT_HERSHEY_COMPLEX_SMALL,1.5,(0,255,0),2)  
                    
    # left hand side

    if Oreo_L=='NONE':
        cv2.putText(img,"NONE",(10,90),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,255),2)
    else :
        cv2.putText(img,Oreo_L,(10,90),cv2.FONT_HERSHEY_COMPLEX_SMALL,1.5,(0,255,0),2)
            
            
            # print(f"right hand gesture {Oreo_R}")   
            # print(Oreo)             
    cv2.imshow("hand_tracking",img)
    
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
        
      
       