from PIL import Image


image_width = 800
image_height = 600

img = Image.new("RGB", (image_width, image_height))
pixels = img.load()
v2 = img.show()