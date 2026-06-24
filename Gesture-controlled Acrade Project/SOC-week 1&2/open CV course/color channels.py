import cv2
import numpy as np
lion=cv2.imread("images&videos/lion")
cv2.imshow("lion",lion)
harvard= cv2.imread("images&videos/harvard.jpg")
cv2.imshow("Harvard",harvard)

# splitting image into 3 colour images.. but by default they will be converted into gray scale images

b,g,r = cv2.split(harvard)
cv2.imshow("b",b)
cv2.imshow("g",g)
cv2.imshow("r",r)


# merging of images  of particular colour 
blank =np.zeros(harvard.shape[:2],dtype="uint8")
b_and_g = cv2.merge([b,g,blank])
cv2.imshow("b ang g",b_and_g)
 
# if i want to view b as complete blue then../
blue= cv2.merge([b,blank,blank])
cv2.imshow("blue",blue)
cv2.waitKey(0)
