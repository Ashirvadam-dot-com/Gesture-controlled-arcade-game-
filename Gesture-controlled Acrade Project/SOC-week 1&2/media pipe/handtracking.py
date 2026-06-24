import cv2
import mediapipe as mp
import numpy as np
import time 


mp_hands=mp.solutions.hands
mp_drawing_tools=mp.solutions.drawing_utils
mp_drawing_styles=mp.solutions.drawing_styles


hands=mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=4,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.5
)

landmark_style=mp_drawing_tools.DrawingSpec(
    color=(255,0,0),
    thickness=-1,
    circle_radius=4)

connection_style=mp_drawing_tools.DrawingSpec(
    color=(0,255,255),
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



cap=cv2.VideoCapture(0)
cap.set(3,640) # width
cap.set(4,400) # height

while True:
    isTrue, frame=cap.read()
    img=cv2.flip(frame,1)
    rgb_img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    
    
    # fps counter
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img,f"FPS={int(fps)}",(50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,0),2)
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
            
            print(lm_list[8])
        


            
    cv2.imshow("hands",img)
    
    if cv2.waitKey(1) & 0xFF==ord("q"):
        break
       
            



"""this is for manual landmark colouring method """
# for id , lm in enumerate(hand_landmarks.landmark):
#     cx=int(lm.x*w)
#     cy=int(lm.y*h)               
#     cv2.circle(img,(cx,cy),3,(0,0,255),-1)


"""this code is to print whether away or towards"""
# z=hand_landmarks.landmark[0].z
# if z< -0.1:
#   print(" hand is moving towards camera")
# elif z > 0.1 :
#   print(" hand is moving away from camera")

    # else : # this will print empty list if no hand is detected
    #     lm_list=[]
    #     print(lm_list)