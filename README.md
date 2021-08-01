# PyCType

Static type inference for foreign functions of Python

## Usage

Enter the `src` folder, and run PyCType with:

```
python evaluate.py [-c CONFIG] project
```

`project` is the path of the project (or file) to be analyzed, `CONFIG` is an optional argument for specifying the compilation options to parse the project.
See `src/ppconfig.yml` for embedded compilation options of CPython3.6, NumPy, Pillow, and python-ldap.
**Absolute paths there should be replaced with yours.**
`src/preprocess.py` can be used to help configure new compilation options.

The following is an output snippet:

```
set_option -> l_ldap_set_option (/Users/hmz/Projects/python-ldap/Modules/functions.c:111:1)
iO:set_option
['int', 'object', []]
--->>>
['None', []]
```

The `->` line marks a map from Python foreign function name to its C implementation.
Following lines above `--->>>` are parameter type constraints of this foreign
function, lines below are return types.
