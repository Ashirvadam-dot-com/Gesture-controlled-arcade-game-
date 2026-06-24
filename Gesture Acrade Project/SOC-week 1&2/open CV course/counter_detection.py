
# import cv2
# import numpy as np

# harvard= cv2.imread("images&videos/harvard.jpg")
# cv2.imshow("Harvard",harvard)

# # first decreasing the complexity by gray scaling
# gray= cv2.cvtColor(harvard,cv2.COLOR_BGR2GRAY)
# cv2.imshow("gray",gray)

# # after we listed the contours of gray-->canny lets add blur in between them
# blur= cv2.GaussianBlur(gray,(5,5),cv2.BORDER_DEFAULT)
# cv2.imshow("blur",blur)

# # then getting edge lined image
# canny=cv2.Canny(gray,125,175)
# cv2.imshow("canny",canny)

# # now lets make a binary image and see how many contours
# ret,thresh= cv2.threshold(gray,125,255,cv2.THRESH_BINARY)
# cv2.imshow("thresh",thresh)

# # writing a line which will take all the contours into a list
# contours,hirearchies= cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
# print(len(contours))



# # gary--> canny  have 2173 contours
# # gray--> blur--> canny have 331 contours
# # gray--> thresh  have 1540 contours
# # gray --> blur --> thresh have 159 contours


# # let us draw the contous of threshold image
# blank= np.zeros(harvard.shape[:2],dtype="uint8")
# cv2.imshow("blank",blank)

# thresh_contour_plot=cv2.drawContours(blank,contours,-1,(255,255,255),1)
# cv2.imshow("thresh_contour_plot",thresh_contour_plot)


# cv2.waitKey(0)
