from PIL import Image
from io import BytesIO
import logging

logger = logging.getLogger(__name__)
img_bytes = ''
cls = ''
crop=True
output= "png"
thumb_size= None

img1 = Image.open('')
logger.debug("Selenium image size: %s", str(img1.size))
if crop and img1.size[1] != cls.window_size[1]:
    desired_ratio = float(cls.window_size[1]) / cls.window_size[0]
    desired_width = int(img1.size[0] * desired_ratio)
    logger.debug("Cropping to: %s*%s", str(img1.size[0]), str(desired_width))
    img = img1.crop((0, 0, img.size[0], desired_width))
logger.debug("Resizing to %s", str(thumb_size))
img2 = img1.resize(thumb_size, Image.ANTIALIAS)
new_img = BytesIO()
if output != "png":
    img3 = img2.convert("RGB")
v1 = img3.save(new_img, output)
v2 = new_img.seek(0)
v3 = new_img.read()