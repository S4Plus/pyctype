#-------------------------------------------------------------------------------
# AST node visitors.
#
# Subclass of pycparser.c_ast.NodeVisitor.
# Define own visit_XXX methods, where XXX is the class name to visit.
#-------------------------------------------------------------------------------
import argparse
from pycparser import c_ast

import pycstructure
import ptypes
import format_string_parser


# (t1)(t2)...(tn)foo -> foo
def Cast2Id(node):
    if isinstance(node, c_ast.ID):
        return node
    else:
        return Cast2Id(node.expr)


# find PyMethodDef-s array declaration in given source file
class PyMethodDefVisitor(c_ast.NodeVisitor):
    def __init__(self, filename):
        self.filename =filename
        self.pymethoddefs = []

    def visit_Decl(self, node):
        # exclude decl. in libraries
        if node.coord.file == self.filename:
            if isinstance(node.type, c_ast.ArrayDecl):
                # Decl.ArrayDecl.TypeDecl.IdentifierType/Struct
                if isinstance(node.type.type.type, c_ast.IdentifierType) and node.type.type.type.names[0] == 'PyMethodDef' or isinstance(node.type.type.type, c_ast.Struct) and node.type.type.type.name == 'PyMethodDef':
                    try:
                        count = 0
                        if node.init:
                            for method in node.init:
                                # name of the method
                                ml_name = method.exprs[0]
                                # pointer to the C implementation
                                if len(method.exprs) <= 2:
                                    # {NULL, NULL} or {NULL} marks 
                                    # the ending of PyMethodDef[] decl.
                                    continue
                                else:
                                    ml_meth_node = method.exprs[1]
                                    ml_flag_node = method.exprs[2]
                                if not isinstance(ml_meth_node, c_ast.Constant):
                                    count += 1
                                    # maybe a cast 
                                    # from function to (PyCFunction)function
                                    ml_meth = Cast2Id(ml_meth_node)
                                    # maybe METH_VARARGS | METH_KEYWORDS
                                    # TODO where left of | can be another BinaryOp
                                    ml_flag = ml_flag_node if isinstance(ml_flag_node, c_ast.Constant) else ml_flag_node.right
                                    self.pymethoddefs.append(
                                        pycstructure.PyMethodDef(
                                            ml_name, ml_meth, ml_flag))
                            if count:
                                print("PyMethodDef [{}] {} (L{})".format(
                                    count, node.name, node.coord.line))
                    except Exception as e:
                        print("[ERROR] Unknown declaration structure in {}".format(
                            node.coord))
                        print(e)


# find wrapper function declaration pointed to by given name from PyMethodDef
# return:
#   wrapper function node
#   parameters of wrapper funciton
class FuncDefVisitor(c_ast.NodeVisitor):
    def __init__(self, funcname):
        self.funcname = funcname
        self.wrapper = [] # TODO eponymous function declarations?
        self.params = None

    def visit_FuncDef(self, node):
        if node.decl.name == self.funcname:
            self.wrapper.append(node)
            if node.decl.type.args:
                self.params = node.decl.type.args.params
            else:
                # wrapper funciton has no parameters
                self.params = None


# find ID call site of parameter in function body
class IDVisitor(c_ast.NodeVisitor):
    def __init__(self, param_name):
        self.param_name = param_name
        self.called = None

    def visit_ID(self, node):
        if node.name == self.param_name:
            self.called = node.coord


# find Python/C API argument parsing function call in wrapper function
# return: arguments node list
class FuncCallVisitor(c_ast.NodeVisitor):
    def __init__(self):
        # may have multiple argument parsing function calls 
        # in one wrapper function
        # TODO not everyone is for argument parsing
        self.apis = []

    def visit_FuncCall(self, node):
        if isinstance(node.name, c_ast.ID):
            if node.name.name in pycstructure.PCAPI_AP_POS or node.name.name in pycstructure.PCAPI_AP_KWD:
                api = {}
                api['name'] = node.name.name
                # FuncCall.ExprList.exprs
                api['args'] = node.args.exprs
                self.apis.append(api)
            else:
                # TODO other argument parsing methods
                # e.g., PyLong_FromLong
                pass


# input:  name of a variable
# output: type given to the variable when declared
class DeclTypeVistor(c_ast.NodeVisitor):
    def __init__(self, varname):
        self.varname = varname
        self.decl = []

    def visit_Decl(self, node):
        if node.name == self.varname:
            if isinstance(node.type, c_ast.PtrDecl):
                type_node = node.type.type # PtrDecl.type is a TypeDecl
            else: # TypeDecl directly
                type_node = node.type
            self.decl.append(type_node.type.names[0]) # TypeDecl.IdentifierType

# input:  name of a variable, search domain
# output: type given to the variable when assigned
# If this variable is referred to another varibale, we handle this propagation with a recursion
class RValVisitor(c_ast.NodeVisitor):
    def __init__(self, lval, origin_node):
        self.lval = lval
        self.rvals = []
        self.origin_node = origin_node

    def visit_Assignment(self, node):
        if not isinstance(node.lvalue, (c_ast.StructRef, c_ast.UnaryOp)): # TODO lvalue is a->b
            # print(node.lvalue)
            if node.lvalue.name == self.lval:
                if isinstance(node.rvalue, c_ast.Constant):
                    # self.rvals.append(node.rvalue.type) # TODO rvalue = NULL
                    pass
                elif isinstance(node.rvalue, c_ast.FuncCall):
                    if isinstance(node.rvalue.name, c_ast.ID):
                        # function call is an API
                        funcname = node.rvalue.name.name
                        if funcname.find('_From') != -1 or funcname.find('_New') != -1:
                            self.rvals.append(str(ptypes.getPTypeFromTrans(funcname)()))
                    else:
                        # TODO inter-procedural
                        pass
                elif isinstance(node.rvalue, c_ast.ID):
                    decltype_vistor = DeclTypeVistor(node.rvalue.name)
                    decltype_vistor.visit(self.origin_node)
                    if decltype_vistor.decl:
                        self.rvals.append(decltype_vistor.decl[-1])

                    rval_visitor = RValVisitor(node.rvalue.name, self.origin_node)
                    rval_visitor.visit(self.origin_node)
                    for v in rval_visitor.rvals:
                        self.rvals.append(v)

