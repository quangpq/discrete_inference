from sympy.logic.boolalg import *
from typing import Set, Dict, List
from parse import parse_expr
from expr_tree import convert_to_not
import itertools

InferenceRuleDict = Dict[BooleanFunction, List[BooleanFunction]]
InferenceRuleResult = (bool, List)


class LogicInference:
    inference_rules = [
        ('Quy tắc Modus Ponens', lambda expr_set: LogicInference.modus_ponens_rule(expr_set)),
        ('Quy tắc Modus Tollens', lambda expr_set: LogicInference.modus_tollens_rule(expr_set)),
        ('Tam đoạn luận', lambda expr_set: LogicInference.syllogism(expr_set)),
        ('Tam đoạn luận rời', lambda expr_set: LogicInference.disjunctive_syllogism(expr_set)),
        ('Quy tắc đơn giản', lambda expr_set: LogicInference.simplification(expr_set)),
        ('Negation Introduction', lambda expr_set: LogicInference.negation_introduction(expr_set)),
        ('Quy tắc chứng minh theo trường hợp', lambda expr_set: LogicInference.case_analysis(expr_set)),
        ('Quy tắc mâu thuẫn', lambda expr_set: LogicInference.contradictions(expr_set)),
    ]
    de_morgan_rules = [
        ('De Morgan 1', lambda expr_set: LogicInference.de_morgan_expand_law(expr_set)),
        ('De Morgan 2', lambda expr_set: LogicInference.de_morgan_reduce_law(expr_set)),
    ]
    constructing_rules = [
        ('Constructing a Disjunction', lambda expr_set: LogicInference.constructing_disjunctions(expr_set)),
        ('Adjunction', lambda expr_set: LogicInference.adjunctions(expr_set)),
    ]

    @staticmethod
    def resolve(premises: Set[BooleanFunction], conclusion: BooleanFunction) -> InferenceRuleResult:

        def check_resolved(_facts: set):
            nonlocal inference_rules

            if _facts.__contains__(conclusion):
                return True
            if conclusion.func is Or:
                args_set = set(conclusion.args)
                joint_args = _facts.intersection(args_set)
                if joint_args.__len__() > 0:
                    inference_rules[conclusion] = ('Luat hoi', list(joint_args))
                    return True
            return False

        def find_facts(_facts: set, _rules: list) -> (bool, set):
            nonlocal facts, resolved, inference_rules
            _found = False
            _new_facts = set()

            for _rule in _rules:
                _new_facts_dict = _rule[1](_facts)
                _inner_facts = set(_new_facts_dict.keys()).difference(facts)
                for _fact in _inner_facts:
                    inference_rules[_fact] = (_rule[0], _new_facts_dict[_fact])

                _found = _found or _inner_facts.__len__() > 0
                _new_facts = _new_facts.union(_inner_facts)
                _facts = _facts.union(_inner_facts)
                facts = facts.union(_inner_facts)
                print(_rule[0])
                print(_inner_facts)

                if check_resolved(_inner_facts):
                    resolved = True
                    break

            return _found, _new_facts

        if check_resolved(premises):
            return True, []

        facts = premises
        inference_rules = dict()
        resolved = False
        found = True

        negative_facts = LogicInference.negative_law(premises)
        facts = facts.union(set(negative_facts.keys()))

        find_facts(facts, LogicInference.de_morgan_rules)

        while found and not resolved:
            print("------------------")
            found, new_facts = find_facts(facts, LogicInference.inference_rules)

            constructing_facts = set()
            if not resolved and not found:
                found, constructing_facts = find_facts(facts, LogicInference.constructing_rules)
                # for rule in LogicInference.constructing_rules:
                #     new_facts_dict = rule[1](facts)
                #     inner_facts = set(new_facts_dict.keys()).difference(facts)
                #     for fact in inner_facts:
                #         inference_rules[fact] = (rule[0], new_facts_dict[fact])
                #
                #     found = found or inner_facts.__len__() > 0
                #     new_facts = new_facts.union(inner_facts)
                #     constructing_facts = constructing_facts.union(inner_facts)
                #     print(rule[0])
                #     print(inner_facts)
                #     if check_resolved(inner_facts):
                #         resolved = True
                #         break
                #
                # facts = facts.union(constructing_facts)

            if not resolved and found:
                find_facts(new_facts.union(constructing_facts), LogicInference.de_morgan_rules)

        if resolved:
            rule_name, fact = inference_rules[conclusion]
            solution = [(rule_name, fact, conclusion)]
            current_facts = set(fact)
            checked_rules = set()

            while current_facts.__len__() > 0:
                new_current_facts = set()
                for fact in current_facts:
                    rule_name, rules = inference_rules[fact]
                    if checked_rules.__contains__((frozenset(rules), fact)):
                        continue
                    else:
                        checked_rules.add((frozenset(rules), fact))
                    rules_set = set(rules).difference(premises)
                    solution.append((rule_name, rules, fact))
                    new_current_facts = new_current_facts.union(rules_set)

                current_facts = new_current_facts

            solution = reversed(solution)
        else:
            solution = []

        return resolved, solution

    @staticmethod
    def negative_law(expr_set: Set[BooleanFunction]) -> InferenceRuleDict:

        def valid_expr(_expr: BooleanFunction):
            return _expr.func is Not and _expr.args[0].func is Not

        new_facts = dict()
        expr_to_convert = filter(lambda x: valid_expr(x), expr_set)
        for ex in expr_to_convert:
            new_expr = ex.args[0].args[0]
            new_facts[new_expr] = [ex]

        return new_facts

    @staticmethod
    def de_morgan_expand_law(expr_set: Set[BooleanFunction]) -> InferenceRuleDict:

        def valid_expr(_expr: BooleanFunction):
            return _expr.func is Not and (_expr.args[0].func is And or _expr.args[0].func is Or)

        new_facts = dict()
        expr_to_convert = filter(lambda x: valid_expr(x), expr_set)
        for ex in expr_to_convert:
            func = And if ex.args[0].func is Or else Or
            args = ex.args[0].args
            new_arg = list(map(lambda sub_arg: convert_to_not(sub_arg), list(args)))
            new_expr = func(*new_arg)
            new_facts[new_expr] = [ex]

        return new_facts

    @staticmethod
    def de_morgan_reduce_law(expr_set: Set[BooleanFunction]) -> InferenceRuleDict:

        def valid_expr(_expr: BooleanFunction):
            if _expr.func is not And and _expr.func is not Or:
                return False
            return [sub_expr for sub_expr in _expr.args if sub_expr.func is Not].__len__() == _expr.args.__len__()

        new_facts = dict()
        expr_to_convert = filter(lambda x: valid_expr(x), expr_set)
        for ex in expr_to_convert:
            func = And if ex.func is Or else Or
            not_args, other_args = sift(ex.args, lambda _arg: _arg.func is Not, binary=True)
            if other_args.__len__() > 0:
                continue
            else:
                not_args = list(map(lambda _arg: _arg.args[0], not_args))
                new_not_expr = Not(func(*not_args))
                new_facts[new_not_expr] = [ex]

        return new_facts

    @staticmethod
    def modus_ponens_rule(expr_set: Set[BooleanFunction]) -> InferenceRuleDict:

        implies_expr, non_implies_expr = sift(expr_set, lambda x: x.func is Implies, binary=True)
        non_implies_expr = set(non_implies_expr)
        new_facts = dict()

        for ex in implies_expr:
            lhs = ex.args[0]
            if non_implies_expr.__contains__(lhs):
                new_facts[ex.args[1]] = [ex, lhs]

        return new_facts

    @staticmethod
    def modus_tollens_rule(expr_set: Set[BooleanFunction]) -> InferenceRuleDict:

        implies_expr, non_implies_expr = sift(expr_set, lambda x: x.func is Implies, binary=True)
        non_implies_expr = set(non_implies_expr)
        new_facts = dict()

        for ex in implies_expr:
            rhs = ex.args[1]
            not_rhs = convert_to_not(rhs)

            if non_implies_expr.__contains__(not_rhs):
                lhs = ex.args[0]
                not_lhs = convert_to_not(lhs)
                new_facts[not_lhs] = [ex, not_rhs]

        return new_facts

    @staticmethod
    def syllogism(expr_set: Set[BooleanFunction]) -> InferenceRuleDict:

        implies_expr = list(filter(lambda x: x.func is Implies, expr_set))
        new_facts = dict()

        for ex in implies_expr:
            rhs = ex.args[1]
            valid_implies_expr = filter(lambda x: x.args[0] == rhs, implies_expr)
            for valid_expr in valid_implies_expr:
                new_expr = Implies(ex.args[0], valid_expr.args[1])
                new_facts[new_expr] = [ex, valid_expr]

        return new_facts

    @staticmethod
    def disjunctive_syllogism(expr_set: Set[BooleanFunction]) -> InferenceRuleDict:

        or_expr = set(filter(lambda x: x.func is Or, expr_set))
        new_facts = dict()

        def check_expr(_expr: BooleanFunction, loop_expr: BooleanFunction, non_args: List[BooleanFunction]):
            nonlocal new_facts
            if expr_set.__contains__(_expr):
                _, new_args = sift(args, lambda x: non_args.__contains__(x), binary=True)
                if new_args.__len__() == 0:
                    return
                elif new_args.__len__() == 1:
                    new_expr = new_args[0]
                else:
                    new_expr = Or(*new_args)
                new_facts[new_expr] = [loop_expr, _expr]

        for ex in or_expr:
            args = list(ex.args)
            for ag in args:
                not_ag = convert_to_not(ag)
                check_expr(not_ag, ex, [ag])

            for l in range(2, args.__len__(), 1):
                combs = list(itertools.combinations(args, l))
                for comb in combs:
                    comb_list = list(comb)
                    not_exprs = list(map(lambda x: convert_to_not(x), comb_list))
                    new_or_expr = Or(*not_exprs)
                    check_expr(new_or_expr, ex, comb_list)

        return new_facts

    @staticmethod
    def simplification(expr_set: Set[BooleanFunction]) -> InferenceRuleDict:

        and_expr = filter(lambda x: x.func is And, expr_set)
        new_facts = dict()

        for ex in and_expr:
            for ag in ex.args:
                new_facts[ag] = [ex]

        return new_facts

    @staticmethod
    def constructing_disjunctions(expr_set: Set[BooleanFunction]) -> InferenceRuleDict:

        non_implies_expr = list(filter(lambda x: x.func is not Implies, expr_set))
        combs = list(itertools.combinations(non_implies_expr, 2))

        new_facts = dict()
        for comb in combs:
            new_expr = Or(*comb)
            new_facts[new_expr] = list(comb)

        return new_facts

    @staticmethod
    def adjunctions(expr_set: Set[BooleanFunction]) -> InferenceRuleDict:

        non_implies_expr = list(filter(lambda x: x.func is not Implies, expr_set))
        combs = list(itertools.combinations(non_implies_expr, 2))

        new_facts = dict()
        for comb in combs:
            new_expr = And(*comb)
            new_facts[new_expr] = list(comb)

        return new_facts

    @staticmethod
    def negation_introduction(expr_set: Set[BooleanFunction]) -> InferenceRuleDict:

        implies_expr = list(filter(lambda x: x.func is Implies, expr_set))
        new_facts = dict()

        for ex in implies_expr:
            lhs = ex.args[0]
            rhs = ex.args[1]
            not_rhs = convert_to_not(rhs)

            valid_implies_expr = list(filter(lambda x: x.args[0] == lhs and x.args[1] == not_rhs, implies_expr))
            if valid_implies_expr.__len__() > 0:
                new_expr = convert_to_not(lhs)
                new_facts[new_expr] = [ex, valid_implies_expr[0]]

        return new_facts

    @staticmethod
    def case_analysis(expr_set: Set[BooleanFunction]) -> InferenceRuleDict:
        # + Constructive dilemma

        implies_expr = list(filter(lambda x: x.func is Implies, expr_set))
        or_expr = list(filter(lambda x: x.func is Or, expr_set))
        new_facts = dict()

        combs = list(itertools.combinations(implies_expr, 2))
        for comb in combs:
            lhs_1 = comb[0].args[0]
            lhs_2 = comb[1].args[0]
            args_set = set()
            if lhs_1.func is Or:
                args_set = args_set.union(set(lhs_1.args))
            else:
                args_set.add(lhs_1)
            if lhs_2.func is Or:
                args_set = args_set.union(set(lhs_2.args))
            else:
                args_set.add(lhs_2)
            new_or_expr = Or(*args_set)

            valid_implies_expr = list(filter(lambda x: x.has(new_or_expr), or_expr))
            if valid_implies_expr.__len__() > 0:
                rhs_1 = comb[0].args[1]
                rhs_2 = comb[1].args[1]
                if rhs_1 == rhs_2:
                    new_expr = rhs_1
                else:
                    new_expr = Or(rhs_1, rhs_2)
                new_facts[new_expr] = [comb[0], comb[1], valid_implies_expr[0]]

        return new_facts

    @staticmethod
    def contradictions(expr_set: Set[BooleanFunction]) -> InferenceRuleDict:

        not_expr = filter(lambda x: x.func is Not and x.args[0].func is And, expr_set)
        new_facts = dict()

        for ex in not_expr:
            args = ex.args[0].args
            not_args, non_not_args = sift(args, lambda x: x.func is Not, binary=True)

            if not_args.__len__() == 1:
                rhs = not_args[0].args[0]
                new_expr = Implies(And(*non_not_args), rhs)
                new_facts[new_expr] = [ex]

        return new_facts


