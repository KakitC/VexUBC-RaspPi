# Test script sandbox
import numpy as np
from PIL import Image as img

cross = img.open('Black cross 60.png')
test = img.open('testColors.png')

rThresh = [200,100,100]
cThresh = [100,200,200]


comx = 0
comy = 0
count = 0

data = np.array(test)
flag = 'green'

for i in range(len(data)):
    for j in range(len(data[i])):
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
                   

if count > 0:
    comx = round(comx/count)
    comy = round(comy/count)
    boxCorner = (comx - round(cross.size[0]/2),comy - round(cross.size[1]/2))

    modTest = img.fromarray(data)
    modTest.paste(cross,boxCorner,cross)
    modTest.show()
else: print("None of that color found")
