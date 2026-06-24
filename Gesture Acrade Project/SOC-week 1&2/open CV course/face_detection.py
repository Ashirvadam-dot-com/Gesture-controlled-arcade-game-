import cv2


face=cv2.imread("images&videos/face-2")
cv2.imshow("face",face)
face=cv2.resize(face,(640,400),interpolation=cv2.INTER_AREA)
gray=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
cv2.imshow("gray image",gray)

face_detector=cv2.CascadeClassifier("open CV course/haar_face.xml")

face_found= face_detector.detectMultiScale(gray,1.1,5)

print(f"number of face(s) found {face_found}")
print(f"The coordinates of face {face_found}")

for (x,y,w,h) in face_found:
    cv2.rectangle(face,(x,y),(x+w,y+h),(0,255,0),3)
cv2.imshow("detected_face",face)

cv2.waitKey(0)