# _facts = {parse_expr('p => q'),
#           parse_expr('p'),
#           parse_expr('~p => r'),
#           parse_expr('~p'),
#           parse_expr('(b | c) => a'),
#           parse_expr('b | c')}
# _new_facts = LogicInference.modus_ponens_rule(_facts)

# _facts = {
#     parse_expr('p => q'),
#     parse_expr('~q'),
#     parse_expr('~p => ~r'),
#     parse_expr('r'),
#     parse_expr('(b | c) => a'),
#     parse_expr('a'),
#     parse_expr('d => (a & b)'),  # them de morgan
#     parse_expr('~(a & b)')
# }
# _new_facts = LogicInference.modus_tollens_rule(_facts)

# _facts = {
#     parse_expr('p => q'),
#     parse_expr('q => r'),
#     parse_expr('(p | t) => q'),
#     parse_expr('q => t'),
#     parse_expr('(p | r) => ~q'),
#     parse_expr('~q => t'),
# }
# _new_facts = LogicInference.syllogism(_facts)

# _facts = {
#     parse_expr('p | q'),
#     parse_expr('~q'),
#     parse_expr('~p | ~r'),
#     parse_expr('r'),
#     parse_expr('(p & t) | q | r'),
#     parse_expr('p & t'),
#     parse_expr('t | q | r'),
#     parse_expr('~r | ~t'),  # them de morgan
# }
# _new_facts = LogicInference.disjunctive_syllogism(_facts)

