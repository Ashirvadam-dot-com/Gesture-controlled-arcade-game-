
import cv2

harvard= cv2.imread("harvard.jpg")
cv2.imshow("Harvard",harvard)

# to grayscale
gray= cv2.cvtColor(harvard,cv2.COLOR_BGR2GRAY)
cv2.imshow("gray",gray)

# blurring
blur= cv2.GaussianBlur(harvard,(5,5),cv2.BORDER_DEFAULT)
cv2.imshow("blur",blur)


# outlining edges
cannal= cv2.Canny(gray,125,175)
cv2.imshow("canny",cannal)

canny_blur=cv2.Canny(blur,125,175)
cv2.imshow("canny(blur)",canny_blur)


#dilating the canny images
# dilated1=cv2.dilate(cannal,(7,7),iterations=3)
# cv2.imshow("dilated1",dilated1)

# dilated2=cv2.dilate(canny_blur,(7,7),iterations=3)
# cv2.imshow("dilated2",dilated2)




# # redilating or erroding the images
# erode1=cv2.erode(dilated1,(7,7),iterations=3)
# cv2.imshow("erodinf of dilated1",erode1)

# erode2=cv2.erode(cannal,(5,5),iterations=5)
# cv2.imshow("eroding of cannal",erode2)

# cv2.waitKey(0)