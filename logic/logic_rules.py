from sympy import *
from sympy.logic.boolalg import *
from expr_tree import convert_to_not, revert_not, remove_double_not
import itertools


def double_negative(_expr: BooleanFunction) -> list:
    """Phủ định của phủ định"""
    not_expr = _expr.atoms(Not)
    not_expr = set(filter(lambda _ex: _ex.args[0].func is Not, not_expr))

    results = list(map(lambda _ex: ("Phủ định của phủ định", _ex, _ex.args[0].args[0]), not_expr))
    return results


def constant_negative(_expr: BooleanFunction) -> list:
    """Luật phủ định"""
    not_expr = _expr.atoms(Not)
    not_expr = set(filter(lambda _ex: _ex.args[0].func is BooleanFalse or _ex.args[0].func is BooleanTrue, not_expr))

    results = list(
        map(lambda _ex: ("Luật phủ định", _ex, true if _ex.args[0].func is BooleanFalse else false), not_expr))
    return results


def negation_law(_expr: BooleanFunction) -> list:
    """Luật về phần tử bù"""

    def apply(ex, _remove_ex, _remove_not_ex):
        nonlocal results
        _remove_not_ex = set(map(lambda _x: Not(_x), _remove_ex))
        new_args = set(ex.args).difference(_remove_ex).difference(_remove_not_ex)

        if new_args.__len__() > 0:
            new_args.add(true if ex.func is Or else false)
            new_ex = ex.func(*new_args)
        else:
            new_ex = true if ex.func is Or else false
        results.append(("Luật về phần tử bù", ex, new_ex))

    parent_expr = _expr.atoms(And, Or)
    results = list()
    for _ex in parent_expr:
        not_ex, other_ex = sift(_ex.args, lambda _x: _x.func is Not, binary=True)
        inner_not_ex = set(map(lambda _x: _x.args[0], not_ex))
        remove_ex = set(other_ex).intersection(inner_not_ex)
        if remove_ex.__len__() > 0:
            remove_not_ex = set(map(lambda _x: Not(_x), remove_ex))
            apply(_ex, remove_ex, remove_not_ex)

        if other_ex.__len__() > 1:
            length = 1
            while length < other_ex.__len__():
                length += 1
                for sub_expr in itertools.combinations(other_ex, length):
                    temp_ex = _ex.func(*sub_expr)
                    temp_not_ex = Not(temp_ex)
                    if temp_not_ex in not_ex:
                        apply(_ex, set(sub_expr), {temp_not_ex})

        double_not_ex, single_not_ex = sift(not_ex, lambda _x: _x.args[0].func is Not, binary=True)
        if double_not_ex.__len__() > 0:
            outer_not_ex = set(map(lambda _x: _x.args[0], double_not_ex))
            remove_ex = set(single_not_ex).intersection(outer_not_ex)
            if remove_ex.__len__() > 0:
                remove_not_ex = set(map(lambda _x: Not(_x), remove_ex))
                apply(_ex, remove_ex, remove_not_ex)

    return results


def domination_and_identity(_expr: BooleanFunction) -> list:
    """Luật thống trị + Luật trung hòa"""
    parent_expr = _expr.atoms(And, Or)
    results = list()

    for _ex in parent_expr:
        true_args, new_args = sift(_ex.args, lambda _x: _x.func is BooleanTrue, binary=True)

        if true_args.__len__() > 0:
            if _ex.func is Or:
                results.append(("Luật thống trị", _ex, true))
            else:
                if new_args.__len__() > 0:
                    new_ex = _ex.func(*new_args)
                else:
                    new_ex = true
                results.append(("Luật trung hòa", _ex, new_ex))
            continue

        false_args, new_args = sift(_ex.args, lambda _x: _x.func is BooleanFalse, binary=True)

        if false_args.__len__() > 0:
            if _ex.func is And:
                results.append(("Luật thống trị", _ex, false))
            else:
                if new_args.__len__() > 0:
                    new_ex = _ex.func(*new_args)
                else:
                    new_ex = false
                results.append(("Luật trung hòa", _ex, new_ex))

    return results


def idempotent(_expr: BooleanFunction) -> list:
    """Luật lũy đẳng"""
    parent_expr = _expr.atoms(And, Or)
    results = list()
    for _ex in parent_expr:
        args_set = list(dict.fromkeys(_ex.args))
        if args_set.__len__() < _ex.args.__len__():
            new_ex = _ex.func(*args_set)
            results.append(("Luật lũy đẳng", _ex, new_ex))

    return results


