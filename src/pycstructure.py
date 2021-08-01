#-------------------------------------------------------------------------------
# Python/C API structures.
#
# Modeled after:
#   - CPython's own C-API documentation
#   - CPython source code
#   - some utilities we add
#-------------------------------------------------------------------------------


# Structure used to describe an extension method.
#
# Ref: https://docs.python.org/3/c-api/structures.html#c.PyMethodDef
#
# ml_name: name of the method
# ml_meth: pointer to the C implementation
# ml_flag: flag bits indicating how the call should be constructed
#   METH_VARARGS    0x0001
#   METH_KEYWORDS   0x0002
#   METH_FASTCALL   0x0080
#   METH_METHOD     ?
#   METH_NOARGS     0x0004
#   METH_O          0x0008
#   METH_CLASS      0x0010
#   METH_STATIC     0x0020
#   METH_COEXIST    0x0040
# c_impl:  C implementation (function declaration)
class PyMethodDef:
    def __init__(self, ml_name, ml_meth, ml_flag):
        # Constant
        self.ml_name = ml_name
        # ID
        self.ml_meth = ml_meth
        # Constant
        self.ml_flag = ml_flag
        # FuncDef
        # may defined in another file
        self.c_impl = None
        # parameter polymerizing Python argument(s) is not used in c_impl
        self.param_unused = False

    def __str__(self):
        c_impl_coord = " ({})".format(
            self.c_impl.coord) if self.c_impl else ""
        output = "{} -> {}{}".format(
            self.ml_name.value[1:-1], self.ml_meth.name, c_impl_coord)
        return output


# Python/C API for argument parsing
# If PY_SSIZE_T_CLEAN is defined, treats #-specifier to mean Py_ssize_t,
# then `api` will be resolved as `_api_SizeT`.

# (PyObject *args, const char *format, ...) or
# (PyObject *args, const char *format, va_list vargs)
PCAPI_AP_POS = [
    'PyArg_Parse',
    'PyArg_ParseTuple',
    'PyArg_VaParse',
    '_PyArg_Parse_SizeT',
    '_PyArg_ParseTuple_SizeT',
    '_PyArg_VaParse_SizeT',
]

# (PyObject *args, PyObject *kw, const char *format, char *keywords[], ...) or
# (PyObject *args, PyObject *kw, const char *format, char *keywords[], 
#   va_list vargs)
# Since version 3.6: Empty names denote positional-only parameters.
PCAPI_AP_KWD = [
    'PyArg_ParseTupleAndKeywords',
    'PyArg_VaParseTupleAndKeywords',
    '_PyArg_ParseTupleAndKeywords_SizeT',
    '_PyArg_VaParseTupleAndKeywords_SizeT',
]


# Python/C API for building value
PCAPI_BV = [
    'Py_BuildValue',
    'Py_VaBuildValue',
    '_Py_VaBuildValue_SizeT',
    '_Py_BuildValue_SizeT'
]
