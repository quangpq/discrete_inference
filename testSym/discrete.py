from sympy import *
from sympy.logic.boolalg import *
from typing import Tuple, FrozenSet, Optional, Set, AnyStr, Dict, SupportsInt
import re
import sys
from sympy.parsing.sympy_parser import *

a, b, c, p, q, r, s, t, m, n = symbols('a b c p q r s t m n')


# Rule = Tuple[FrozenSet, BooleanFunction, BooleanFunction]

# SRule = Tuple[AnyStr, AnyStr]

# BRule = Tuple[Dict[SupportsInt: BooleanFunction], BooleanFunction]

# rules = {
#     (frozenset({p}), ~~p, p),
#     (frozenset({p, q}), ~(p & q), ~p | ~q),
#     (frozenset({p, r}), ~(p & r), ~p | ~r),
#     (frozenset({p, q}), ~(p | q), ~p & ~q),
#     (frozenset({p, q}), p & q, q & p),
#     (frozenset({p, q}), p | q, q | p),
#     (frozenset({p, q, r}), (p & q) & r, p & (q & r)),
#     (frozenset({p, q, r}), (p | q) | r, p | (q | r)),
#     (frozenset({p, q, r}), p | (q & r), (p | q) & (p | r)),
#     (frozenset({p, q, r}), p & (q | r), (p & q) | (p & r)),
#     (frozenset({p}), p & p, p),
#     (frozenset({p}), p | p, p),
#     (frozenset({p, true}), p & true, p),
#     (frozenset({p, true}), true & p, p),
#     (frozenset({p, false}), p | false, p),
#     (frozenset({p, false}), false | p, p),
#     (frozenset({p, false}), p & ~p, false),
#     (frozenset({p, false}), ~p & p, false),
#     (frozenset({p, true}), p | ~p, true),
#     (frozenset({p, true}), ~p | p, true),
#     (frozenset({p, false}), p & false, false),
#     (frozenset({p, false}), false & p, false),
#     (frozenset({p, true}), p | true, true),
#     (frozenset({p, true}), true | p, true),
#     (frozenset({p, q}), p | (p & q), p),
#     (frozenset({p, q}), p | (q & p), p),
#     (frozenset({p, q}), p & (p | q), p),
#     (frozenset({p, q}), p & (q | p), p),
#     (frozenset({p, q}), p >> q, ~p & q),
# }
#
# rules2 = {
#     ('~~p', 'p'),
#     ('~(p & q)', '~p | ~q'),
# }
#
# rules3 = {
#     (frozenset({p, q}), ~(p & q), ~p | ~q),
#     (frozenset({p, r}), ~(p & r), ~p | ~r),
#     (frozenset({p, false}), p & ~p, false),
# }


#
# def find_solution(gt):
#     solution = []
#     known_1 = set()
#     known_2 = set()
#     for u in gt:
#         if type(u) is Eq and type(u.args[0]) is Symbol:
#             known_1.add(u)
#         else:
#             known_2.add(u)
#     print(known_1)
#     print(known_2)
#     found = true
#     names = {x.args[0] for x in list(known_1.union(known_2))}
#
#     while found and not kl.issubset(names):
#         found = false
#         names = {x.args[0] for x in list(known_1.union(known_2))}
#         print(names)
#
#         for rule in rules:
#             if rule[0].issubset(names) and not ({rule[1].args[0]}.issubset(names)):
#                 found = true
#                 solution.append(rule)
#                 if rule is Eq and rule.args[0] is symbol:
#                     known_1.add(rule[1])
#                 else:
#                     known_2.add(rule[1])
#
#     print(found)
#     print(known_1)
#     print(known_2)
#
#     return solution


# def apply_rule(rule: Rule, expr: str) -> str:
#     return expr.replace(str(rule[1]), str(rule[2]))


# def find_rule(rules: Set[Rule], expr: str) -> Optional[Rule]:
#     for rule in rules:
#         if expr.__contains__(str(rule[1])):
#             return rule
#
#     return None


