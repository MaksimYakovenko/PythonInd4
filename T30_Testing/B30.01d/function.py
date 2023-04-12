def function(x, eps):
    assert abs(x) < 1
    assert eps > 0

    a = 1
    s = a

    while abs(a) > eps:
        a *= - x ** 2
        s += a

    return s
