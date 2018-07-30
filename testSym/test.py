from rule import *
from reduce import *

# expr_str2 = 'x & (t | (x & z))'
expr_str2 = '(¬p ∧ ¬q) ∨ ¬p ∨ ¬q'

# coms = Rule.generate_sub_expr(expr)
# print(coms)
# #
# rules, ex_list = Rule.find_all_rules_of_expr_str(expr_str2)
# for rule, ex in zip(rules, ex_list):
#     print("rule:", rule)
#     pprint(ex)

# print(min(rules, key=lambda rul: set(rul[1].atoms(Symbol))))


# print(Reduce.simpler(expr2, expr))
expr_str = '((p >> q) & (q >> r)) >> (p >> r)'  # True
# expr_str = '~(p | q) | ((~p & q)| ~q)'  # ¬(q ∧ p)
# expr_str = '~(p | ~(p & q))'
# expr_str = 'm & (n | p) & (~m | ~n | p)'  # m ∧ p
# expr_str = '((a >> c) >> (b >> c)) >> (a & b)'  # b ∧ (a ∨ ¬c)
#
min_ex, rules, expr_list = Reduce.reduce_2_expr_string(expr_str)
print("-------------------")
pprint(min_ex)
print("-------------------")
for ex, r in zip(expr_list, rules):
    print(r)
    pprint(ex)
