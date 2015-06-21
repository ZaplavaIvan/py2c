class Type:

    def __init__(self, python_type, cpp_type, cpp_include=None):
        self.python_type = python_type
        self.cpp_type = cpp_type
        self.cpp_include = cpp_include if cpp_include else []

    def __repr__(self):
        return 'Type(cpp_type={0})'.format(self.cpp_type)


IntT = Type(int, 'int')
FloatT = Type(float, 'float')

_matcher = {
    'int': IntT,
    'float': FloatT
}


def register_type(type_name, type):
    _matcher[type_name] = type


def match_type(str_type):
    return _matcher.get(str_type)