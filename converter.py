from string import ascii_uppercase as letters


def to_tenth(n, base):
    exponent = 0
    res = 0
    for point in str(n)[::-1]:
        if not point.isdigit():
            try:
                point = letters[:base - 10].index(point.upper()) + 10
            except ValueError:
                raise ValueError('СИ не соответсвует числу')
        else:
            point = int(point)
        if point > base:
            raise ValueError('СИ не соответсвует числу')
        res += point * (base ** exponent)
        exponent += 1
    return res


def from_tenth(n, base):
    if n >= base:
        res = ''
        while n > 1:
            left = n % base
            n = (n - left) // base
            if left > 9:
                left = letters[:base - 10][left - 10]
            res = str(left) + res
        res = str(n) + res
        return res
    else:
        return n


def convert(n, base, target):
    if base > 36 or target > 36:
        raise ValueError('СИ не может превышать 36')
    tenth = to_tenth(n, base)
    res = from_tenth(tenth, target)
    return res