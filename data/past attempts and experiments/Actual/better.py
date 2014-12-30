import cv2
import numpy as np
import math
import sys
from scipy import ndimage
import EdgeData as edge
import PlateTools as pt

# import image and convert to grayscale
if len(sys.argv) == 1:
    print "needs arguments"
    sys.exit(0)


img_rgb = cv2.imread(sys.argv[1])
img = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
w, h = img.shape[0], img.shape[1]
print "APPLYING SOBEL FILTER..."
mags, dirs, max_mag = edge.sobel(img)
print "APPLYING NON-MAXIMUM SUPPRESSION..."
mags = edge.nonmax_supp(mags, dirs)
print "EDGE SMOOTHING USING HYSTERESIS..."
edges = edge.hysteresis(mags)
print "PERFORMING EDGE DILATION..."
edges = edge.edge_dilation(edges, 1)





print "FINDING LICENSE PLATE..."

results = []
ratio_list = pt.filter_ratio(edges, 0.5)


MIN_SIZE = 1600
# count the number of components along the middle horizontal line!
for loc in ratio_list:
    # target that satisfies ratio
    target = img[loc]
    target_w, target_h = target.shape[1], target.shape[0]
    middle_h = target_h / 2

    # if min_size is not satisfied, skip
    if target.size < MIN_SIZE:
        continue

    # threshold the middle thirds height of the image
    # and the middle half of width of image
    middle_third = target[(target_h/3):(target_h/3*2),(target_w/8):(target_w/8*7)]
    middle_third = pt.threshold(middle_third, middle_third.shape[0] / 2)

    num = td.count_comps(middle_third, middle_third.shape[0] / 2)

    # LICENSE PLATES must have more than 3 and less than 8 components along middle.
    if num > 3 and num < 8:
        results.append(loc)


# for each plate, analyze text









