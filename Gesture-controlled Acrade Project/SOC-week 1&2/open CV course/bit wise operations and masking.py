import cv2
import numpy as np

harvard= cv2.imread("images&videos/harvard.jpg")
cv2.imshow("Harvard",harvard)

blank= np.zeros(harvard.shape[:2],dtype="uint8")
rectangle=cv2.rectangle(blank.copy(),(20,20),(250,250),255,-1)
cv2.imshow("rectangle",rectangle)
circle= cv2.circle(blank.copy(),(135,135),int(230/2),255,-1)
cv2.imshow("circle",circle)


# operating bit wise functions
bitwise_and= cv2.bitwise_and(rectangle,circle)
cv2.imshow("bitwise_and",bitwise_and)

bitwise_or=cv2.bitwise_or(rectangle,circle)
cv2.imshow("bitwise_or",bitwise_or)

bitwise_xor=cv2.bitwise_xor(rectangle,circle)
cv2.imshow("bitwise_xor",bitwise_xor)

bitwise_not= cv2.bitwise_not(rectangle)
cv2.imshow("bitwise_not",bitwise_not)




# masking
masking= cv2.bitwise_and(harvard,harvard,mask=rectangle)
cv2.imshow("masked image",masking)

masking_circle= cv2.bitwise_and(harvard,harvard,mask=circle)
cv2.imshow("masking with circle",masking_circle)


cv2.waitKey(0)




