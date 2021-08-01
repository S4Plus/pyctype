import numpy as np


# This is a correct case, in which you cannot pass anything to copy(), 
# otherwise you will get a TypeError at compile time.

# numpy.nditer.copy()
x = np.arange(10)
y = x + 1
it = np.nditer([x, y])
next(it)
it2 = it.copy()
next(it2)


# The following are wrong cases.

# numpy.flatiter.__array__()
# METH_VARARGS + NPY_UNUSED
x = np.arange(6).reshape(2, 3)
fl = x.flat
fl.__array__(1, "str")

# numpy.ndarray.__reduce__()
# METH_VARARGS + NPY_UNUSED
# https://numpy.org/doc/stable/reference/generated/numpy.ndarray.__reduce__.html
x = np.arange(6)
x.__reduce__(1, "str")

# numpy.ndarray.__complex__()
# METH_VARARGS + NPY_UNUSED
# https://numpy.org/doc/stable/reference/generated/numpy.ndarray.__complex__.html
x = np.arange(1) # TypeError: only length-1 arrays can be converted to Python scalars
x.__complex__(1, "str")

# numpy.dtype.__reduce__()
# METH_VARARGS + NPY_UNUSED
# https://numpy.org/doc/stable/reference/generated/numpy.dtype.__reduce__.html
dt = np.dtype('>i4')
dt.__reduce__(1, "str")

# numpy.nditer.__exit__()
# METH_VARARGS + NPY_UNUSED
x = np.arange(6).reshape(2, 3)
with np.nditer(x, op_flags=['readwrite']) as it:
    it.__exit__(1, "str")

# numpy.nditer.close()
# METH_VARARGS + no args parameter
# https://numpy.org/doc/stable/reference/generated/numpy.nditer.close.html
x = np.arange(6).reshape(2, 3)
with np.nditer(x, op_flags=['readwrite']) as it:
    it.close(1, "str")
    for x in it:
        x[...] = 2 * x
