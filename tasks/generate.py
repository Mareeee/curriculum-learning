import csv
import random
from fractions import Fraction

from tasks.registry import ALL_TYPE_NAMES, DOMAIN_OF_TYPE, TASK_FUNCTIONS

COLUMNS = [
    "id", "seed", "type", "domain", "expression", "answer",
    "expression_length", "answer_length", "answer_is_integer",
    "answer_greater_than_one",
]

PATIENCE = 5000


def generate_tasks(type_name, count, seed):
    rng = random.Random(f"{seed}-{type_name}")
    make_task = TASK_FUNCTIONS[type_name]
    tasks = []
    for _ in range(count):
        expression, answer = make_task(rng)
        tasks.append((type_name, expression, answer))
    return tasks


def generate_unique_tasks(type_name, target, seed, excluded_expressions):
    rng = random.Random(f"{seed}-{type_name}")
    make_task = TASK_FUNCTIONS[type_name]
    seen = set(excluded_expressions)
    tasks = []
    misses_in_a_row = 0
    while len(tasks) < target and misses_in_a_row < PATIENCE:
        expression, answer = make_task(rng)
        if expression in seen:
            misses_in_a_row += 1
            continue
        seen.add(expression)
        tasks.append((type_name, expression, answer))
        misses_in_a_row = 0
    return tasks


def generate_mixed_batch(count_per_type, seed):
    batch = []
    for type_name in ALL_TYPE_NAMES:
        batch += generate_tasks(type_name, count_per_type, seed)
    random.Random(seed).shuffle(batch)
    return batch


def make_row(row_id, seed, type_name, expression, answer):
    value = Fraction(answer)
    return {
        "id": row_id,
        "seed": seed,
        "type": type_name,
        "domain": DOMAIN_OF_TYPE[type_name],
        "expression": expression,
        "answer": answer,
        "expression_length": len(expression),
        "answer_length": len(answer),
        "answer_is_integer": int(value.denominator == 1),
        "answer_greater_than_one": int(value > 1),
    }


def build_rows(count_per_type, seed, type_names, excluded_expressions):
    rows = []
    for type_name in type_names:
        tasks = generate_unique_tasks(type_name, count_per_type, seed, excluded_expressions)
        for _, expression, answer in tasks:
            rows.append(make_row(len(rows), seed, type_name, expression, answer))
    return rows


def write_rows(rows, path, columns):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def print_summary(rows, type_names, path, count_per_type):
    print(f"Wrote {len(rows)} tasks to {path}")
    for type_name in type_names:
        count = sum(1 for row in rows if row["type"] == type_name)
        note = "" if count == count_per_type else "  (task space exhausted)"
        print(f"  {type_name:24s} n={count:5d}{note}")


def generate_task_file(path, count_per_type=1000, seed=0, type_names=None, excluded_expressions=()):
    type_names = type_names or ALL_TYPE_NAMES
    rows = build_rows(count_per_type, seed, type_names, set(excluded_expressions))
    write_rows(rows, path, COLUMNS)
    print_summary(rows, type_names, path, count_per_type)
    return rows
