class Meta:

    def __init__(self):
        self.module_name = None
        self._funcs = {}

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
        self.args = args
        self.rtype = rtype
        self.doc = doc
        self.is_ext = is_ext


class Context:

    def __init__(self, meta=None):
        if meta is None: meta = Meta()
        self.meta = meta
        self._indent_size = 0
        self._out = ''

    def indent_inc(self):
        self._indent_size += 4

    def indent_dec(self):
        self._indent_size -= 4

    def indent(self):
        return ' ' * self._indent_size

    def write(self, data):
        self._out += data