def absorption(_expr: BooleanFunction) -> list:
    """Luật hấp thụ"""
    parent_expr = _expr.atoms(And, Or)
    results = list()
    for _ex in parent_expr:
        op_func = Or if _ex.func is And else And
        inner_ex, other_args = sift(_ex.args, lambda _x: _x.func is op_func, binary=True)
        if inner_ex.__len__() < 1:
            continue

        other_args_set = set(other_args)
        for in_ex in inner_ex:
            in_args_set = set(in_ex.args)
            new_args = in_args_set.intersection(other_args_set)
            if new_args.__len__() > 0:
                args = list(_ex.args)
                args.remove(in_ex)
                new_ex = _ex.func(*args)
                results.append(("Luật hấp thụ", _ex, new_ex))

        if inner_ex.__len__() > 1:
            for _ex1, _ex2 in itertools.combinations(inner_ex, 2):
                new_args = set(_ex1.args).intersection(set(_ex2.args))
                remove_args = max(_ex1, _ex2, key=lambda _x: _x.args.__len__())
                min_args = min(_ex1, _ex2, key=lambda _x: _x.args.__len__())

                if new_args.__len__() == min_args.args.__len__():
                    args = list(_ex.args)
                    args.remove(remove_args)
                    new_ex = _ex.func(*args)
                    results.append(("Luật hấp thụ", _ex, new_ex))

    return results


def conditional(_expr: BooleanFunction) -> list:
    """Luật kéo theo"""
    results = list()

    not_expr = _expr.atoms(Not)
    for _exp in not_expr:
        if _exp.args[0].func is Implies:
            new_ex = And(_exp.args[0].args[0], Not(_exp.args[0].args[1]))
            results.append(("Luật kéo theo", _exp, new_ex))

    implies_expr = _expr.atoms(Implies)
    for _exp in implies_expr:
        new_ex = Or(Not(_exp.args[0]), _exp.args[1])
        results.append(("Luật kéo theo", _exp, new_ex))

    return results


def distribution_expand(_expr: BooleanFunction) -> list:
    """Luật phân phối"""
    results = list()
    parent_expr = _expr.atoms(And, Or)
    for _ex in parent_expr:
        op_func = Or if _ex.func is And else And
        op_ex, other_args = sift(_ex.args, lambda _x: _x.func is op_func, binary=True)

        if op_ex.__len__() < 1:
            continue
        elif op_ex.__len__() == 1:
            # p & q & (r | t)
            length = 0
            right_args = list(op_ex[0].args)

            while length < other_args.__len__():
                length += 1
                for sub_expr in itertools.combinations(other_args, length):
                    left_args = _ex.func(*sub_expr)
                    sub_args = list(map(lambda _x: _ex.func(left_args, _x), right_args))
                    new_distribution_expr = op_func(*sub_args)

                    _, redundant_args = sift(other_args, lambda _x: _x in sub_expr, binary=True)

                    if redundant_args.__len__() > 0:
                        new_args = [new_distribution_expr, *redundant_args]
                        new_expr = _ex.func(*new_args)
                    else:
                        new_expr = new_distribution_expr
                    results.append(("Luật phân phối", _ex, new_expr))

        elif op_ex.__len__() >= 2:
            # (p | q) & (r | t)
            for _ex1, _ex2 in itertools.combinations(op_ex, 2):
                left_args = list(_ex1.args)
                right_args = list(_ex2.args)
                if left_args.__len__() <= 3 or right_args.__len__() <= 3:
                    sub_args = [_ex.func(lhs, rhs) for lhs, rhs in itertools.product(left_args, right_args)]
                    _, other_inner = sift(op_ex, lambda _x: _x == _ex1 or _x == _ex2, binary=True)
                    new_distribution_expr = op_func(*sub_args)
                    if other_args.__len__() > 0 or other_inner.__len__() > 0:
                        new_args = [new_distribution_expr, *other_args, *other_inner]
                        new_expr = _ex.func(*new_args)
                    else:
                        new_expr = new_distribution_expr
                    results.append(("Luật phân phối", _ex, new_expr))

    return results


