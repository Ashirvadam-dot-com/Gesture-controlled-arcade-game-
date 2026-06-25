""" in this chapter we will convert one form of colour system to another""" 
import cv2

harvard= cv2.imread("images&videos/harvard.jpg")
cv2.imshow("Harvard",harvard)

# BGR to HSV
hsv=cv2.cvtColor(harvard,cv2.COLOR_BGR2HSV)
cv2.imshow("hsv image",hsv)

# BGR to LAB
lab=cv2.cvtColor(harvard,cv2.COLOR_BGR2Lab)
cv2.imshow("LAB image",lab)

# bgr to rgb
rgb= cv2.cvtColor(harvard,cv2.COLOR_BGR2RGB)
cv2.imshow("RGB image",rgb) # this will give an inverse colour image

# similarly we can do vice versa of reconverting
# if I want to go grom hsv to lab . first I will convert hsv to bgr then bgr to lab .. this should be the method


cv2.waitKey(0)

