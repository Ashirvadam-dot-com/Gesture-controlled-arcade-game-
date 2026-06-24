""" this is the code for rescalling as well as cropping"""

import cv2

def rescalling(frame,scale):
    width= int(frame.shape[1]*scale)
    height= int(frame.shape[0]*scale)
    dimensions=(height,width)
    return cv2.resize(frame,dimensions,interpolation=cv2.INTER_AREA)

# normal image
harvard= cv2.imread("Gesture Acrade Project/SOC-week 1&2/images&videos/harvard.jpg")
cv2.imshow("Harvard",harvard)

# resizing by same factor then we will use a function
resized_harvard=rescalling(harvard,0.75)
cv2.imshow("resized harvard",resized_harvard)
print(harvard.shape)

# resizing by different factor 
resized= cv2.resize(harvard,(500,300),interpolation=cv2.INTER_AREA)
cv2.imshow("resized",resized)


# this will crop the image  , numbers are like first- top to bottom then left to right . this covers an rectangle
cropping=harvard[0:harvard.shape[0]//2,0:harvard.shape[1]//2]
cv2.imshow("cropped image",cropping)
cv2.waitKey(0)

