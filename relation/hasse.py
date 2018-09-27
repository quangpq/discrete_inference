from lattice import Lattice
import re


def _parse_set(text: str):
    tok = re.compile("{[0-9, ]*}")
    text = text.strip()
    results = tok.findall(text)

    if results.__len__() != 1:
        return None
    a_str = results[0][1:-1]
    set_a = set(a_str.split(","))

    try:
        set_a = set(map(lambda x: int(x.strip()), set_a))
    except ValueError:
        return None

    return set_a


def hasse_from_string(pset: str, order: str):
    a_set = _parse_set(pset)
    if a_set is None:
        return None

    a_list = sorted(a_set)
    return hasse(a_list, order)


def hasse(pset: list, order: str):
    if order == 'lcm':
        lat = Lattice(pset, lcm)
    elif order == 'gcd':
        lat = Lattice(pset, gcd)
    elif order == 'lt':
        lat = Lattice(pset, lt)
    elif order == 'gt':
        lat = Lattice(pset, gt)
    elif order == 'lte':
        lat = Lattice(pset, lte)
    elif order == 'gte':
        lat = Lattice(pset, gte)
    elif order == 'mod':
        lat = Lattice(pset, mod)
    else:
        return None

    return lat.hasse()


def gcd(a, b):
    return b == gcd_value(a, b)


def gcd_value(a, b):
    while b > 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    return b == lcm_value(a, b)


def lcm_value(a, b):
    return a * b / gcd_value(a, b)


def mod(a, b):
    return b % a == 0


def gt(a, b):
    return a > b


def lt(a, b):
    return a < b


def gte(a, b):
    return a >= b


def lte(a, b):
    return a <= b


if __name__ == "__main__":
    s = "{1, 2, 3, 4} "
    print(hasse_from_string(s, "gt"))
