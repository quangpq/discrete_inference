from sympy import *

a, b, c, p, s, r = symbols('a b c p s r')
gt = {Eq(a, 5), Eq(b, 4), Eq(c, 3)}
# print(type(Eq(a, 3).args[1]))
kl = {a, b, c, p}
gt1 = set()
for g in gt:
    gt1.add(g.args[0])

print(kl.issubset(gt1))
