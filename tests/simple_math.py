__all__ = ['func1', 'func3']


def func1(a, b, c):
    """
    :type a: int
    :type b: int
    :type c: int
    :rtype: int
    """
    return a + b + c


def func2(a, b):
    """
    :type a: int
    :type b: int
    :rtype: int
    """
    return func1(a, b, 1) + a + b


def func3(a, b, c, d):
    """
    :type a: int
    :type b: int
    :type c: int
    :type d: int
    :rtype: int
    """
    return func1(a, b, c) - func2(a, d)