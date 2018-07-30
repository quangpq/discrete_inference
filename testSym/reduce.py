from rule import *


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
                    if _new_rule and not ex_set.__contains__(_h) and Reduce.simpler(_h, _ex):
                        print("found")
                        if found_result:
                            if Reduce.k_degree(found_ex) > Reduce.k_degree(_h):
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
        while found and Reduce.k_degree(min_ex) > 0:
            found = False
            for r in rules_1:
                temp_rules = Reduce.apply_equal_rule(min_ex, r)
                for temp_r in temp_rules:
                    h, new_rule = Rule.rule_replace(min_ex, temp_r)
                    if new_rule and not old_ex_set.__contains__(h) and Reduce.simpler(h, min_ex):
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
        while found and Reduce.k_degree(temp_ex) > 0:
            found, f_ex, f_rule = step_3(temp_ex, old_ex_set)
            if f_ex is not None and f_rule:
                rules.append(f_rule)
                ex_list.append(f_ex)
                old_ex_set.add(f_ex)
                temp_ex = f_ex
                if Reduce.simpler(f_ex, min_ex):
                    min_ex = f_ex

            if not found and (can_expand or Reduce.k_degree(temp_ex) <= 0):
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

        def find_rules(_ex, rules_list, find_all=True):
            nonlocal ex_list, rules, min_ex, temp_ex, old_ex_set
            new_ex_count = 0

            for _rule in rules_list:
                found_result = False
                found_ex = None
                found_rule = None

                # print("r", _rule)
                _temp_rules = Reduce.apply_equal_rule(_ex, _rule)
                for _temp_rule in _temp_rules:
                    # print("temp_r", temp_r)
                    _h, _new_rule = Rule.rule_replace(_ex, _temp_rule)
                    # print("h", h)
                    if _new_rule and not old_ex_set.__contains__(_h):
                        if found_result:
                            if set(found_ex.atoms(Symbol)).__len__() > set(_h.atoms(Symbol)).__len__():
                                # Trong một luật, chọn ra các tạo biểu thức ngắn nhất
                                found_ex = _h
                                found_rule = _rule
                        else:
                            found_result = True
                            found_ex = _h
                            found_rule = _rule

                if found_result:
                    print("found_rule", found_rule)
                    pprint(found_ex)

                    rules.append(found_rule)
                    ex_list.append(found_ex)
                    old_ex_set.add(found_ex)
                    temp_ex = found_ex
                    _ex = found_ex
                    if Reduce.simpler(found_ex, min_ex):
                        min_ex = found_ex
                    new_ex_count += 1
                    if not find_all:
                        break

            return new_ex_count > 0

        def remove_useless_steps():
            nonlocal ex_list, rules
            if min_ex == temp_ex:
                return
            if min_ex in ex_list:
                i = ex_list.index(min_ex)
                ex_list = ex_list[0:i + 1]
                rules = rules[0:i + 1]

        # Step 0
        all_groups = ["group_1", "group_2", "group_3", "group_4", "group_5", "group_6", "group_7"]
        all_rules = Rule.read_rules_2("rules_2.json", all_groups)
        rules_1 = all_rules[0]
        rules_2 = all_rules[1]
        rules_3 = all_rules[2]
        rules_4 = all_rules[3]
        rules_5 = all_rules[4]
        rules_6 = all_rules[5]
        rules_7 = all_rules[6]

        g = ex
        rules = []
        ex_list = []
        min_ex = g
        temp_ex = g
        old_ex_set = {g}

        found = True

        while found and Reduce.k_degree(temp_ex) > 0:
            found = False

            # Group 2
            found_in_group_2 = temp_ex.atoms(Not).__len__() > 0 or temp_ex.atoms(
                BooleanTrue).__len__() > 0 or temp_ex.atoms(
                BooleanFalse).__len__() > 0
            while found_in_group_2:
                found_in_group_2 = find_rules(temp_ex, rules_2)
                found_in_group_2 = found_in_group_2 and (temp_ex.atoms(Not).__len__() > 0 or temp_ex.atoms(
                    BooleanTrue).__len__() > 0 or temp_ex.atoms(
                    BooleanFalse).__len__() > 0)

            found = found_in_group_2 or found
            print('found in group 2', found)

            # Group 1
            while find_rules(temp_ex, rules_1):
                found = True

            print('found in group 1', found)

            # Group 4
            found_implies = False
            implies_count = temp_ex.atoms(Implies).__len__()
            while implies_count > 0:
                found_implies = find_rules(temp_ex, rules_4) or found_implies
                implies_count = temp_ex.atoms(Implies).__len__()

            print('found in group 4', found_implies)

            if found_implies:
                found = True
                while find_rules(temp_ex, rules_5):
                    print('found in group 5')

            # Group 3
            while find_rules(temp_ex, rules_3):
                found = True

            print('found in group 3', found)

            if found is False:
                found = find_rules(temp_ex, rules_7, find_all=False) or found

            if found is False:
                found = find_rules(temp_ex, rules_6) or found

        remove_useless_steps()

        return min_ex, rules, ex_list

    @staticmethod
    def k_degree(ex: BooleanFunction) -> int:
        args = [ag for ag in postorder_traversal(ex) if
                ag.func is Symbol or ag.func is BooleanFalse or ag.func is BooleanTrue]

        not_count = [ag for ag in postorder_traversal(ex) if ag.func is Not].__len__()

        args_count = args.__len__()

        removed_constant_list = [ag for ag in args if ag.func is Symbol]
        args_set_count = set(removed_constant_list).__len__()
        return args_count - args_set_count + not_count

    @staticmethod
    def simple_degree(ex: BooleanFunction) -> int:
        def height(_ex: BooleanFunction) -> int:
            sub_ex = [ag for ag in _ex.args if
                      ag.func is not Symbol and ag.func is not BooleanFalse and ag.func is not BooleanTrue]
            if sub_ex.__len__() == 0:
                return 1
            else:
                return max([height(_ex) for _ex in sub_ex]) + 1

        def length(_ex) -> int:
            count = 0
            for ag in postorder_traversal(_ex):
                if ag.func is Symbol or ag.func is BooleanFalse or ag.func is BooleanTrue or ag.func is Not:
                    count += 1

            return count

        return length(ex) + height(ex)

    @staticmethod
    def simpler(ex_1: BooleanFunction, ex_2: BooleanFunction) -> bool:
        return Reduce.simple_degree(ex_1) <= Reduce.simple_degree(ex_2)

    @staticmethod
    def apply_equal_rule(ex: BooleanFunction, rule):
        left_rule_ex = rule[1]
        right_rule_ex = rule[2]

        rules = Rule.apply_rule(ex, left_rule_ex, right_rule_ex)
        # rules.extend(Reduce.apply_rule(ex, right_rule_ex, left_rule_ex))

        return rules
