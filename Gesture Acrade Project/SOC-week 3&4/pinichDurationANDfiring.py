import cv2
def pinch(img,Oreo_R,ctime,start_time,duration):
    IS_PINCH=True if Oreo_R=="PINCH" else False  
    
    
    if IS_PINCH is False :
        start_time=ctime
        duration=0
    elif duration>3:
        Oreo_R="GRAB"
        cv2.putText(img,f"successfully grabbed an object",(int(img.shape[1]//2)-200,int(img.shape[0])-90),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,255,0),2)
    else :
        duration=ctime-start_time
    
    
    return start_time,duration,Oreo_R

def fire(img,Oreo_R,Oreo_L,ctime,Start_time,Duration):
    
    is_Fire=True if Oreo_R=="POINTING" and Oreo_L=="FIST" else False
    FIRE_START=True if Duration>1 else False
    
    if FIRE_START  :
        cv2.putText(img,f"FIRING HAS BEEN STARTED",(int(img.shape[1]//2)-200,int(img.shape[0])-90),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,255,0),2)
    
    if is_Fire is False :
        Start_time=ctime
        Duration=0
    else :
        Duration=ctime-Start_time
    
    return Start_time,Duration