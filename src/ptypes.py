#-------------------------------------------------------------------------------
# Python types.
#-------------------------------------------------------------------------------


# type variable
class pVar():
    def __str__(self):
        return 'var'

# pNone
class pNone():
    def __str__(self):
        return 'None'

# PyObject
class pObject(object):
    def __str__(self):
        return 'object'

# Long
class pInt(int):
    def __str__(self):
        return 'int'

# Bytes
class pBytes(bytes):
    def __str__(self):
        return 'bytes'

# List
## list
## array: a list of numeric
class pList(list):
    def __str__(self):
        return 'list'

# bool
class pBool(object):
    def __str__(self):
        return 'bool'


# instance a pType with a name string
def newPType(name):
    t = pObject
    if name == 'Long':
        t = pInt
    elif name == 'Bytes':
        t = pBytes
    elif name == 'List' or name == 'Array':
        t = pList
    elif name == 'Object':
        t = pObject
    else:
        print(name)
    return t


# PyT_FromT2 -> T
def getPTypeFromTrans(api):
    if api.find('_From') != -1:
        tText = api[2:api.find('_From')]
    else:
        tText = api[2:api.find('_New')]

    t = newPType(tText)
    return t


# PyObject -> object
# PyArrayObject -> list
def getPTypeFromName(api):
    if api.find('Py') != -1:
        t = api[api.find('Py') + 2:]
        if t != 'Object':
            t = t[:t.find('Object')]
    else:
        t = api
    return newPType(t)


if __name__ == '__main__':
    print(pNone())
    print(pObject())
    print(pInt())
    print(getPTypeFromName('PyArrayObject')())