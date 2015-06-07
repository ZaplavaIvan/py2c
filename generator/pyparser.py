import re
from os import path
import imp
import compiler
from compiler.ast import *

from prims import Meta, FunctionMeta


def prepare_meta(meta, mod, node):
    if isinstance(node, Function):
        args = map(lambda x: (x, get_func_argt(node, x)), node.argnames)
        rtype = get_func_argt(node, 'rtype')
        is_ext = node.name in mod.__all__
        meta.add_func(FunctionMeta(node.name, args, rtype, node.doc, is_ext))

    for child in filter(lambda x: isinstance(x, Node), node.getChildren()):
        prepare_meta(meta, mod, child)


def get_func_argt(node, arg):
    """
    :type func: Function
    :type arg: str
    """
    if arg == 'rtype':
        pattern = '.*:rtype: (?P<type>[.a-zA-Z]*)'
    else:
        pattern = '.*:type {0}: (?P<type>[.a-zA-Z]*)'.format(arg)

    match = re.match(pattern, node.doc, re.DOTALL)
    return match.group('type') if match else None


def parse(module_path):
    directory, module_name = path.split(module_path)

    mod = imp.load_source(path.splitext(module_name)[0], module_path)
    ast_tree = compiler.parseFile(module_path)
    meta = Meta()
    meta.module_name = mod.__name__
    prepare_meta(meta, mod, ast_tree)

    return mod, ast_tree, meta

if __name__ == '__main__':
    pass