import cv2
import cv
import numpy as np
import math
from scipy import ndimage

gray=cv2.imread('temp.png', 0)
tup = gray.shape
imwidth = tup[0] 
imheight = tup[1] 

#convert to 32 bit
gray2=cv.CreateImage ((imwidth, imheight), 32, 1)
for r in range(imwidth):
    for c in range(imheight):
        gray2[r][c]=gray[r][c]
 
# define the filter:
lapl=cv.CreateImage ((imheight, imwidth), 32, 1)
m=cv.CreateImage ((3,3), 32, 1)
m[0][0]=-1
m[0][1]=-1
m[0][2]=-1
m[2][0]=-1
m[2][1]=-1
m[2][2]=-1
m[1][0]=-1
m[1][2]=-1
m[1][1]=8
cvFilter2D(gray2,lapl,m)
maxv=0
for r in range(imwidth):
    for c in range(imheight):
        if(lapl[r][c]>maxv):
            maxv=lapl[r][c]
            
for r in range(imwidth):
    for c in range(imheight):
        v=int(255*lapl[r][c]/maxv)
        gray[r][c]=gray[r][c]+v
        maxv=0

for r in range(imwidth):
    for c in range(imheight):
        if(gray[r][c]>maxv):
            maxv=gray[r][c]

for r in range(imwidth):
    for c in range(imheight):
        v=int(255*gray[r][c]/maxv)
        gray[r][c]=v

