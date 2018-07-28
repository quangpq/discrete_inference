from sympy import *
from sympy.logic.boolalg import *
from typing import Optional, Set


class DiscreteRule:
    a, b, c, p, q, r, s, t, m, n = symbols('a b c p q r s t m n')

    rules1 = [
        ('Phủ định của phủ định', lambda ag: ag.func is Not and ag.args[0].func is Not,
         lambda ex, ag: ex.replace(ag, ag.args[0].args[0])),

        ('Luật lũy đẳng', lambda ag: ag.func is Or and ag.args.__len__() > set(ag.args).__len__(),
         lambda ex, ag: ex.replace(ag, Or(*set(ag.args)))),
        ('Luật lũy đẳng', lambda ag: ag.func is And and ag.args.__len__() > set(ag.args).__len__(),
         lambda ex, ag: ex.replace(ag, And(*set(ag.args)))),

        # ('Luật lũy đẳng', lambda ag: ag.func is Or and ag.args[0] == ag.args[1],
        #  lambda ex, ag: ex.replace(ag, ag.args[0])),
        # ('Luật lũy đẳng', lambda ag: ag.func is And and ag.args[0] == ag.args[1],
        #  lambda ex, ag: ex.replace(ag, ag.args[0])),

        ('Luật De Morgan', lambda ag: ag.func is Not and ag.args[0].func is And,
         lambda ex, ag: ex.replace(ag, Or(
             *list(map(lambda x: Not(x), list(ag.args[0].args)))))),
        ('Luật De Morgan', lambda ag: ag.func is Not and ag.args[0].func is Or,
         lambda ex, ag: ex.replace(ag, And(
             *list(map(lambda x: Not(x), list(ag.args[0].args)))))),

        ('Luật kéo theo', lambda ag: ag.func is Implies,
         lambda ex, ag: ex.replace(ag, Or(Not(ag.args[0]), ag.args[1]))),

        ('Luật về phần tử bù',
         lambda ag: ag.func is And and any(
             x for x in ag.args if x.func is Not and any(y for y in ag.args if y == x.args[0])),
         lambda ex, ag: DiscreteRule.negation_law(ex, ag)),
        ('Luật về phần tử bù',
         lambda ag: ag.func is Or and any(
             x for x in ag.args if x.func is Not and any(y for y in ag.args if y == x.args[0])),
         lambda ex, ag: DiscreteRule.negation_law(ex, ag)),

        ('Luật thống trị', lambda ag: ag.func is Or and [x for x in ag.args if x.func is BooleanTrue].__len__() > 0,
         lambda ex, ag: ex.replace(ag, true)),
        (
            'Luật thống trị',
            lambda ag: ag.func is And and [x for x in ag.args if x.func is BooleanFalse].__len__() > 0,
            lambda ex, ag: ex.replace(ag, false)),

        ('Luật trung hòa', lambda ag: ag.func is Or and [x for x in ag.args if x.func is BooleanFalse].__len__() > 0,
         lambda ex, ag: DiscreteRule.identity_law(ex, ag)),
        ('Luật trung hòa', lambda ag: ag.func is And and [x for x in ag.args if x.func is BooleanTrue].__len__() > 0,
         lambda ex, ag: DiscreteRule.identity_law(ex, ag)),

        ('Luật hấp thụ', lambda ag: ag.func is Or and any(
            x for x in ag.args if x.func is And and any(y for y in ag.args if list(x.args).__contains__(y))),
         lambda ex, ag: DiscreteRule.absorption_law(ex, ag)),
        ('Luật hấp thụ', lambda ag: ag.func is And and any(
            x for x in ag.args if x.func is Or and any(y for y in ag.args if list(x.args).__contains__(y))),
         lambda ex, ag: DiscreteRule.absorption_law(ex, ag)),

        ('Luật phân phối', lambda ag: ag.func is And and any(
            x for x in ag.args if
            x.func is Or and any(
                y for y in ag.args if
                y.func is Or and x != y and set(y.args).intersection(set(x.args)).__len__() > 0)),
         lambda ex, ag: DiscreteRule.revert_distributive_law(ex, ag)),
        ('Luật phân phối', lambda ag: ag.func is Or and any(x for x in ag.args if x.func is And and any(
            y for y in ag.args if y.func is And and x != y and set(y.args).intersection(set(x.args)).__len__() > 0)),
         lambda ex, ag: DiscreteRule.revert_distributive_law(ex, ag)),
    ]

    # tăng kích thước biểu thức
    rules2 = [
        ('Luật phân phối 2', lambda ag: ag.func is And and any(
            x for x in ag.args if
            x.func is Or),
         lambda ex, ag: DiscreteRule.absorption_law(ex, ag)),
        ('Luật phân phối 2', lambda ag: ag.func is Or and any(x for x in ag.args if x.func is And),
         lambda ex, ag: DiscreteRule.absorption_law(ex, ag)),
    ]

    @staticmethod
    def negation_law(ex: BooleanFunction, ag: BooleanFunction) -> BooleanFunction:

        args = list(ag.args)
        remove_args = set(x for x in ag.args if any(
            y for y in ag.args if (y.func is Not and y.args[0] == x) or (x.func is Not and x.args[0] == y)))

        for ag in ag.args:
            if remove_args.__contains__(ag):
                args.remove(ag)

        bool_var = false if ag.func is And else true

        args.append(bool_var)
        sub_expr = ag.func(*args)
        return ex.replace(ag, sub_expr)

    @staticmethod
    def absorption_law(ex: BooleanFunction, ag: BooleanFunction) -> BooleanFunction:
        args = list(ag.args)
        remove_func = And if ag.func is Or else Or
        remove_args = set(
            x for x in ag.args if x.func is remove_func and any(y for y in ag.args if list(x.args).__contains__(y)))

        for ag in ag.args:
            if remove_args.__contains__(ag):
                args.remove(ag)

        sub_expr = ag.func(*args)
        return ex.replace(ag, sub_expr)

    @staticmethod
    def distributive_law(ex: BooleanFunction, ag: BooleanFunction) -> BooleanFunction:
        args = list(ag.args)
        func = And if ag.func is Or else Or

        small_args = args
        big_args = max([x for x in ag.args if x.func is func], key=lambda x: x.args.__len__())
        small_args.remove(big_args)

        # tìm biểu thức trong small_args có phàn trùng lớn nhất với big_args
        count = 0
        best_args = small_args[0]
        big_args_set = DiscreteRule.normalise_args_set(set(big_args.args))
        for a in small_args:
            if a.func is Symbol:
                count_a = 1 if big_args_set.__contains__(a) else 0
            else:
                set_a = DiscreteRule.normalise_args_set(set(a.args))
                count_a = (big_args_set.intersection(set_a)).__len__()

            if count_a > count:
                count = count_a
                best_args = a

        small_args.remove(best_args)

        new_args = list(map(lambda x: ag.func(best_args, x), list(big_args.args)))
        sub_expr = func(*new_args)
        small_args.append(sub_expr)

        return ex.replace(ag, ag.func(*small_args))

    @staticmethod
    def revert_distributive_law(ex: BooleanFunction, ag: BooleanFunction) -> Optional[BooleanFunction]:
        absorption_var = set()
        func = And if ag.func is Or else Or

        for i, ag in enumerate(ag.args):
            if ag.func is func:
                for j, ag_2 in enumerate(ag.args, start=i + 1):
                    v = set(ag.args).intersection(set(ag_2.args))
                    if v.__len__() > 0:
                        absorption_var = v
                        break

        absorption_list = set()
        non_absorption_list = []

        for ag in ag.args:
            if ag.func is func and absorption_var.issubset(set(ag.args)):
                a = list(set(ag.args).difference(absorption_var))
                absorption_list.add(func(*a))
            else:
                non_absorption_list.append(ag)

        if absorption_list.__len__() == 0:
            return None

        sub_absorption = func(*absorption_var, ag.func(*absorption_list))
        sub_expr = ag.func(sub_absorption, *non_absorption_list)
        return ex.replace(ag, sub_expr)

    @staticmethod
    def identity_law(ex: BooleanFunction, ag: BooleanFunction) -> BooleanFunction:
        args = list(ag.args)
        remove_args = false if ag.func is Or else true

        for ag in ag.args:
            if remove_args == ag:
                args.remove(ag)

        sub_expr = ag.func(*args)
        return ex.replace(ag, sub_expr)

    @staticmethod
    def normalise_args_set(s: Set[BooleanFunction]) -> Set[BooleanFunction]:
        item_to_remove = set(item for item in s if item.func is Not)
        s = s.difference(item_to_remove)
        new_items = set()
        for i in item_to_remove:
            new_items = new_items.union(set(i.args))

        return s.union(new_items)
