from typing import Tuple, Set, List
from itertools import combinations

Relation = Set[Tuple]


def check_relation(r: Relation, set_a: Set):
    reflexive_of_r = reflexive(r, set_a)
    symmetric_of_r = symmetric(r)
    antisymmetric_of_r = antisymmetric(r)
    transitive_of_r = transitive(r)

    return '<span>Quan hệ có các tính chất:</span><ul>' + \
           '<li>' + str_reflexive(reflexive_of_r) + '</li>' + \
           '<li>' + str_symmetric(symmetric_of_r) + '</li>' + \
           '<li>' + str_antisymmetric(antisymmetric_of_r) + '</li>' + \
           '<li>' + str_transitive(transitive_of_r) + '</li></ul>'


def check_order_relation(r: Relation, set_a: Set):
    reflexive_of_r = reflexive(r, set_a)
    antisymmetric_of_r = antisymmetric(r)
    transitive_of_r = transitive(r)
    full_order_of_r = check_full_order_relation(r, set_a)

    negative_str = '<span>Quan hệ không phải một quan hệ thứ tự vì:</span><ul>'
    if reflexive_of_r[0] and antisymmetric_of_r[0] and transitive_of_r[0]:
        return True, '<span>Quan hệ là một quan hệ thứ tự vì:</span><ul>' + \
               '<li>' + str_reflexive(reflexive_of_r) + '</li>' + \
               '<li>' + str_antisymmetric(antisymmetric_of_r) + '</li>' + \
               '<li>' + str_transitive(transitive_of_r) + '</li>' + \
               '<li>' + str_full_order_relation(full_order_of_r) + '</li></ul>'
    elif not reflexive_of_r[0]:
        negative_str += '<li>' + str_reflexive(reflexive_of_r) + '</li>'
    elif not antisymmetric_of_r[0]:
        negative_str += '<li>' + str_antisymmetric(antisymmetric_of_r) + '</li>'
    elif not transitive_of_r[0]:
        negative_str += '<li>' + str_transitive(transitive_of_r) + '</li>'

    negative_str += "</ul>"
    return False, negative_str


def str_full_order_relation(result: (bool, List)):
    string = ''
    mes = result[1]
    if result[0]:
        string += '<span>Quan hệ là thứ tự toàn phần, vì:</span><ul>'
        for m in mes:
            string += f"<li>Với {m[0]} ∈ R, ta có {m[1]} ∈ R</li>"
    else:
        string += '<span>Quan hệ là thứ tự bán phần, vì:</span><ul>'
        for m in mes:
            string += f'<li>Với {m[0]} ∈ R, ta có {m[1]} ∉ R</li>'
    string += "</ul>"
    return string


def check_full_order_relation(r: Relation, set_a: Set) -> (bool, List):
    """Kiểm tra quan hệ có phải thứ tự toàn phần trên set_a không?"""
    reflexive_tuple = []
    for x, y in combinations(set_a, 2):
        if (y, x) not in r:
            return False, [((x, y), (y, x))]
        reflexive_tuple.append(((x, y), (y, x)))
    return True, reflexive_tuple


def check_equivalence_relation(r: Relation, set_a: Set):
    reflexive_of_r = reflexive(r, set_a)
    symmetric_of_r = symmetric(r)
    transitive_of_r = transitive(r)

    negative_str = '<span>Quan hệ không phải một quan hệ tương đương vì:</span><ul>'
    if reflexive_of_r[0] and symmetric_of_r[0] and transitive_of_r[0]:
        return True, '<span>Quan hệ là một quan hệ tương đương vì:</span><ul>' + \
               '<li>' + str_reflexive(reflexive_of_r) + '</li>' + \
               '<li>' + str_symmetric(symmetric_of_r) + '</li>' + \
               '<li>' + str_transitive(transitive_of_r) + '</li></ul>'
    elif not reflexive_of_r[0]:
        negative_str += '<li>' + str_reflexive(reflexive_of_r) + '</li>'
    elif not symmetric_of_r[0]:
        negative_str += '<li>' + str_symmetric(symmetric_of_r) + '</li>'
    elif not transitive_of_r[0]:
        negative_str += '<li>' + str_transitive(transitive_of_r) + '</li>'

    negative_str += '</ul>'
    return False, negative_str


def str_reflexive(result: (bool, List)):
    string = ''
    mes = result[1]
    if result[0]:
        string += '<span>Quan hệ có tính phản xạ, vì:</span><ul>'
        for m in mes:
            string += f"<li>Với {m[0]} ∈ A, ta có {m[1]} ∈ R</li>"
    else:
        string += 'Quan hệ không có tính phản xạ, vì:</span><ul>'
        for m in mes:
            string += f'<li>Với {m[0]} ∈ A, ta có {m[1]} ∉ R</li>'
    string += "</ul>"
    return string


