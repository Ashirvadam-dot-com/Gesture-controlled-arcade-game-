import cv2 
import numpy as np
import os


DIR=r"C:\Users\Ashirvadam\Downloads\Gesture Acrade Project\photos"
people=[]
features=[]
labels=[]
face_detector=cv2.CascadeClassifier("open CV course/haar_face.xml")
def create_training():
    for person in os.listdir(DIR):
        people.append(person)
        person_path=os.path.join(DIR,person)
        
        for img in os.listdir(person_path):
            img_path=os.path.join(person_path,img)
            image=cv2.imread(img_path)
            if image is None:
                continue
            
            gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            face_found=face_detector.detectMultiScale(gray,1.1,5)
            
            for (x,y,w,h) in face_found:
                cropped_image=gray[y:y+h,x:x+h]
                features.append(cropped_image)
                labels.append(people.index(person))
                
create_training()

features=np.array(features,dtype="object")
labels=np.array(labels)

face_recognizer=cv2.face.LBPHFaceRecognizer_create()
face_recognizer.train(features,labels)

face_recognizer.save("face_has_been_trained.yml")
np.save("features_list",features)
np.save("lables list",labels)


# code is working
      
        