# _facts = {
#     parse_expr('p & q'),
#     parse_expr('~q & (t | a) & r'),
#     parse_expr('~(p | ~r) & c & d'),
# }
# _new_facts = LogicInference.simplification(_facts)

# _facts = {
#     parse_expr('p & q'),
#     parse_expr('t | q'),
#     parse_expr('~(p | ~r)'),
#     parse_expr('~z | ~q'),
# }
# _new_facts = LogicInference.adjunctions(_facts)

# _facts = {
#     parse_expr('~p => q'),
#     parse_expr('~p => ~q'),
#     parse_expr('(p | t) => q'),
#     parse_expr('(p | t) => ~q'),
#     parse_expr('(p | r) => ~q'),
#     parse_expr('~q => t'),
# }
# _new_facts = LogicInference.negation_introduction(_facts)

# _facts = {
#     parse_expr('~p => r'),
#     parse_expr('q => t'),
#     parse_expr('~p | q'),
#     parse_expr('(p | t) => z'),
#     parse_expr('(p | r) => z'),
#     parse_expr('p | t | r'),
#     parse_expr('a => b'),
#     parse_expr('c => d'),
#     parse_expr('a | c | g'),
# }
# _new_facts = LogicInference.case_analysis(_facts)

# _facts = {
#     parse_expr('~p => r'),
#     parse_expr('q => t'),
#     parse_expr('~(p & ~q)'),
#     parse_expr('~(p & r)'),
#     parse_expr('~(a & c & ~s)'),
#     parse_expr('~(d & e & ~s & ~a)'),
# }
# _new_facts = LogicInference.contradictions(_facts)
#
# print(_new_facts)

