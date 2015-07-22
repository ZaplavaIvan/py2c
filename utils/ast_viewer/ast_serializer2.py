import ast
from ast import AST, iter_fields, iter_child_nodes


def serialize(node, level, indent, write):
    pfx = indent * level

    children = iter_child_nodes(node)
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


def format_node(node):
    return node.__class__.__name__

if __name__ == '__main__':
    import ast
    data = open('../../tests/test1.py').read()
    tree = ast.parse(data)

    def printer(e):
        print e

    serialize(tree, 0, '', printer)
