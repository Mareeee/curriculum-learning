from fractions import Fraction
from math import gcd


def frac_sub_same_den(rng):
    denominator = rng.randint(3, 12)
    while True:
        first, second = rng.randint(1, denominator - 1), rng.randint(1, denominator - 1)
        if first < second:
            first, second = second, first
        if first == second or gcd(first - second, denominator) == 1:
            result = Fraction(first - second, denominator)
            return f"{first}/{denominator}-{second}/{denominator}=", str(result)


def frac_sub_diff_den(rng):
    while True:
        den1, den2 = rng.choice([2, 3, 4, 5, 6, 8, 9]), rng.choice([2, 3, 4, 5, 6, 8, 9])
        if den1 == den2:
            continue
        num1, num2 = rng.randint(1, den1 * 2), rng.randint(1, den2)
        frac1, frac2 = Fraction(num1, den1), Fraction(num2, den2)
        if 0 < frac1 < 1 and frac1 > frac2 > 0:
            return f"{num1}/{den1}-{num2}/{den2}=", str(frac1 - frac2)


def frac_whole_minus_frac(rng):
    whole, denominator = rng.randint(1, 5), rng.randint(2, 8)
    numerator = rng.randint(1, denominator - 1)
    return f"{whole}-{numerator}/{denominator}=", str(whole - Fraction(numerator, denominator))


def mixed_sub_noborrow(rng):
    while True:
        denominator = rng.randint(3, 12)
        whole1, whole2 = rng.randint(2, 7), rng.randint(1, 7)
        num1, num2 = rng.randint(1, denominator - 1), rng.randint(1, denominator - 1)
        if whole1 >= whole2 and num1 >= num2:
            first = whole1 + Fraction(num1, denominator)
            second = whole2 + Fraction(num2, denominator)
            if first - second > 0:
                text = f"{whole1} {num1}/{denominator}-{whole2} {num2}/{denominator}="
                return text, str(first - second)


def mixed_sub_borrow(rng):
    while True:
        denominator = rng.randint(3, 12)
        whole1, whole2 = rng.randint(2, 7), rng.randint(1, 6)
        num1, num2 = rng.randint(1, denominator - 1), rng.randint(1, denominator - 1)
        if whole1 > whole2 and num1 < num2:
            first = whole1 + Fraction(num1, denominator)
            second = whole2 + Fraction(num2, denominator)
            text = f"{whole1} {num1}/{denominator}-{whole2} {num2}/{denominator}="
            return text, str(first - second)


def frac_sub_simplify(rng):
    while True:
        denominator = rng.choice([4, 6, 8, 9, 10, 12])
        first, second = rng.randint(2, denominator - 1), rng.randint(1, denominator - 2)
        if first > second and gcd(first - second, denominator) > 1:
            result = Fraction(first - second, denominator)
            return f"{first}/{denominator}-{second}/{denominator}=", str(result)


def frac_mul(rng):
    den1, den2 = rng.randint(2, 8), rng.randint(2, 8)
    num1, num2 = rng.randint(1, den1 - 1), rng.randint(1, den2 - 1)
    result = Fraction(num1, den1) * Fraction(num2, den2)
    return f"{num1}/{den1}*{num2}/{den2}=", str(result)


def frac_sub_improper(rng):
    den1 = rng.randint(2, 9)
    num1 = rng.randint(den1 + 1, 2 * den1 + 3)
    if rng.random() < 0.5:
        num2, den2 = rng.randint(1, den1 - 1), den1
    else:
        den2 = rng.choice([x for x in range(2, 10) if x != den1])
        num2 = rng.randint(1, den2 - 1)
    result = Fraction(num1, den1) - Fraction(num2, den2)
    return f"{num1}/{den1}-{num2}/{den2}=", str(result)


def mixed_minus_whole(rng):
    whole1 = rng.randint(2, 9)
    whole2 = rng.randint(1, whole1)
    denominator = rng.randint(3, 9)
    numerator = rng.randint(1, denominator - 1)
    result = whole1 + Fraction(numerator, denominator) - whole2
    return f"{whole1} {numerator}/{denominator}-{whole2}=", str(result)


def whole_minus_mixed(rng):
    whole1 = rng.randint(3, 9)
    whole2 = rng.randint(1, whole1 - 1)
    denominator = rng.randint(3, 9)
    numerator = rng.randint(1, denominator - 1)
    result = whole1 - whole2 - Fraction(numerator, denominator)
    return f"{whole1}-{whole2} {numerator}/{denominator}=", str(result)


def mixed_sub_diff_den(rng):
    denominators = [2, 3, 4, 5, 6, 8, 10, 12]
    while True:
        den1, den2 = rng.choice(denominators), rng.choice(denominators)
        if den1 == den2:
            continue
        whole1, whole2 = rng.randint(2, 7), rng.randint(1, 6)
        num1, num2 = rng.randint(1, den1 - 1), rng.randint(1, den2 - 1)
        result = (whole1 + Fraction(num1, den1)) - (whole2 + Fraction(num2, den2))
        if whole1 >= whole2 and result > 0:
            return f"{whole1} {num1}/{den1}-{whole2} {num2}/{den2}=", str(result)


def mixed_sub_improper(rng):
    while True:
        denominator = rng.randint(2, 6)
        whole1, whole2 = rng.randint(3, 7), rng.randint(1, 4)
        num2 = rng.randint(denominator + 1, 2 * denominator - 1) if denominator > 2 else 3
        first_value = Fraction(whole1)
        first_text = f"{whole1}"
        if rng.random() > 0.25:
            num1 = rng.randint(1, denominator - 1)
            first_value += Fraction(num1, denominator)
            first_text = f"{whole1} {num1}/{denominator}"
        result = first_value - (whole2 + Fraction(num2, denominator))
        if result >= 0:
            return f"{first_text}-{whole2} {num2}/{denominator}=", str(result)


FRACTION_TASKS = {
    "frac_sub_same_den": frac_sub_same_den,
    "frac_sub_diff_den": frac_sub_diff_den,
    "frac_whole_minus_frac": frac_whole_minus_frac,
    "mixed_sub_noborrow": mixed_sub_noborrow,
    "mixed_sub_borrow": mixed_sub_borrow,
    "frac_sub_simplify": frac_sub_simplify,
    "frac_mul": frac_mul,
    "frac_sub_improper": frac_sub_improper,
    "mixed_minus_whole": mixed_minus_whole,
    "whole_minus_mixed": whole_minus_mixed,
    "mixed_sub_diff_den": mixed_sub_diff_den,
    "mixed_sub_improper": mixed_sub_improper,
}
