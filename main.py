import cv2 
import math
import numpy as np
import random
from ThienLien import * 
from divideImage import *
from Affine import *
import os

# Read Image 
img = cv2.imread('girl.png')

AffineObj = affine(256)
enDetails = AffineObj.Encrypt(img)
DivObj = DivideImage(2)
DivDetails = DivObj.DivideIntoRQ(enDetails[0])
thienObj = ThienLien()
shareDetails = thienObj.createShare(DivDetails[0],4,6)


combineShare = thienObj.CombineShare(shareDetails,4)
DivDetails[0] = combineShare
org = DivObj.CombineRQ(DivDetails[0], DivDetails[1])
enDetails[0] = org
original = AffineObj.Decrypt(enDetails)


