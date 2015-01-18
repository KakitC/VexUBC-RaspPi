import io
import numpy as np
from PIL import Image as img
import picamera as pic
from time import sleep
from colorsys import *

cross = img.open('Black cross 60.png')
flag = 'red'

# TODO update this to support HSL thresholds, preferably not hardcoded
rThresh = [200,100,100]
cThresh = [100,200,200]
res = (640,360)
stream = io.BytesIO()

with pic.PiCamera() as cam:
    cam.resolution = res
    cam.framerate = 24
    cam.start_preview()

    while True:
        comx = 0
        comy = 0
        count = 0
        cam.capture(stream, format='jpeg')

        data = np.fromstring(stream.getvalue(), dtype=np.uint8)

        # [H x W x RGB] image data array
        for i in range(len(data)):
            for j in range(len(data[i])):
                #RGB to HSL

                
                if flag == 'green':
                    if ((data[i,j,0] < cThresh[0]) and
                        (data[i,j,1] > cThresh[1]) and
                        (data[i,j,2] > cThresh[2])):
                           data[i,j] = [0,0,0]
                           comy = comy + i
                           comx = comx + j
                           count = count + 1
                if flag == 'red':    
                    if ((data[i,j,0] > rThresh[0]) and
                        (data[i,j,1] < rThresh[1]) and
                        (data[i,j,2] < rThresh[2])):
                           data[i,j] = [0,0,0]
                           comx = comx + j
                           comy = comy + i
                           count = count + 1
                           

        if count > 3:
            comx = round(comx/count)
            comy = round(comy/count)
            boxCorner = (comx - round(cross.size[0]/2),comy - round(cross.size[1]/2))
            
            overlay = img.new('RGBA', res,(0,0,0,0))
            overlay.paste(cross,boxCorner,cross)
            o = cam.add_overlay(overlay.tostring(), layer=3, alpha=255)
            cam.annotate_text = 'TARGET ACQUIRED'
            time.sleep(1)
            cam.remove_overlay(o)

        else:
            cam.annotate_text = 'TARGET NOT FOUND'
            time.sleep(1)
        
        
def RGB_HLS(RGB):
    "Turns a 0-255 RGB 3-tuple into an HSL 3-tuple"
    RGBnorm = [x/255 for x in RGB]
    HSLnorm = rgb_to_hls(RGBnorm[0],RGBnorm[1],RGBnorm[2])
    HSL = tuple(255*x for x in HSLnorm)

    
