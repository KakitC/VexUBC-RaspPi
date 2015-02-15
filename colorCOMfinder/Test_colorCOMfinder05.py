import time
from PIL import Image as Img
import colorCOMfinder05 as Comf


def test_out(pic, com, save_name):
    """ Display a copy of the input picture with the target color marked
        with a cross.

        Doesn't run if there is none of that color in the picture.

        Args:
            pic_data: <Array> Modified image data from search result
            com: <2-tuple> x-y coordinates of center of mass of target
        Returns:
            None
       """

    cross = Img.open('Black cross 64.png')
    box_corner = (com[0] - round(cross.size[0]/2),
                  com[1] - round(cross.size[1]/2))
    pic.paste(cross, tuple(box_corner), cross)
    pic.save(save_name)

# Test colors
teal, teal_rgb = (127, 127, 255), (0, 255, 255)
green, green_rgb = (85, 127, 255), (0, 255, 0)
blue, blue_rgb = (170, 127, 255), (0, 0, 255)
gray, gray_rgb = (0, 127, 0), (127, 127, 127)
greengray, greengray_rgb = (85, 80, 175), (150, 200, 150)
white, white_rgb = (0, 255, 0), (255, 255, 0)
whiteish, whiteish_rgb = (0, 200, 0), (205, 205, 205)
red, red_rgb = (0, 127, 255), (255, 0, 0)
picky, loose = (15, 30, 50), (40, 50, 80)

# Pixel color match checking
assert Comf._pixel_compare(green_rgb, Comf.gen_rgb_range(green, picky))
assert not Comf._pixel_compare(green_rgb, Comf.gen_rgb_range(teal, picky))
assert not Comf._pixel_compare(greengray_rgb, Comf.gen_rgb_range(green, picky))
assert not Comf._pixel_compare(green_rgb, Comf.gen_rgb_range(greengray, picky))
assert not Comf._pixel_compare(gray_rgb, Comf.gen_rgb_range(white, picky))
assert not Comf._pixel_compare(whiteish_rgb, Comf.gen_rgb_range(white, picky))
assert Comf._pixel_compare(whiteish_rgb, Comf.gen_rgb_range(white, loose))

# Time testing
t0 = time.time()
arr = Comf.gen_rgb_range(white,picky)
for i in range(100000): Comf._pixel_compare(white_rgb, arr)
print("10000 pixel_compare()'s takes", (time.time() - t0) / 10, "seconds.")

t0 = time.time()
for i in range(10):
    Comf.gen_px_list((160, 120))
print("Generating pixel search list takes", (time.time() - t0) / 10, "seconds")

test_suite = [1,2,3]


# look for red in testPic photos    
if 1 in test_suite:
    file_pics = ['testPic' + str(x+1) + '.jpg' for x in range(5)]
    for filename in file_pics:
        test_pic = Img.open(filename)
        res = test_pic.size
        print(filename, " Resolution:", res)

        search_list = Comf.gen_px_list(res)
        target = Comf.gen_rgb_range(red, picky)

        t0 = time.time()
        coords = Comf.color_com(test_pic, target, search_list)
        print(time.time() - t0)

        print(coords)
        test_out(test_pic, coords, "testOut_" + filename)


# Performance testing on lower res pics
if 2 in test_suite:
    file_pics = ['testPic' + str(x+1) + 'small.jpg' for x in range(5)]
    for filename in file_pics:
        test_pic = Img.open(filename)
        res = test_pic.size
        print(filename, " Resolution:", res)

        search_list = Comf.gen_px_list(res)
        target = Comf.gen_rgb_range(red, picky)

        n = 5
        t0 = time.time()
        for i in range(n):
            coords = Comf.color_com(test_pic, target, search_list)
        print("Time taken:", (time.time() - t0) / n)
        print(coords)

# Performance testing on even lower res pics
if 3 in test_suite:
    file_pics = ['testPic' + str(x+1) + 'smaller.jpg' for x in range(5)]
    for filename in file_pics:
        test_pic = Img.open(filename)
        res = test_pic.size
        print(filename, " Resolution:", res)

        search_list = Comf.gen_px_list(res)
        target = Comf.gen_rgb_range(red, picky)

        n = 5
        t0 = time.time()
        for i in range(n):
            coords = Comf.color_com(test_pic, target, search_list)
        print("Time taken:", (time.time() - t0) / n)
        print(coords)
