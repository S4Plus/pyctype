import array

# array.array.__deepcopy__
# /Users/hmz/Projects/Python/Python-3.6.11/Modules/arraymodule.c
# METH_O + PyObject *unused
a = array.array('b',  [ord('g'), ord('e'), ord('e'), ord('k')])
print(a.__deepcopy__('str'))
print(a.__deepcopy__(1))
print(a.__deepcopy__([1,'str']))