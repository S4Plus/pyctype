from PIL import Image

import numpy
from numpy import (amin, amax, ravel, asarray, arange, ones, newaxis,
                   transpose, iscomplexobj, uint8, issubdtype, array)


pillow_installed = True
PILLOW_ERROR_MESSAGE = (
    "The Python Imaging Library (PIL) is required to load data "
    "from jpeg files. Please refer to "
    "https://pillow.readthedocs.io/en/stable/installation.html "
    "for installing PIL."
)
_errstr = "Mode is unknown or incompatible with input array shape."
__all__ = ['bytescale', 'imread', 'imsave', 'fromimage', 'toimage', 'imresize']

arr = []
high=255
low=0
cmin=None
cmax=None
pal=True
mode=None
channel_axis=None

if not pillow_installed:
    raise ImportError(PILLOW_ERROR_MESSAGE)

data = asarray(arr)
if iscomplexobj(data):
    raise ValueError("Cannot convert a complex-valued array.")
shape = list(data.shape)
valid = len(shape) == 2 or ((len(shape) == 3) and
                            ((3 in shape) or (4 in shape)))
if not valid:
    raise ValueError("'arr' does not have a suitable array shape for "
                        "any mode.")
if len(shape) == 2:
    shape = (shape[1], shape[0])  # columns show up first
    data32 = data.astype(numpy.float32)
    image = Image.frombytes(mode, shape, data32.tobytes())
    v1 = image
    bytedata = bytescale(data, high=high, low=low,
                            cmin=cmin, cmax=cmax)
    image = Image.frombytes('L', shape, bytedata.tobytes())
    v6 = image.putpalette(asarray(pal, dtype=uint8).tobytes())
    # Becomes a mode='P' automagically.
    pal = (arange(0, 256, 1, dtype=uint8)[:, newaxis] *
            ones((3,), dtype=uint8)[newaxis, :])
    v7 = image.putpalette(asarray(pal, dtype=uint8).tobytes())
    v2 = image
    bytedata = (data > high)
    image = Image.frombytes('1', shape, bytedata.tobytes())
    v3 = image
    if cmin is None:
        cmin = amin(ravel(data))
    if cmax is None:
        cmax = amax(ravel(data))
    data = (data*1.0 - cmin)*(high - low)/(cmax - cmin) + low
    if mode == 'I':
        data32 = data.astype(numpy.uint32)
        image = Image.frombytes(mode, shape, data32.tobytes())
    else:
        raise ValueError(_errstr)
    v4 = image

# if here then 3-d array with a 3 or a 4 in the shape length.
# Check for 3 in datacube shape --- 'RGB' or 'YCbCr'
if channel_axis is None:
    if (3 in shape):
        ca = numpy.flatnonzero(asarray(shape) == 3)[0]
    else:
        ca = numpy.flatnonzero(asarray(shape) == 4)
        if len(ca):
            ca = ca[0]
        else:
            raise ValueError("Could not find channel dimension.")
else:
    ca = channel_axis

numch = shape[ca]
if numch not in [3, 4]:
    raise ValueError("Channel axis dimension is not valid.")

bytedata = bytescale(data, high=high, low=low, cmin=cmin, cmax=cmax)
if ca == 2:
    strdata = bytedata.tobytes()
    shape = (shape[1], shape[0])
elif ca == 1:
    strdata = transpose(bytedata, (0, 2, 1)).tobytes()
    shape = (shape[2], shape[0])
elif ca == 0:
    strdata = transpose(bytedata, (1, 2, 0)).tobytes()
    shape = (shape[2], shape[1])
if mode is None:
    if numch == 3:
        mode = 'RGB'
    else:
        mode = 'RGBA'

if mode not in ['RGB', 'RGBA', 'YCbCr', 'CMYK']:
    raise ValueError(_errstr)

if mode in ['RGB', 'YCbCr']:
    if numch != 3:
        raise ValueError("Invalid array shape for mode.")
if mode in ['RGBA', 'CMYK']:
    if numch != 4:
        raise ValueError("Invalid array shape for mode.")

# Here we know data and mode is correct
image = Image.frombytes(mode, shape, strdata)
v5 = image