from sympy import *
from sympy.logic.boolalg import *
from typing import Tuple, FrozenSet, Optional, Set, AnyStr, Dict, SupportsInt
import re
import sys
from sympy.parsing.sympy_parser import *
import discrete_rules

# a, b, c, p, q, r, s, t, m, n = symbols('a b c p q r s t m n')


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
    result_from_rules1, rule, arg = find_a_rule(expr, discrete_rules.rules1, exclusion_rules, exclusion_args)
    if result_from_rules1:
        return result_from_rules1, rule, arg
    else:
        return find_a_rule(expr, discrete_rules.rules2, exclusion_rules, exclusion_args)


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


# def multireplace(string, replacements):
#     """
#     Given a string and a replacement map, it returns the replaced string.
#
#     :param str string: string to execute replacements on
#     :param dict replacements: replacement dictionary {value to find: value to replace}
#     :rtype: str
#
#     """
#     # Place longer ones first to keep shorter substrings from matching
#     # where the longer ones should take place
#     # For instance given the replacements {'ab': 'AB', 'abc': 'ABC'} against
#     # the string 'hey abc', it should produce 'hey ABC' and not 'hey ABc'
#     substrs = sorted(replacements, key=len, reverse=True)
#
#     # Create a big OR regex that matches any of the substrings to replace
#     regexp = re.compile('|'.join(map(re.escape, substrs)))
#
#     # For each match, look up the new string in the replacements
#     return regexp.sub(lambda match: replacements[match.group(0)], string)


# def create_rules(rules: Set[SRule], p: AnyStr, q: AnyStr, r: AnyStr) -> Set[SRule]:
#     l_rules = list(rules)
#     for i, (r1, r2) in enumerate(l_rules):
#         replacements = {'r': r, 'q': q, 'p': p}
#         new_r1 = multireplace(r1, replacements)
#         new_r2 = multireplace(r2, replacements)
#         l_rules[i] = (new_r1, new_r2)
#     return set(l_rules)
