import numpy as np
import cv2
import math 
import random
import os

class affine:
    def __init__(self, mod = 256):
        os.mkdir('Affine Details')
        self.__m = mod
        while self.__m == 0:
            print("\nError : Alphabet Size should not be zero!")
            var = int(input("Please Enter Alphabet size : "))
            self.__m = var

    #-----------------------------
    # Definition inverse function 
    #-----------------------------
    def Inverse(self, n, m):
        """
        This function takes input number, m (modulo) and return inverse of n over modulo m
        Parameters :
        ------------
        n(int) : number 
        m(int) : Modulo m

        Return :
        --------
            inv(int) : Inverse of n modulo m
        """
        inv = 2
        while 1:
            if inv*n % m == 1:
                return inv
            else:
                inv += 1

    #-----------------------------
    # Definition E(x) function 
    #-----------------------------
    def __E(self, x, a, b, m):
        return (a*x + b) % m

    #-----------------------------
    # Definition D(y) function 
    #-----------------------------
    def __D(self, y, a, invA, b, m):
        return (invA * (y - b)) % m

    #----------------------------------
    # Definition Encryption function 
    #----------------------------------
    def Encrypt(self, image):
        """
        Defn : This function encrypt each Pixel of input image using affine cipher

        Paramters :
        -----------
            image : Input image

        Returns :
            EncryptionDetails (List) : Contains details of encryption
            Where, 
                EncryptionDetails[0] : Encrypted Image
                EncryptionDetails[1] : A Value
                EncryptionDetails[1] : B Value
                EncryptionDetails[1] : H Value
                EncryptionDetails[1] : Hb Value
                EncryptionDetails[1] : W Value
                EncryptionDetails[1] : Wb Value
        """
        # A, B details
        CoPrime = []
        for i in range(0, self.__m):
            if math.gcd(i, self.__m) == 1 :
                CoPrime.append(i)
        A = random.choice(CoPrime)
        B = random.randint(1, self.__m)

        # Height Details
        Height = image.shape[0]
        CoPrime = []
        for i in range(0, Height):
            if math.gcd(i, Height) == 1 :
                CoPrime.append(i)
        H = random.choice(CoPrime)
        Hb = random.randint(1, Height)

        # Width details 
        Width = image.shape[1]
        CoPrime = []
        for i in range(0, Width):
            if math.gcd(i, Width) == 1 :
                CoPrime.append(i)
        W = random.choice(CoPrime)
        Wb = random.randint(1, Width)

        # Creating blank image image of same size of original image
        encrypted_image = np.zeros((Height, Width, 3), np.uint8)

        print("Encryption starts ",end="")
        per = Height // 10  
        for h in range(0, Height):
            enH = self.__E(h, H, Hb, Height)
            for w in range(0, Width):
                enW = self.__E(w, W, Wb, Width)
                rbg = image[h][w]
                r = self.__E(rbg[0], A, B, self.__m)
                b = self.__E(rbg[1], A, B, self.__m)
                g = self.__E(rbg[2], A, B, self.__m)
                encrypted_image[enH][enW] = [r, b, g]
            if h % per == 0 :
                print(' .',end="")
        print(" done!")

        cv2.imwrite(os.path.join('Affine Details','encrypted_Img.png'), encrypted_image)
        # cv2.imwrite('encrypted_Img.png', encrypted_image)

        EncryptionDetails = [encrypted_image, A, B, H, Hb, W, Wb]
        return EncryptionDetails

    #-----------------------------------
    # Definition Decryption function 
    #-----------------------------------   
    def Decrypt(self, Details):
        """
        Defn : This function take details of encryption then decrypt it to original image

        Parameters :
        ------------
            Details(List) : Details of Encryption
            Where, 
                Details[0] : Encrypted Image
                Details[1] : A Value
                Details[1] : B Value
                Details[1] : H Value
                Details[1] : Hb Value
                Details[1] : W Value
                Details[1] : Wb Value
                
        Returns :
        --------
            Original Image : return original image on the basis of given details
        """
        encrypted_image = Details[0]

        # A , B details
        A = Details[1]
        invA = self.Inverse(A, self.__m)
        B = Details[2]

        # Height details
        Height = encrypted_image.shape[0]
        H = Details[3]
        invH = self.Inverse(H, Height)
        Hb = Details[4]

        # Width details
        Width = encrypted_image.shape[1]
        W = Details[5]
        invW = self.Inverse(W, Width)
        Wb = Details[6]

        # Create blank image of same size that of original image
        decrypted_image = np.zeros((Height, Width, 3), np.uint8)

        print("Decryption starts ",end="")
        per = Height//10
        for h in range(0, Height):
            deH = self.__D(h, H, invH, Hb, Height)
            for w in range(0, Width):
                deW = self.__D(w, W, invW, Wb, Width)
                rbg = encrypted_image[h][w]
                r = self.__D(rbg[0], A, invA, B, self.__m)
                b = self.__D(rbg[1], A, invA, B, self.__m)
                g = self.__D(rbg[2], A, invA, B, self.__m)
                decrypted_image[deH][deW] = [r,b,g]
            if h % per == 0:
                print(' .',end="")
        print(" done!")
        cv2.imwrite(os.path.join('Affine Details','Decrypted_Img.png'), decrypted_image)
        # cv2.imwrite('Decrypted_Img.png', decrypted_image)
        return decrypted_image