def multireplace(string, replacements):
    """
    Given a string and a replacement map, it returns the replaced string.

    :param str string: string to execute replacements on
    :param dict replacements: replacement dictionary {value to find: value to replace}
    :rtype: str

    """
    # Place longer ones first to keep shorter substrings from matching
    # where the longer ones should take place
    # For instance given the replacements {'ab': 'AB', 'abc': 'ABC'} against
    # the string 'hey abc', it should produce 'hey ABC' and not 'hey ABc'
    substrs = sorted(replacements, key=len, reverse=True)

    # Create a big OR regex that matches any of the substrings to replace
    regexp = re.compile('|'.join(map(re.escape, substrs)))

    # For each match, look up the new string in the replacements
    return regexp.sub(lambda match: replacements[match.group(0)], string)


# def create_rules(rules: Set[SRule], p: AnyStr, q: AnyStr, r: AnyStr) -> Set[SRule]:
#     l_rules = list(rules)
#     for i, (r1, r2) in enumerate(l_rules):
#         replacements = {'r': r, 'q': q, 'p': p}
#         new_r1 = multireplace(r1, replacements)
#         new_r2 = multireplace(r2, replacements)
#         l_rules[i] = (new_r1, new_r2)
#     return set(l_rules)


rules1 = [
    ('Phủ định của phủ định', lambda arg: arg.func is Not and arg.args[0].func is Not,
     lambda expr, arg: expr.replace(arg, arg.args[0].args[0])),

    ('Luật lũy đẳng', lambda arg: arg.func is Or and arg.args.__len__() > set(arg.args).__len__(),
     lambda expr, arg: expr.replace(arg, Or(*set(arg.args)))),
    ('Luật lũy đẳng', lambda arg: arg.func is And and arg.args.__len__() > set(arg.args).__len__(),
     lambda expr, arg: expr.replace(arg, And(*set(arg.args)))),

    ('Luật lũy đẳng', lambda arg: arg.func is Or and arg.args[0] == arg.args[1],
     lambda expr, arg: expr.replace(arg, arg.args[0])),
    ('Luật lũy đẳng', lambda arg: arg.func is And and arg.args[0] == arg.args[1],
     lambda expr, arg: expr.replace(arg, arg.args[0])),

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
     lambda expr, arg: identity_law(expr, arg)),

    ('Luật hấp thụ', lambda arg: arg.func is Or and any(
        x for x in arg.args if x.func is And and any(y for y in arg.args if list(x.args).__contains__(y))),
     lambda expr, arg: identity_law(expr, arg)),
    ('Luật hấp thụ', lambda arg: arg.func is And and any(
        x for x in arg.args if x.func is Or and any(y for y in arg.args if list(x.args).__contains__(y))),
     lambda expr, arg: identity_law(expr, arg)),

    ('Luật phân phối', lambda arg: arg.func is And and any(
        x for x in arg.args if
        x.func is Or and any(
            y for y in arg.args if y.func is Or and x != y and set(y.args).intersection(set(x.args)).__len__() > 0)),
     lambda expr, arg: revert_absorption_law(expr, arg)),
    ('Luật phân phối', lambda arg: arg.func is Or and any(x for x in arg.args if x.func is And and any(
        y for y in arg.args if y.func is And and x != y and set(y.args).intersection(set(x.args)).__len__() > 0)),
     lambda expr, arg: revert_absorption_law(expr, arg)),
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


def identity_law(expr: BooleanFunction, arg: BooleanFunction) -> BooleanFunction:
    args = list(arg.args)
    remove_func = And if arg.func is Or else Or
    remove_args = set(
        x for x in arg.args if x.func is remove_func and any(y for y in arg.args if list(x.args).__contains__(y)))

    for ag in arg.args:
        if remove_args.__contains__(ag):
            args.remove(ag)

    sub_expr = arg.func(*args)
    return expr.replace(arg, sub_expr)


def absorption_law(expr: BooleanFunction, arg: BooleanFunction) -> BooleanFunction:
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


def revert_absorption_law(expr: BooleanFunction, arg: BooleanFunction) -> Optional[BooleanFunction]:
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


def associative_law(expr: BooleanFunction, arg: BooleanFunction) -> BooleanFunction:
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


