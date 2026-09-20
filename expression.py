"""ITECC04 Laboratory 4, Parts B and C: the converter and the evaluator.

Part B turns infix into postfix using the Shunting Yard algorithm.
Part C evaluates a postfix expression.

Both use your own stack. Import it, do not use a bare Python list. If your
ArrayStack is not finished, these functions cannot work, so finish Part A
first.

TOKENS ARE SEPARATED BY SPACES. "3 + 4" is valid input, "3+4" is not. This
is deliberate: writing a real tokeniser is a different exercise, and mixing
it in here hides the algorithm you are meant to be learning.
"""

from stack_array import ArrayStack

# Written for you. Higher number binds tighter
PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "%": 2, "^": 3}
RIGHT_ASSOCIATIVE = {"^"}  # Written for you

def tokenize(expression):
    """Written for you. Splits on whitespace."""
    return expression.split()

def infix_to_postfix(expression, trace=None):
    """Step 1. Convert infix to postfix. Return a space-separated string."""
    output = []
    operators = ArrayStack()
    for token in tokenize(expression):
        if token in PRECEDENCE:
            while (not operators.is_empty()
                   and operators.peek() != "("
                   and (PRECEDENCE[operators.peek()] > PRECEDENCE[token]
                        or (PRECEDENCE[operators.peek()] == PRECEDENCE[token]
                            and token not in RIGHT_ASSOCIATIVE))):
                output.append(operators.pop())
            operators.push(token)
            action = "push operator"
        elif token == "(":
            operators.push(token)
            action = "push ("
        elif token == ")":
            while not operators.is_empty() and operators.peek() != "(":
                output.append(operators.pop())
            if operators.is_empty():
                raise ValueError("unbalanced parentheses: no matching (")
            operators.pop()  # discard the "("
            action = "pop to ("
        else:
            output.append(token)
            action = "operand to output"

        if trace is not None:
            trace.append((token, action, " ".join(output), " ".join(operators._items)))

    while not operators.is_empty():
        top = operators.pop()
        if top == "(":
            raise ValueError("unbalanced parentheses: no matching )")
        output.append(top)

    if trace is not None:
        trace.append(("end", "drain stack", " ".join(output), ""))
    return " ".join(output)

def apply_operator(operator, left, right):
    """Step 3. Return the result of `left operator right`.
    Handle + - * / % ^. Raise ZeroDivisionError for / and % when right is 0.
    Raise ValueError for any operator you do not know."""
    if operator == "+":
        return left + right
    if operator == "-":
        return left - right
    if operator == "*":
        return left * right
    if operator == "/":
        if right == 0:
            raise ZeroDivisionError("division by zero in the expression")
        return left / right
    if operator == "%":
        if right == 0:
            raise ZeroDivisionError("modulo by zero in the expression")
        return left % right
    if operator == "^":
        return left ** right
    raise ValueError(f"unknown operator '{operator}'")

def _fmt(value):
    """Format value: show as integer if whole number, else decimal."""
    return str(int(value)) if float(value).is_integer() else str(value)

def evaluate_postfix(expression, trace=None):
    """Step 2. Evaluate a postfix expression. Return a float."""
    values = ArrayStack()
    for token in tokenize(expression):
        if token in PRECEDENCE:
            if values.size() < 2:
                raise ValueError(f"not enough operands for '{token}'")
            right = values.pop()
            left = values.pop()
            values.push(apply_operator(token, left, right))
        else:
            values.push(float(token))

        if trace is not None:
            trace.append((token, " ".join(_fmt(v) for v in values._items)))

    if values.size() != 1:
        raise ValueError("malformed expression: operands left over")
    return values.pop()

def convert_and_evaluate(expression):
    """Written for you. Used by the test file and by the classwork demo."""
    postfix = infix_to_postfix(expression)
    return postfix, evaluate_postfix(postfix)

if __name__ == "__main__":
    # Once Steps 1 to 3 are written, this prints the worked example from the
    # lecture. Until then it reports which step is still missing.
    try:
        postfix, value = convert_and_evaluate("3 + 4 * 2")
        print("infix  : 3 + 4 * 2")
        print("postfix:", postfix)
        print("value  :", value)
    except NotImplementedError as unfinished:
        print("Not written yet ->", unfinished)
