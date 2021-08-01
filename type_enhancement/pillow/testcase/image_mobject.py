from PIL import Image

path=''
image = Image.open(path)
pw, ph = image.size
x_alpha = 1
y_alpha = 1
rgb = image.getpixel((
    int((pw - 1) * x_alpha),
    int((ph - 1) * y_alpha),
))