# _premises = {
#     parse_expr('t => u'),
#     parse_expr('r => (s | t)'),
#     parse_expr('(~p | q) => r'),
#     parse_expr('~(s | u)'),
# }
# _conclusion = parse_expr('p')

# _premises = {
#     parse_expr('p'),
#     parse_expr('p => q'),
#     parse_expr('s | r'),
#     parse_expr('r => ~q'),
# }
# _conclusion = parse_expr('s | t')

# _premises = {
#     parse_expr('r => (s | t)'),
#     parse_expr('(~p | q) => r'),
#     parse_expr('~s & ~u'),
#     parse_expr('~u => ~t'),
# }
# _conclusion = parse_expr('p')

# _resolved, _solution = LogicInference.resolve(_premises, _conclusion)
# print(_resolved)
# print('===================')
# for sol in _solution:
#     print(sol)
#
# from sympy.parsing.sympy_parser import *
# try:
#     print(parse_expr('p => q | r'))
# except Exception:
#     print('fail')

if __name__ == '__main__':
    _premises = {
        parse_expr('r => (s | t)'),
        parse_expr('(~p | q) => r'),
        parse_expr('~s & ~u'),
        parse_expr('~u => ~t'),
    }
    _conclusion = parse_expr('p')

    _resolved, _solution = LogicInference.resolve(_premises, _conclusion)
    print(_resolved)
    print('===================')
    for sol in _solution:
        print(sol)