def k_degree(expr: BooleanFunction) -> int:
    args = [arg for arg in postorder_traversal(expr) if
            arg.func is Symbol or arg.func is BooleanFalse or arg.func is BooleanTrue]
    # func_count = [arg for arg in postorder_traversal(expr) if arg.func is BooleanFunction].__len__()

    args_count = args.__len__()
    args_set_count = set(args).__len__()
    return args_count - args_set_count  # + func_count


def reduce(expr: BooleanFunction):
    new_expr = expr
    pprint(new_expr)
    solutions = []
    rules = []
    current_k = k_degree(new_expr)
    print("-------------------------------")
    while new_expr:
        temp_expr, rule, arg = find_rules(new_expr)
        if not temp_expr:
            break
        if check_duplicated_rule(solutions, temp_expr):  # Thuật toán bị rơi vào vòng lặp của các phép biến đổi
            print("LOOP")
            temp_expr, rule, arg = find_rules(new_expr, [rule], [arg])

            if not temp_expr:
                print("{{{{{{")
                clean_up_result(solutions, rules)
                print("}}}}}}")
                break
        new_expr = temp_expr
        solutions.append(new_expr)
        rules.append(rule)
        print("\n")
        pprint(new_expr)
        print(new_expr)
        print("-------------------------------")
        current_k = k_degree(new_expr)
        if current_k == 0:  # tìm được biểu thức tốt nhất
            break

    return solutions, rules


def check_duplicated_rule(a_list, item):
    p_rule = pretty(item)
    for r in a_list:
        if p_rule == pretty(r):
            return True
    return False


def clean_up_result(solutions, rules):
    for s, r in zip(solutions, rules):
        print(r[0])
        pprint(s)
    print("-------------------------------")
    for i, sol in enumerate(reversed(solutions)):
        if i > 1:
            k_before = k_degree(solutions[i - 1])
            k = k_degree(solutions[i])
            if k_before < k:
                rules.remove(rules[i])
                solutions.remove(solutions[i])
                break

    for s, r in zip(solutions, rules):
        print(r[0])
        pprint(s)


def find_rules(expr: BooleanFunction, exclusion_rules=None, exclusion_args=None):
    result_from_rules1, rule, arg = find_a_rule(expr, rules1, exclusion_rules, exclusion_args)
    if result_from_rules1:
        return result_from_rules1, rule, arg
    else:
        return find_a_rule(expr, rules2, exclusion_rules, exclusion_args)


def find_a_rule(expr: BooleanFunction, rules, exclusion_rules=None, exclusion_args=None):
    best_k = sys.maxsize
    best_rule = None
    best_expr = None
    changed_arg = None
    for arg in postorder_traversal(expr):
        if arg.func is Symbol:
            continue
        for rule in rules:
            if exclusion_rules and exclusion_rules.__contains__(
                    rule) and exclusion_args and exclusion_args.__contains__(arg):
                continue
            if rule[1](arg):
                new_expr = rule[2](expr, arg)
                if not new_expr:
                    continue
                k = k_degree(new_expr)
                print(rule[0], ":", k)
                pprint(new_expr)
                if k < best_k:
                    best_k = k
                    best_rule = rule
                    best_expr = new_expr
                    changed_arg = arg
                    print("---", rule[0])
    if best_rule:
        return best_expr, best_rule, changed_arg
    return None, None, None

# def find_a_type_2_rule(expr: BooleanFunction, rules):
#     best_k = sys.maxsize
#     best_rule = None
#     best_expr = None
#     for arg in postorder_traversal(expr):
#         if arg.func is Symbol:
#             continue
#         for rule in rules:
#             if rule[1](arg):
#                 new_expr = rule[2](expr, arg)
#                 k = k_degree(new_expr)
#                 k1 = k_degree(expr)
#                 print(rule[0], ":", new_expr, k1, k)
#                 if k < best_k:  # & k < previous_k:
#                     best_k = k
#                     best_rule = rule
#                     best_expr = new_expr
#                     print(rule[0])
#     if best_rule:
#         return best_expr, best_rule
#     return None, None

# h = q | (~p | ~(p & r))
# create_rules(rules2, 'q', 'p', 'r')
# check_rules(g)

# Add(q, q, p,  evaluate=False)
# with evaluate(False):
#     f = g.replace({j: Or(*list(map(lambda x: Not(x), list(j.args[0].args))))})
# absorption_law(g, g)
