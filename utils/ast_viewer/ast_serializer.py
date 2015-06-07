import json
from compiler.ast import *


def serialize(node, level, indent, write):
    pfx = indent * level

    children = get_children(node)
    ending = ',' if children else ''

    write(pfx + "{")
    write(pfx + '"name": "{0}"{1}'.format(format_node(node), ending))

    if children:
        write(pfx + '"children": [')

        for i, child in enumerate(children):
            if i != 0:
                write(pfx + ',')
            serialize(child, level+1, indent, write)

        write(pfx + ']')

    write(pfx + "}")


def get_children(node):
    if isinstance(node, (Name, Const)):
        return []
    return filter(lambda e: not e is None, node.getChildren()) if isinstance(node, Node) else []


def format_node(node):
    if isinstance(node, str):
        if len(node.split('\n')) == 1:
            return node
    elif isinstance(node, Function):
        return 'Function: {0}'.format(node.name)
    elif isinstance(node, (Name, Const)):
        return node
    return node.__class__.__name__
