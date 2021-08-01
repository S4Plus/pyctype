import os
import time
import argparse

from pycparser import c_ast

import preprocess
import astvisitor
import pycstructure
import format_string_parser


ap = argparse.ArgumentParser()
ap.add_argument('project', help='project to be analyzed')
ap.add_argument('-c', '--config', 
    help='compilation options for specific project')
# ap.add_argument('-s', '--sources', 
#     help='source paths already given in a file')
args = ap.parse_args()


count_compilable = 0
count_wrapper = 0
count_wrapper_has_fmtstr = 0 # can have several fmtstr's in one wrapper function
count_wrapper_marked_noarg = 0
bugs_flag_mismatch = set()


start_time = time.time()


# project -> C source
sources = []
if os.path.isfile(args.project):
    sources.append(args.project)
else:
    for dir, subdirs, files in os.walk(args.project):
        for f in files:
            if f.endswith('.c'):
                sources.append(os.path.join(dir, f))


for s in sources:
    print(s)

    # C source -> ast
    # preprocess, parse
    ast = None
    try:
        ast = preprocess.cpp(s, args.config)
        count_compilable += 1
    except Warning as w:
        print(w)
    except Exception as e:
        print(e)
        print("[ERROR] Preprocess failed, fix compilation options.")
    if not ast:
        continue

    # ast -> pymethoddef-s array
    pymethoddef_visitor = astvisitor.PyMethodDefVisitor(s)
    pymethoddef_visitor.visit(ast)
    for method in pymethoddef_visitor.pymethoddefs:
        # pymethoddef -> C implementation (function declaration)
        funcdef_visitor = astvisitor.FuncDefVisitor(method.ml_meth.name)
        funcdef_visitor.visit(ast)

        # C implementation -> argument parsing Python/C API call
        funccall_visitor = astvisitor.FuncCallVisitor()
        if not funcdef_visitor.wrapper:
            continue
        funccall_visitor.visit(funcdef_visitor.wrapper[0])

        method.c_impl = funcdef_visitor.wrapper[0]
        print(method)
        count_wrapper += 1

        BUG_MSG = "[BUG] function declared without param or with unused param but ml_flag is not METH_NOARGS"

        if method.ml_flag.value != '0x0004' and method.ml_flag.value != '0x0010': # METH_NOARGS, * | METH_CLASS
            # check unused parameter in C implementation
            try:
                id_visitor = astvisitor.IDVisitor(funcdef_visitor.params[1].name)
                id_visitor.visit(method.c_impl.body)
                if not id_visitor.called:
                    method.param_unused = True
                    if funcdef_visitor.params[1].name.startswith('__NPY_UNUSED_TAGGED'):
                        print(BUG_MSG)
                        bugs_flag_mismatch.add(method)
            except Exception as e:
                print(BUG_MSG)
                bugs_flag_mismatch.add(method)

        if funccall_visitor.apis:
            count_wrapper_has_fmtstr += 1

        # API call -> format string
        for api in funccall_visitor.apis:
            fmtstr = None
            if api['name'] in pycstructure.PCAPI_AP_KWD:
                if isinstance(api['args'][2], c_ast.Constant):
                    fmtstr = api['args'][2].value[1:-1]
                else:
                    pass
                    # TODO propagation
            elif api['name'] in pycstructure.PCAPI_AP_POS:
                if isinstance(api['args'][1], c_ast.Constant):
                    fmtstr = api['args'][1].value[1:-1]
                else:
                    pass
                    # TODO propagation
            else:
                pass

            if fmtstr is not None:
                if fmtstr: # skip ""
                    print(fmtstr)

                # format string -> type signature
                type_signature = format_string_parser.parse(fmtstr)
                format_string_parser.print_signature(type_signature)
        else:
            if method.ml_flag.value == '0x0004':
                print("[]")
                count_wrapper_marked_noarg += 1
            elif method.param_unused:
                print("[]")
                print(BUG_MSG)
                bugs_flag_mismatch.add(method)

        print('--->>>')
        # C implementation -> valid return
        return_visitor = astvisitor.ReturnVisitor(funcdef_visitor.wrapper[0])
        return_visitor.visit(funcdef_visitor.wrapper[0])
        format_string_parser.print_signature(return_visitor.returns)


end_time = time.time()

print("========== statistics ==========")

print("time elapse: {:.3f}s".format(end_time - start_time))
print("file analyzed directly: {}".format(len(sources)))
print("file analyzed directly and compilable: {}".format(count_compilable))

print("wrapper function (WP): {}".format(count_wrapper))
print("WP has format string(s): {}".format(count_wrapper_has_fmtstr))
print("WP with METH_NOARGS: {}".format(count_wrapper_marked_noarg))

print("WP possibly with a bug: {}".format(len(bugs_flag_mismatch)))
for bug in bugs_flag_mismatch:
    print(bug)