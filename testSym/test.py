from discrete import *
from discrete_rules import *
from rule import *
from reduce import *

# ((m & n) & p) | ((m & p) & ~p) | ~n -> (m ∧ p) ∨ ¬n
# (a & ~b & b & ~c) | (a & ~b & ~b & c) | (~a & b & b & ~c) | (~a & b & ~b & c) -> (a & ~b & c) | (~a & b & ~c)
# g = parse_expr('(a & ~b & b & ~c) | (a & ~b & ~b & c) | (~a & b & b & ~c) | (~a & b & ~b & c)',
#                local_dict={'p': p, 'q': q, 'r': r, 's': s, 't': t, 'm': m, 'n': n})
#
# solutions, rules = reduce(g)
#
# print("++++++++++++++++++++++++++++++")
#
# for s, r in zip(solutions, rules):
#     print(r[0])
#     pprint(s)

# expr = parse_expr('(x >> y) | (z >> y)')
expr = parse_expr('x | z | (y & z)')
# expr2 = parse_expr('x & (t | (x & z))')

rules = Rule.generate_rules(expr)
for rule in rules:
    print("rule:", rule)
    new_ex = Rule.rule_replace(expr, (rule[0], rule[1]))[0]
    pprint(new_ex)


# print(Reduce.simpler(expr2, expr))

# min_ex, rules, expr_list = Reduce.reduce(expr)
# print("-------------------")
# pprint(min_ex)
# for ex, r in zip(expr_list, rules):
#     print(r)
#     pprint(ex)
