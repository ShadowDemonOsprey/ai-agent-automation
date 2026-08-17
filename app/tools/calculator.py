"""
Advanced calculator tool.

A secure mathematical expression evaluator.

Unlike the original implementation this tool never uses
Python's eval(). Instead it:

1. Parses the expression with the ast module.
2. Validates every node against a whitelist
   (no attributes, subscripts, imports or code).
3. Evaluates using only math functions and constants
   that are explicitly allowed.

Supported mathematics:
- Arithmetic: + - * / % ** (power)
- Roots: sqrt, cbrt, power
- Trigonometry: sin, cos, tan, asin, acos, atan, atan2
- Hyperbolic: sinh, cosh, tanh
- Logarithms: log(x), log(x, base), log2, log10, ln
- Exponentials: exp, pow
- Integer & number theory: factorial, gcd, lcm, comb, perm, mod
- Rounding: round, floor, ceil, trunc, abs
- Aggregates: min, max, fsum, prod
- Special functions: gamma, lgamma, erf, hypot
- Conversions: degrees, radians
- Constants: pi, e, tau, phi (golden ratio), inf, nan
- Comparison helpers inside conditions

Examples:
    "sin(pi/2)"
    "sqrt(144) + 2^3"
    "log(1000, 10)"
    "factorial(5)"
    "5!"
    "2pi"
    "max(3, 7, 5)"
"""


import ast
import math
import operator
import re


class ExpressionError(ValueError):
    """
    Raised when an expression cannot be evaluated safely.
    """


    pass



def _cbrt(x: float) -> float:
    """
    Cube root that works for negative numbers.
    """

    if x < 0:
        return -((-x) ** (1.0 / 3.0))

    return x ** (1.0 / 3.0)


def _mod(a: float, b: float) -> float:
    """
    Safe modulo operator (Python floor modulo).
    """

    return a % b


def _fsum(*args) -> float:
    """
    Sum a variable number of arguments accurately.
    """

    return math.fsum(args)


def _prod(*args) -> float:
    """
    Multiply a variable number of arguments.
    """

    result = 1

    for value in args:
        result *= value

    return result


def _sci(value: int) -> str:
    """
    Format a very large integer in scientific notation
    without stringifying every digit.

    Python limits int-to-str conversion to about 4300
    digits, so huge results such as 2**1000000 must be
    converted through integer arithmetic instead.
    """

    sign = "-" if value < 0 else ""

    value = abs(value)

    # Approximate decimal exponent from the bit length.
    exponent = int(
        (value.bit_length() - 1) * 0.30102999566398114
    )

    # Correct the estimate by direct comparison.
    while 10 ** (exponent + 1) <= value:

        exponent += 1

    while exponent > 0 and 10 ** exponent > value:

        exponent -= 1

    if exponent >= 8:

        # First 9 significant digits as a mantissa in [1, 10).
        head = value // (10 ** (exponent - 8))

        mantissa = head / 100_000_000.0

        return f"{sign}{mantissa:.6f}e+{exponent}"

    return f"{sign}{value}"


def _fmt_result(value: object):
    """
    Format a numeric result for display.

    Integers stay integers (very large ones become
    scientific notation). Floats are rounded to remove
    floating point noise such as 0.30000000000000004.
    """

    if isinstance(value, bool):
        return int(value)

    if isinstance(value, int):

        if value and value.bit_length() > 1024:

            return _sci(value)

        return value

    if isinstance(value, float):

        if math.isinf(value):
            return value

        if math.isnan(value):
            return value

        rounded = round(value, 12)

        if rounded.is_integer():
            return int(rounded)

        return rounded

    return value


# Functions available inside expressions.
FUNCTIONS = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "atan2": math.atan2,
    "sinh": math.sinh,
    "cosh": math.cosh,
    "tanh": math.tanh,
    "log": math.log,
    "log2": math.log2,
    "log10": math.log10,
    "ln": math.log,
    "exp": math.exp,
    "sqrt": math.sqrt,
    "cbrt": _cbrt,
    "abs": abs,
    "floor": math.floor,
    "ceil": math.ceil,
    "trunc": math.trunc,
    "round": round,
    "min": min,
    "max": max,
    "pow": math.pow,
    "gcd": math.gcd,
    "lcm": math.lcm,
    "factorial": math.factorial,
    "mod": _mod,
    "fmod": math.fmod,
    "hypot": math.hypot,
    "degrees": math.degrees,
    "radians": math.radians,
    "comb": math.comb,
    "perm": math.perm,
    "fsum": _fsum,
    "prod": _prod,
    "gamma": math.gamma,
    "lgamma": math.lgamma,
    "erf": math.erf,
    "copysign": math.copysign,
    "isclose": math.isclose,
    "remainder": math.remainder,
}

