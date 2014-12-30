import cv2
import numpy as np
import math
from scipy import ndimage
from PIL import ImageFilter
from PIL import Image
global ext


# works!

ext = ".jpg"

# open image
imageFile = "output1.png"
im1 = Image.open(imageFile)

# define the sharpen filter for the image
def filterSHARP(im):

    im1 = im.filter(ImageFilter.SHARPEN)

    im1.save("car11s" + ext)

filterSHARP(im1)
