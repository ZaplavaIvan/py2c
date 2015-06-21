import re
from os import path
import imp
import compiler
from compiler.ast import *

from prims import Meta, FunctionMeta, VarMeta
from meta import match_type, IntT, FloatT


def prepare_meta(meta, mod, node):
    if isinstance(node, Function):
        args = map(lambda x: (x, get_func_argt(node.doc, x)), node.argnames)
        rtype = get_func_argt(node.doc, 'rtype')
        is_ext = not hasattr(mod, '__all__') or node.name in mod.__all__
        func_meta = FunctionMeta(node.name, args, rtype, node.doc, is_ext)
        prepare_func_meta(func_meta, node)
        node.meta = func_meta
        meta.add_func(func_meta)

    for child in filter(lambda x: isinstance(x, Node), node.getChildren()):
        prepare_meta(meta, mod, child)


def prepare_func_meta(meta, node):
    """
    :type meta: FunctionMeta
    :type node: Node
    :return:
    """
    if isinstance(node, Assign):
        lvalue, rvalue = node.getChildren()
        is_declared = lvalue.name in meta.locals
        if not is_declared:
            lvalue_type = infer_type(meta, rvalue)
            meta.locals[lvalue.name] = lvalue_type
        else:
            lvalue_type = meta.locals[lvalue.name]
        var_meta = VarMeta(lvalue.name, lvalue_type, is_declared)
        lvalue.meta = var_meta

    for child in filter(lambda x: isinstance(x, Node), node.getChildren()):
        prepare_func_meta(meta, child)


def infer_type(meta, node):
    if isinstance(node, CallFunc):
        call_node = node.getChildren()[0]
        if isinstance(call_node, Name):
            type = infer_type(meta, call_node)
            if type is not None: return type
            if call_node.name in ['min']:
                return infer_type(meta, node.getChildren()[1])
        else:
            return infer_type(meta, call_node)
    elif isinstance(node, Name):
        return infer_Name(meta, node)
    elif isinstance(node, Getattr):
        var, attr = node.getChildren()[0], node.getChildren()[1]
        var_type = infer_type(meta, var)
        attr_doc = getattr(var_type.python_type, attr).__doc__
        return get_func_argt(attr_doc, 'rtype')
    elif isinstance(node, Const):
        const_type = node.value.__class__
        if const_type is int:
            return IntT
        elif const_type is float:
            return FloatT
    return None


def infer_Name(meta, node):
    match = match_type(node.name)
    if match:
        return match
    if node.name in meta.locals:
        return meta.get_var_type(node.name)

def get_func_argt(doc, arg):
    """
    :type doc: str
    :type arg: str
    """
    if arg == 'rtype':
        pattern = '.*:rtype: (?P<type>[.a-zA-Z0-9]*)'
    else:
        pattern = '.*:type {0}: (?P<type>[.a-zA-Z0-9]*)'.format(arg)

    match = re.match(pattern, doc, re.DOTALL)
    return match_type(match.group('type')) if match else None


def parse(module_path):
    directory, module_name = path.split(module_path)

    mod = imp.load_source(path.splitext(module_name)[0], module_path)
    ast_tree = compiler.parseFile(module_path)
    meta = Meta()
    meta.module_name = mod.__name__
    prepare_meta(meta, mod, ast_tree)

    return mod, ast_tree, meta

if __name__ == '__main__':
    import meta
    import os
    import sys
    from os.path import join
    sys.path.append('../tests')
    import Math
    Vector3 = meta.Type(Math.Vector3, 'Vector3', ['vector3.hpp'])
    meta.register_type('Vector3', Vector3)

    module, tree, meta = parse(join(os.getcwd(), '../tests/test2.py'))