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
        if d % 2 == 0:
            x += a + b * c
            continue
        elif d == 3 or d == 7:
            x *= 8
            break
        else:
            x -= a - b
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