import cv2
import mediapipe as mp
import time
import numpy as np

    
    

mp_pose=mp.solutions.pose
mp_drawing_tools=mp.solutions.drawing_utils

pose=mp_pose.Pose(
    static_image_mode=False,
    model_complexity=2,
    smooth_landmarks=True,
    enable_segmentation=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5 
)

landmark_style=mp_drawing_tools.DrawingSpec(
    color=(255,255,255),
    thickness=-1,
    circle_radius=4  
)

connection_style=mp_drawing_tools.DrawingSpec(
    color=(255,0,0),
    thickness=3  
)

def get_landmark(pose_landmarks,img):
    h,w,c=img.shape
    landmark_list=[]
    for id,lm in enumerate(pose_landmarks.landmark):
        cx=int(lm.x*w)
        cy=int(lm.y*h)
        cz=lm.z
        cv=lm.visibility
        landmark_list.append([id,cx,cy,cz,cv])
    return landmark_list

def calc_angle(a,b,c): # these three points will be in the form of [x,y]
    a=np.array(a)
    b=np.array(b)
    c=np.array(c)
    
    radians=np.arctan2(c[1]-b[1],c[0]-b[0])-np.arctan2(a[1]-b[1],a[0]-b[0])
    angle=np.abs(radians*180/np.pi)
    
    if angle>180:
        angle=360-angle
    return angle
    

ctime=0
ptime=0

cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

count=0
stage=None

while True:
    isTrue,frame=cap.read()
    
    img=cv2.flip(frame,1)
    rgb_img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    
    #fps count
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    
    cv2.rectangle(img,(0,0),(int(img.shape[1]//5.5),int(img.shape[0]//5.5)+20),(0,255,0),-1)
    cv2.putText(img,f'FPS : {int(fps)}',(0,120),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(0,0,0),2)
    
    results=pose.process(rgb_img)
    
    if results.pose_landmarks:
        mp_drawing_tools.draw_landmarks(
            img,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_style,
            connection_style
        )
        landmark_list=get_landmark(results.pose_landmarks,img)
        
        shoulder=[landmark_list[11][1],landmark_list[11][2]]
        elbow=[landmark_list[13][1],landmark_list[13][2]]
        wrist=[landmark_list[15][1],landmark_list[15][2]]
        
        angle=calc_angle(shoulder,elbow,wrist)
        cv2.putText(img,f'{int(angle)}',(landmark_list[13][1],landmark_list[13][2]),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(0,0,0),2)
        
        # threshold angles are from 40 to 160
        if angle>150:
            stage='DOWN'
        if angle <80 and stage=='DOWN':
            stage="UP"
            count+=1
        
        
        # let us display thses things
        cv2.putText(img,f'COUNT :{count}',(0,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(0,0,0),3)
    
    cv2.imshow("video",img)
    if cv2.waitKey(1) & 0xFF==ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
