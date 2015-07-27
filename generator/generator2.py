import ast
from ast import \
    And, Or, \
    Add, Sub, Mult, Div, Mod, Pow, LShift, RShift, BitOr, BitXor, BitAnd, FloorDiv, \
    Invert, Not, UAdd, USub, \
    Eq, NotEq, Lt, LtE, Gt, GtE, Is, IsNot, In, NotIn, \
    UAdd, USub, Invert, BitAnd, BitOr, BitXor, \
    Module, FunctionDef, While, For, If, Assign, AugAssign, Return, Name, Num, Compare, Break, Continue, \
    operator, BoolOp, BinOp, UnaryOp


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

    @property
    def indent_up(self):
        return " "*(self.indentSize + 4)

    def make_unique(self, var_name):
        self.VAR_ID += 1
        return var_name + str(self.VAR_ID)

    def up(self):
        return PrintContext(self.meta, self.indentSize + 4)

    def zero(self):
        return PrintContext(self.meta, 0)

def cmp_operators(A, B):
    """
    :type A: operator
    :type B: operator
    :rtype: int
    """

    precedence = [
        [Or],
        [And],
        [Lt, LtE, Gt, GtE, NotEq, Eq],
        [BitOr],
        [BitXor],
        [BitAnd],
        [RShift, LShift],
        [Add, Sub],
        [Mult, Div, Mod, FloorDiv],
        [Invert, UAdd, USub],
        [Pow]
    ]
    def get_priority(op):
        for i, p in enumerate(precedence):
            if op in p:
                return i
        return -1

    return cmp(get_priority(A), get_priority(B))


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

        expr = print_expr(ctx, child, node)
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
{indent_up}{cond_var} = {cond_expr};
{indent}}}
{indent}if (!{cond_var})
{indent}{{
{orelse_expr}
{indent}}}
"""
        cond_var = ctx.make_unique('cond_var')
        cond_expr = print_expr(ctx.zero(), test, node)
        body_expr = print_expr(ctx.up(), body, node)
        orelse_expr = print_expr(ctx.up(), orelse, node)

        return template.format(indent=ctx.indent,
                               indent_up=ctx.indent_up,
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
        cond_expr = print_expr(ctx.zero(), test, node)
        body_expr = print_expr(ctx.up(), body, node)

        return template.format(indent=ctx.indent,
                               cond_expr=cond_expr,
                               body_expr=body_expr)

def print_for(ctx, node):
    """
    :type node: For
    :rtype: string
    """
    pass


def print_if(ctx, node, sibling=None):
    """
    :type node: If
    :rtype: string
    """

    test, body, orelse = node.test, node.body, node.orelse
    template = """{indent}{clause}({cond_expr})
{indent}{{
{body_expr}
{indent}}}
"""
    clause = "if" if sibling is None else "elif"
    head = template.format(indent=ctx.indent,
                           cond_expr=print_expr(ctx.zero(), test, node),
                           body_expr=print_expr(ctx.up(), body, node),
                           clause=clause)
    if not orelse:
        return head

    if isinstance(orelse[0], If):
        return head + print_if(ctx, orelse[0], node)
    else:
        template = """{indent}else
{indent}{{
{body_expr}
{indent}}}
"""
        return head + template.format(indent=ctx.indent,
                                      body_expr=print_expr(ctx.up(), orelse, node))


def print_assign(ctx, node):
    """
    :type ctx: PrintContext
    :type node: Assign
    :rtype: string
    """
    targets = node.targets
    value = node.value

    template = "{indent}{target_type}{target_expr} = {value_expr};"
    var_meta = targets[0].meta

    return template.format(target_expr=print_expr(ctx.zero(), targets[0], node),
                           target_type=("" if var_meta.is_declared else "%s "%var_meta.type.cpp_type),
                           value_expr=print_expr(ctx.zero(), value, node),
                           indent=ctx.indent)

def get_operator_shield(parent, op):
    if isinstance(parent, (BinOp, UnaryOp, BoolOp)):
        parent_op = parent.op
        if cmp_operators(parent_op.__class__, op.__class__) > 0:
            return "(", ")"
    return "", ""

def print_binop(ctx, left, op, right, node, parent):
    template = "{l}{left_expr} {op} {right_expr}{r}"
    l, r = get_operator_shield(parent, op)

    return template.format(left_expr=print_expr(ctx.zero(), left, node),
                           op=print_operator(op.__class__),
                           right_expr=print_expr(ctx.zero(), right, node),
                           l=l, r=r)

def print_boolop(ctx, node, parent):
    op, values = node.op, node.values
    template = "{l}{body}{r}"
    l, r = get_operator_shield(parent, op)
    values_exprs = map(lambda e: print_expr(ctx, e, node), values)
    separator = " {op} ".format(op=print_operator(op.__class__))
    return template.format(body=separator.join(values_exprs),
                           l=l,r=r)


def print_expr(ctx, node, parent):
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
        return template.format(left_expr=print_expr(ctx.zero(), target, node),
                               op=print_operator(op.__class__),
                               right_expr=print_expr(ctx.zero(), value, node),
                               indent=ctx.indent)
    elif cls is Return:
        return "{indent}return {value_expr};".format(indent=ctx.indent, value_expr=print_expr(ctx.zero(), node.value, node))
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
                                             operand_expr=print_expr(ctx.zero(), operand, node))
    elif cls is BinOp:
        return print_binop(ctx, node.left, node.op, node.right, node, parent)
    elif cls is BoolOp:
        return print_boolop(ctx, node, parent)
    elif cls is Compare:
        left, ops, comparators = node.left, node.ops, node.comparators
        return print_binop(ctx, left, ops[0], comparators[0], node, parent)
    elif cls is list:
        return print_stmt(ctx, node)
    else:
        return None

if __name__ == '__main__':
    import pyparser2
    import meta
    import os
    from os.path import join

    module, tree, meta = pyparser2.parse(join(os.getcwd(), '../tests/test1.py'))
    ctx = PrintContext(meta, 0)
    print print_expr(ctx, tree, None)