import re

from prims import Context, Meta
from compiler.ast import *

__all__ = ['generate_write', 'generate']


def generate_write(ast_tree, meta, out_dir, module_name):
    from os.path import join

    ctx = generate(ast_tree, meta)
    out_file = module_name + ".cpp"
    f = open(join(out_dir, out_file), 'w+')
    f.write(ctx._out)
    f.close()
    return ctx, out_file


def generate(ast_tree, meta):
    """
    :type ast_tree: Node
    :type meta: Meta
    """
    ctx = Context(meta)
    gen_expr(ctx, ast_tree)
    return ctx


def _child_gen(ctx, parent):
    for child in filter(lambda x: isinstance(x, Node), parent.getChildren()):
        gen_expr(ctx, child)


def _is_skippable(node):
    if node.__class__ is Assign:
        if node.getChildren()[0].name == '__all__':
            return True
    return False


def _infer_type(ctx, node):
    if isinstance(node, CallFunc):
        print dir(node.getChildren()[0])
        func_name = node.getChildren()[0].name
        func_meta = next(iter(filter(lambda x: x.name == func_name, ctx.meta.funcs)))
        return func_meta.rtype
    return None


def gen_expr(ctx, node):
    """
    :type ctx: Context
    :type node: compiler.ast.Node
    """
    cls = node.__class__
    if _is_skippable(node):
        return

    if cls is Function:
        func_name = node.name
        func_meta = ctx.meta.get_func(func_name)

        pfx = 'static ' if not func_meta.is_ext else ''
        pfx += func_meta.rtype

        args = ', '.join(map(lambda x: '{0} {1}'.format(x[1], x[0]), func_meta.args))

        ctx.write('{pfx} {func_name}({args})\n'.format(pfx=pfx, func_name=func_name, args=args))
        ctx.write('{\n')
        ctx.indent_inc()

        _child_gen(ctx, node)

        ctx.indent_dec()
        ctx.write('}\n\n')
    elif cls is Return:
        ctx.write(ctx.indent() + 'return ')

        _child_gen(ctx, node)

        ctx.write(';\n')
    elif cls is Add:
        gen_expr(ctx, node.left)
        ctx.write(' + ')
        gen_expr(ctx, node.right)
    elif cls is Sub:
        gen_expr(ctx, node.left)
        ctx.write(' - ')
        gen_expr(ctx, node.right)
    elif cls is Name:
        ctx.write(node.name)
    elif cls is Assign:
        lvalue, rvalue = node.getChildren()
        lvalue_type = _infer_type(ctx, rvalue)

        ctx.write(ctx.indent() + '{type} {var}'.format(type=lvalue_type, var=lvalue.name))
        ctx.write(' = ')
        gen_expr(ctx, rvalue)
        ctx.write(';\n')
    elif cls is Const:
        ctx.write(str(node.value))
    elif cls is CallFunc:
        func_name = node.getChildren()[0]
        children = filter(lambda x: isinstance(x, Node), node.getChildren())[1:]

        ctx.write(func_name.name)
        ctx.write('(')

        out = []
        for c in children:
            tctx = Context(ctx.meta)
            gen_expr(tctx, c)
            out.append(tctx._out)

        ctx.write(', '.join(out))
        ctx.write(')')
    else:
        for child in filter(lambda x: isinstance(x, Node), node.getChildren()):
            gen_expr(ctx, child)

if __name__ == "__main__":
    import pyparser
    import os
    import sys
    from os.path import join
    sys.path.append('../tests')
    module, tree = pyparser.parse(join(os.getcwd(), '../tests/flight_model.py'))
    ctx = generate(module, tree)
    print ctx._out