def distribution_reduce(_expr: BooleanFunction) -> list:
    """Luật phân phối"""
    results = list()

    parent_expr = _expr.atoms(And, Or)
    for _ex in parent_expr:
        op_func = Or if _ex.func is And else And
        inner_ex, other_args = sift(_ex.args, lambda _x: _x.func is op_func, binary=True)
        if inner_ex.__len__() > 1:
            length = 1
            while length < inner_ex.__len__():
                length += 1
                for sub_expr in itertools.combinations(inner_ex, length):
                    sub_args = list(map(lambda _x: set(_x.args), sub_expr))
                    dup_args = sub_args[0].intersection(*sub_args[1:])

                    if dup_args.__len__() > 0 and dup_args not in sub_args:
                        new_inner_big_args = list()
                        for sub in sub_args:
                            new_inner_args = sub.difference(dup_args)
                            new_inner_big_args.append(op_func(*new_inner_args))

                        new_inner_big_expr = _ex.func(*new_inner_big_args)
                        dup_args.add(new_inner_big_expr)
                        new_distributed_expr = op_func(*dup_args)

                        new_args = [new_distributed_expr]
                        if other_args.__len__() > 0:
                            new_args.extend(other_args)

                        if inner_ex.__len__() > length:
                            _, new_inner = sift(inner_ex, lambda _x: _x in sub_expr, binary=True)
                            new_args.extend(new_inner)

                        new_ex = _ex.func(*new_args)
                        results.append(("Luật phân phối", _ex, new_ex))

    return results


def absorption_and_distribution(_expr: BooleanFunction) -> list:
    """Luật phân phối và hấp thụ"""
    parent_expr = _expr.atoms(And, Or)
    results = list()

    for _ex in parent_expr:
        op_func = Or if _ex.func is And else And
        inner_ex, other_args = sift(_ex.args, lambda _x: _x.func is op_func, binary=True)
        if inner_ex.__len__() < 1:
            continue

        not_other_expr_set = set(map(lambda _x: convert_to_not(_x), other_args))
        for in_ex in inner_ex:
            in_args = list(map(lambda _x: remove_double_not(_x), in_ex.args))
            in_args_set = set(in_args)
            dup_not_args = in_args_set.intersection(not_other_expr_set)
            _, other_inner_expr = sift(inner_ex, lambda _x: _x == in_ex, binary=True)

            if dup_not_args.__len__() > 0:
                # p | (~p & q)
                _, new_inner_args = sift(in_args, lambda _x: _x in dup_not_args, binary=True)
                if new_inner_args.__len__() == 0:
                    new_inner_expr = true if _ex.func is Or else false
                    _, new_other_args = sift(other_args, lambda _x: convert_to_not(_x) in dup_not_args, binary=True)
                    new_args = [new_inner_expr, *new_other_args, *other_inner_expr]
                    new_ex = _ex.func(*new_args)
                    results.append(("Luật về phần tử bù", _ex, new_ex))
                    continue
                new_inner_expr = op_func(*new_inner_args)
                new_args = [new_inner_expr, *other_args, *other_inner_expr]
                new_ex = _ex.func(*new_args)
                results.append(("Luật phân phối và hấp thụ", _ex, new_ex))
            else:
                # ~(p & q) | (p & q & r)
                for not_expr in not_other_expr_set:
                    if (not_expr.func is Not and not_expr.args[0].func is Symbol) or (not_expr.func is Symbol):
                        continue
                    not_expr_args = set(not_expr.args)
                    dup_not_args = not_expr_args.intersection(in_args_set)
                    if dup_not_args.__len__() == not_expr_args.__len__():
                        _, new_inner_args = sift(in_ex.args, lambda _x: _x in dup_not_args, binary=True)
                        if new_inner_args.__len__() == 0:
                            continue
                        new_inner_expr = op_func(*new_inner_args)
                        new_args = [new_inner_expr, *other_args, *other_inner_expr]
                        new_ex = _ex.func(*new_args)
                        results.append(("Luật phân phối và hấp thụ", _ex, new_ex))

        if inner_ex.__len__() > 1:
            for _ex1, _ex2 in itertools.combinations(inner_ex, 2):
                if _ex1.args.__len__() == _ex2.args.__len__():
                    continue
                if _ex1.args.__len__() > _ex2.args.__len__():
                    _ex1, _ex2 = _ex2, _ex1
                ex1_not = convert_to_not(_ex1)

                if ex1_not in _ex2.args:
                    new_inner_args = list(_ex2.args)
                    new_inner_args.remove(ex1_not)
                    if new_inner_args.__len__() == 0:
                        continue
                    new_inner_expr = op_func(*new_inner_args)
                    _, other_inner = sift(inner_ex, lambda _x: _x == _ex1 or _x == _ex2, binary=True)
                    new_args = [new_inner_expr, _ex1, *other_args, *other_inner]
                    new_ex = _ex.func(*new_args)
                    results.append(("Luật phân phối và hấp thụ", _ex, new_ex))

    return results


