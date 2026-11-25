def digits_reversed(number):
    return [int(digit) for digit in str(number)[::-1]]


def int_add_nocarry(rng):
    while True:
        first, second = rng.randint(10, 99), rng.randint(10, 99)
        digit_pairs = zip(digits_reversed(first), digits_reversed(second))
        if all(x + y < 10 for x, y in digit_pairs):
            return f"{first}+{second}=", str(first + second)


def int_add_carry(rng):
    while True:
        first, second = rng.randint(10, 99), rng.randint(10, 99)
        if (first % 10) + (second % 10) >= 10:
            return f"{first}+{second}=", str(first + second)


def int_sub_noborrow(rng):
    while True:
        first, second = rng.randint(10, 99), rng.randint(10, 99)
        ones_ok = (first % 10) >= (second % 10)
        tens_ok = (first // 10) >= (second // 10)
        if first > second and ones_ok and tens_ok:
            return f"{first}-{second}=", str(first - second)


def int_sub_borrow1(rng):
    while True:
        first, second = rng.randint(10, 99), rng.randint(10, 99)
        if first > second and (first % 10) < (second % 10):
            return f"{first}-{second}=", str(first - second)


def int_sub_borrow_multi(rng):
    while True:
        first, second = rng.randint(100, 999), rng.randint(10, 999)
        ones_borrow = (first % 10) < (second % 10)
        tens_borrow = ((first // 10) % 10) < ((second // 10) % 10 + 1)
        if first > second and ones_borrow and tens_borrow:
            return f"{first}-{second}=", str(first - second)


def int_mul_1d(rng):
    first, second = rng.randint(2, 9), rng.randint(2, 9)
    return f"{first}*{second}=", str(first * second)


def int_mul_2d1d(rng):
    first, second = rng.randint(11, 99), rng.randint(2, 9)
    return f"{first}*{second}=", str(first * second)


INTEGER_TASKS = {
    "int_add_nocarry": int_add_nocarry,
    "int_add_carry": int_add_carry,
    "int_sub_noborrow": int_sub_noborrow,
    "int_sub_borrow1": int_sub_borrow1,
    "int_sub_borrow_multi": int_sub_borrow_multi,
    "int_mul_1d": int_mul_1d,
    "int_mul_2d1d": int_mul_2d1d,
}
