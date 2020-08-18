import cv2 
import math
import numpy as np
import random
import os

class ThienLien:
    def __init__(self):
        os.mkdir('Shares')
        self.mod = 251
    #---------------------------------------------------------------
    # Definition Absolute function (i.e. to find Nearest Integer) 
    #_--------------------------------------------------------------    
    def __absVal(self, x):
        if abs(math.ceil(x) - x) > abs(math.floor(x) - x):
            return math.floor(x)
        else:
            return math.ceil(x)
    
    #---------------------------------------
    # Definition RetrievePixel  function 
    #_--------------------------------------
    def __RetrievePixel(self, Det, Pixel):
        P = 0
        Pixel %= self.mod
        while 1 :
            if (Det * P) % self.mod == Pixel:
                return P
            P += 1

    #----------------------------------
    # Definition cofactor function 
    #_---------------------------------
    def __CoFactor(self, Mat, r):
        cofactor_Mat = []
        for row in range(0, r):
            cofactorRow = []
            for col in range(0,r):
                tempMatrix = []
                for i in range(0,r):
                    if i == row:
                        continue
                    tempMatrix.append(Mat[i][0:col]+Mat[i][col+1:])
                tempMatrix = np.array(tempMatrix)
                d = self.__absVal(np.linalg.det(tempMatrix))
                if (row + col) % 2 :
                    d = -d
                cofactorRow.append(d)
            cofactor_Mat.append(cofactorRow)
        cofactor_Mat = np.array(cofactor_Mat)
        return np.transpose(cofactor_Mat)

    #------------------------------------
    # Definition createImage  function 
    #_-----------------------------------
    def __CreateImage(self, image, Width):
        Height = image.shape[0]
        CurrWdth = image.shape[1]
        tempImage = np.zeros((Height, Width, 3), np.uint8)
        for h in range(0, Height):
            for w in range(0,CurrWdth):
                tempImage[h][w] = image[h][w]
        return tempImage

    #---------------------------------------------
    # Definition calculatePolynomial  function 
    #_--------------------------------------------
    def __CalculatePolynomial(self, x, Pixels):
        Fx = Pixels[0]
        var = x
        for i in range(1, len(Pixels)):
            Fx = (Fx + Pixels[i]*var) % self.mod
            var = (var * x) % self.mod
        return Fx

    #--------------------------------------
    # Definition CreateShare function 
    #_-------------------------------------
    def createShare(self, image, r, n):
        """
        Defn : This function create input image into n Share_Image oof size height*(width//r)

        Paramters :
        -----------
            image : Input image 
            r(int) : Minimum shares to reconstruct original image 
            n(int) : Maximum Shares to Distribute

        Return :
        --------
            ShareDetails (List): All  share details  (Size = n)

            Details 
            ShareDetails[i] : ith Share details and It is a list containing two fields 
            i.e. ShareDetails[i][0] : ith Share Image
            And, ShareDetails[i][1] : Key Value corresponding to ith  share image
        """
        Height = image.shape[0]
        Width = image.shape[1]
        ShareWidth = Width // r
        if Width % r != 0:
            ShareWidth += 1
            image = self.__CreateImage(image, ShareWidth*r)

        Shares = []
        xValues =  random.sample(range(1,256),n)
        
        print("Share creation start ",end="")
        for share in range(0,n):
            tempShare = np.zeros((Height, ShareWidth, 3), np.uint8)
            for h in range(0, Height):
                Swidth = 0
                for w in range(0, (ShareWidth*r), r):
                    rPixels = []
                    gPixels = []
                    bPixels = []
                    for p in range(w,w+r):
                        rPixels.append(image[h][p][0])
                        gPixels.append(image[h][p][1])
                        bPixels.append(image[h][p][2])

                    R = self.__CalculatePolynomial(xValues[share], rPixels)
                    G = self.__CalculatePolynomial(xValues[share], gPixels)
                    B = self.__CalculatePolynomial(xValues[share], bPixels)
                    tempShare[h][Swidth] = [R,G,B]
                    Swidth += 1
            print(". ", end="")

            cv2.imwrite(os.path.join('Shares', 'Share.{}.png'.format(share)), tempShare)
            # cv2.imwrite('share{}.png'.format(share), tempShare)
            Shares.append([tempShare, xValues[share]])
        print("done!")
        
        return Shares

    #--------------------------------------
    # Definition CombineShare function 
    #_-------------------------------------
    def CombineShare(self, ShareDetails, r):
        """
        Defn : This function combines r shares to reconstruct original Share

        Parameters :
        ------------
            ShareDetails(list) : Details of minimum r shares (minimum Size = r)
            ShareDetails[i] : Details of ith share
            Like , ShareDetails[i][0] : contains ith Share Image
            And, ShareDetails[i][1] : Contains Key of ith Share Image

        Return :
        --------
            None : if Size of ShareDetails < r
            Original Image : if size of ShareDetails >= r and if given values are true

        """
        if len(ShareDetails) < r:
            return 

        # Dimention details    
        Height = ShareDetails[0][0].shape[0]
        Width = ShareDetails[0][0].shape[1]

        # find Coefficient Matrix 
        CoeffientMatrix = []
        for i in range(0, r):
            tempRow = [1]
            var = ShareDetails[i][1] % self.mod
            for x in range(1,r):
                tempRow.append(var)
                var = (var * ShareDetails[i][1]) % self.mod
            CoeffientMatrix.append(tempRow)

        Det_Of_CoefficientMatrix = self.__absVal(np.linalg.det(CoeffientMatrix)) 
        Cofacor_of_CoefficientMatrix = self.__CoFactor(CoeffientMatrix,r)

        OriginalShare = np.zeros((Height, Width*r, 3), np.uint8)

        for h in range(0, Height):
            sw = 0
            for w in range(0, Width):
                RList = []
                GList = []
                BList = []

                for i in range(0, r):
                    RList.append([ShareDetails[i][0][h][w][0]])
                    GList.append([ShareDetails[i][0][h][w][1]])
                    BList.append([ShareDetails[i][0][h][w][2]])

                RPixels = np.dot(Cofacor_of_CoefficientMatrix, RList)
                GPixels = np.dot(Cofacor_of_CoefficientMatrix, GList)
                BPixels = np.dot(Cofacor_of_CoefficientMatrix, BList)

                # Retrieving each pixel
                for i in range(0, r):
                    R = self.__RetrievePixel(Det_Of_CoefficientMatrix, RPixels[i])
                    G = self.__RetrievePixel(Det_Of_CoefficientMatrix, GPixels[i])
                    B = self.__RetrievePixel(Det_Of_CoefficientMatrix, BPixels[i])

                    OriginalShare[h][sw] = [R,G,B]
                    sw += 1
        cv2.imwrite(os.path.join('Shares', 'OriginalShare.png'), OriginalShare)

        # cv2.imwrite('OriginalShare.png', OriginalShare)
        return OriginalShare

