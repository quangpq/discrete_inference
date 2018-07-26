from rule import *


class Reduce:
    @staticmethod
    def reduce(expr: BooleanFunction):

        # Step 0
        rules_1, rules_2, rules_3 = Rule.read_rules("rules.json")
        g = expr
        rules = []
        expr_list = []
        min_expr = g
        temp_expr = g
        old_expr_set = {g}
        rules_13 = rules_1 # + rules_3

        def step_2(ex, ex_set):
            print("STEP 2")
            found_result = False
            found_expr = None
            found_rule = None
            for r in rules_2:
                print("r", r)
                temp_rules = Reduce.apply_equal_rule(ex, r)
                for temp_r in temp_rules:
                    print("temp_r", temp_r)
                    h, new_rule = Rule.rule_replace(ex, temp_r)
                    if new_rule and not ex_set.__contains__(h):
                        found_result = True
                        found_expr = h
                        found_rule = r
                        print("h", h)
                        print("found")
                        break
                if found_result:
                    break
            return found_result, found_expr, found_rule

        def step_3(ex, ex_set):
            print("STEP 3")
            found_result = False
            found_expr = None
            found_rule = None
            for r in rules_13:
                print("r", r)
                temp_rules = Reduce.apply_equal_rule(ex, r)
                for temp_r in temp_rules:
                    print("temp_r", temp_r)
                    h, new_rule = Rule.rule_replace(ex, temp_r)
                    print("h", h)
                    if new_rule and not ex_set.__contains__(h) and Reduce.simpler(h, ex):
                        print("found")
                        if found_result:
                            if Reduce.k_degree(found_expr) > Reduce.k_degree(h):
                                print("choose better rule")
                                found_expr = h
                                found_rule = r
                        else:
                            found_result = True
                            found_expr = h
                            found_rule = r
                        break
                if found_result:
                    break
            return found_result, found_expr, found_rule

        def step_4(min_ex, temp_ex, ex_list, rule_list):
            if min_ex == temp_ex:
                return ex_list, rule_list
            if min_ex in ex_list:
                i = ex_list.index(min_expr)
                return ex_list[0:i + 1], rule_list[0:i + 1]
            else:
                return ex_list, rule_list

        # Step 1
        found = True
        while found and Reduce.k_degree(min_expr) > 0:
            found = False
            for r in rules_1:
                print("r", r)
                temp_rules = Reduce.apply_equal_rule(min_expr, r)
                for temp_r in temp_rules:
                    print("temp_r", temp_r)
                    h, new_rule = Rule.rule_replace(min_expr, temp_r)
                    if new_rule and not old_expr_set.__contains__(h) and Reduce.simpler(h, min_expr):
                        found = True
                        rules.append(r)
                        expr_list.append(h)
                        old_expr_set.add(h)
                        min_expr = h
                        temp_expr = h
                        print("h", h)
                        print("found")
                        break
                if found:
                    break

        # if rules.__len__() == 0:
        #     return min_expr, rules  # to step 2
        # el
        if min_expr.args.__len__() == 1 and (
                min_expr.args[0].func is BooleanTrue or min_expr.args[0].func is BooleanFalse):
            expr_list, rules = step_4(min_expr, temp_expr, expr_list, rules)
            return min_expr, rules, expr_list  # to step 4

        # Step 2
        print("STEP 2")
        found, f_expr, f_rule = step_2(temp_expr, old_expr_set)

        if f_expr and f_rule:
            rules.append(f_rule)
            expr_list.append(f_expr)
            old_expr_set.add(f_expr)
            temp_expr = f_expr

        if not found:
            expr_list, rules = step_4(min_expr, temp_expr, expr_list, rules)
            return min_expr, rules, expr_list  # to step 4

        # Step 3
        print("STEP 3")
        can_expand = True
        found = True
        while found and Reduce.k_degree(temp_expr) > 0:
            found, f_expr, f_rule = step_3(temp_expr, old_expr_set)
            if f_expr and f_rule:
                rules.append(f_rule)
                expr_list.append(f_expr)
                old_expr_set.add(f_expr)
                temp_expr = f_expr
                if Reduce.simpler(f_expr, min_expr):
                    min_expr = f_expr

            if not found and (can_expand or Reduce.k_degree(temp_expr) <= 0):
                can_expand, f_expr, f_rule = step_2(temp_expr, old_expr_set)
                found = can_expand
                if f_expr and f_rule:
                    rules.append(f_rule)
                    expr_list.append(f_expr)
                    old_expr_set.add(f_expr)
                    temp_expr = f_expr

        expr_list, rules = step_4(min_expr, temp_expr, expr_list, rules)
        return min_expr, rules, expr_list

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

    @staticmethod
    def apply_equal_rule(expr: BooleanFunction, rule):
        left_rule_expr = rule[1]
        right_rule_expr = rule[2]

        rules = Rule.apply_rule(expr, left_rule_expr, right_rule_expr)
        # rules.extend(Reduce.apply_rule(expr, right_rule_expr, left_rule_expr))

        return rules