def de_morgan_expand(_expr: BooleanFunction) -> list:
    """Luật De Morgan"""
    results = list()

    parent_expr = _expr.atoms(Not)
    for _ex in parent_expr:
        sub_expr = _ex.args[0]
        if sub_expr.func is Or or sub_expr.func is And:
            op_func = Or if sub_expr.func is And else And
            new_arg = list(map(lambda _x: Not(_x), list(sub_expr.args)))
            new_expr = op_func(*new_arg)
            results.append(("Luật De Morgan", _ex, new_expr))

    return results


def de_morgan_reduce(_expr: BooleanFunction) -> list:
    """Luật De Morgan"""
    results = list()

    parent_expr = _expr.atoms(And, Or)
    for _ex in parent_expr:
        op_func = Or if _ex.func is And else And

        not_args, other_args = sift(_ex.args, lambda _arg: _arg.func is Not, binary=True)
        if not_args.__len__() == 0:
            continue

        not_args = list(map(lambda _arg: _arg.args[0], not_args))

        new_not_expr = Not(op_func(*not_args))

        if other_args.__len__() > 0:
            new_expr = _ex.func(new_not_expr, *other_args)
        else:
            new_expr = new_not_expr
        results.append(("Luật De Morgan", _ex, new_expr))

    return results


if __name__ == '__main__':
    from logic.parse import parse_expr

    # expr_str = '~~(p | q) & (~~p | ~q)'
    # print(double_negative(parse_expr(expr_str)))

    # expr_str = '~~(p | q) & (~~p | ~q | ~1) & ~1'
    # print(constant_negative(parse_expr(expr_str)))

    # expr_str = '~(p | q) & (~p | p) & (p | q)'
    # expr_str = 'p | q | r | ~(p | q)'
    # expr_str = 'q | r | ~p | ~~p'
    # print(negation_law(parse_expr(expr_str)))

    # expr_str = '~(p | q | 1) & (~p | p | p | 0) & (p | q) & 1'
    # expr_str = 'r | (1 & 1)'
    # print(domination_and_identity(parse_expr(expr_str)))

    # expr_str = '~(p | q | 1) & (~p | p | p | 0) & (p | q)'
    # print(idempotent(parse_expr(expr_str)))

    # expr_str = '(p | q | 1) & (~p | p | p | 0) & p'
    # expr_str = '(p | q | 1) & (~p | p | (p & r)) & (p | q)'
    # expr_str = '(p & q) | (p & q & (a | t)) | s'
    # print(absorption(parse_expr(expr_str)))

    # expr_str = '~((p | r) => q) => (q => (t & a))'
    # print(conditional(parse_expr(expr_str)))

    # expr_str = '(p | q) & (p | r) & (p | (q & t))'
    # print(distributive_reduce(parse_expr(expr_str)))

    # expr_str = '(~p | (p & q)) & (p & (~p | q))'
    # expr_str = '~(p & q) | (p & q & t & s) | r'
    # expr_str = 'm & (n | p) & (~m | ~n | p)'
    # expr_str = 'b & (a | b) & (a | ~c)'
    # expr_str = '(a & b) | ~(a | c | ~b)'
    # expr_str = 'p | q | r | (~p & ~q)'
    expr_str = 'r | (~~p & ~~q) | ~p | ~q'
    print(absorption_and_distribution(parse_expr(expr_str)))

    # expr_str = '~(p & q & t & s) | ~(a | b)'
    # print(de_morgan_expand(parse_expr(expr_str)))

    # expr_str = '~(p & q & t & s) | ~(a | b) | c'
    # print(de_morgan_reduce(parse_expr(expr_str)))

    # expr_str = 'p | c | (e & f)'
    # expr_str = '(p & c) | (e & f) | t'
    # expr_str = '(a & b) | (b & ~c) | (d & e)'
    # print(distribution_expand(parse_expr(expr_str)))
