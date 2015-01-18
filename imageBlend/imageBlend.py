# Creates a horrifying image

from PIL import Image as img

old = img.open('old.jpg')
new = img.open('baby.jpg')

weird = img.blend(old,new,0.5)
weird.show()
