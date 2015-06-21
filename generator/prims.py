class Meta:

    def __init__(self):
        self.module_name = None
        self._funcs = {}
        self.locals = {}

    @property
    def funcs(self):
        return self._funcs.itervalues()

    def add_func(self, func):
        """
        :type func: FunctionMeta
        """
        self._funcs[func.name] = func

    def get_func(self, name):
        """
        :type name: str
        :rtype: FunctionMeta
        """
        return self._funcs[name]

    def is_ext_function(self, func_name):
        return self._funcs[func_name].is_ext

    def get_func_argt(self, func_name, arg):
        func = self._funcs[func_name]
        if arg == 'rtype': return func.rtype
        return next(iter(filter(lambda e: e[0] == arg, func.args)))


class FunctionMeta:

    def __init__(self, func_name, args, rtype, doc, is_ext):
        self.name = func_name
        self.locals = dict(args)
        self.args = args
        self.rtype = rtype
        self.doc = doc
        self.is_ext = is_ext

    def get_var_type(self, var_name):
        return self.locals[var_name]


class CallFuncMeta:

    def __init__(self, t, is_explicit_namespace, namespace):
        self.type = t
        self.is_explicit_namespace = is_explicit_namespace
        self.namespace = namespace


class GetAttrMeta:

    def __init__(self, is_static, t, is_explicit_namespace, namespace):
        self.is_static = is_static
        self.type = t
        self.is_explicit_namespace = is_explicit_namespace
        self.namespace = namespace


class VarMeta:

    def __init__(self, name, t, is_declared):
        self.name = name
        self.type = t
        self.is_declared = is_declared

    def __repr__(self):
        return 'VarMeta(name={0}, type={1}, is_declared={2})'.format(self.name, self.type, self.is_declared)


class Context:

    def __init__(self):
        self.stream = StringIO()

    @property
    def out(self):
        return self._out.getvalue()


class Block:

    VAR_ID = 0

    def __init__(self, meta, indent=4):
        self.meta = meta
        self.locals = []
        self._indent = indent
        self._out = ""

    @staticmethod
    def make_unique(var_name):
        Block.VAR_ID += 1
        return var_name + str(Block.VAR_ID)

    @staticmethod
    def from_parent(parent, indent=None):
        blk = Block(parent.meta, parent.next_indent if indent is None else indent)
        blk.locals = parent.locals
        return blk

    @property
    def base_indent(self):
        return " "*4

    @property
    def next_indent(self):
        return self._indent + 4

    @property
    def out(self):
        return self._out

    def new_line(self):
        self._out += '\n';

    def write(self, data, use_indent=True):
        if use_indent and (len(self._out) == 0 or self._out[-1] == '\n'):
            self._out += " " * self._indent

        self._out += data