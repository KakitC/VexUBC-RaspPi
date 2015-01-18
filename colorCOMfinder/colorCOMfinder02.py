# Jan 17 2014
# Finds center of mass for a given color in a test image
# Uses HLS coordinates for threshold value
# Targets high saturation, mid lumosity colors

import numpy as np
from PIL import Image as img
from colorsys import *


def RGB_HLS(RGB):
    """Turns a 0-255 RGB 3-tuple into an HSL 3-tuple"""
    RGBnorm = [x/255 for x in RGB]
    HLSnorm = rgb_to_hls(RGBnorm[0],RGBnorm[1],RGBnorm[2])
    HLS = tuple(255*x for x in HLSnorm)
    return HLS

def hue_compare(hue,target,thresh):
    """Compares a given hue to the target hue within
    a threshold, on a circular color wheel"""
    comp = abs(hue - target)
    if comp < thresh:
        return True
    elif hue > (target - thresh + 255):
        return hue_compare(hue - 255, target, thresh)
    elif hue < (target + thresh - 255):
        return hue_compare(hue + 255, target, thresh)
    else:
        return False


cross = img.open('Black cross 60.png')
test = img.open('testColors.png')

hTarget = 127
lTarget = 127
sThresh = 200 # above sThresh saturation

hThresh = 30 # within hThresh of hTarget hue
lThresh = 30 # within lThresh of lTarget lumosity


comx = 0
comy = 0
count = 0

data = np.array(test)

# [H x W x RGB] image data array
for i in range(len(data)):
    for j in range(len(data[i])):
        hls = RGB_HLS(tuple(data[i,j]))
        
        if (hue_compare(hls[0],hTarget,hThresh) and 
            (abs(hls[1] - lTarget) < lThresh) and
            (hls[2] > sThresh)):
               data[i,j] = [127,127,127]
               comx = comx + j
               comy = comy + i
               count = count + 1
                   
# TODO Make it if only a contiguous blob
# of the color, not just min number of pixels
if count > 10: 
    comx = round(comx/count)
    comy = round(comy/count)
    boxCorner = (comx - round(cross.size[0]/2),comy - round(cross.size[1]/2))

    mod = img.fromarray(data)
    mod.paste(cross,boxCorner,cross)
    mod.show()
    
else: print("None of that color found")

