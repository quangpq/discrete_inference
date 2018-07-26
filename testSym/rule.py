import json
from sympy import *
from sympy.logic.boolalg import *
from sympy.parsing.sympy_parser import *
import itertools
from sympy import sympify


class Rule:
    @staticmethod
    def load_rules() -> [(str, str)]:
        rules = []
        with open('rules.json') as f:
            data = json.load(f)
            for rule in data:
                rules.append((rule["name"], rule["rule"]))
        return rules

    @staticmethod
    def generate_rules(expr: BooleanFunction) -> [(BooleanFunction, BooleanFunction)]:
        rule_strings = 'p | S.true = S.true'.split("=")

        left_rule_expr = parse_expr(rule_strings[0])
        right_rule_expr = parse_expr(rule_strings[1])

        return Rule.apply_rule(expr, left_rule_expr, right_rule_expr)

    @staticmethod
    def apply_rule(expr: BooleanFunction, rule: BooleanFunction, equal_rule: BooleanFunction):
        rules = []

        constant_set = {true, false}
        symbol_set = set(rule.atoms(Symbol)).difference(constant_set)
        expr_symbol_set = Rule.generate_sub_expr(expr)

        combinations_of_symbols = [list(zip(x, symbol_set)) for x in
                                   itertools.permutations(expr_symbol_set, len(symbol_set))]

        checked_expr = set()

        for combination in combinations_of_symbols:
            replace_dict = dict()
            for e, r in combination:
                replace_dict[r] = e
            new_expr = Rule.normalize_expr(rule.xreplace(replace_dict))
            if checked_expr.__contains__(new_expr):
                continue
            checked_expr.add(new_expr)
            print('new expr', new_expr, 'has', expr.has(new_expr))

            if expr.has(new_expr):
                right_expr = equal_rule.xreplace(replace_dict)
                rules.append((new_expr, right_expr))

        return rules

    @staticmethod
    def read_rules(file_name: str) -> (
            [(str, BooleanFunction, BooleanFunction)], [(str, BooleanFunction, BooleanFunction)],
            [(str, BooleanFunction, BooleanFunction)]):
        rules_1 = []
        rules_2 = []
        rules_3 = []

        with open(file_name) as f:
            data = json.load(f)
            group_1 = data["group_1"]
            group_2 = data["group_2"]
            group_3 = data["group_3"]
            for rule in group_1:
                rule_left, rule_right = Rule.convert_string_to_rule(rule["rule"])
                rules_1.append((rule["name"], rule_left, rule_right))
            for rule in group_2:
                rule_left, rule_right = Rule.convert_string_to_rule(rule["rule"])
                rules_2.append((rule["name"], rule_left, rule_right))
            for rule in group_3:
                rule_left, rule_right = Rule.convert_string_to_rule(rule["rule"])
                rules_3.append((rule["name"], rule_left, rule_right))

        return rules_1, rules_2, rules_3

    @staticmethod
    def convert_string_to_rule(string: str) -> (BooleanFunction, BooleanFunction):
        rule_strings = string.split("=")

        left_rule_expr = parse_expr(rule_strings[0])
        right_rule_expr = parse_expr(rule_strings[1])
        return left_rule_expr, right_rule_expr

    @staticmethod
    def symbols_from_expression(expr: BooleanFunction) -> {Symbol}:
        results = set([x for x in postorder_traversal(expr) if x.func is Symbol])
        return results

    @staticmethod
    def normalize_expr(expr: BooleanFunction):

        has_true = False
        has_false = False
        args = list(expr.args)
        for i in range(len(args) - 1, -1, -1):
            if args[i] is true:
                if has_true:
                    del args[i]
                else:
                    has_true = True
            elif args[i] is false:
                if has_false:
                    del args[i]
                else:
                    has_false = True

        return expr.func(*args)

    @staticmethod
    def rule_replace(expr: BooleanFunction, rule):
        if not expr.has(rule[0]):
            return expr, False

        result = Rule._rule_replace(expr, rule)
        if result:
            return result, True
        else:
            args = []
            changed = False

            for a in expr.args:
                a_xr = Rule.rule_replace(a, rule)
                args.append(a_xr[0])
                changed |= a_xr[1]
            args = tuple(args)
            if changed:
                return expr.func(*args), True

        return expr, False

    # @staticmethod
    # def _has(expr: BooleanFunction, pattern: BooleanFunction) -> bool:
    #     def match(ex: BooleanFunction, other: BooleanFunction):
    #         return ex == other and ex.args.__len__() == other.args.__len__()
    #     return any(match(pattern, arg) for arg in preorder_traversal(expr))

    @staticmethod
    def generate_sub_expr(expr: BooleanFunction) -> set:
        expr_symbol_set = set(expr.atoms(Symbol))

        for x in preorder_traversal(expr):
            if x.func is not Symbol:
                if not x == expr:
                    expr_symbol_set.add(x)
                sym_set = set(x.args)
                length = 2
                while length < sym_set.__len__():
                    for sym_list in itertools.permutations(sym_set, length):
                        expr_symbol_set.add(x.func(*sym_list))
                    length += 1

        return expr_symbol_set.difference({true, false})

    @staticmethod
    def _rule_replace(e, rule):
        if e.func is Symbol:
            return None

        if e == rule[0]:
            return rule[1]

        if rule[0].func is not rule[1].func:
            # Nếu hai vế có phép toán khác nhau, check xem có thay thế theo một
            # tham số được không
            for a in e.args:
                if a == rule[0]:
                    args = list(e.args)
                    i = args.index(a)
                    args[i] = rule[1]
                    return e.func(*args)
        # Nếu không thay thế theo một tham số được thì phải thay theo nhiều tham số
        expr_args = set(e.args)
        rule_left_args = set(rule[0].args)
        if expr_args.intersection(rule_left_args) == rule_left_args:
            args = list(expr_args.difference(rule_left_args))
            args.append(rule[1])
            return e.func(*args)

        return None
