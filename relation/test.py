from .lattice import Lattice
from graphviz import Source

if __name__ == '__main__':
    # powerset = [1, 2, 3, 4]
    # def intersection(a, b): return min(a, b)
    # def union(a, b): return max(a, b)


    # powerset = [set(), {'a'}, {'b'}, {'c'}, {'a', 'b'}, {'a', 'c'}, {'c', 'b'}, {'a', 'b', 'c'}]
    # powerset = [0b000, 0b001, 0b010, 0b011, 0b100, 0b101, 0b110, 0b111]
    powerset = [2, 4, 5, 10, 12, 20, 25]
    def intersection(a, b): return a & b
    def union(a, b): return a | b

    def gcd(a, b):
        while b > 0:
            a, b = b, a % b
        return a

    def lcm(a, b):
        return a * b / gcd(a, b)


    L = Lattice(powerset, lcm, gcd)
    hasse = L.hasse()
    print(hasse)
    src = Source(hasse)
    src.render('hasse.gv', view=True)
