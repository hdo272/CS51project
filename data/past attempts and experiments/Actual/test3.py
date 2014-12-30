import cv2
import numpy as np
import math
import sys
from scipy import ndimage

# import image and convert to grayscale
if len(sys.argv) == 1:
    print "needs arguments"
    sys.exit(0)


img_rgb = cv2.imread(sys.argv[1])
img = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
w, h = img.shape[0], img.shape[1]

# DEFINE VARIABLES HERE.
# mags contain the magnitude of each pixel in grayscale
mags = img.copy()
# dirs contain the ROUNDED angles of the gradient vectors
dirs = np.zeros((w,h))
# edges matrix mark which pixels are definitely edges, used
# during hysteresis edge smoothing. 0s are for not yet searched pixel
# or not an edge, and 255s are for definite edge pixels.
edges = np.zeros((w,h))
MAX_PIXEL = 255




# STEP 1. Apply sobel filter. Retrieve magnitudes and directions
# of gradients. Round directions to either 0, 45, 90, or 135.
# We save the max mag value to normalize our mags matrix later on.

print "APPLYING SOBEL FILTER..."

mat_x = np.matrix('-1 0 1; -2 0 2; -1 0 1')
mat_y = np.matrix('1 2 1; 0 0 0; -1 -2 -1')

# for keeping track of maximum mag
max_mag = 0

for x in range(0, w):
    if x == 0:
        print("0 ..."),
    elif x == int(w * .25):
        print(" 25 ..."),
    elif x == int(w * .5):
        print(" 75 ..."),
    elif x == w - 1:
        print("100")

    for y in range(0, h):
        sum_x = 0
        sum_y = 0

        # edge cases
        if x == 0 or y == 0 or x == w - 1 or y == h - 1:
            mags.itemset((x,y), 0)
            continue

        for n in range(-1, 2):
            for m in range(-1, 2):
                sum_x += mat_x.item((n,m)) * img.item((x+n, y+m))
                sum_y += mat_y.item((n,m)) * img.item((x+n, y+m))

        # compute magnitude of gradient
        mag = math.sqrt(sum_x ** 2 + sum_y ** 2)

        # if mag is greater than 255, truncate to 255
        # this means any mag greater than 255 is treated
        # equally (as a clear edge)
        if mag > 255:
            mag = 255

        # set pixel in result matrix
        mags.itemset((x,y), mag)

        # update max mag accordingly
        if mag > max_mag:
            max_mag = mag

        # Next: compute direction
        # but first check if sum_x is 0
        if sum_x == 0:
            theta = 90
        else:
            theta = math.degrees(math.atan2(sum_y, sum_x))
            # now we "round" the angles
            if ((theta >= -22.5 and theta < 22.5)
                    or theta > 157.5 or theta <= -157.5):
                theta = 0
            elif ((theta >= 22.5 and theta < 67.5)
                    or (theta > -157.5 and theta <= -112.5)):
                theta = 45
            elif ((theta >= 67.5 and theta < 112.5)
                    or (theta > -112.5 and theta <= -67.5)):
                theta = 90
            else:
                theta = 135

        # save the angle
        dirs.itemset((x,y), theta)

# STEP 2. Apply non-maximum suppression. If pixel is smaller than
# left/right pixel (respective of edge direction), set its mag to 0.

print "APPLYING NON-MAXIMUM SUPPRESSION..."

# notice how the ranges don't include the edges
for x in range(1, w - 1):
    for y in range(1, h - 1):
        theta = dirs.item((x,y))
        curr_pixel = mags.item((x,y))

        # compare theta!
        if theta == 0:
            # horizontal edge; compare up and down
            pixel1 = mags.item((x, y + 1))
            pixel2 = mags.item((x, y - 1))
        elif theta == 45:
            # compare southeast, northwest
            pixel1 = mags.item((x - 1, y - 1))
            pixel2 = mags.item((x + 1, y + 1))
        elif theta == 90:
            # vertical edge; compare left and right
            pixel1 = mags.item((x - 1, y))
            pixel2 = mags.item((x + 1, y))
        else:
            # compare northeast, southwest
            pixel1 = mags.item((x + 1, y + 1))
            pixel2 = mags.item((x - 1, y - 1))

        # now compare the pixel values
        # if left or right has a larger value, current pixel
        # cannot be an edge
        if (curr_pixel < pixel1 or curr_pixel < pixel2):
            mags.itemset((x,y), 0)


# STEP 3. Hysteresis edge smoothing. Using high and low thresholds,
# we check which pixels are certain to be edges using the high
# threshold, and which pixels near the edges are also edges using
# the low threshold.

print "EDGE SMOOTHING USING HYSTERESIS..."

# we first define our two thresholds, high and low.
thresh_high = 180
thresh_low = 100

# hystConnect searches for pixels adjacent
# to definitive edges, and marks those above
# the LOW threshold as edges

# this version requires A LOT of stack frames
# stack overflow for large pictures :/ not good


def hystConnect(x, y, thresh):
    # check in all 8 directions
    for i in range(-1, 2):

        # edge cases for x!
        if (x == 0 and i == -1) or (x == w - 1 and i == 1):
            continue

        for j in range(-1, 2):
            # check edge cases for y
            if (y == 0 and j == -1) or (y == h - 1 and j == 1):
                continue

            # if pixel is over threshold, mark as edge
            # and propagate
            # but if already marked as edge, ignore
            if (mags.item((x + i, y + j)) > thresh
                    and edges.item((x + i, y + j)) != MAX_PIXEL):
                edges.itemset((x + i, y + j), MAX_PIXEL)
                hystConnect(x + i, y + j, thresh)