def reflexive(r: Relation, set_a: Set) -> (bool, List):
    """Kiểm tra tính phản xạ của r trên set_a"""
    reflexive_tuple = []
    for x in set_a:
        if (x, x) not in r:
            return False, [(x, (x, x))]
        reflexive_tuple.append((x, (x, x)))
    return True, reflexive_tuple


def str_symmetric(result: (bool, List)):
    string = ''
    mes = result[1]
    if result[0]:
        string += '<span>Quan hệ có tính đối xứng, vì:</span><ul>'
        for m in mes:
            string += f'<li>Với {m[0]} ∈ R, ta có {m[1]} ∈ R</li>'
    else:
        string += '<span>Quan hệ không có tính đối xứng, vì:</span><ul>'
        for m in mes:
            string += f'<li>Với {m[0]} ∈ R, ta có {m[1]} ∉ R</li>'
    string += "</ul>"
    return string


def symmetric(r: Relation) -> (bool, List):
    """Kiểm tra tính đối xứng của r"""
    symmetric_tuple = []
    checked_tuple = set()

    for x, y in r:
        if x == y or (x, y) in checked_tuple:
            continue
        if (y, x) not in r:
            return False, [((x, y), (y, x))]
        symmetric_tuple.append(((x, y), (y, x)))
        checked_tuple.add((y, x))
    return True, symmetric_tuple


def str_antisymmetric(result: (bool, List)):
    string = ''
    mes = result[1]
    if result[0]:
        string += '<span>Quan hệ có tính phản xứng, vì:</span><ul>'
        for m in mes:
            string += f'<li>Với {m[0]} ∈ R, ta có {m[1]} ∉ R</li>'
    else:
        string += '<span>Quan hệ không có tính phản xứng, vì:</span><ul>'
        for m in mes:
            string += f'<li>Với {m[0]} ∈ R, ta có {m[1]} ∈ R</li>'
    string += "</ul>"
    return string


def antisymmetric(r: Relation) -> (bool, List):
    """Kiểm tra tính phản xứng của r"""
    antisymmetric_tuple = []
    for x, y in r:
        if x == y:
            continue
        if (y, x) in r:
            return False, [((x, y), (y, x))]
        antisymmetric_tuple.append(((x, y), (y, x)))
    return True, antisymmetric_tuple


def str_transitive(result: (bool, List)):
    string = ''
    mes = result[1]
    if result[0]:
        string += '<span>Quan hệ có tính bắc cầu, vì:</span><ul>'
        for m in mes:
            string += f'<li>Với {m[0][0]},{m[0][1]} ∈ R, ta có {m[1]} ∈ R</li>'
    else:
        string += '<span>Quan hệ không có tính bắc cầu, vì:</span><ul>'
        for m in mes:
            string += f'<li>Với {m[0][0]},{m[0][1]} ∈ R, ta có {m[1]} ∉ R</li>'
    string += "</ul>"
    return string


def transitive(r: Relation) -> (bool, List):
    """Kiểm tra tính bắc cầu của r trên set_a"""
    transitive_tuple = []
    for x, y in r:
        equal_y_tuple = set(filter(lambda _x: _x[0] == y, r))
        for x1, y1 in equal_y_tuple:
            if (x, y) == (x1, y1):
                continue
            if (x, y1) not in r:
                return False, [(((x, y), (x1, y1)), (x, y1))]
            transitive_tuple.append((((x, y), (x1, y1)), (x, y1)))
    return True, transitive_tuple


if __name__ == '__main__':
    # a = {1, 2, 3, 4, 5, 6}
    # re = {(1, 1), (1, 2), (2, 1), (2, 2), (3, 3), (4, 4), (4, 5), (5, 4), (5, 5), (6, 6)}
    a = {3, 6, 9, 15, 18, 30}
    re = {(3, 3), (6, 3), (9, 3), (15, 3), (18, 3), (30, 3), (6, 6), (18, 6), (30, 6), (9, 6), (9, 9), (18, 9),
          (15, 6), (15, 9), (15, 15),
          (18, 18), (18, 15), (30, 9), (30, 15), (30, 18), (30, 30)}
    print(reflexive(re, a))
    print(symmetric(re))
    print(transitive(re))
    print(antisymmetric(re))
    print(check_order_relation(re, a)[1])
    print(check_equivalence_relation(re, a)[1])