# Constants available inside expressions.
CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
    "phi": (1 + math.sqrt(5)) / 2,
    "inf": math.inf,
    "infinity": math.inf,
    "nan": math.nan,
}

# Binary operators mapped to Python operations.
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Comparison operators.
_COMPARE_OPS = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
}

MAX_EXPRESSION_LENGTH = 2000
MAX_DEPTH = 100


def _normalize(expression: str) -> str:
    """
    Clean common mathematical notation into Python syntax.
    """

    expression = expression.strip().lower()

    # Unicode symbols.
    expression = expression.replace("×", "*")
    expression = expression.replace("÷", "/")
    expression = expression.replace("−", "-")
    expression = expression.replace("π", "pi")
    expression = expression.replace("∞", "inf")
    expression = expression.replace("√(", "sqrt(")
    expression = expression.replace("²", "**2")
    expression = expression.replace("³", "**3")

    # Word operators.
    expression = re.sub(r"\bmod\b", "%", expression)
    expression = re.sub(r"\bdiv\b", "/", expression)

    # "to the power of" must be replaced before "power of"
    # so the phrase does not leave "to the" behind.
    expression = re.sub(r"to the power of", "**", expression)
    expression = re.sub(r"\bpower of\b", "**", expression)

    # Thousands separators: "1,000" -> "1000".
    # Commas inside function calls ("log(8, 2)") are kept
    # because a comma there is not followed by three digits.
    expression = re.sub(
        r"(?<=\d),(?=\d{3}(?!\d))",
        "",
        expression,
    )

    # Root phrases: "square root of 144" and "cube root of 27".
    expression = re.sub(
        r"square root of\s*(-?[0-9a-z.]+)",
        r"sqrt(\1)",
        expression,
    )
    expression = re.sub(
        r"cube root of\s*(-?[0-9a-z.]+)",
        r"cbrt(\1)",
        expression,
    )

    # Factorial words: "5 factorial" and "factorial of 5".
    expression = re.sub(
        r"(\d+(?:\.\d+)?)\s+factorial\b",
        r"factorial(\1)",
        expression,
    )
    expression = re.sub(
        r"factorial\s+of\s+(\d+(?:\.\d+)?)",
        r"factorial(\1)",
        expression,
    )

    # ^ means power in calculators.
    expression = expression.replace("^", "**")

    # Postfix factorial: 5! -> factorial(5).
    # The negative lookahead prevents matching "!="
    # as factorial of the preceding number.
    expression = re.sub(
        r"(\d+(?:\.\d+)?)\s*!(?!=)",
        r"factorial(\1)",
        expression
    )

    # Implicit multiplication: "2pi" -> "2*pi".
    #
    # Only applies when the following letters spell a
    # known constant, so scientific notation such as
    # "1e100" and words like "if"/"else" are untouched.
    def _implicit_multiply(match):

        number, name = match.groups()

        if name in CONSTANTS:

            return f"{number}*{name}"

        return match.group(0)

    expression = re.sub(
        r"(\d)\s*([a-z]+)(?![0-9.])",
        _implicit_multiply,
        expression
    )

    # Parenthesis adjacency: "(2)(3)" -> "(2)*(3)".
    #
    # The lookbehind prevents breaking function names
    # that end in digits such as "atan2(...)".
    expression = re.sub(
        r"(?<![0-9a-zA-Z_.])(\d+(?:\.\d+)?)\s*\(",
        r"\1*(",
        expression
    )
    expression = re.sub(r"\)\s*\(", r")*(", expression)
    expression = re.sub(r"\)\s*(\d)", r")*\1", expression)

    return expression


