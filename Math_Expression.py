from itertools import product

DEBUG = False
operators = ["+", "-", "*", "/", "//", "%", "**"]


def format_expr(expression: str) -> str:
    formatted_expression = ""
    idx = 0
    while idx < len(expression):
        char = expression[idx]
        if char in operators and idx + 1 < len(expression):
            if char == expression[idx + 1]:
                formatted_expression += f" {char + expression[idx + 1]} "
                idx += 1
            else:
                formatted_expression += f" {char} "
        else:
            formatted_expression += char
        idx += 1
    return formatted_expression.strip()


def add_parentheses(expression: list[str]) -> list[list[str]]:
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


def find_pattern(result: int, numbers: list[int]) -> str | None:
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
    number = list(map(int, input("Enter numbers: ").split()))
    result = int(input("Enter result: ").strip())
    length = len(str(result))
    print()

    for iterate in range(result + 1):
        pattern = find_pattern(iterate, number)
        space = ' ' * (length - len(str(iterate)))
        if pattern:
            print(f"{iterate}{space} = {format_expr(pattern)}")
        else:
            print(f"No pattern found for {iterate}")