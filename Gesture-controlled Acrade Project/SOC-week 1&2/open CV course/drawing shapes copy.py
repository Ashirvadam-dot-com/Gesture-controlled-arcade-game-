import cv2
import numpy as np

blank = np.zeros((500,500,3),dtype="uint8")
cv2.imshow("blank",blank)

# drawing a rectangle
cv2.rectangle(blank,(20,50),(300,400),(0,0,255),1)
cv2.imshow("rectangle",blank)

# writing a text
cv2.putText(blank,"Hello ! my name is Ashirvadam",(20,250),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255),1)
cv2.imshow("text putted",blank)


cv2.waitKey(0)