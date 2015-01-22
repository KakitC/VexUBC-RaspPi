from colorCOMfinder03 import *
from PIL import Image as img

# TODO time performance of each colorCOMfinder call and compare against img size

testSuite = (3,)

# look for red in testColors pics
if 1 in testSuite:    
    fileColors = ['testColor' + str(x+1) + '.png' for x in range(4)]
    for filename in fileColors:
        print(filename)
        colorCOMfinder((0,127,255), img.open(filename))

# look for red-ish in testImg pics
if 2 in testSuite:
    fileImgs = ['testImg' + str(x+1) + '.png' for x in range(3)]
    for filename in fileImgs:
        print(filename)
        colorCOMfinder((0,127,255), img.open(filename), (40,50,80))

# look for red in testPic photos    
if 3 in testSuite:
    filePics = ['testPic' + str(x+1) + '.jpg' for x in range(4)]
    for filename in filePics:
        print(filename)
        colorCOMfinder((0,127,255), img.open(filename), (15,40,120))
