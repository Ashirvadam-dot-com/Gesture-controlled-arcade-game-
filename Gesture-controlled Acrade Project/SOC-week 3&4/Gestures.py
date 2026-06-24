
import math
from mediapipe_setup import normalised_distance

def finger_oreo_hand(lm_list,hand_label):
    tips=[8,12,16,20] # except thumb

    # normalised distance
    distance=normalised_distance(lm_list,4,8)

    Orientation=[]
    if hand_label=="Right":
        Orientation.append(1 if lm_list[3][1]>lm_list[4][1] else 0)
    else :
        Orientation.append(1 if lm_list[3][1]<lm_list[4][1] else 0)
    for tip in tips :
        Orientation.append(1 if lm_list[tip][2]<lm_list[tip-2][2] else 0)
        
    # orientation list has been created with 0's and 1's 
    gesture="NONE"
    if Orientation==[0,0,0,0,0]:
        gesture= "FIST"
    elif Orientation==[1,1,1,1,1]:
        gesture= "OPEN PALM"
    elif Orientation==[0,1,0,0,0]:
        gesture= "POINTING"
    elif Orientation==[0,1,1,0,0]:
        gesture= "PEACE"
    elif Orientation==[1,0,1,1,1]  and distance <0.25:
        gesture ="PINCH"
    
    return gesture , Orientation

    
    
    
