"""
Advanced calculator tests.

Covers the secure expression evaluator with strong
mathematics: arithmetic, trigonometry, logarithms,
roots, factorials, special functions, constants,
natural language notation and security hardening.
"""


from app.tools.calculator import calculator


def test_basic_arithmetic():
    assert calculator("25 * 40")["result"] == 1000
    assert calculator("2 + 3 * 4")["result"] == 14
    assert calculator("(2 + 3) * 4")["result"] == 20
    assert calculator("10 / 4")["result"] == 2.5
    assert calculator("10 % 3")["result"] == 1
    assert calculator("17 // 5")["result"] == 3


def test_powers_and_roots():
    assert calculator("2 ** 10")["result"] == 1024
    assert calculator("2^10")["result"] == 1024
    assert calculator("sqrt(144)")["result"] == 12
    assert calculator("cbrt(27)")["result"] == 3
    assert calculator("sqrt(2)^2")["result"] == 2
    assert calculator("pow(2, 0.5)")["result"] == 1.414213562373


def test_trigonometry():
    assert calculator("sin(pi/2)")["result"] == 1
    assert calculator("cos(0)")["result"] == 1
    assert calculator("tan(pi/4)")["result"] == 1
    assert calculator("asin(1)")["result"] == 1.570796326795
    assert calculator("acos(1)")["result"] == 0
    assert calculator("atan(1)")["result"] == 0.785398163397
    assert calculator("atan2(1, 1)")["result"] == 0.785398163397
    assert calculator("degrees(pi)")["result"] == 180
    assert calculator("radians(180)")["result"] == 3.14159265359


def test_hyperbolic():
    assert calculator("sinh(0)")["result"] == 0
    assert calculator("cosh(0)")["result"] == 1
    assert calculator("tanh(0)")["result"] == 0


def test_logarithms_and_exponential():
    assert calculator("log(1000, 10)")["result"] == 3
    assert calculator("log10(1000)")["result"] == 3
    assert calculator("log2(8)")["result"] == 3
    assert calculator("ln(e)")["result"] == 1
    assert calculator("exp(1)")["result"] == 2.718281828459
    assert calculator("e**2")["result"] == 7.389056098931


def test_integer_theory():
    assert calculator("factorial(5)")["result"] == 120
    assert calculator("5!")["result"] == 120
    assert calculator("gcd(48, 36)")["result"] == 12
    assert calculator("lcm(4, 6)")["result"] == 12
    assert calculator("comb(5, 2)")["result"] == 10
    assert calculator("perm(5, 2)")["result"] == 20


def test_special_functions():
    assert calculator("gamma(5)")["result"] == 24
    assert calculator("hypot(3, 4)")["result"] == 5
    assert calculator("abs(-5)")["result"] == 5
    assert calculator("floor(2.7)")["result"] == 2
    assert calculator("ceil(2.1)")["result"] == 3
    assert calculator("round(3.14159, 2)")["result"] == 3.14
    assert calculator("trunc(-2.9)")["result"] == -2


def test_aggregates():
    assert calculator("min(3, 1, 2)")["result"] == 1
    assert calculator("max(3, 1, 2)")["result"] == 3
    assert calculator("fsum(0.1, 0.2)")["result"] == 0.3
    assert calculator("prod(2, 3, 4)")["result"] == 24


def test_constants():
    assert calculator("pi")["result"] == 3.14159265359
    assert calculator("2pi")["result"] == 6.28318530718
    assert calculator("e")["result"] == 2.718281828459
    assert calculator("phi")["result"] == 1.61803398875


def test_natural_language_notation():
    assert calculator("2(3+4)")["result"] == 14
    assert calculator("(2)(3)")["result"] == 6
    assert calculator("10 mod 3")["result"] == 1
    assert calculator("sqrt(4) if 2 > 1 else 0")["result"] == 2
    assert calculator("5! + 1")["result"] == 121


def test_floating_point_noise_removed():
    assert calculator("0.1 + 0.2")["result"] == 0.3
    assert calculator("1/3 * 3")["result"] == 1


def test_scientific_notation():
    assert calculator("1e3")["result"] == 1000
    assert calculator("1e100")["result"] == 1e100


def test_division_by_zero_returns_error():
    result = calculator("1/0")
    assert "error" in result


def test_unknown_symbol_rejected():
    result = calculator("a + b")
    assert "error" in result


def test_code_injection_rejected():
    for malicious in [
        "__import__('os')",
        "os.system('rm -rf /')",
        "1; import os",
        "(lambda: 1)()",
        "open('file')",
        "1 << 2",
        "1 if True else [][0]",
        "dir()",
    ]:
        result = calculator(malicious)
        assert "error" in result, (
            f"Expected {malicious!r} to be rejected"
        )


def test_unknown_function_rejected():
    result = calculator("evil(1)")
    assert "error" in result


def test_attribute_access_rejected():
    result = calculator("(1).__class__")
    assert "error" in result


def test_empty_expression_rejected():
    assert "error" in calculator("")
    assert "error" in calculator("   ")


def test_overly_long_expression_rejected():
    huge = "+".join(["1"] * 3000)
    assert "error" in calculator(huge)