# a non-recursive version that uses a stack instead!
# no more stack overflows

def betterHystConnect(x, y, thresh):
    stack = [(x, y)]

    while len(stack) > 0:
        coords = stack.pop()
        x, y = coords[0], coords[1]

        for i in range(-1, 2):

            # edge cases for x!
            if (x == 0 and i == -1) or (x == w - 1 and i == 1):
                continue

            for j in range(-1, 2):
                # check edge cases for y
                if (y == 0 and j == -1) or (y == h - 1 and j == 1):
                    continue

                # if pixel is over threshold, mark as edge
                # and propagate
                # but if already marked as edge, ignore
                if (mags.item((x + i, y + j)) > thresh
                        and edges.item((x + i, y + j)) != MAX_PIXEL):
                    edges.itemset((x + i, y + j), MAX_PIXEL)
                    stack.append((x+i, y+j))



def process():
    for x in range(0, w):
        for y in range(0, h):
            if (edges.item((x,y)) != MAX_PIXEL
                and mags.item((x,y)) >= thresh_high):
                edges.itemset((x,y), MAX_PIXEL)
                betterHystConnect(x, y, thresh_low)

process()

print "PERFORMING EDGE DILATION..."

# Dilate the pixels!
# newly dilated pixels have value MAX_PIXEL - 1 (or 254)
# so that we don't dilate the newly added pixels!


def edge_dilation(num):
    for i in range(1, num + 1):
        for x in range(0, w):
            for y in range(0, h):
                if edges.item((x,y)) >= MAX_PIXEL - i + 1:
                    if x != 0 and edges.item((x-1, y)) == 0:
                        edges.itemset((x-1, y), MAX_PIXEL - i)
                    elif y != 0 and edges.item((x, y-1)) == 0:
                        edges.itemset((x, y-1), MAX_PIXEL - i)
                    elif x != w - 1 and edges.item((x+1, y)) == 0:
                        edges.itemset((x+1, y), MAX_PIXEL - i)
                    elif y != h - 1 and edges.item((x, y+1)) == 0:
                        edges.itemset((x, y+1), MAX_PIXEL - i)

edge_dilation(1)







print "FINDING LICENSE PLATE..."

# License plate detection!
# First, let scipy label our connected components
labeled_edges, num_labels = ndimage.label(edges)

# set up some variables!
# ratio list contains all the candidates with the correct ratios
# results contains the final list
ratio_list = []
results = []

# FIRST, iterate through each component,
# and check the ratio! if approx. 1:2, then add to list
for label in range(1, num_labels + 1):
    # note: loc is a slice object, which is annoying
    loc = ndimage.find_objects(labeled_edges == label)[0]
    array = edges[loc]
    w1, h1 = len(array[0]), len(array)
    ratio = h1 / float(w1)
    if ratio > 0.4 and ratio < 0.6:
        ratio_list.append(loc)



# NEXT, we threshold the image, and
# label the components.
# If the bounding box has a lot of different connected
# components along the horizontal line dividing the plate into
# top and bottom halves, then those components
# are likely to be letters, meaning that the
# box is likely to be a license plate.

# threshold the image
#threshold = MAX_PIXEL * .25
#td = np.zeros((w, h))
#
#for x in range(0, w):
#    for y in range(0, h):
#        if img.item((x,y)) < threshold:
#            td.itemset((x,y), MAX_PIXEL)

MIN_SIZE = 1600
i = 0
# count the number of components along the middle horizontal line!
for loc in ratio_list:
    # target that satisfies ratio
    target = img[loc]
    w2, h2 = target.shape[1], target.shape[0]
    middle_h = h2 / 2

    # if min_size is not satisfied, skip
    if target.size < MIN_SIZE:
        continue


    #compute threshold
    thresh = 0
    for val in range(0, w2):
        thresh += target[middle_h][val]
    thresh /= w2

    # threshold the middle thirds height of the image
    # and the middle half of width of image
    middle_third = target[(h2/3):(h2/3*2),(w2/8):(w2/8*7)]
    w3, h3 = middle_third.shape[1], middle_third.shape[0]
    for val1 in range(0, h3):
        for val2 in range(0, w3):
            if middle_third.item((val1, val2)) < thresh:
                middle_third.itemset((val1, val2), MAX_PIXEL)
            else:
                middle_third.itemset((val1,val2), 0)


    cv2.imwrite('data' + str(i) + '.png', middle_third)
    i += 1

    # label this third
    comps, num = ndimage.label(middle_third)

    # look at number of unique labels along the middle
    comp_height = len(comps)

    num = len(set(comps[comp_height/2]))

    if num > 3 and num < 8:
        results.append(loc)



# PRINT OUT RESULTS.
num = len(results)
if num == 0:
    print "NO PLATE FOUND."
else:
    i = 1
    for loc in results:
        cv2.imwrite('output' + str(i) + '.png', img_rgb[loc])
        i += 1
    print "SUCCESS!"
    print str(num) + " PLATE(S) FOUND!"

cv2.imwrite('edges.png', edges)



