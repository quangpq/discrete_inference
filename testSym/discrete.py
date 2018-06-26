from sympy import *
from sympy.logic.boolalg import *
from typing import Tuple, FrozenSet, Optional, Set, AnyStr, Dict, SupportsInt
import re
from sympy.parsing.sympy_parser import *

a, p, q, r, s, t = symbols('a p q r s t')

Rule = Tuple[FrozenSet, BooleanFunction, BooleanFunction]

SRule = Tuple[AnyStr, AnyStr]

# BRule = Tuple[Dict[SupportsInt: BooleanFunction], BooleanFunction]

rules = {
    (frozenset({p}), ~~p, p),
    (frozenset({p, q}), ~(p & q), ~p | ~q),
    (frozenset({p, r}), ~(p & r), ~p | ~r),
    (frozenset({p, q}), ~(p | q), ~p & ~q),
    (frozenset({p, q}), p & q, q & p),
    (frozenset({p, q}), p | q, q | p),
    (frozenset({p, q, r}), (p & q) & r, p & (q & r)),
    (frozenset({p, q, r}), (p | q) | r, p | (q | r)),
    (frozenset({p, q, r}), p | (q & r), (p | q) & (p | r)),
    (frozenset({p, q, r}), p & (q | r), (p & q) | (p & r)),
    (frozenset({p}), p & p, p),
    (frozenset({p}), p | p, p),
    (frozenset({p, true}), p & true, p),
    (frozenset({p, true}), true & p, p),
    (frozenset({p, false}), p | false, p),
    (frozenset({p, false}), false | p, p),
    (frozenset({p, false}), p & ~p, false),
    (frozenset({p, false}), ~p & p, false),
    (frozenset({p, true}), p | ~p, true),
    (frozenset({p, true}), ~p | p, true),
    (frozenset({p, false}), p & false, false),
    (frozenset({p, false}), false & p, false),
    (frozenset({p, true}), p | true, true),
    (frozenset({p, true}), true | p, true),
    (frozenset({p, q}), p | (p & q), p),
    (frozenset({p, q}), p | (q & p), p),
    (frozenset({p, q}), p & (p | q), p),
    (frozenset({p, q}), p & (q | p), p),
    (frozenset({p, q}), p >> q, ~p & q),
}

rules2 = {
    ('~~p', 'p'),
    ('~(p & q)', '~p | ~q'),
}

rules3 = {
    (frozenset({p, q}), ~(p & q), ~p | ~q),
    (frozenset({p, r}), ~(p & r), ~p | ~r),
    (frozenset({p, false}), p & ~p, false),
}


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


def apply_rule(rule: Rule, expr: str) -> str:
    return expr.replace(str(rule[1]), str(rule[2]))


def find_rule(rules: Set[Rule], expr: str) -> Optional[Rule]:
    for rule in rules:
        if expr.__contains__(str(rule[1])):
            return rule

    return None


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


def create_rules(rules: Set[SRule], p: AnyStr, q: AnyStr, r: AnyStr) -> Set[SRule]:
    l_rules = list(rules)
    for i, (r1, r2) in enumerate(l_rules):
        replacements = {'r': r, 'q': q, 'p': p}
        new_r1 = multireplace(r1, replacements)
        new_r2 = multireplace(r2, replacements)
        l_rules[i] = (new_r1, new_r2)
    return set(l_rules)


rules4 = {
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
}


def negation_law(expr: BooleanFunction, arg: BooleanFunction) -> BooleanFunction:
    args = list(expr.args)
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
    args = list(expr.args)
    remove_func = And if arg.func is Or else Or
    remove_args = set(
        x for x in arg.args if x.func is remove_func and any(y for y in arg.args if list(x.args).__contains__(y)))

    for ag in arg.args:
        if remove_args.__contains__(ag):
            args.remove(ag)

    sub_expr = arg.func(*args)
    return expr.replace(arg, sub_expr)


def absorption_law(expr: BooleanFunction, arg: BooleanFunction) -> BooleanFunction:
    args = list(expr.args)
    func = And if arg.func is Or else Or
    big_args = [x for x in arg.args if x.func is func][0]
    args.remove(big_args)

    small_args = list(map(lambda x: arg.func(*args, x), list(big_args.args)))
    sub_expr = func(*small_args)
    return expr.replace(arg, sub_expr)


def revert_absorption_law(expr: BooleanFunction, arg: BooleanFunction) -> BooleanFunction:
    absorption_var = set()
    func = And if arg.func is Or else Or

    for i, ag in enumerate(arg.args):
        if ag.func is func:
            for j, ag_2 in enumerate(arg.args, start=i+1):
                v = set(ag.args).intersection(set(ag_2.args))
                if v.__len__() > 0:
                    absorption_var = v
                    break

    absorption_list = set()
    non_absorption_list = []

    for ag in arg.args:
        if ag.func is func and absorption_var.issubset(set(ag.args)):
            a = set(ag.args).difference(absorption_var)
            absorption_list = absorption_list.union(a)
        else:
            non_absorption_list.append(ag)

    sub_absorption = func(*absorption_var, arg.func(*absorption_list))
    sub_expr = arg.func(sub_absorption, *non_absorption_list)
    return expr.replace(arg, sub_expr)


def associative_law(expr: BooleanFunction, arg: BooleanFunction) -> BooleanFunction:
    args = list(expr.args)
    remove_args = false if arg.func is Or else true

    for ag in arg.args:
        if remove_args == ag:
            args.remove(ag)

    sub_expr = arg.func(*args)
    return expr.replace(arg, sub_expr)


def check_rules(expr: BooleanFunction):
    for arg in preorder_traversal(expr):
        if arg.func is Symbol:
            continue
        for rule in rules4:
            if rule[1](arg):
                print(rule[0], ":")
                return rule[2](expr, arg)
    return None

# h = q | (~p | ~(p & r))
# create_rules(rules2, 'q', 'p', 'r')
# check_rules(g)

# Add(q, q, p,  evaluate=False)
# with evaluate(False):
#     f = g.replace({j: Or(*list(map(lambda x: Not(x), list(j.args[0].args))))})
