import collections


class Lattice(object):
    def __init__(self, elements, le_func):
        """Create a lattice:

        Keyword arguments:
        elements -- list. The lattice set.
        le_func  -- compare function that operates to elements.

        Returns a lattice instance.
        """
        self.elements = elements
        self.less = le_func

    def wrap(self, index):
        """Wraps an object as a lattice element:

        Keyword argument:
        object -- any item from the lattice set.
        """
        return LatticeElement(self, index)

    def element_by_index(self, element_index):
        return LatticeElement(self, self.elements[element_index])

    @property
    def top_element(self):
        top = self.wrap(self.elements[0])
        for element in self.elements[1:]:
            next_top = top | self.wrap(element)
            unwrapped = next_top.unwrap
            if top != next_top and unwrapped is not None and unwrapped in self.elements:
                top = next_top
        return top

    def top_elements(self, graph: dict):
        top = set()
        for element in self.elements:
            index = self.elements.index(element)
            if graph[index].__len__() == 0:
                top.add(element)

        return top

    def bottom_elements(self, graph: dict):
        bottom = set()
        for element in self.elements:
            is_valid = True
            index = self.elements.index(element)
            for k, v in graph.items():
                if v.__contains__(index):
                    is_valid = False
                    break

            if is_valid:
                bottom.add(element)

        return bottom

    @property
    def bottom_element(self):
        bottom = self.wrap(self.elements[0])
        for element in self.elements[1:]:
            next_bottom = bottom & self.wrap(element)
            unwrapped = next_bottom.unwrap
            if bottom != next_bottom and unwrapped is not None and unwrapped in self.elements:
                bottom = next_bottom
        return bottom

    def normalize_graph(self, graph):
        a_set = set()
        new_graph = dict()
        for s, ds in graph.items():
            new_ds = [x for x in ds if x not in a_set]
            a_set = a_set.union(set(ds))
            new_graph[s] = new_ds

        return new_graph

    def hasse(self):
        graph = dict()
        for indexS, elementS in enumerate(self.elements):
            graph[indexS] = []
            for indexD, elementD in enumerate(self.elements):
                if self.wrap(elementS) <= self.wrap(elementD):
                    if not bool(sum([int(self.element_by_index(x) <= self.wrap(elementD)) for x in
                                     graph[indexS]])) and not elementS == elementD:
                        graph[indexS] += [indexD]

        graph = self.normalize_graph(graph)
        dotcode = 'digraph G {\nsplines="line"\nrankdir=BT\n'
        top = self.top_elements(graph)
        bottom = self.bottom_elements(graph)

        for t in top:
            dotcode += '\"' + str(t) + '\" [shape=hexagon];\n'

        for b in bottom:
            dotcode += '\"' + str(b) + '\" [shape=box];\n'

        for s, ds in graph.items():
            for d in ds:
                dotcode += "\"" + str(self.element_by_index(s)) + "\""
                dotcode += " -> "
                dotcode += "\"" + str(self.element_by_index(d)) + "\""
                dotcode += ";\n"
        dotcode += "}"

        return dotcode

    def __repr__(self):
        """Represents the lattice as an instance of Lattice."""
        return 'Lattice(%s,%s)' % (self.elements, self.less)


class LatticeElement:
    def __init__(self, lattice, element):
        self.lattice = lattice
        if element not in lattice.elements:
            # raise ValueError('The given value is not a lattice element')
            self.element_index = None
        else:
            self.element_index = lattice.elements.index(element)

    @property
    def unwrap(self):
        if self.element_index is None:
            return None
        return self.lattice.elements[self.element_index]

    def __str__(self):
        return str(self.unwrap)

    def __repr__(self):
        """Represents the lattice element as an instance of LatticeElement."""
        return "LatticeElement(L, %s)" % str(self)

    def __eq__(self, b):
        return self.unwrap == b.unwrap

    def __le__(self, b):
        a = self

        return self.lattice.less(a.unwrap, b.unwrap)
