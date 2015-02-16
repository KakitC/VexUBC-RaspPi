import picamera as pic
from PIL import Image as img
import numpy as np
import time
from ..colorCOMfinder import colorCOMfinder05 as comf5


def run():
    res = (80, 60)
    red, red_rgb = (0, 127, 255), (255, 0, 0)
    thresh = (15, 30, 30)

    with pic.PiCamera() as cam:
        cam.resolution = res
        cam.start_preview()

        o = np.zeros((res[0], res[1], 3), dtype=np.uint8)

        olay = cam.add_overlay(np.getbuffer(o), layer=3, alpha=64)
        try:
            while True:
                for i in range(res[0]-3):
                    o = np.zeros((res[0], res[1], 3), dtype=np.uint8)
                    o[i:i+3, :, :] = 255
                    olay.update(np.getbuffer(o))
                    time.sleep(.2)
        finally:
            cam.remove_overlay(olay)