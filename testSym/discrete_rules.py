from sympy import *
from sympy.logic.boolalg import *
from typing import Tuple, FrozenSet, Optional, Set, AnyStr, Dict, SupportsInt

a, b, c, p, q, r, s, t, m, n = symbols('a b c p q r s t m n')


rules1 = [
    ('Phủ định của phủ định', lambda arg: arg.func is Not and arg.args[0].func is Not,
     lambda expr, arg: expr.replace(arg, arg.args[0].args[0])),

    ('Luật lũy đẳng', lambda arg: arg.func is Or and arg.args.__len__() > set(arg.args).__len__(),
     lambda expr, arg: expr.replace(arg, Or(*set(arg.args)))),
    ('Luật lũy đẳng', lambda arg: arg.func is And and arg.args.__len__() > set(arg.args).__len__(),
     lambda expr, arg: expr.replace(arg, And(*set(arg.args)))),

    # ('Luật lũy đẳng', lambda arg: arg.func is Or and arg.args[0] == arg.args[1],
    #  lambda expr, arg: expr.replace(arg, arg.args[0])),
    # ('Luật lũy đẳng', lambda arg: arg.func is And and arg.args[0] == arg.args[1],
    #  lambda expr, arg: expr.replace(arg, arg.args[0])),

    ('Luật De Morgan', lambda arg: arg.func is Not and arg.args[0].func is And,
     lambda expr, arg: expr.replace(arg, Or(
         *list(map(lambda x: Not(x), list(arg.args[0].args)))))),
    ('Luật De Morgan', lambda arg: arg.func is Not and arg.args[0].func is Or,
     lambda expr, arg: expr.replace(arg, And(
         *list(map(lambda x: Not(x), list(arg.args[0].args)))))),

    ('Luật kéo theo', lambda arg: arg.func is Implies,
     lambda expr, arg: expr.replace(arg, Or(Not(arg.args[0]), arg.args[1]))),

    ('Luật về phần tử bù',
     lambda arg: arg.func is And and any(
         x for x in arg.args if x.func is Not and any(y for y in arg.args if y == x.args[0])),
     lambda expr, arg: negation_law(expr, arg)),
    ('Luật về phần tử bù',
     lambda arg: arg.func is Or and any(
         x for x in arg.args if x.func is Not and any(y for y in arg.args if y == x.args[0])),
     lambda expr, arg: negation_law(expr, arg)),

    ('Luật thống trị', lambda arg: arg.func is Or and [x for x in arg.args if x.func is BooleanTrue].__len__() > 0,
     lambda expr, arg: expr.replace(arg, true)),
    ('Luật thống trị', lambda arg: arg.func is And and [x for x in arg.args if x.func is BooleanFalse].__len__() > 0,
     lambda expr, arg: expr.replace(arg, false)),

    ('Luật trung hòa', lambda arg: arg.func is Or and [x for x in arg.args if x.func is BooleanFalse].__len__() > 0,
     lambda expr, arg: identity_law(expr, arg)),
    ('Luật trung hòa', lambda arg: arg.func is And and [x for x in arg.args if x.func is BooleanTrue].__len__() > 0,
     lambda expr, arg: identity_law(expr, arg)),

    ('Luật hấp thụ', lambda arg: arg.func is Or and any(
        x for x in arg.args if x.func is And and any(y for y in arg.args if list(x.args).__contains__(y))),
     lambda expr, arg: absorption_law(expr, arg)),
    ('Luật hấp thụ', lambda arg: arg.func is And and any(
        x for x in arg.args if x.func is Or and any(y for y in arg.args if list(x.args).__contains__(y))),
     lambda expr, arg: absorption_law(expr, arg)),

    ('Luật phân phối', lambda arg: arg.func is And and any(
        x for x in arg.args if
        x.func is Or and any(
            y for y in arg.args if y.func is Or and x != y and set(y.args).intersection(set(x.args)).__len__() > 0)),
     lambda expr, arg: revert_distributive_law(expr, arg)),
    ('Luật phân phối', lambda arg: arg.func is Or and any(x for x in arg.args if x.func is And and any(
        y for y in arg.args if y.func is And and x != y and set(y.args).intersection(set(x.args)).__len__() > 0)),
     lambda expr, arg: revert_distributive_law(expr, arg)),
]

