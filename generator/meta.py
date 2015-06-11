class Type:

    def __init__(self, python_type, cpp_type):
        self.python_type = python_type
        self.cpp_type = cpp_type

IntT = Type(int, 'int')
FloatT = Type(float, 'float')


def match_type(str_type):
    matcher = {
        'int' : IntT,
        'float' : FloatT
    }
    return matcher.get(str_type)