from rule import *
from expr_tree import *
from typing import Optional, Set


class Reduce:
    @staticmethod
    def reduce_expr_string(ex_str: str):
        ex = parse_expr(ex_str)
        return Reduce.reduce(ex)

    @staticmethod
    def reduce(ex: BooleanFunction):

        # Step 0
        rules_1, rules_2, rules_3 = Rule.read_rules("rules.json")
        g = ex
        rules = []
        ex_list = []
        min_ex = g
        temp_ex = g
        old_ex_set = {g}
        rules_13 = rules_1  # + rules_3

        def step_2(_ex, ex_set):
            print("STEP 2")
            found_result = False
            found_ex = None
            found_rule = None
            for _rule in rules_2:
                _temp_rules = Reduce.apply_equal_rule(_ex, _rule)
                for _temp_rule in _temp_rules:
                    # print("temp_r", temp_r)
                    _h, _new_rule = Rule.rule_replace(_ex, _temp_rule)
                    if _new_rule and not ex_set.__contains__(_h):
                        found_result = True
                        found_ex = _h
                        found_rule = _rule
                        print("r", _rule)
                        print("h", _h)
                        print("found")
                        break
                if found_result:
                    break
            return found_result, found_ex, found_rule

        def step_3(_ex, ex_set):
            print("STEP 3")
            found_result = False
            found_ex = None
            found_rule = None
            for _rule in rules_13:
                # print("r", _rule)
                _temp_rules = Reduce.apply_equal_rule(_ex, _rule)
                for _temp_rule in _temp_rules:
                    # print("temp_r", temp_r)
                    _h, _new_rule = Rule.rule_replace(_ex, _temp_rule)
                    # print("h", h)
                    if _new_rule and not ex_set.__contains__(_h) and simpler(_h, _ex):
                        print("found")
                        if found_result:
                            if k_degree(found_ex) > k_degree(_h):
                                print("choose better rule")
                                found_ex = _h
                                found_rule = _rule
                        else:
                            found_result = True
                            found_ex = _h
                            found_rule = _rule
                        print("r", _rule)
                        print("h", _h)
                        break
                if found_result:
                    break
            return found_result, found_ex, found_rule

        def step_4(min_expr, temp_expr, expr_list, rule_list):
            if min_expr == temp_expr:
                return expr_list, rule_list
            if min_expr in expr_list:
                i = expr_list.index(min_expr)
                return expr_list[0:i + 1], rule_list[0:i + 1]
            else:
                return expr_list, rule_list

        # Step 1
        found = True
        while found and k_degree(min_ex) > 0:
            found = False
            for r in rules_1:
                temp_rules = Reduce.apply_equal_rule(min_ex, r)
                for temp_r in temp_rules:
                    h, new_rule = Rule.rule_replace(min_ex, temp_r)
                    if new_rule and not old_ex_set.__contains__(h) and simpler(h, min_ex):
                        if found:
                            print("choose better rule")
                            rules.append(r)
                            ex_list.append(h)
                            old_ex_set.add(h)
                            min_ex = h
                            temp_ex = h
                        else:
                            rules.append(r)
                            ex_list.append(h)
                            old_ex_set.add(h)
                            min_ex = h
                            temp_ex = h
                        print("h", h)
                        print("r", r)
                        print("found")
                        break
                if found:
                    break

        # if rules.__len__() == 0:
        #     return min_ex, rules  # to step 2
        # el
        if min_ex.args.__len__() == 1 and (
                min_ex.args[0].func is BooleanTrue or min_ex.args[0].func is BooleanFalse):
            ex_list, rules = step_4(min_ex, temp_ex, ex_list, rules)
            return min_ex, rules, ex_list  # to step 4

        # Step 2
        print("STEP 2")
        found, f_ex, f_rule = step_2(temp_ex, old_ex_set)

        if f_ex and f_rule:
            rules.append(f_rule)
            ex_list.append(f_ex)
            old_ex_set.add(f_ex)
            temp_ex = f_ex

        if not found:
            ex_list, rules = step_4(min_ex, temp_ex, ex_list, rules)
            return min_ex, rules, ex_list  # to step 4

        # Step 3
        print("STEP 3")
        can_expand = True
        found = True
        while found and k_degree(temp_ex) > 0:
            found, f_ex, f_rule = step_3(temp_ex, old_ex_set)
            if f_ex is not None and f_rule:
                rules.append(f_rule)
                ex_list.append(f_ex)
                old_ex_set.add(f_ex)
                temp_ex = f_ex
                if simpler(f_ex, min_ex):
                    min_ex = f_ex

            if not found and (can_expand or k_degree(temp_ex) <= 0):
                can_expand, f_ex, f_rule = step_2(temp_ex, old_ex_set)
                found = can_expand
                if f_ex and f_rule:
                    rules.append(f_rule)
                    ex_list.append(f_ex)
                    old_ex_set.add(f_ex)
                    temp_ex = f_ex

        ex_list, rules = step_4(min_ex, temp_ex, ex_list, rules)
        return min_ex, rules, ex_list

    @staticmethod
    def reduce_2_expr_string(ex_str: str):
        ex = parse_expr(ex_str)
        return Reduce.reduce_2(ex)

    @staticmethod
    def reduce_2(ex: BooleanFunction):

        def apply_found_rule(_ex, _rule):
            nonlocal ex_list, rules, min_ex, temp_ex, old_ex_set

            print("found_rule", _rule)
            pprint(_ex)

            rules.append(_rule)
            ex_list.append(_ex)
            old_ex_set.add(_ex)
            temp_ex = _ex
            if simpler(_ex, min_ex):
                min_ex = _ex

        def find_rules(_ex, rules_list, find_all=True):
            nonlocal ex_list, rules, min_ex, temp_ex, old_ex_set
            new_ex_count = 0
            found_result = True

            while found_result:
                found_result = False
                found_ex = None
                found_rule = None

                for _rule in rules_list:
                    # print("r", _rule)
                    _temp_rules = Reduce.apply_equal_rule(_ex, _rule)
                    for _temp_rule in _temp_rules:
                        # print("temp_r", temp_r)
                        _h, _new_rule = Rule.rule_replace(_ex, _temp_rule)

                        # print("h", h)
                        if _new_rule and not old_ex_set.__contains__(_h):
                            if found_result:
                                if find_all and simple_degree(found_ex) > simple_degree(
                                        _h) or not find_all and simple_degree(found_ex) < simple_degree(_h):
                                    # Trong một luật, chọn ra các tạo biểu thức ngắn nhất
                                    found_ex = _h
                                    found_rule = _rule
                            else:
                                found_result = True
                                found_ex = _h
                                found_rule = _rule

                if found_result:
                    apply_found_rule(found_ex, found_rule)
                    _ex = found_ex
                    new_ex_count += 1

                if found_result and not find_all:
                    break
            return new_ex_count > 0

        def distribute_rules(_ex):
            nonlocal ex_list, rules, min_ex, temp_ex, old_ex_set
            found_result = False
            found_ex = None
            found_rule = ('Luật phân phối', None, None)

            def valid_expr(_expr: BooleanFunction):
                if _expr.func is Or:
                    return len([sub_ag for sub_ag in ag.args if sub_ag.func is And])
                elif _expr.func is And:
                    return len([sub_ag for sub_ag in ag.args if sub_ag.func is Or])
                return 0

            for ag in preorder_traversal(_ex):
                valid_count = valid_expr(ag)
                if valid_count > 0:
                    if valid_count == 1:
                        _h = Reduce.distributive_law(_ex, ag)
                    elif valid_count == 2 and ag.args.__len__() == 2:
                        _h = Reduce.distributive_law_2_args(_ex, ag)
                    else:
                        continue

                    if _h is not None and not old_ex_set.__contains__(_h):
                        if found_result:
                            if simple_degree(_h) > simple_degree(found_ex):
                                found_ex = _h
                        else:
                            found_result = True
                            found_ex = _h

            if found_result:
                apply_found_rule(found_ex, found_rule)

            return found_result

        def de_morgan_rules(_ex):
            nonlocal ex_list, rules, min_ex, temp_ex, old_ex_set
            found_result = False
            found_ex = None
            found_rule = ('Luật De Morgan', None, None)

            def valid_expr(_expr: BooleanFunction):
                return _expr.func is Not and (_expr.args[0].func is And or _expr.args[0].func is Or)

            for ag in preorder_traversal(_ex):
                if valid_expr(ag):
                    _h = Reduce.de_morgan_law(_ex, ag)

                    if _h is not None and not old_ex_set.__contains__(_h):
                        if found_result:
                            if simple_degree(_h) < simple_degree(found_ex):
                                found_ex = _h
                        else:
                            found_result = True
                            found_ex = _h

            if found_result:
                apply_found_rule(found_ex, found_rule)

            return found_result

        def remove_useless_steps():
            nonlocal ex_list, rules
            if min_ex == temp_ex:
                return
            if min_ex in ex_list:
                i = ex_list.index(min_ex)
                ex_list = ex_list[0:i + 1]
                rules = rules[0:i + 1]

        # Step 0
        all_groups = ["group_1", "group_2", "group_3", "group_4", "group_5", "group_6", "group_7", "group_2_1"]
        all_rules = Rule.read_rules_2("rules_2.json", all_groups)
        rules_1 = all_rules[0]
        rules_2 = all_rules[1]
        rules_3 = all_rules[2]
        rules_4 = all_rules[3]
        rules_5 = all_rules[4]
        rules_6 = all_rules[5]
        rules_7 = all_rules[6]
        rules_2_1 = all_rules[7]

        g = ex
        rules = []
        ex_list = []
        min_ex = g
        temp_ex = g
        old_ex_set = {g}

        found = True
        distribution_count = 0
        found_distribution = False

        while found and k_degree(temp_ex) > 0:
            found = False

            # Group 1
            found_in_group_1 = temp_ex.atoms(Not).__len__() > 0 or temp_ex.atoms(
                BooleanTrue).__len__() > 0 or temp_ex.atoms(
                BooleanFalse).__len__() > 0
            while found_in_group_1:
                found_in_group_1 = find_rules(temp_ex, rules_1)
                found_in_group_1 = found_in_group_1 and (temp_ex.atoms(Not).__len__() > 0 or temp_ex.atoms(
                    BooleanTrue).__len__() > 0 or temp_ex.atoms(
                    BooleanFalse).__len__() > 0)

            found = found_in_group_1 or found
            print('found in group 1', found)

            # Group 2
            while find_rules(temp_ex, rules_2):
                found = True

            print('found in group 2', found)

            # Group 2.1
            if not found_distribution:
                while find_rules(temp_ex, rules_2_1):
                    found = True

            print('found in group 2.1', found)

            # Group 4
            found_implies = False
            implies_count = temp_ex.atoms(Implies).__len__()
            while implies_count > 0:
                found_implies = find_rules(temp_ex, rules_4) or found_implies
                implies_count = temp_ex.atoms(Implies).__len__()

            print('found in group 4', found_implies)

            # Group 5
            if found_implies:
                found = True
                while find_rules(temp_ex, rules_5):
                    print('found in group 5')

            # Group 3
            while find_rules(temp_ex, rules_3):
                found = True

            print('found in group 3', found)

            if found is False and distribution_count < 5:
                found_distribution = distribute_rules(temp_ex)
                found = found_distribution or found
                if found:
                    distribution_count += 1
            else:
                found_distribution = False

            if found is False:
                found = de_morgan_rules(temp_ex) or found

        remove_useless_steps()

        return min_ex, rules, ex_list

    @staticmethod
    def apply_equal_rule(ex: BooleanFunction, rule):
        left_rule_ex = rule[1]
        right_rule_ex = rule[2]

        rules = Rule.apply_rule(ex, left_rule_ex, right_rule_ex)
        # rules.extend(Reduce.apply_rule(ex, right_rule_ex, left_rule_ex))

        return rules

    @staticmethod
    def de_morgan_law(ex: BooleanFunction, ag: BooleanFunction) -> BooleanFunction:
        func = And if ag.args[0].func is Or else Or
        args = ag.args[0].args
        new_arg = list(map(lambda sub_arg: Not(sub_arg), list(args)))
        return ex.xreplace({ag, func(*new_arg)})

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
        big_args_set = Reduce.normalise_args_set(set(big_args.args))
        for a in small_args:
            if a.func is Symbol:
                count_a = 1 if big_args_set.__contains__(a) else 0
            else:
                set_a = Reduce.normalise_args_set(set(a.args))
                count_a = (big_args_set.intersection(set_a)).__len__()

            if count_a > count:
                count = count_a
                best_args = a

        small_args.remove(best_args)

        new_args = list(map(lambda x: ag.func(best_args, x), list(big_args.args)))
        sub_expr = func(*new_args)
        small_args.append(sub_expr)

        return ex.xreplace({ag: ag.func(*small_args)})

    @staticmethod
    def distributive_law_2_args(ex: BooleanFunction, ag: BooleanFunction) -> Optional[BooleanFunction]:
        if ag.args.__len__() != 2:
            return None

        left_args = list(ag.args[0].args)
        right_args = list(ag.args[1].args)

        if left_args.__len__() > 3 or right_args.__len__() > 3:
            return None

        func = And if ag.func is Or else Or

        from itertools import product

        sub_expr = [ag.func(lhs, rhs) for lhs, rhs in product(left_args, right_args)]

        return ex.xreplace({ag: func(*sub_expr)})

    @staticmethod
    def normalise_args_set(s: Set[BooleanFunction]) -> Set[BooleanFunction]:
        item_to_remove = set(item for item in s if item.func is Not)
        s = s.difference(item_to_remove)
        new_items = set()
        for i in item_to_remove:
            new_items = new_items.union(set(i.args))

        return s.union(new_items)