class ExpressionEvaluator:
    """
    Safe evaluator for mathematical expressions.
    """


    def evaluate(self, expression: str):
        """
        Evaluate a mathematical expression.

        Args:
            expression:
                Mathematical expression.

        Returns:
            Numeric result.

        Raises:
            ExpressionError:
                If the expression is invalid or unsafe.
        """

        if not isinstance(expression, str) or not expression.strip():

            raise ExpressionError("Empty expression")

        if len(expression) > MAX_EXPRESSION_LENGTH:

            raise ExpressionError("Expression too long")

        normalized = _normalize(expression)

        try:

            tree = ast.parse(
                normalized,
                mode="eval"
            )

        except SyntaxError as error:

            raise ExpressionError(
                f"Invalid expression: {error}"
            )

        return self._eval(tree, depth=0)



    def _eval(self, node, depth: int):
        """
        Recursively evaluate an AST node.
        """

        if depth > MAX_DEPTH:

            raise ExpressionError("Expression too deeply nested")

        # Expression wrapper.
        if isinstance(node, ast.Expression):

            return self._eval(node.body, depth + 1)

        # Literal numbers.
        if isinstance(node, ast.Constant):

            if isinstance(node.value, (int, float)):

                return node.value

            raise ExpressionError(
                f"Literal {node.value!r} is not allowed"
            )

        # Constants such as pi and e.
        if isinstance(node, ast.Name):

            name = node.id.lower()

            if name in CONSTANTS:

                return CONSTANTS[name]

            raise ExpressionError(
                f"Unknown symbol '{node.id}'"
            )

        # Binary operations.
        if isinstance(node, ast.BinOp):

            left = self._eval(node.left, depth + 1)

            right = self._eval(node.right, depth + 1)

            operation = _BIN_OPS.get(type(node.op))

            if operation is None:

                raise ExpressionError(
                    f"Operator '{type(node.op).__name__}' not allowed"
                )

            try:

                return operation(left, right)

            except ZeroDivisionError:

                raise ExpressionError("Division by zero")

            except OverflowError:

                raise ExpressionError("Result too large")

        # Unary plus/minus.
        if isinstance(node, ast.UnaryOp):

            value = self._eval(node.operand, depth + 1)

            if isinstance(node.op, ast.USub):

                return -value

            if isinstance(node.op, ast.UAdd):

                return +value

            raise ExpressionError("Unary operator not allowed")

        # Function calls.
        if isinstance(node, ast.Call):

            return self._eval_call(node, depth)

        # Conditional expressions.
        if isinstance(node, ast.IfExp):

            condition = self._eval(node.test, depth + 1)

            if condition:

                return self._eval(node.body, depth + 1)

            return self._eval(node.orelse, depth + 1)

        # Comparisons used inside conditions.
        if isinstance(node, ast.Compare):

            left = self._eval(node.left, depth + 1)

            for operator_node, comparator in zip(
                node.ops,
                node.comparators
            ):

                right = self._eval(comparator, depth + 1)

                comparison = _COMPARE_OPS.get(type(operator_node))

                if comparison is None:

                    raise ExpressionError(
                        "Comparison operator not allowed"
                    )

                if not comparison(left, right):

                    return False

                left = right

            return True

        # Boolean logic inside conditions.
        if isinstance(node, ast.BoolOp):

            if isinstance(node.op, ast.And):

                for value in node.values:

                    if not self._eval(value, depth + 1):

                        return False

                return True

            if isinstance(node.op, ast.Or):

                for value in node.values:

                    if self._eval(value, depth + 1):

                        return True

                return False

        raise ExpressionError(
            "Expression contains unsupported syntax"
        )



    def _eval_call(self, node, depth: int):
        """
        Evaluate a function call node safely.
        """

        # Only direct function names are allowed.
        if not isinstance(node.func, ast.Name):

            raise ExpressionError(
                "Only direct function calls are allowed"
            )

        name = node.func.id.lower()

        function = FUNCTIONS.get(name)

        if function is None:

            raise ExpressionError(
                f"Function '{node.func.id}' is not supported"
            )

        # Keyword arguments are not allowed.
        if node.keywords:

            raise ExpressionError("Keyword arguments not allowed")

        arguments = [
            self._eval(argument, depth + 1)
            for argument in node.args
        ]

        try:

            return function(*arguments)

        except ZeroDivisionError:

            raise ExpressionError("Division by zero in function")

        except OverflowError:

            raise ExpressionError("Result too large")

        except (ValueError, TypeError) as error:

            raise ExpressionError(
                f"Error in {name}: {error}"
            )



def calculator(expression: str) -> dict:
    """
    Calculate a mathematical expression.

    Args:
        expression (str):
            Mathematical expression.

            Example:
            "sqrt(144) + 2^3"

    Returns:
        dict:
            Calculation result or error.
    """

    try:

        evaluator = ExpressionEvaluator()

        result = evaluator.evaluate(expression)

        return {
            "tool": "calculator",
            "expression": expression,
            "result": _fmt_result(result)
        }

    except ExpressionError as error:

        return {
            "tool": "calculator",
            "expression": expression,
            "error": str(error)
        }

    except Exception as error:

        return {
            "tool": "calculator",
            "expression": expression,
            "error": f"Calculation failed: {error}"
        }
