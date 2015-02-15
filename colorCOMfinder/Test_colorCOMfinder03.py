import time
from PIL import Image as img
from colorCOMfinder03 import *


testSuite = (4,)

# look for red in testColors pics
if 1 in testSuite:    
    fileColors = ['testColor' + str(x+1) + '.png' for x in range(4)]
    for filename in fileColors:
        print(filename)
        t0 = time.time()
        colorCOMfinder((0,127,255), img.open(filename), show=True)
        print(time.time() - t0)

# look for red-ish in testImg pics
if 2 in testSuite:
    fileImgs = ['testImg' + str(x+1) + '.png' for x in range(3)]
    for filename in fileImgs:
        print(filename)
        t0 = time.time()
        colorCOMfinder((0,127,255), img.open(filename), (40,50,80), show=True)
        print(time.time() - t0)

# look for red in testPic photos    
if 3 in testSuite:
    filePics = ['testPic' + str(x+1) + '.jpg' for x in range(4)]
    for filename in filePics:
        print(filename)
        t0 = time.time()
        colorCOMfinder((0,127,255), img.open(filename), (15,50,120), show=True)
        print(time.time() - t0)

# Performance testing on lower res pics
if 4 in testSuite:
    filePics = ['testPic' + str(x+1) + 'small.jpg' for x in range(5)]
    for filename in filePics:
        print(filename)
        t0 = time.time()
        colorCOMfinder((0, 127, 255), img.open(filename), (15, 50, 120))
        print(time.time() - t0)

