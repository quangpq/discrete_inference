from discrete import *

# ((m & n) & p) | ((m & p) & ~p) | ~n -> (m ∧ p) ∨ ¬n
# (a & ~b & b & ~c) | (a & ~b & ~b & c) | (~a & b & b & ~c) | (~a & b & ~b & c) -> (a & ~b & c) | (~a & b & ~c)
g = parse_expr('(a & ~b & b & ~c) | (a & ~b & ~b & c) | (~a & b & b & ~c) | (~a & b & ~b & c)',
               local_dict={'p': p, 'q': q, 'r': r, 's': s, 't': t, 'm': m, 'n': n})

solutions, rules = reduce(g)

print("++++++++++++++++++++++++++++++")

for s, r in zip(solutions, rules):
    print(r[0])
    pprint(s)
