import cv2
import numpy as np

harvard= cv2.imread("harvard.jpg")
cv2.imshow("Harvard",harvard)

#translation
def translate(image,x,y):
    (height,width)=image.shape[:2]
    transMAt=np.float32([[1,0,x],[0,1,y]])
    dimensions=(width,height)
    return cv2.warpAffine(image,transMAt,dimensions)

translated_image=translate(harvard,100,100)
cv2.imshow("translated_image",translated_image)

# +x --> right
# -x --> left
# +y --> down
# -y --> up



# rotation of an image
def rotation(image,angle,rotPoint=None):
    (height,width)=image.shape[:2]
    if rotPoint is None:
        rotPoint=(width,height)
    rotMat= cv2.getRotationMatrix2D(rotPoint,angle,1.0)
    dimensions=(width,height)
    return cv2.warpAffine(image,rotMat,dimensions)

rotated_image=rotation(harvard,45)
cv2.imshow("rotated_image",rotated_image)

# +0 --> ACW
# -0 --> CW



# flipping
flipped_Y= cv2.flip(harvard,1)
cv2.imshow("flipped_Y",flipped_Y)
flipped_X=cv2.flip(harvard,0)
cv2.imshow("flipped_X",flipped_X)
flipped_XnY = cv2.flip(harvard,-1)
cv2.imshow("flipped_XnY",flipped_XnY)

# 0--> flip around X axis
# 1--> flip around Y axis
# -1--> flip around both the axis

cv2.waitKey(0)