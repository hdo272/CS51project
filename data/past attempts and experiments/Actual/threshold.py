import cv2
import numpy as np
import math
import sys
from scipy import ndimage


img_rgb = cv2.imread(sys.argv[1])
print img_rgb.shape
img = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
h, w = img.shape[0], img.shape[1]

middle_h = h / 2
total = 0
avg = 0
MAX_PIXEL = 255



for x in range(0, w):
    avg += img.item((middle_h, x))
avg /= w



for x in range(0, w):
    for y in range(0, h):
        if img.item((y,x)) < avg:
            img.itemset((y,x), MAX_PIXEL)
            if y == middle_h:
                total += MAX_PIXEL
        else:
            img.itemset((y,x), 0)


# start at middle; go up
up_bound = 0
down_bound = 0
for y in range(middle_h, h):
    row = 0
    for x in range(0, w):
        row += img.item((y, x))
    if row < total * .3 or row > total * 1.7:
        up_bound = y
        break

reversed_range = reversed(range(0, middle_h))

for y in reversed_range:
    row = 0
    for x in range(0, w):
        row += img.item((y, x))
    if row < total * .3 or row > total * 1.7:
        down_bound = y
        break

cut_image = img[down_bound:up_bound]
new_w, new_h = cut_image.shape[1], cut_image.shape[0]
min_size = 30
min_width = .05 * new_w
min_height = .25 * new_h
comps, num = ndimage.label(cut_image)


for label in range(1, num + 1):
    # note: loc is a slice object, which is annoying
    loc = ndimage.find_objects(comps == label)[0]
    array = cut_image[loc]

    if (array.size < min_size
            or array.shape[0] < min_height
            # if the width is really small, then it better be an i
            or (array.shape[1] < min_width and
                np.count_nonzero(array) < .9 * array.size)
            # if it's files the entire height and left/right boundaries, delete.
            or (array.shape[0] == new_h and
                    (comps[0][0] == label
                        or comps[0][new_w-1] == label))):
        cut_image[loc] = 0





cv2.imwrite('threshed_cut.png', cut_image)
cv2.imwrite('threshed.png', img)



img2 = cut_image
h, w = img2.shape[0], img2.shape[1]
bar = np.zeros(w)
widths = []

for x in range(0, w):
    darkpix = 0
    for y in range(0, h):
        curr_pixel = img2.item((y, x))
        if curr_pixel > 250:
            darkpix += 1
    bar.itemset(x, darkpix)


num = len(bar)
begin = -1
empty_thresh = 4

for z in range(0, num):
    if bar[z] <= empty_thresh and begin != -1 and z - begin > min_width:
        widths.append((begin, z))
        begin = -1
    elif bar[z] > empty_thresh and begin == -1:
        begin = z

# each letter is from begin...z-1

wnum = len(widths)
for i in range(0, wnum):
    b, e = widths[i][0], widths[i][1]
    cut = img2[:,b:e]
    cv2.imwrite('cut' + str(i) + '.png', cut)

