import mediapipe as mp
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

def distance(lm_list,p1,p2):
    x1,y1=lm_list[p1][1],lm_list[p1][2]
    x2,y2=lm_list[p2][1],lm_list[p2][2]
    
    return math.hypot(x2-x1,y2-y1)

def normalised_distance(lm_list,p1,p2):
    x1,y1=lm_list[p1][1],lm_list[p1][2]
    x2,y2=lm_list[p2][1],lm_list[p2][2]
    
    distance=math.hypot(x2-x1,y2-y1)
    
    ref=math.hypot(lm_list[0][1]-lm_list[9][1],lm_list[0][2]-lm_list[9][2])
    
    if ref==0:
        return distance
    else:
        return distance/ref

    