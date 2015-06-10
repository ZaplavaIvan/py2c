import re

from prims import Context, Block, Meta
from compiler.ast import *


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
    blk = Block(meta, 0)
    gen_expr(blk, ast_tree)
    return blk


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
        func_name = node.getChildren()[0].name
        func_meta = next(iter(filter(lambda x: x.name == func_name, ctx.meta.funcs)))
        return func_meta.rtype
    elif isinstance(node, Const):
        try:
            int(node.value)
            return 'int'
        except e:
            pass
        try:
            float(node.value)
            return 'float'
        except e:
            pass
        return 'string'

    return None


def get_children(node):
    return filter(lambda e: not e is None, node.getChildren())


def transform_stmt(ctx, node):
    for child in get_children(node):
        if isinstance(child, (While,)):
            ctx.new_line()

        gen_expr(ctx, child)

        if isinstance(child, (Assign, AugAssign)):
            ctx.write(';')
            ctx.new_line()


def gen_expr(ctx, node):
    """
    :type ctx: Block
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

        body_blk = Block(ctx.meta, ctx.next_indent)
        body_blk.locals.extend(map(lambda e: e[0], func_meta.args))
        _child_gen(body_blk, node)
        ctx.write(body_blk.out)

        ctx.write('}\n\n')
    elif cls is Stmt:
        transform_stmt(ctx, node)
    elif cls is Return:
        ctx.write('return ')

        _child_gen(ctx, node)

        ctx.write(';\n')
    elif cls is Continue:
        ctx.write('continue;')
        ctx.new_line()
    elif cls is Break:
        ctx.write('break;')
        ctx.new_line()
    elif cls is If:
        children = get_children(node)

        if len(children) % 2 != 0:
            if_stmts, else_node = children[:-1], children[-1]
        else:
            if_stmts, else_node = children, None

        for i, ifpack in enumerate(zip(if_stmts[:-1: 2], if_stmts[1::2])):
            if_node, stmt_node = ifpack
            ctx.write(('if' if i == 0 else 'else if') + ' (')
            gen_expr(ctx, if_node)
            ctx.write(')')
            ctx.new_line()
            ctx.write('{\n')

            blk = Block.from_parent(ctx)
            gen_expr(blk, stmt_node)
            ctx.write(blk.out, False)

            ctx.write('}\n')

        if else_node:
            ctx.write('else\n')
            ctx.write('{\n')

            blk = Block.from_parent(ctx)
            gen_expr(blk, else_node)
            ctx.write(blk.out, False)

            ctx.write('}\n')
    elif cls is Mod:
        gen_expr(ctx, node.left)
        ctx.write(' % ')
        gen_expr(ctx, node.right)
    elif cls is Add:
        gen_expr(ctx, node.left)
        ctx.write(' + ')
        gen_expr(ctx, node.right)
    elif cls is Sub:
        gen_expr(ctx, node.left)
        ctx.write(' - ')
        gen_expr(ctx, node.right)
    elif cls is Mul:
        gen_expr(ctx, node.left)
        ctx.write(' * ')
        gen_expr(ctx, node.right)
    elif cls is Div:
        gen_expr(ctx, node.left)
        ctx.write(' / ')
        gen_expr(ctx, node.right)
    elif cls is Or:
        left, right = get_children(node)
        gen_expr(ctx, left)
        ctx.write(' || ')
        gen_expr(ctx, right)
    elif cls is Name:
        ctx.write(node.name)
    elif cls is Assign:
        lvalue, rvalue = node.getChildren()
        lvalue_type = _infer_type(ctx, rvalue)

        var_name = lvalue.name
        is_declared = var_name in ctx.locals
        pfx = '{type} '.format(type=lvalue_type) if not is_declared else ''

        if not is_declared:
            ctx.locals.append(var_name)

        ctx.write(pfx + '{var}'.format(var=var_name))
        ctx.write(' = ')
        gen_expr(ctx, rvalue)
    elif cls is AugAssign:
        lvalue, op, rnode = node.getChildren()

        ctx.write(lvalue.name)
        ctx.write(' {0} '.format(op))
        gen_expr(ctx, rnode)
    elif cls is Const:
        ctx.write(str(node.value))
    elif cls is CallFunc:
        func_name = node.getChildren()[0]
        children = filter(lambda x: isinstance(x, Node), node.getChildren())[1:]

        ctx.write(func_name.name)
        ctx.write('(')

        out = []
        for c in children:
            tctx = Block(ctx.meta)
            gen_expr(tctx, c)
            out.append(tctx.out)

        ctx.write(', '.join(out))
        ctx.write(')')
    elif cls is Compare:
        lnode, op, rnode = node.getChildren()

        gen_expr(ctx, lnode)
        ctx.write(' {0} '.format(op))
        gen_expr(ctx, rnode)
    elif cls is While:
        cond_node, body_node = get_children(node)

        ctx.write('while(')
        gen_expr(ctx, cond_node)
        ctx.write(')\n')
        ctx.write('{\n')

        body_blk = Block.from_parent(ctx)
        gen_expr(body_blk, body_node)
        ctx.write(body_blk.out, False)

        ctx.write('}\n')
    else:
        for child in filter(lambda x: isinstance(x, Node), node.getChildren()):
            gen_expr(ctx, child)

if __name__ == "__main__":
    import pyparser
    import os
    import sys
    from os.path import join
    sys.path.append('../tests')
    module, tree, meta = pyparser.parse(join(os.getcwd(), '../tests/test1.py'))
    ctx = generate(tree, meta)
    print ctx.out