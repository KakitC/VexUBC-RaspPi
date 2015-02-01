# Jan 21 2014

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

def colorCOMfinder(hlsTarget, testPic, hlsThresh=(20,50,50), show=False):
    """Finds the center of mass of a color in testPic and shows a new
       picture of the target colors grayed out and marked with a cross.

       Targets high saturation colors. Image must be a RGB, or
       RGBA format (png, jpg, etc.)

       Arguements:
       hslTarget - <3-tuple> HSL value (0-255) to search for
       testPic - <Image> to locate a color mass
       hslThresh - <3-tuple> Threshold range for picking out target color
       """

    cross = img.open('Black cross 64.png')

    hTarg, lTarg, sTarg = hlsTarget
    hThresh, lThresh, sThresh = hlsThresh

    comx = 0
    comy = 0
    count = 0

    data = np.array(testPic)

    # [H x W x RGB] image data array
    # TODO optimize processing speed, or parallelize or something - it's slow
    for i in range(len(data)):
        for j in range(len(data[i])):
            hls = RGB_HLS(tuple(data[i,j]))
            
            if (hue_compare(hls[0],hTarg,hThresh) and 
                (abs(hls[1] - lTarg) < lThresh) and
                (abs(hls[2] - sTarg) < sThresh)):
                   if len(data[i,j]) == 3: data[i,j] = [127,127,127] 
                   elif len(data[i,j]) == 4: data[i,j] = [127,127,127,255] 
                   comx = comx + j
                   comy = comy + i
                   count = count + 1
                       
    # TODO Make it if only a contiguous blob
    # of the color, not just min number of pixels
    if count > 10: 
        comx = round(comx/count)
        comy = round(comy/count)

        if show:
            box_corner = (comx - round(cross.size[0]/2),comy - round(cross.size[1]/2))
            mod = img.fromarray(data)
            mod.paste(cross,box_corner,cross)
            mod.show()
        
    else: print("None of that color found")

