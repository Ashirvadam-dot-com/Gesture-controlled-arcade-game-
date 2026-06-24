import cv2
import mediapipe as mp
import time

mp_pose=mp.solutions.pose
mp_drawing_tools=mp.solutions.drawing_utils

pose=mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    smooth_landmarks=True,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)

landmarks_style=mp_drawing_tools.DrawingSpec(
    color=(255,255,255),
    thickness=-1,
    circle_radius=4
)

connections_style=mp_drawing_tools.DrawingSpec(
    color=(255,0,0),
    thickness=3
)

def get_coordinates(pose_landmarks,image):
    h,w,c=image.shape
    lm_list=[]
    for id, lm in enumerate(pose_landmarks.landmark):
        cx=int(lm.x*w)
        cy=int(lm.y*h)
        cz=lm.z
        cv=lm.visibility
        lm_list.append([id,cx,cy,cz,cv])
    return lm_list


cap=cv2.VideoCapture(0)

ctime=0
ptime=0

while True:
    isTrue,frame=cap.read()
    img=cv2.flip(frame,1)
    rgb_img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img,f"FPS = {int(fps)}",(30,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(0,0,0),2)
    
    results=pose.process(rgb_img)
    
    if results.pose_landmarks:
        
        mp_drawing_tools.draw_landmarks(
            img,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmarks_style,
            connections_style
            )
        lm_coordinates=get_coordinates(results.pose_landmarks,img)
        
        # this was to print the coordinates of wrist (L and R)
        # id1,left_wrist_x,left_wrist_y,lw_z,lw_v=lm_coordinates[16]
        # id2,right_wrist_x,right_wrist_y,rw_z,rw_v=lm_coordinates[15]
        
        # cv2.putText(img,f"(xL,yL)={left_wrist_x,left_wrist_y}",(50,80),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),3)
        # cv2.putText(img,f"(xR,yR)={right_wrist_x,right_wrist_y}",(550,80),cv2.FONT_HERSHEY_COMPLEX,1,(0,165,255),3)

    
    cv2.imshow("project",img)
    
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()