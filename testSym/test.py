from rule import *
from reduce import *
from logic_inference import *
from expr_tree import simple_degree


# expr_str2 = 's | t | (True) | ~p | ~q'
# expr_str2 = '(¬p ∧ ¬q) ∨ ¬p ∨ ¬q'
# expr_str2 = '~(p & (~p | (r & q)) & (~r | t | t) & ~s) | t'
# expr_str2 = ' (~r | t | t | t) & (t | r)'
# expr_str2 = '~(~r | q | p | z)'
expr_str2 = '(s | (p & ~r)) & (~p | ~p | ~s) & (r | ~p | ~q)'
# coms = Rule.generate_sub_expr(expr)
# print(coms)
# #
# rules, ex_list = Rule.find_all_rules_of_expr_str(expr_str2)
# for rule, _ex in zip(rules, ex_list):
#     print("rule:", rule)
#     pprint(_ex)
#
# print(min(ex_list, key=lambda e: simple_degree(e)))


# print(Reduce.simpler(expr2, expr))
# expr_str = '((q => r) & (q | ~p)) => (p => r)'  # 1
# expr_str = '~(p | q) | ((~p & q)| ~q)'  # ¬(q ∧ p)
# expr_str = 'm & (n | p) & (~m | ~n | p)'  # m ∧ p
# expr_str = '((a => c) => (b => c)) => (a & b)'  # b ∧ (a ∨ ¬c)
# expr_str = '(p & (p => (r & q)) & (r => (s | t)) & ~s) => t'  # true
# expr_str = '((p | q) & (p => r) & (q => r)) => r'  # true
# expr_str = '(p => r) | (q => r)'  # r ∨ ¬p ∨ ¬q
# expr_str = '(p & (p => q)) => q'  # true
# expr_str = '~(~(p | q) & ~q)'  # p ∨ q
# expr_str = '~p | (p & q)'  # q ∨ ¬p
# expr_str = '(p => (q => r)) => ((p & q) => r)'  # 1
# expr_str = '(p & (~r | q | ~q)) | ((r | t | ~r) & ~q)'  # p ∨ ¬q
# expr_str = '(p | (p & q) | (p & q & ~r)) & ((p & r & t) | t)'  # p ∧ t
# expr_str = '(r & q) | (p & ~q & r) | (~p & ~q & r)'  # r
# expr_str = '(x & y) | ((z | x) & ~y)'  # x ∨ (z ∧ ¬y)
# expr_str = '((x | y) & z) | ((~z | x) & (y | z))'
# expr_str = '~(x & ~y) => (~y => x)'  # x ∨ y
# expr_str = '((p | q) & (p | ~q)) | q'  # p ∨ q
# expr_str = '(p => q) & (~q & (r | ~q))'  # ¬(p ∨ q)
# expr_str = '~(p & (q | r) & ((p & q) => r))'  # ¬(p ∧ r)
# expr_str = '(p | q) & ~(~p & q)'  # p
# expr_str = '(m => (n => p)) => (n => p)'  # m ∨ p ∨ ¬n
# expr_str = '~n | (m & (~(m |~n) | p))'  # (m ∧ p) ∨ ¬n
# expr_str = '((~m => n) | (n => ~m)) => (m & n)'  # m ∧ n
# expr_str = '(m => (n | p)) => ((m => p) | (n => p))'  # p ∨ ¬(m ∧ n)
# expr_str = '~(p | ~(p & q))'  # 0
# expr_str = 'p & (~p | q | ~~(z | ~q))'  # p
# expr_str = '(p & r) | ((p | s) & (p | a))'  # p ∨ (a ∧ s)
# expr_str = '(p | (p & y)) => ((p & q) & (r & ~p))'  # ¬p
# expr_str = '(p => ((~q | r) & ~s)) & (~s => (~r & p))'  # (p ∧ ¬q ∧ ¬r ∧ ¬s) ∨ (¬p ∧ s)
# expr_str = '~(x & (y | z) & (~x | ~y | z))'  # ¬(x ∧ z)
# expr_str = '~((x & y) => z)'  # x ∧ y ∧ ¬z
# expr_str = '~(x | y | (~x & ~y & z))'  # ¬(x ∨ y ∨ z)
# expr_str = '(m & n & p) | (m & p & ~p) | ~n'  # (m ∧ p) ∨ ¬n

# expr_str = '((p => q) & (q => r)) => (p => r)'  # True
# expr_str = '~(p | ~(p & q))'  # false

# min_ex, rules, expr_list = Reduce.reduce_2_expr_string(expr_str)
# print("-------------------")
# pprint(min_ex)
# print(rules.__len__())
# print("-------------------")
# for ex, r in zip(expr_list, rules):
#     print(r)
#     pprint(ex)

# expr_str_1 = '(p => (q => (p & q & r)))'
# expr_str_2 = 'q => (p => r)'

expr_str_1 = '(p | q) & (~p | ~q)'
expr_str_2 = '(p & ~q) | (~p & q)'

result, step_1, step_2 = Reduce.equivalent_expr_string(expr_str_1, expr_str_2)
print("-------------------")
print(result)
print("-------------------")
if step_1 is not None:
    print("Cac luat cua bieu thuc")
    ex1, rules_1, expr_list_1 = step_1
    pprint(ex1)
    for ex, r in zip(expr_list_1, rules_1):
        print(r)
        pprint(ex)
print("-------------------")
if step_2 is not None:
    print("Cac luat cua bieu thuc")
    ex2, rules_2, expr_list_2 = step_2
    pprint(ex2)
    for ex, r in zip(expr_list_2, rules_2):
        print(r)
        pprint(ex)
