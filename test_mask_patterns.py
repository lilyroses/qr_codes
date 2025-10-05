from mask_patterns import *
from PIL import Image

size = (21,21)
img = Image.new("L", size, color=255)
pixels = img.load()
img_name = "mask_0.bmp"
img.save(img_name)
# 
print(f"{img_name} created")

for row in range(size[0]):
    for col in range(size[1]):
        bit = pixels[column, row]
        
        if pixels[column, row] ==
print(pixels)