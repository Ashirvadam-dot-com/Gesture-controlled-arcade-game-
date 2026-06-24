
# import cv2
# import matplotlib.pyplot as plt
# import numpy as np


# harvard= cv2.imread("images&videos/harvard.jpg")
# cv2.imshow("Harvard",harvard)
# blank= np.zeros(harvard.shape,dtype='uint8')
# cv2.imshow("bkank",blank)

# circle= cv2.circle(blank.copy(),(135,135),int(230/2),255,-1)
# cv2.imshow("circle",circle)

# # histogram for coloured images 
# plt.figure()
# plt.title("colored histogram")
# plt.xlabel("bin")
# plt.ylabel("# of pixels")
# colour=('b','g','r')
# for i, col in enumerate(colour):
#     hist=cv2.calcHist([harvard],[i],None,[256],[0,256])
#     plt.plot(hist)
#     plt.xlim([0,256])
# plt.show()


# # masked_image=cv2.bitwise_and(harvard,harvard,circle)
# # cv2.imshow("masked image",masked_image)

# # for i , col in enumerate (colour):
# #     hist=cv2.calcHist([harvard],[i],masked_image,[256],[0,256])
# #     plt.plot(hist)
# #     plt.xlim([0,256])
# #     plt.show()
    
    
    
# # # for grayscale image
# # gray=cv2.cvtColor(harvard,cv2.COLOR_BGR2GRAY)
# # cv2.imshow("gray",gray)

# # gray_hist= cv2.calcHist([gray],[0],None,[256],[0,256])
# # plt.figure()
# # plt.title("gray scale histogram")
# # plt.xlabel("bin")
# # plt.ylabel("# of pixels")
# # plt.plot(gray_hist)
# # plt.xlim([0,256])
# # plt.show()

# # # masking of gray image and then calc.. histogram
# # masking_gray=cv2.bitwise_and(gray,gray,mask=circle)
# # cv2.imshow("masking_gray",masking_gray)
# # gray_hist_masked= cv2.calcHist([gray],[0],masking_gray,[256],[0,256])
# # plt.figure()
# # plt.title("gray scale histogram 'masked")
# # plt.xlabel("bin")
# # plt.ylabel("# of pixels")
# # plt.plot(gray_hist)
# # plt.xlim([0,256])
# # plt.show()

# # cv2.waitKey(0)


import cv2
import matplotlib.pyplot as plt
import numpy as np


class Hist_plot:
    def __init__(self,image,image_name,colour,masking):
        self.image=image
        self.image_name=image_name
        self.colour=colour
        self.masking=masking
    def plot(self):
        plt.figure()
        plt.title(f"{self.image_name} image histogram ")
        plt.xlabel("bin")
        plt.ylabel("no. of pixels")
        if type(self.colour) is not int:
            for i , col in enumerate(self.colour):
                Hist=cv2.calcHist([self.image],[i],self.masking,[256],[0,256])
                plt.plot(Hist)
                plt.xlim([0,256])
        else:
            Hist=cv2.calcHist([self.image],[self.colour],self.masking,[256],[0,256])
            plt.plot(Hist)
            plt.xlim([0,256])
        plt.show()
        
harvard=cv2.imread("images&videos/harvard.jpg")
gray=cv2.cvtColor(harvard,cv2.COLOR_BGR2GRAY)

Calc_hist1=Hist_plot(harvard,"harvard",("b","g",'r'),None)
Calc_hist1.plot()

# Calc_hist=Hist_plot(gray,"gray",0,None)
# Calc_hist.plot()

# let us try with masking
blank=np.zeros(harvard.shape[:2],dtype="uint8")
mask=cv2.circle(blank,(300,100),50,255,-1)

masked_image=cv2.bitwise_and(harvard,harvard,mask=mask)

cv2.imshow("masked-image",masked_image)


Calc_hist2=Hist_plot(harvard,"harvard",("b","g",'r'),mask)
Calc_hist2.plot()

cv2.waitKey()




