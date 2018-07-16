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

expr = parse_expr('x & (t | (x & z & (x | y)))')
expr2 = parse_expr('x & (t | (x & z))')

# rules = Rule.generate_rules(expr)
#
# for rule in rules:
#     print("rule:", rule)
#     print(Rule.rule_replace(expr, (rule[0], rule[1]))[0])


print(Reduce.simpler(expr2, expr))
