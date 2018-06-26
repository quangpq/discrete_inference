from sympy import *
from sympy.logic.boolalg import *
from typing import Tuple, FrozenSet, Optional, Set, AnyStr, Dict, SupportsInt
import re
from discrete import *


g = parse_expr('(p | q) & (p | s) & (r | t)', local_dict={'p': p, 'q': q, 'r': r, 's': s, 't': t})

result = g
pprint(result)

while result:
    result = check_rules(result)
    pprint(result)
