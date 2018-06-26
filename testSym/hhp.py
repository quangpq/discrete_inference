from sympy import *
from models import *

A, B, C, R, S, a, b, c, ha, hb, hc, p, r = symbols('A B C R S a b c ha hb hc p r')
rules = {
    (frozenset({A, B}), Eq(C, pi - A - B)),
    (frozenset({A, C}), Eq(B, pi - A - C)),
    (frozenset({B, C}), Eq(A, pi - B - C)),
    (frozenset({a, ha}), Eq(S, (1 / 2) * (a * ha))),
    (frozenset({b, hb}), Eq(S, (1 / 2) * (b * hb))),
    (frozenset({c, hc}), Eq(S, (1 / 2) * (c * hc))),
    (frozenset({p, r}), Eq(S, p * r)),
    (frozenset({A, R, a}), Eq(a / sin(A), 2 * R)),
    (frozenset({A, b, c}), Eq(S, (1 / 2) * b * c * sin(A))),
    (frozenset({A, b, c}), Eq(a ^ 2, b ^ 2 + c ^ 2 + 2 * b * c * cos(A))),
    (frozenset({B, R, b}), Eq(b / sin(B), 2 * R)),
    (frozenset({B, a, c}), Eq(S, (1 / 2) * a * c * sin(B))),
    (frozenset({B, a, c}), Eq(b ^ 2, a ^ 2 + c ^ 2 + 2 * a * c * cos(B))),
    (frozenset({C, R, c}), Eq(c / sin(C), 2 * R)),
    (frozenset({C, a, b}), Eq(S, (1 / 2) * a * b * sin(C))),
    (frozenset({C, a, b}), Eq(c ^ 2, a ^ 2 + b ^ 2 + 2 * a * b * cos(C))),
    (frozenset({a, b, c}), Eq(p, (a + b + c) * (1 / 2))),
    (frozenset({A, B, a, b}), Eq(a / sin(A), b / sin(B))),
    (frozenset({A, C, a, c}), Eq(a / sin(A), c / sin(C))),
    (frozenset({B, C, b, c}), Eq(b / sin(B), c / sin(C))),
    (frozenset({S, a, b, c}), Eq(R, (a * b * c) / (4 * S))),
    (frozenset({a, b, c, p}), Eq(S, sqrt(p * (p - a) * (p - b) * (p - c)))),
}


def find_solution(gt, kl):
    solution = []
    known_1 = set()
    known_2 = set()
    for u in gt:
        if type(u) is Eq and type(u.args[0]) is Symbol:
            known_1.add(u)
        else:
            known_2.add(u)
    print(known_1)
    print(known_2)
    found = true
    names = {x.args[0] for x in list(known_1.union(known_2))}

    while found and not kl.issubset(names):
        found = false
        names = {x.args[0] for x in list(known_1.union(known_2))}
        print(names)

        for rule in rules:
            if rule[0].issubset(names) and not ({rule[1].args[0]}.issubset(names)):
                found = true
                solution.append(rule)
                if rule is Eq and rule.args[0] is symbol:
                    known_1.add(rule[1])
                else:
                    known_2.add(rule[1])

    print(found)
    print(known_1)
    print(known_2)

    if kl.issubset({x.args[0] for x in list(known_1.union(known_2))}):
        return solution
    else:
        return []


GT = {Eq(a, 5), Eq(b, 4), Eq(c, 3)}
KL = {S, R}

SL = find_solution(GT, KL)
print("solution")
print(SL)




# print(type(Eq(a, 3).args[1]))
# gt = {Eq(a, 5), Eq(b, 4), Eq(c, 3)}

# kl = {a, b, c, p}
# gt1 = set()
# for g in gt:
#     gt1.add(g.args[0])
#
# print(kl.issubset(gt1))
