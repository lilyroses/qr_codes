from PIL import Image


def create_bitmap(size, img_name):
    img = Image.new("L", size, color=255)
    pixels = img.load()
    img.save(img_name)
    print(f"{img_name} created")
