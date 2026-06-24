import cv2


harvard= cv2.imread("images&videos/harvard.jpg")
cv2.imshow("Harvard",harvard)

# averaging method
average=cv2.blur(harvard,(5,5))
cv2.imshow("avrage blurring",average)


# gaussian blur
G_blur=cv2.GaussianBlur(harvard,(5,5),0,cv2.BORDER_DEFAULT)
cv2.imshow("gaussian blur",G_blur)

#median blur
median_blur=cv2.medianBlur(harvard,5)
cv2.imshow("median blur",median_blur)

#bilateral blur
bilateral=cv2.bilateralFilter(harvard,10,20,20,cv2.BORDER_DEFAULT)
cv2.imshow("bilateral",bilateral)

cv2.waitKey(0)

