# PyCType

This project is a static type inference tool for foreign functions of Python, 
which is proposed in paper:
**Static Type Inference for Foreign Functions of Python**.
This tool is developed by [Mingzhe Hu](https://www.mingzhehu.cn) 
under the guidance of Prof. [Yu Zhang](http://staff.ustc.edu.cn/~yuzhang/) 
in the [S4Plus](https://s4plus.ustc.edu.cn) team 
of [USTC](https://www.ustc.edu.cn).

If you use PyScan in your research, please cite our paper as follows:

```
@inproceedings{hu2021pyctype,
    title = {Static Type Inference for Foreign Functions of Python},
    author = {Hu, Mingzhe and Zhang, Yu and Huang, Wenchao and Xiong, Yan},
    booktitle = {32nd International Symposium on Software Reliability Engineering (ISSRE 2021)},
    month = {October},
    year = {2021},
    organization = {IEEE},
    pages = {?},
}
```

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

## License

This project is licensed under [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0).