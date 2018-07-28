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
        rules_13 = rules_1 # + rules_3

        def step_2(ex, ex_set):
            print("STEP 2")
            found_result = False
            found_ex = None
            found_rule = None
            for r in rules_2:
                temp_rules = Reduce.apply_equal_rule(ex, r)
                for temp_r in temp_rules:
                    # print("temp_r", temp_r)
                    h, new_rule = Rule.rule_replace(ex, temp_r)
                    if new_rule and not ex_set.__contains__(h):
                        found_result = True
                        found_ex = h
                        found_rule = r
                        print("r", r)
                        print("h", h)
                        print("found")
                        break
                if found_result:
                    break
            return found_result, found_ex, found_rule

        def step_3(ex, ex_set):
            print("STEP 3")
            found_result = False
            found_ex = None
            found_rule = None
            for r in rules_13:
                # print("r", r)
                temp_rules = Reduce.apply_equal_rule(ex, r)
                for temp_r in temp_rules:
                    # print("temp_r", temp_r)
                    h, new_rule = Rule.rule_replace(ex, temp_r)
                    # print("h", h)
                    if new_rule and not ex_set.__contains__(h) and Reduce.simpler(h, ex):
                        print("found")
                        if found_result:
                            if Reduce.k_degree(found_ex) > Reduce.k_degree(h):
                                print("choose better rule")
                                found_ex = h
                                found_rule = r
                        else:
                            found_result = True
                            found_ex = h
                            found_rule = r
                        print("r", r)
                        print("h", h)
                        break
                if found_result:
                    break
            return found_result, found_ex, found_rule

        def step_4(min_ex, temp_ex, ex_list, rule_list):
            if min_ex == temp_ex:
                return ex_list, rule_list
            if min_ex in ex_list:
                i = ex_list.index(min_ex)
                return ex_list[0:i + 1], rule_list[0:i + 1]
            else:
                return ex_list, rule_list

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
            if (f_ex or f_ex is false) and f_rule:
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
    def k_degree(ex: BooleanFunction) -> int:
        args = [arg for arg in postorder_traversal(ex) if
                arg.func is Symbol or arg.func is BooleanFalse or arg.func is BooleanTrue]

        not_count = [arg for arg in postorder_traversal(ex) if arg.func is Not].__len__()

        args_count = args.__len__()

        removed_constant_list = [arg for arg in args if arg.func is Symbol]
        args_set_count = set(removed_constant_list).__len__()
        return args_count - args_set_count + not_count

    @staticmethod
    def simple_degree(ex: BooleanFunction) -> int:
        def height(ex: BooleanFunction) -> int:
            sub_ex = [arg for arg in ex.args if
                        arg.func is not Symbol and arg.func is not BooleanFalse and arg.func is not BooleanTrue]
            if sub_ex.__len__() == 0:
                return 1
            else:
                return max([height(ex) for ex in sub_ex]) + 1

        def length(ex) -> int:
            count = 0
            for arg in postorder_traversal(ex):
                if arg.func is Symbol or arg.func is BooleanFalse or arg.func is BooleanTrue or arg.func is Not:
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

