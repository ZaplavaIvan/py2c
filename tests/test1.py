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
        d += 1
        a = 0
        if (d % 2) and (a < 10 and (a > 5 or a < 3)) and 3 == 3 or a == 1:
            x += (a + b) * c
            continue
        elif d == 3 or d == 7:
            x *= 8
            break
        elif d == 11 or d == 231:
            x *= 8
        else:
            x -= a - b
            x += 1
    return x


def func2(b, c):
    """
    :type b: int
    :type c: int
    :rtype: int
    """
    if not (c + 1):
        c = 8

    b = 100

    while b > 0:
        b -= 1
        if (b + 1) == 8:
            break
    else:
        c = 100

    while b > 0:
        b -= 1
    else:
        c = 1

    return b + c


def func3(a, b, c):
    """
    :type a: int
    :type b: float
    :type c: float
    :rtype: float
    """
    d = 0
    s = 0.0
    while d < 100:
        d += 1
        s += b / c
    return s


def func4():
    """
    :rtype: int
    """
    return func1(1, 2, 3) + func2(3, 4)
