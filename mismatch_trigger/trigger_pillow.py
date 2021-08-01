from PIL import Image


# ImagingCore.split()
# METH_VARARGS + args not used
im = Image.open("./test.png")
ic = im.getdata()
ic.split('str', 1)

# ImagingCore.isblock()
# METH_VARARGS + args not used
im = Image.open("./test.png")
ic = im.getdata()
ic.isblock('str', 1)

# ImagingCore.getbbox()
# METH_VARARGS + args not used
im = Image.open("./test.png")
ic = im.getdata()
ic.getbbox('str', 1)

# ImagingCore.chop_invert()
# METH_VARARGS + args not used
im = Image.open("./test.png")
ic = im.getdata()
ic.chop_invert('str', 1)

# ImagingCore.getextrema()
# METH_VARARGS + args not used
im = Image.open("./test.png")
ic = im.getdata()
ic2 = ic.convert("L") # RGB (3x8-bit pixels, true color) -> L (8-bit pixels, black and white)
ic2.getextrema('str', 1)

# ImagingCore.getpalettemode()
# METH_VARARGS + args not used
im = Image.open("./test.png")
ic = im.getdata()
ic2 = ic.convert("P") # P (8-bit pixels, mapped to any other mode using a color palette)
ic2.getpalettemode('str', 1)

# ImagingCore.getprojection()
# METH_VARARGS + args not used
im = Image.open("./test.png")
ic = im.getdata()
ic.getprojection('str', 1)


# TODO How to get an object of the class?
# ImagingEncoder.cleanup()
# ImagingEncoder.encode_to_pyfd()
# ImagingDecoder.cleanup()