from fractions import Fraction

from tasks.generate import generate_tasks, write_rows

TATSUOKA_ITEMS = [
    ("5/3-3/4=", "frac_sub_improper"),
    ("3/4-3/8=", "frac_sub_diff_den"),
    ("5/6-1/9=", "frac_sub_diff_den"),
    ("3 1/2-2 3/2=", "mixed_sub_improper"),
    ("4 3/5-3 4/10=", "mixed_sub_diff_den"),
    ("6/7-4/7=", "frac_sub_same_den"),
    ("3-2 1/5=", "whole_minus_mixed"),
    ("2/3-2/3=", "frac_sub_same_den"),
    ("3 7/8-2=", "mixed_minus_whole"),
    ("4 4/12-2 7/12=", "mixed_sub_borrow"),
    ("4 1/3-2 4/3=", "mixed_sub_improper"),
    ("11/8-1/8=", "frac_sub_improper"),
    ("3 3/8-2 5/6=", "mixed_sub_diff_den"),
    ("3 4/5-3 2/5=", "mixed_sub_noborrow"),
    ("2-1/3=", "frac_whole_minus_frac"),
    ("4 5/7-1 4/7=", "mixed_sub_noborrow"),
    ("7 3/5-2 4/5=", "mixed_sub_borrow"),
    ("4 1/10-2 8/10=", "mixed_sub_borrow"),
    ("4-1 4/3=", "mixed_sub_improper"),
    ("4 1/3-1 5/3=", "mixed_sub_improper"),
]


def tatsuoka_expressions():
    return {expression for expression, _ in TATSUOKA_ITEMS}


def parse_number(text):
    total = Fraction(0)
    for part in text.split():
        total += Fraction(part)
    return total


def solve_expression(expression):
    left, right = expression[:-1].split("-", 1)
    return parse_number(left) - parse_number(right)


def types_seen_in_generator(sample_size, seed=12345):
    seen = {}
    for _, type_name in TATSUOKA_ITEMS:
        if type_name not in seen:
            tasks = generate_tasks(type_name, sample_size, seed)
            seen[type_name] = {expression for _, expression, _ in tasks}
    return seen


def build_item_rows(sample_size=0):
    seen = types_seen_in_generator(sample_size) if sample_size > 0 else {}
    rows = []
    for number, (expression, type_name) in enumerate(TATSUOKA_ITEMS, start=1):
        row = {
            "item": number,
            "expression": expression,
            "answer": str(solve_expression(expression)),
            "type": type_name,
        }
        if sample_size > 0:
            row["seen_in_generator_sample"] = int(expression in seen[type_name])
        rows.append(row)
    return rows


def write_tatsuoka_items(path, sample_size=0):
    rows = build_item_rows(sample_size)
    write_rows(rows, path, list(rows[0]))
    return rows
