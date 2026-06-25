
import cv2
import numpy as np

harvard= cv2.imread("images&videos/harvard.jpg")
cv2.imshow("Harvard",harvard)
harvard= cv2.cvtColor(harvard,cv2.COLOR_BGR2GRAY)

# canny method
canny= cv2.Canny(harvard,125,175)
cv2.imshow("canny",canny)

# laplacian
lap=cv2.Laplacian(harvard,cv2.CV_64F)
lap=np.uint8(np.absolute(lap))
cv2.imshow("laplacian",lap)

# sobel method
sobelx= cv2.Sobel(harvard,cv2.CV_64F,1,0)
cv2.imshow("sobel in x", sobelx)
sobely= cv2.Sobel(harvard,cv2.CV_64F,0,1)
cv2.imshow("sobel in y", sobely)

sobel_in_both= cv2.bitwise_or(sobelx,sobely)
cv2.imshow("sobel_in_both",sobel_in_both)

cv2.waitKey(0)