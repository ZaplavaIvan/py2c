import re
from os import path
import imp
import ast
from ast import iter_child_nodes, AST, FunctionDef, Assign, Num

from prims import Meta, FunctionMeta, VarMeta
from meta import match_type, IntT, FloatT


def create_meta(meta, mod, node):
    cls = node.__class__

    if cls is FunctionDef:
        return create_func_meta(meta, mod, node)
    elif cls is Assign:
        return create_assign_meta(meta, mod, node)
    else:
        if cls is list:
            for child in node:
                create_meta(meta, mod, child)
        else:
            for child in iter_child_nodes(node):
                create_meta(meta, mod, child)


def create_func_meta(meta, mod, node):
    name, args, body = node.name, node.args, node.body
    doc = body[0].value.s

    kargs = map(lambda e: e.id, args.args)
    kargsData = map(lambda x: (x, get_func_argt(doc, x)), kargs)
    rtype = get_func_argt(doc, 'rtype')
    is_ext = not hasattr(mod, '__all__') or name in mod.__all__

    func_meta = FunctionMeta(name, kargsData, rtype, doc, is_ext)
    create_meta(func_meta, mod, body)
    node.meta = func_meta
    meta.add_func(func_meta)


def create_assign_meta(meta, mod, node):
    targets, rvalue = node.targets, node.value
    lvalue = targets[0]

    is_declared = lvalue.id in meta.locals
    if not is_declared:
        lvalue_type = infer_type(meta, rvalue)
        meta.locals[lvalue.id] = lvalue_type
    else:
        lvalue_type = meta.locals[lvalue.id]

    var_meta = VarMeta(lvalue.id, lvalue_type, is_declared)
    lvalue.meta = var_meta


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


def infer_type(meta, node):
    cls = node.__class__

    if cls is Num:
        if isinstance(node.n, int):
            return IntT
        if isinstance(node.n, float):
            return FloatT
    else:
        raise 'Not supported type:', cls


def parse(module_path):
    directory, module_name = path.split(module_path)

    mod = imp.load_source(path.splitext(module_name)[0], module_path)
    data = open(module_path).read()
    ast_tree = ast.parse(data)
    meta = Meta()
    meta.module_name = mod.__name__
    create_meta(meta, mod, ast_tree)

    return mod, ast_tree, meta

if __name__ == '__main__':
    import os
    import sys
    from os.path import join
    sys.path.append('../tests')

    module, tree, meta = parse(join(os.getcwd(), '../tests/test1.py'))