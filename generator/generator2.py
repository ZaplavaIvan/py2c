import ast
from ast import \
    And, Or, \
    Add, Sub, Mult, Div, Mod, Pow, LShift, RShift, BitOr, BitXor, BitAnd, FloorDiv, \
    Invert, Not, UAdd, USub, \
    Eq, NotEq, Lt, LtE, Gt, GtE, Is, IsNot, In, NotIn, \
    Module, FunctionDef, While, For, If, Assign, AugAssign, Return, Name, Num, Compare, BinOp, UnaryOp, Break, Continue


def generate_write(ast_tree, meta, out_dir, module_name):
    from os.path import join

    ctx = PrintContext(meta, 0)
    data = print_expr(ctx, ast_tree)
    out_file = module_name + ".cpp"
    f = open(join(out_dir, out_file), 'w+')
    f.write(data)
    f.close()
    return data, out_file


class PrintContext:

    VAR_ID = 0

    def __init__(self, meta, indent=0):
        self.meta = meta
        self.indentSize = indent

    @property
    def indent(self):
        return " "*self.indentSize

    def make_unique(self, var_name):
        self.VAR_ID += 1
        return var_name + str(self.VAR_ID)

    def up(self):
        return PrintContext(self.meta, self.indentSize + 4)

    def zero(self):
        return PrintContext(self.meta, 0)


def print_operator(op):
    return {
        And   : '&&',
        Or    : '||',
        Add   : '+',
        Sub   : '-',
        Mult  : '*',
        Div   : '/',
        Mod   : '%',
        Eq    : '==',
        NotEq : '!=',
        Lt    : '<',
        LtE   : '<=',
        Gt    : '>',
        GtE   : '>=',
        Not   : '!'
    }[op]


def print_module(ctx, node):
    """
    :type node: Module
    """

    return print_stmt(ctx, node)


def print_stmt(ctx, node):
    childs = []

    if isinstance(node, list):
        childs = node
    elif isinstance(node, ast.AST):
        childs = list(ast.iter_child_nodes(node))

    data = ''

    for i in range(len(childs)):
        child = childs[i]
        isLast = i == len(childs) - 1

        if isinstance(child, FunctionDef):
            ending = ""
        else:
            ending = "\n" if not isLast else ""

        expr = print_expr(ctx, child)
        if expr is None: continue

        data += "{expr}{ending}".format(expr=expr, ending=ending)

    return data

def print_function(ctx, node):
    """
    :type node: FunctionDef
    :rtype: string
    """

    name, body = node.name, node.body
    func_meta = ctx.meta.get_func(name)

    pfx = 'static ' if not func_meta.is_ext else ''
    pfx += func_meta.rtype.cpp_type

    args = ', '.join(map(lambda x: '{0} {1}'.format(x[1].cpp_type, x[0]), func_meta.args))

    template = """
{pfx} {func_name}({args})
{{
{body}
}}
    """

    return template.format(pfx=pfx, func_name=name, args=args, body=print_stmt(ctx.up(), body))

def print_while(ctx, node):
    """
    :type node: While
    :rtype: string
    """

    test, body, orelse = node.test, node.body, node.orelse

    if orelse:
        template = """{indent}bool {cond_var} = {cond_expr};
{indent}while({cond_var})
{indent}{{
{body_expr}
{indent}}}
{indent}if (!{cond_var})
{indent}{{
{orelse_expr}
{indent}}}
"""
        cond_var = ctx.make_unique('cond_var')
        cond_expr = print_expr(ctx.zero(), test)
        body_expr = print_expr(ctx.up(), body)
        orelse_expr = print_expr(ctx.up(), orelse)

        return template.format(indent=ctx.indent,
                               cond_var=cond_var,
                               cond_expr=cond_expr,
                               body_expr=body_expr,
                               orelse_expr=orelse_expr)
    else:
        template = """{indent}while({cond_expr})
{indent}{{
{body_expr}
{indent}}}
"""
        cond_expr = print_expr(ctx.zero(), test)
        body_expr = print_expr(ctx.up(), body)

        return template.format(indent=ctx.indent,
                               cond_expr=cond_expr,
                               body_expr=body_expr)

def print_for(ctx, node):
    """
    :type node: For
    :rtype: string
    """
    pass


def print_if(ctx, node):
    """
    :type node: If
    :rtype: string
    """

    test, body, orelse = node.test, node.body, node.orelse
    template = """{indent}if({cond_expr})
{indent}{{
{body_expr}
{indent}}}
"""
    return template.format(indent=ctx.indent,
                           cond_expr=print_expr(ctx.zero(), test),
                           body_expr=print_expr(ctx.up(), body))


def print_assign(ctx, node):
    """
    :type ctx: PrintContext
    :type node: Assign
    :rtype: string
    """
    targets = node.targets
    value = node.value

    template = "{indent}{target_type}{target_expr} = {value_expr};"

    return template.format(target_expr=print_expr(ctx.zero(), targets[0]),
                           target_type="",
                           value_expr=print_expr(ctx.zero(), value),
                           indent=ctx.indent)

def print_expr(ctx, node):
    cls = node.__class__

    if cls is Module:
        return print_module(ctx, node)
    elif cls is FunctionDef:
        return print_function(ctx, node)
    elif cls is While:
        return print_while(ctx, node)
    elif cls is For:
        return print_for(ctx, node)
    elif cls is If:
        return print_if(ctx, node)
    elif cls is Assign:
        return print_assign(ctx, node)
    elif cls is AugAssign:
        target, op, value = node.target, node.op, node.value
        template = "{indent}{left_expr} {op}= {right_expr};"
        return template.format(left_expr=print_expr(ctx.zero(), target),
                               op=print_operator(op.__class__),
                               right_expr=print_expr(ctx.zero(), value),
                               indent=ctx.indent)
    elif cls is Return:
        return "{indent}return {value_expr};".format(indent=ctx.indent, value_expr=print_expr(ctx.zero(), node.value))
    elif cls is Break:
        return "{indent}break;".format(indent=ctx.indent)
    elif cls is Continue:
        return "{indent}continue;".format(indent=ctx.indent)
    elif cls is Name:
        return node.id
    elif cls is Num:
        return str(node.n) + ("f" if node.n.__class__ is float else "")
    elif cls is UnaryOp:
        op, operand = node.op, node.operand
        return "{op}({operand_expr})".format(op=print_operator(op.__class__),
                                             operand_expr=print_expr(ctx.zero(), operand))
    elif cls is BinOp:
        left, op, right = node.left, node.op, node.right
        return "{left_expr} {op} {right_expr}".format(left_expr=print_expr(ctx.zero(), left),
                                                      op=print_operator(op.__class__),
                                                      right_expr=print_expr(ctx.zero(), right))
    elif cls is Compare:
        left, ops, comparators = node.left, node.ops, node.comparators
        return "{left_expr} {op} {right_expr}".format(left_expr=print_expr(ctx.zero(), left),
                                                      op=print_operator(ops[0].__class__),
                                                      right_expr=print_expr(ctx.zero(), comparators[0]))
    elif cls is list:
        return print_stmt(ctx, node)
    else:
        return None

if __name__ == '__main__':
    data = open('../tests/test1.py').read()

    import pyparser
    import meta
    import os
    from os.path import join

    module, tree, meta = pyparser.parse(join(os.getcwd(), '../tests/test1.py'))
    tree = ast.parse(data)
    ctx = PrintContext(meta, 0)
    print print_expr(ctx, tree)
