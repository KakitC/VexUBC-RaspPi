import time
from PIL import Image as img
from colorCOMfinder04 import *

# Unit tests
teal, teal_rgb = (127, 127, 255), (0, 255, 255)
green, green_rgb = (85, 127, 255), (0, 255, 0)
blue, blue_rgb = (170, 127, 255), (0, 0, 255)
gray, gray_rgb = (0, 127, 0), (127, 127, 127)
greengray, greengray_rgb = (85, 191, 255), (127, 255, 127)
white, white_rgb = (0, 255, 0), (255, 255, 0)
whiteish, whiteish_rgb = (0, 230, 0), (230, 230, 230)
red, red_rgb = (0, 127, 255), (255, 0, 0)
picky, loose = (15, 20, 20), (40, 50, 80)

# Pixel color match checking
assert pixel_compare(green_rgb, gen_rgb_range(green, picky))
assert not pixel_compare(green_rgb, gen_rgb_range(teal, picky))
assert not pixel_compare(greengray_rgb, gen_rgb_range(green, picky))
assert not pixel_compare(green_rgb, gen_rgb_range(greengray, picky))
assert not pixel_compare(gray_rgb, gen_rgb_range(white, picky))
assert not pixel_compare(whiteish_rgb, gen_rgb_range(white, picky))
assert pixel_compare(whiteish_rgb, gen_rgb_range(white, loose))

# Time testing
t0 = time.time()
arr = gen_rgb_range(white,picky)
for i in range(100000): pixel_compare(gray_rgb, arr)
print("100000 pixel_compare()'s takes", time.time() - t0, "seconds.")

t0 = time.time()
for i in range(10): gen_px_list((160,120))
print("Generating pixel search list takes", (time.time() - t0) / 10, "seconds")

# Functionality tests
test_suite = [4]

# look for red in testColors pics
if 1 in test_suite:    
    file_colors = ['testColor' + str(x+1) + '.png' for x in range(4)]
    for filename in file_colors:
        print(filename)
        t0 = time.time()
        print(color_com_finder(img.open(filename), red, show_flag=True))
        print(time.time() - t0)

# look for red-ish in testImg pics
if 2 in test_suite:
    file_imgs = ['testImg' + str(x+1) + '.png' for x in range(3)]
    for filename in file_imgs:
        print(filename)
        t0 = time.time()
        print(color_com_finder(img.open(filename), red, picky, show_flag=True))
        print(time.time() - t0)

# look for red in testPic photos    
if 3 in test_suite:
    file_pics = ['testPic' + str(x+1) + '.jpg' for x in range(5)]
    for filename in file_pics:
        print(filename)
        t0 = time.time()
        print(color_com_finder(img.open(filename), red,
                               (15, 30, 30), show_flag=True))
        print(time.time() - t0)

# Performance testing on lower res pics
if 4 in test_suite:
    file_pics_small = ['testPic' + str(x+1) + 'small.jpg' for x in range(5)]
    for filename in file_pics_small:
        print(filename)
        pic = img.open(filename)
        print(color_com_finder(pic, red,
                               (15, 30, 30), show_flag=True))

        n = 5
        t0 = time.time()
        for i in range(n):
            color_com_finder(pic, red,
                               (15, 30, 30), show_flag=False)
        print((time.time() - t0) / n)
