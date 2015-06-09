def func1(a, b, c):
    """
    :type a: int
    :type b: int
    :type c: int
    :rtype: int
    """
    d = 0
    x = 0
    while d < 100:
        a = 0
        if d % 2 == 0:
            x += a + b * c
        elif d == 3 or d == 7:
            x *= 8
        else:
            x -= a - b
        d += 1
    return x

def func2(b, c):
    """
    :type b: int
    :type c: int
    :rtype: int
    """
    c = 8
    return b + c