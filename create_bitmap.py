from PIL import Image

size = (21,21)

img = Image.new("L", size, color=255)

pixels = img.load()

img.save("test.bmp")