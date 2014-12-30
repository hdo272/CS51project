import cv2
import numpy as np
import math
from scipy import ndimage
from matplotlib import pyplot as plt

# import image
pic = cv2.imread('edges.png')
pic2 = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
hp, wp = pic.shape[0], pic.shape[1]
bar = np.zeros(wp)
widths = []

for x in range(0, wp):
    darkpix = 0
    for y in range(0, hp):
        c_pixel = pic2.item((y, x))
        if c_pixel > 250:
            darkpix += 1
    bar.itemset(x, darkpix)

# print bar (REMOVE)

numBar = len(bar)
begin = -1
for z in range(0, numBar):
    if bar[z] == 0 and begin != -1:
        widths.append((begin, z))
        begin = -1
    elif bar[z] != 0 and begin == -1:
        begin = z
if begin != -1:
    widths.append((begin, numBar))

# each letter is from begin...z-1

wnum = len(widths)
for i in range(0, wnum):
    b, e = widths[i][0], widths[i][1]
    seg = img[:,b:e]
    cv2.imwrite('seg' + str(i) + '.png', seg)




