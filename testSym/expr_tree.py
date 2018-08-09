from sympy import *
from sympy.logic.boolalg import *


def k_degree(ex: BooleanFunction) -> int:
    args = [ag for ag in postorder_traversal(ex) if
            ag.func is Symbol or ag.func is BooleanFalse or ag.func is BooleanTrue]

    not_count = ex.atoms(Not).__len__()

    args_count = args.__len__()

    removed_constant_list = [ag for ag in args if ag.func is Symbol]
    args_set_count = set(removed_constant_list).__len__()
    return args_count - args_set_count + not_count


def height_of_expr(_ex: BooleanFunction) -> int:
    sub_ex = [ag for ag in _ex.args if
              ag.func is not Symbol and ag.func is not BooleanFalse and ag.func is not BooleanTrue]
    if sub_ex.__len__() == 0:
        return 1
    else:
        return max([height_of_expr(_ex) for _ex in sub_ex]) + 1


def length_of_expr(_ex) -> int:
    count = 0
    for ag in postorder_traversal(_ex):
        if ag.func is Symbol or ag.func is BooleanFalse or ag.func is BooleanTrue or ag.func is Not:
            count += 1

    return count


def simple_degree(ex: BooleanFunction) -> int:
    return length_of_expr(ex) + height_of_expr(ex)


def simpler(ex_1: BooleanFunction, ex_2: BooleanFunction) -> bool:
    return length_of_expr(ex_1) <= length_of_expr(ex_2) and height_of_expr(ex_1) <= height_of_expr(ex_2)
