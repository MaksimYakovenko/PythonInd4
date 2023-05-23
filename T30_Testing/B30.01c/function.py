def function(x, eps):
    assert abs(x) < 1
    assert eps > 0

    a = 1
    s = a
    k = 1

    while abs(a) > eps:
        k += 1
        a *= -k * x / (k - 1)
        s += a

    return s
