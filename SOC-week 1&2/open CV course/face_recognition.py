import cv2
import numpy as np
import os

DIR=r"C:\Users\Ashirvadam\Downloads\Gesture Acrade Project\photos"
people=[]

for person in os.listdir(DIR):
    people.append(person)
# peoplr list has been created

face_detector=cv2.CascadeClassifier("open CV course/haar_face.xml")

face_recognizer=cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read("open CV course/face_has_been_trained.yml")

image=r"C:\Users\Ashirvadam\Downloads\Gesture Acrade Project\photos\charlote\5"

img= cv2.imread(image)

gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# creating a cropped image
face_found=face_detector.detectMultiScale(gray,1.1,10)

for (x,y,w,h) in face_found:
    cropped_image=gray[y:y+h,x:x+w]
    # predicting the image
    labels,confidence=face_recognizer.predict(cropped_image)
    print(f"face found - {people[labels]} \ncondidence is {confidence}")
    
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    
    cv2.putText(img,f"{people[labels]}",(20,20),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,255,0))

cv2.imshow("recognised image",img)
cv2.waitKey(0)   
