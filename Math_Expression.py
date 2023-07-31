from itertools import product

DEBUG = False
operators = ["+", "-", "*", "/", "//", "%", "**"]


def add_parentheses(expression):
    def evaluate_expression(exp):
        try:
            return eval(''.join(exp))
        except:
            return False

    def add_parentheses_recursive(exp, start, end):
        results = []
        if start == end:
            if evaluate_expression(exp):
                return [''.join(exp[start:end + 1])]

        for i in range(start, end + 1):
            if exp[i] in operators:
                left  = add_parentheses_recursive(exp, start, i - 1)
                right = add_parentheses_recursive(exp, i + 1, end)
                for l in left:
                    for r in right:
                        results.append(f"({l}{exp[i]}{r})")
        return results

    return add_parentheses_recursive(expression, 0, len(expression) - 1)


def find_pattern(result, numbers, operators):
    num_repeat = len(numbers) - 1

    # for permutation in list(permutations(numbers)):
    for op_combination in product(operators, repeat=num_repeat):
        expression = []
        for i, num in enumerate(numbers):
            expression += [str(num)]
            if i < len(op_combination):
                expression += [op_combination[i]]
        
        # Calculate Expression
        parentheses = add_parentheses(expression)
        for math_expr in parentheses:
            try:
                if eval(math_expr) == result:
                    return math_expr
            except Exception as error:
                if DEBUG == True:
                    print(error)
                continue
    return None


if __name__ == '__main__':
    result = 9
    numbers = [3, 7, 5]

    pattern = find_pattern(result, numbers, operators)
    if pattern:
        print(f"{result} = {pattern}")
    else:
        print("No pattern found.")
