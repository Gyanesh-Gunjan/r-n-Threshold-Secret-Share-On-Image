import numpy as np
import cv2
import math 
import random
import os
class DivideImage:
    def __init__(self, dividend):
        os.mkdir('Divide Image')
        self.dividend = dividend
        if type(dividend) != int or dividend == 0:
            print("\nError : Wrong format of dividend!\n")
            var = int(input("Enter Dividend : "))
            self.dividend = var

    #----------------------------------
    # Defining DivideIntoRQ function 
    #_---------------------------------
    def DivideIntoRQ(self, image):
        """
        This function divide Input Image into two part i.e. remainder and quotient images

        Parameters :
        ------------
        Image : 
        Dividend(int):
            This input take during object creation

        Returns :
        ---------
            list : A list contains Remainder and Quotient Images
        """
        height = image.shape[0]
        width = image.shape[1]
        R_image = np.zeros((height, width, 3), np.uint8)
        Q_image = np.zeros((height, width, 3), np.uint8)
        for h in range(0,height):
            for w in range(0,width):
                rbg = image[h][w]
                Q_image[h][w] = [rbg[0]//self.dividend, rbg[1]//self.dividend, rbg[2]//self.dividend]
                R_image[h][w] = [rbg[0]%self.dividend, rbg[1]%self.dividend, rbg[2]%self.dividend]
        
        cv2.imwrite(os.path.join('Divide Image', 'Quotient.png'), Q_image)
        cv2.imwrite(os.path.join('Divide Image', 'Remainder.png'), Q_image)
        # cv2.imwrite('Quotient.png',Q_image)
        # cv2.imwrite('Remainder.png',R_image)
        return [Q_image, R_image]

    #----------------------------------
    # Defining CombineRQ function 
    #_---------------------------------
    def CombineRQ(self, QImage, RImage):
        """
        This function combines input images (i.e. Remainder and Quotient images) into original image

        Paramerters :
        -------------
        Remainder Image :
        Quotient Image :
        Dividend(int):
            This input take during object creation

        return :
        --------
            Image : Combined image of remainder and quotient images
        """
        if RImage.shape[0] == QImage.shape[0] and RImage.shape[1] == QImage.shape[1]:
            height = RImage.shape[0]
            width = RImage.shape[1]
            C_image = np.zeros((height, width, 3), np.uint8)
            for h in range(0, height):
                for w in range(0, width):
                    rbg_Q = QImage[h][w]
                    rbg_R = RImage[h][w]
                    C_image[h][w] = [rbg_Q[0]*self.dividend + rbg_R[0], rbg_Q[1]*self.dividend + rbg_R[1], rbg_Q[2]*self.dividend + rbg_R[2]]
           
            cv2.imwrite(os.path.join('Divide Image', 'combineQR.png'), C_image)
            
            #cv2.imwrite('combine.png', C_image)
            return C_image
        else:
            print("Dimension doesn't match!")
            


