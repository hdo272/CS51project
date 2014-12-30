import cv2
import numpy as np
import math
from scipy import ndimage
from matplotlib import pyplot as plt

# import image
img = cv2.imread('threshed_cut.png')
img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
h, w = img.shape[0], img.shape[1]
bar = np.zeros(w)
widths = []

for x in range(0, w):
    darkpix = 0
    for y in range(0, h):
        curr_pixel = img2.item((y, x))
        if curr_pixel > 250:
            darkpix += 1
    bar.itemset(x, darkpix)

print bar

num = len(bar)
begin = -1
empty_thresh = 4
min_width = 3

for z in range(0, num):
    if bar[z] <= empty_thresh and begin != -1 and z - begin > min_width:
        widths.append((begin, z))
        begin = -1
    elif bar[z] > empty_thresh and begin == -1:
        begin = z
if begin != -1:
    widths.append((begin, num))

# each letter is from begin...z-1

wnum = len(widths)
for i in range(0, wnum):
    b, e = widths[i][0], widths[i][1]
    cut = img[:,b:e]
    cv2.imwrite('cut' + str(i) + '.png', cut)




