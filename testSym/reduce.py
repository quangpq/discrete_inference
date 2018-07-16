from rule import *


class Reduce:
    @staticmethod
    def reduce(expr: BooleanFunction):
        rules_1, rules_2, rules_3 = Rule.read_rules("rules.json")

        return expr

    @staticmethod
    def k_degree(expr: BooleanFunction) -> int:
        args = [arg for arg in postorder_traversal(expr) if
                arg.func is Symbol or arg.func is BooleanFalse or arg.func is BooleanTrue]

        not_count = [arg for arg in postorder_traversal(expr) if arg.func is Not].__len__()

        args_count = args.__len__()

        removed_constant_list = [arg for arg in args if arg.func is Symbol]
        args_set_count = set(removed_constant_list).__len__()
        return args_count - args_set_count + not_count

    @staticmethod
    def simpler(expr_1: BooleanFunction, expr_2: BooleanFunction) -> bool:
        def height(expr: BooleanFunction) -> int:
            sub_expr = [arg for arg in expr.args if
                         arg.func is not Symbol and arg.func is not BooleanFalse and arg.func is not BooleanTrue]
            if sub_expr.__len__() == 0:
                return 1
            else:
                return max([height(ex) for ex in sub_expr]) + 1

        def length(expr) -> int:
            count = 0
            for arg in postorder_traversal(expr):
                if arg.func is Symbol or arg.func is BooleanFalse or arg.func is BooleanTrue or arg.func is Not:
                    count += 1

            return count

        return length(expr_1) <= length(expr_2) and height(expr_1) <= height(expr_2)
