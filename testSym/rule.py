import json
from sympy import *
from sympy.logic.boolalg import *
from sympy.parsing.sympy_parser import *
import itertools


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
        rules = []
        rule_strings = 'p & (p | q) = p'.split("=")

        left_rule_expr = parse_expr(rule_strings[0])
        right_rule_expr = parse_expr(rule_strings[1])

        symbol_set = left_rule_expr.atoms(Symbol)

        expr_symbol_set = expr.atoms(Symbol)

        combinations_of_symbols = [list(zip(x, symbol_set)) for x in
                                   itertools.permutations(expr_symbol_set, len(symbol_set))]
        for combination in combinations_of_symbols:
            replace_dict = dict()
            for e, r in combination:
                replace_dict[r] = e

            new_expr = left_rule_expr.subs(replace_dict)
            if expr.has(new_expr):
                right_expr = right_rule_expr.xreplace(replace_dict)
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

    @staticmethod
    def _rule_replace(e, rule):
        if e.func is Symbol:
            return None
        expr_args = set(e.args)
        rule_left_args = set(rule[0].args)
        if expr_args.intersection(rule_left_args) == rule_left_args:
            args = expr_args.difference(rule_left_args)
            if rule[1].func is Symbol:
                return e.func(*args, rule[1])
            else:
                args = args.union(set(rule[1].args))
            return e.func(*args)
        return None
