import cv2


harvard= cv2.imread("images&videos/harvard.jpg")
cv2.imshow("Harvard",harvard)

gray=cv2.cvtColor(harvard,cv2.COLOR_BGR2GRAY)
cv2.imshow("gray",gray)

# simple thresholding:
threshold,simple_thresh= cv2.threshold(gray,150,255,cv2.THRESH_BINARY)
cv2.imshow("simple_thresh",simple_thresh)
print(threshold) # 150 

Threshold, simple_thresh_inv= cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV)
cv2.imshow("simple_thresh_inv",simple_thresh_inv)


# adaptive thresholding
adaptive= cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,15,3)
cv2.imshow("adaptiveThreshold",adaptive)

adaptive_inv= cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,15,3)
cv2.imshow("adaptiveThreshold inverse",adaptive_inv)

cv2.waitKey(0)