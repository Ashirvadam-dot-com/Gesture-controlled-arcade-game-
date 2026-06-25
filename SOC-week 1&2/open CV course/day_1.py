

# import cv2


# harvard= cv2.imread("images&videos/harvard.jpg")
# cv2.imshow("Harvard",harvard)

# cv2.waitKey(0)


# """ this is the basic code to load an image or video """

# my_image= cv2.imread("Screenshot 2026-05-01 001810.png")
# cv2.imshow("MY IMAGE IS ", my_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# """ this code is to open a video file """

# video_file=cv2.VideoCapture("rainy video.mp4")   # if I enter 0 (pc's front camera will open ) , 1 and 2 will open external cameras
# while True :
#     isTrue, frame= video_file.read()
#     cv2.imshow("THE VIDEO IS ",frame)
    
#     if cv2.waitKey(15) & 0xFF==ord("x"):
#         break
    
# video_file.release()
# cv2.destroyAllWindows()