# input:  name of a variable, search domain
# output: possible values of the input, including
#         initialization declaration, assignment, propagration
def value_analysis(var, ast):
    values = []
    
    decltype_vistor = DeclTypeVistor(var)
    decltype_vistor.visit(ast)
    if decltype_vistor.decl:
        values.append(decltype_vistor.decl[-1])

    rval_visitor = RValVisitor(var, ast)
    rval_visitor.visit(ast)
    for v in rval_visitor.rvals:
        values.append(v)

    return values


# find valid return statement in wrapper function
class ReturnVisitor(c_ast.NodeVisitor):
    def __init__(self, parent_function):
        self.parent_function = parent_function
        self.returns = []

    def visit_Return(self, node):
        # exclude return NULL
        if not isinstance(node.expr, (c_ast.Constant, c_ast.TernaryOp)):
            if isinstance(node.expr, c_ast.FuncCall):
                funcname = node.expr.name.name
                if isinstance(funcname, c_ast.ID):
                    funcname = funcname.name
                if funcname.startswith('_Py') or funcname.startswith('Py'):
                    if funcname in pycstructure.PCAPI_BV:
                        fmtstr = node.expr.args.exprs[0].value[1:-1]
                        try:
                            type_signature = format_string_parser.parse(fmtstr)
                        except:
                            print("[BUG] Illegal format string: {}".format(fmtstr))
                            type_signature = [[]]
                        self.returns.append(type_signature) # always a product type
                    elif funcname.find('_From') != -1 or funcname.find('_New') != -1:
                        # return Py*_From*, Py*_New
                        self.returns.append(ptypes.getPTypeFromTrans(funcname)())
                    else:
                        # Unknown Python/C API
                        self.returns.append(ptypes.pObject())
                # return a self-defined function call, usually for error handling
                else:
                    self.returns.append(ptypes.pObject())
            elif isinstance(node.expr, c_ast.UnaryOp):
                # return Py_None
                if node.expr.expr.name == '_Py_NoneStruct':
                    self.returns.append(ptypes.pNone())
            elif isinstance(node.expr, c_ast.ExprList):
                # Macro for returning Py_None, Py_True. Py_False
                if node.expr.exprs:
                    last_expr = node.expr.exprs[-1].expr
                    if isinstance(last_expr, c_ast.ID):
                        last_expr_name = last_expr.name
                    elif isinstance(last_expr, c_ast.UnaryOp):
                        last_expr_name = last_expr.expr.name
                    else:
                        last_expr_name = None
                    if last_expr_name:
                        if last_expr_name == '_Py_NoneStruct':
                            self.returns.append(ptypes.pNone())
                        elif last_expr_name == '_Py_TrueStruct' or last_expr_name == '_Py_FalseStruct':
                            self.returns.append(ptypes.pBool())
            elif isinstance(node.expr, c_ast.Cast):
                self.returns.append(ptypes.getPTypeFromName(node.expr.to_type.type.type.type.names[0])())
            else:
                # return a variable
                for v in value_analysis(node.expr.name, self.parent_function):
                    self.returns.append(ptypes.getPTypeFromName(v)())


if __name__ == "__main__":
    filename = '/Users/hmz/Projects/Pillow/src/_imaging.c'
    ppconfig = 'pillow'

    import preprocess
    ast = preprocess.cpp(filename, ppconfig)

    pymethoddef_visitor = PyMethodDefVisitor(filename)
    pymethoddef_visitor.visit(ast)
    for method in pymethoddef_visitor.pymethoddefs:
        print(method)

    funcname = '_getbbox'
    funcdef_visitor = FuncDefVisitor(funcname)
    funcdef_visitor.visit(ast)
    print(funcdef_visitor.wrapper[0].coord)

    id_visitor = IDVisitor(funcdef_visitor.params[1].name)
    id_visitor.visit(funcdef_visitor.wrapper[0].body)
    if not id_visitor.called:
        print("{} is not used in {}".format(funcdef_visitor.params[1].name, 
            funcdef_visitor.wrapper[0].decl.name))
    else:
        print("{} is used in {}".format(funcdef_visitor.params[1].name, 
            id_visitor.called))

    funccall_visitor = FuncCallVisitor()
    funccall_visitor.visit(funcdef_visitor.wrapper[0])

    # decltype_vistor = DeclTypeVistor('result')
    # decltype_vistor.visit(funcdef_visitor.funcnode)
    # print(decltype_vistor.decl)

    # rval_visitor = RValVisitor('result', funcdef_visitor.funcnode)
    # rval_visitor.visit(funcdef_visitor.funcnode)
    # print(rval_visitor.rvals)

    # print(value_analysis('result', funcdef_visitor.wrapper[0]))

    return_visitor = ReturnVisitor(funcdef_visitor.wrapper[0])
    return_visitor.visit(funcdef_visitor.wrapper[0])
    format_string_parser.print_signature(return_visitor.returns)