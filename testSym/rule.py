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
    def generate_rules_from_str(ex_str: str) -> [(BooleanFunction, BooleanFunction)]:
        ex = parse_expr(ex_str)
        return Rule.generate_rules(ex)

    @staticmethod
    def generate_rules(ex: BooleanFunction) -> [(BooleanFunction, BooleanFunction)]:
        rule_strings = 'p | true = true'.split("=")

        left_rule_ex = parse_expr(rule_strings[0])
        right_rule_ex = parse_expr(rule_strings[1])

        return Rule.apply_rule(ex, left_rule_ex, right_rule_ex)

    @staticmethod
    def find_all_rules_of_expr_str(ex_str: str):
        ex = parse_expr(ex_str)
        rules = Rule.generate_rules(ex)
        ex_list = []
        for rule in rules:
            new_ex = Rule.rule_replace(ex, (rule[0], rule[1]))[0]
            ex_list.append(new_ex)
        return rules, ex_list

    @staticmethod
    def apply_rule(ex: BooleanFunction, rule: BooleanFunction, equal_rule: BooleanFunction):
        rules = []

        constant_set = {true, false}
        symbol_set = set(rule.atoms(Symbol)).difference(constant_set)
        ex_symbol_set = Rule.generate_sub_expr(ex)

        combinations_of_symbols = (list(zip(x, symbol_set)) for x in
                                   itertools.permutations(ex_symbol_set, len(symbol_set)))

        checked_ex = set()

        for combination in combinations_of_symbols:
            replace_dict = dict()
            for e, r in combination:
                replace_dict[r] = e
            # print('replace_dict', replace_dict)
            new_ex = Rule.normalize_constant_in_expr(rule.xreplace(replace_dict))

            # Nếu luật cần phần trùng thì không cần loại bỏ
            if rule.args.__len__() > set(rule.args).__len__():
                normal_ex = new_ex
            else:
                normal_ex = Rule.normalize_duplicate_in_expr(new_ex)
            # print('new expr', new_ex, 'has', ex.has(new_ex), 'normal_ex', normal_ex)

            if new_ex.func is rule.func and new_ex == normal_ex and ex.has(new_ex):
                right_ex = equal_rule.xreplace(replace_dict)
                if checked_ex.__contains__((new_ex, right_ex)):
                    continue
                checked_ex.add((new_ex, right_ex))
                # right_ex = Rule.normalize_double_not_in_expr(right_ex)

                rules.append((new_ex, right_ex))

        rules = sorted(rules, key=lambda rul: set(rul[0].atoms(Symbol)).__len__())

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
    def read_rules_2(file_name: str, groups: [str]):

        def extract_group(name: str, _data):
            _group = _data[name]
            _rules = []
            for _rule in _group:
                _rule_left, _rule_right = Rule.convert_string_to_rule(_rule["rule"])
                _rules.append((_rule["name"], _rule_left, _rule_right))
            return _rules

        rules = []

        with open(file_name) as f:
            data = json.load(f)
            for g in groups:
                rules.append(extract_group(g, data))

        return rules

    @staticmethod
    def convert_string_to_rule(string: str) -> (BooleanFunction, BooleanFunction):
        rule_strings = string.split("=")

        left_rule_ex = parse_expr(rule_strings[0])
        right_rule_ex = parse_expr(rule_strings[1])
        return left_rule_ex, right_rule_ex

    @staticmethod
    def symbols_from_expression(ex: BooleanFunction) -> {Symbol}:
        results = set([x for x in postorder_traversal(ex) if x.func is Symbol])
        return results

    @staticmethod
    def normalize_constant_in_expr(ex: BooleanFunction):

        has_true = False
        has_false = False
        args = list(ex.args)
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

        return ex.func(*args)

    @staticmethod
    def normalize_double_not_in_expr(ex: BooleanFunction):

        if ex.atoms(Not).__len__() < 2:  # khong ton tai phu dinh cua phu dinh
            return ex

        arg_to_replace = list()

        for ag in postorder_traversal(ex):
            if ag.func is Not and ag.args[0].func is Not:
                arg_to_replace.append((ag, ag.args[0].args[0]))

        new_ex = ex
        for ag, new_ag in arg_to_replace:
            new_ex = new_ex.replace(ag, new_ag)

        return new_ex

    @staticmethod
    def normalize_duplicate_in_expr(ex: BooleanFunction):
        args = list(dict.fromkeys(ex.args))  # cần quan tâm thứ tự
        return ex.func(*args)

    @staticmethod
    def rule_replace(ex: BooleanFunction, rule):
        if not ex.has(rule[0]):
            return ex, False

        result = Rule._rule_replace(ex, rule)
        if result is not None:
            return result, True
        else:
            args = []
            changed = False

            for a in ex.args:
                a_xr = Rule.rule_replace(a, rule)
                args.append(a_xr[0])
                changed |= a_xr[1]
            args = tuple(args)
            if changed:
                return ex.func(*args), True

        return ex, False

    # @staticmethod
    # def _has(ex: BooleanFunction, pattern: BooleanFunction) -> bool:
    #     def match(ex: BooleanFunction, other: BooleanFunction):
    #         return ex == other and ex.args.__len__() == other.args.__len__()
    #     return any(match(pattern, arg) for arg in preorder_traversal(ex))

    @staticmethod
    def generate_sub_expr(ex: BooleanFunction) -> list:
        ex_symbol_set = set(ex.atoms(Symbol))
        for x in preorder_traversal(ex):
            if x.func is not Symbol:
                if not x == ex:
                    ex_symbol_set.add(x)
                arg_list = list(
                    filter(lambda e: e.func is not BooleanFalse and e.func is not BooleanTrue, list(x.args)))

                if arg_list.__len__() < 1:
                    continue

                ex_with_out_const = x.func(*arg_list)
                if not ex_with_out_const == ex:
                    ex_symbol_set.add(ex_with_out_const)

                if x.func is Implies:
                    for sym_list in itertools.combinations(arg_list, 2):
                        ex_symbol_set.add(x.func(*sym_list))
                else:
                    length = 1
                    while length < arg_list.__len__():
                        for sym_list in itertools.combinations(arg_list, length):
                            ex_symbol_set.add(x.func(*sym_list))
                        length += 1

        ex_symbol_set = ex_symbol_set.difference({true, false})
        return sorted(ex_symbol_set, key=lambda e: set(e.atoms(Symbol)))

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
                    return Rule.normalize_constant_in_expr(e.func(*args))
        # Nếu không thay thế theo một tham số được thì phải thay theo nhiều tham số
        # nhưng không áp dụng cho phép Not
        if rule[0].func is Not:
            return None

        ex_args = set(e.args)
        rule_left_args = set(rule[0].args)
        if ex_args.intersection(rule_left_args) == rule_left_args:
            args = list(ex_args.difference(rule_left_args))
            args.append(rule[1])
            return Rule.normalize_constant_in_expr(e.func(*args))

        return None
