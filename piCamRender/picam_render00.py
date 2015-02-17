import picamera as pic
from PIL import Image as img
import numpy as np
import io
from colorCOMfinder import colorCOMfinder05 as comf5


def make_overlay(coords, res):
    """ Creates a padded image for overlaying the camera preview, with
        a dot marking the position of the target coordinates

        Params:
            coords - <2-tuple> Coordinates of target position in image
            res - <2-tuple> Camera resolution
        Returns:
            <Image> Image containing targeting dot, padded to overlay buffer size
    """

    o = np.zeros((res[1], res[0], 3), dtype=np.uint8)
    if 0 <= coords[0] < res[0] and 0 <= coords[1] < res[1]:
        o[coords[1], coords[0], :] = 0xff
    omg = img.fromarray(o)
    opad = img.new('RGB', (
             ((res[0] + 31) // 32) * 32,
             ((res[1] + 15) // 16) * 16))
    opad.paste(omg, (0, 0))
    return opad


def render_target():
    res = (80, 60)
    target_red = (0, 127, 255)
    thresh = (15, 30, 30)

    with pic.PiCamera() as cam:
        cam.resolution = res

        opad = make_overlay((-1, -1), res)
        olay = cam.add_overlay(opad.tostring(), size=(res[1], res[0], 3),
                               layer=3, alpha=96)
        stream = io.BytesIO()
        target_range = comf5.gen_rgb_range(target_red, thresh)
        px_search_list = comf5.gen_px_list(res)

        cam.start_preview()

        try:
            while True:
                cam.capture(stream, format='jpeg')
                stream.seek(0)
                image = img.open(stream)
                coords = comf5.color_com(image, target_range, px_search_list)
                opad = make_overlay(coords, res)
                olay.update(opad)
        finally:
            cam.remove_overlay(olay)