# tăng kích thước biểu thức
rules2 = [
    ('Luật phân phối 2', lambda arg: arg.func is And and any(
        x for x in arg.args if
        x.func is Or),
     lambda expr, arg: absorption_law(expr, arg)),
    ('Luật phân phối 2', lambda arg: arg.func is Or and any(x for x in arg.args if x.func is And),
     lambda expr, arg: absorption_law(expr, arg)),
]


def negation_law(expr: BooleanFunction, arg: BooleanFunction) -> BooleanFunction:
    args = list(arg.args)
    remove_args = set(x for x in arg.args if any(
        y for y in arg.args if (y.func is Not and y.args[0] == x) or (x.func is Not and x.args[0] == y)))

    for ag in arg.args:
        if remove_args.__contains__(ag):
            args.remove(ag)

    bool_var = false if arg.func is And else true

    args.append(bool_var)
    sub_expr = arg.func(*args)
    return expr.replace(arg, sub_expr)


def absorption_law(expr: BooleanFunction, arg: BooleanFunction) -> BooleanFunction:
    args = list(arg.args)
    remove_func = And if arg.func is Or else Or
    remove_args = set(
        x for x in arg.args if x.func is remove_func and any(y for y in arg.args if list(x.args).__contains__(y)))

    for ag in arg.args:
        if remove_args.__contains__(ag):
            args.remove(ag)

    sub_expr = arg.func(*args)
    return expr.replace(arg, sub_expr)


def distributive_law(expr: BooleanFunction, arg: BooleanFunction) -> BooleanFunction:
    args = list(arg.args)
    func = And if arg.func is Or else Or

    small_args = args
    big_args = max([x for x in arg.args if x.func is func], key=lambda x: x.args.__len__())
    small_args.remove(big_args)

    # tìm biểu thức trong small_args có phàn trùng lớn nhất với big_args
    count = 0
    best_args = small_args[0]
    big_args_set = normalise_args_set(set(big_args.args))
    for a in small_args:
        if a.func is Symbol:
            count_a = 1 if big_args_set.__contains__(a) else 0
        else:
            set_a = normalise_args_set(set(a.args))
            count_a = (big_args_set.intersection(set_a)).__len__()

        if count_a > count:
            count = count_a
            best_args = a

    small_args.remove(best_args)

    new_args = list(map(lambda x: arg.func(best_args, x), list(big_args.args)))
    sub_expr = func(*new_args)
    small_args.append(sub_expr)

    return expr.replace(arg, arg.func(*small_args))


def revert_distributive_law(expr: BooleanFunction, arg: BooleanFunction) -> Optional[BooleanFunction]:
    absorption_var = set()
    func = And if arg.func is Or else Or

    for i, ag in enumerate(arg.args):
        if ag.func is func:
            for j, ag_2 in enumerate(arg.args, start=i + 1):
                v = set(ag.args).intersection(set(ag_2.args))
                if v.__len__() > 0:
                    absorption_var = v
                    break

    absorption_list = set()
    non_absorption_list = []

    for ag in arg.args:
        if ag.func is func and absorption_var.issubset(set(ag.args)):
            a = list(set(ag.args).difference(absorption_var))
            absorption_list.add(func(*a))
        else:
            non_absorption_list.append(ag)

    if absorption_list.__len__() == 0:
        return None

    sub_absorption = func(*absorption_var, arg.func(*absorption_list))
    sub_expr = arg.func(sub_absorption, *non_absorption_list)
    return expr.replace(arg, sub_expr)


def identity_law(expr: BooleanFunction, arg: BooleanFunction) -> BooleanFunction:
    args = list(arg.args)
    remove_args = false if arg.func is Or else true

    for ag in arg.args:
        if remove_args == ag:
            args.remove(ag)

    sub_expr = arg.func(*args)
    return expr.replace(arg, sub_expr)


def normalise_args_set(s: Set[BooleanFunction]) -> Set[BooleanFunction]:
    item_to_remove = set(item for item in s if item.func is Not)
    s = s.difference(item_to_remove)
    new_items = set()
    for i in item_to_remove:
        new_items = new_items.union(set(i.args))

    return s.union(new_items)
