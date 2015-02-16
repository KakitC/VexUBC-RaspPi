import picamera as pic
from PIL import Image as img
import numpy as np
import time
from colorCOMfinder import colorCOMfinder05 as comf5


def run():
    res = (80, 60)
    red, red_rgb = (0, 127, 255), (255, 0, 0)
    thresh = (15, 30, 30)

    with pic.PiCamera() as cam:
        cam.resolution = res
        cam.start_preview()

        o = np.zeros((res[1], res[0], 3), dtype=np.uint8)
        o[40, :, :] = 0xff
        omg = img.fromarray(o)
        opad = img.new('RGB', (
             ((res[0] + 31) // 32) * 32,
             ((res[1] + 15) // 16) * 16))
        opad.paste(omg, (0,0))
        olay = cam.add_overlay(opad.tostring(), size=omg.size,
                               layer=3, alpha=64)

        try:
            while True:
                for i in range(res[1])[::-1]:
                    o = np.zeros((res[1], res[0], 3), dtype=np.uint8)
                    o[i, :, :] = 0xff
                    omg = img.fromarray(o)
                    opad = img.new('RGB', (
                         ((res[0] + 31) // 32) * 32,
                         ((res[1] + 15) // 16) * 16))
                    opad.paste(omg, (0,0))
                    olay.update(opad.tostring())
                    time.sleep(.2)
        finally:
            cam.remove_overlay(olay)
