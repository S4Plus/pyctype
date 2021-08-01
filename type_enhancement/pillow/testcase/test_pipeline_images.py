import io
from PIL import Image

SIZE = (100, 100)
COLOUR = (0, 127, 255)

format = 'JPEG'
a='RGB'
kw=SIZE, COLOUR

buf = ''
v1 = Image.new(*a, **kw)
v2 = v1.save(buf, format)
v3 = buf.seek(0)
v4 = Image.open(buf)