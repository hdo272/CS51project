import cv2
import numpy as np
from matplotlib import pyplot as plt
from operator import itemgetter

# get the images
img_rgb = cv2.imread('res1.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
zero = cv2.imread('0.jpg',0)
one = cv2.imread('1.jpg',0)
w,h = zero.shape[::-1]

# pull the coordinates for one, zeros
res = cv2.matchTemplate(img_gray, zero, cv2.TM_CCOEFF_NORMED)
threshold = 0.53
loc = np.where( res >= threshold)
zero_pts = zip(*loc[::-1])

res2 = cv2.matchTemplate(img_gray, one, cv2.TM_CCOEFF_NORMED)
loc = np.where( res2 >= threshold )
one_pts = zip(*loc[::-1])

# define process list, which pulls x coordinates, deletes duplicates, and sorts
def processList(lst):
    only_xs = map(lambda (x,y): x, lst)
    averageout = map(lambda x: x / 20, only_xs)
    no_dup = list(set(averageout))
    return sorted(no_dup)

# process lists, pull lengths
lst1, lst2 = processList(zero_pts), processList(one_pts)
len1, len2 = len(lst1), len(lst2)

# loop through lists and add 0/1s as need be
mark1, mark2 = 0, 0
result = ""
while mark1 < len1 or mark2 < len2:
    if mark2 >= len2 or (mark1 < len1 and lst1[mark1] <= lst2[mark2]):
        result += "0"
        mark1 += 1
    else:
        result += "1"
        mark2 += 1

print result

for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

cv2.imwrite('resres.png',img_rgb)
