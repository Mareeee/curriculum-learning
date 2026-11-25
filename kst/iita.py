import csv


def load_answers(path):
    with open(path) as file:
        rows = list(csv.reader(file))[1:]
    return [[int(value) for value in row] for row in rows]


def share_correct(answers):
    n_students = len(answers)
    n_items = len(answers[0])
    shares = {}
    for item in range(1, n_items + 1):
        total = sum(student[item - 1] for student in answers)
        shares[item] = total / n_students
    return shares


def pair_table(answers, first, second):
    table = {"both solved": 0, "only first solved": 0, "only second solved": 0, "none solved": 0}
    for student in answers:
        first_correct = student[first - 1] == 1
        second_correct = student[second - 1] == 1
        if first_correct and second_correct:
            table["both solved"] += 1
        elif first_correct:
            table["only first solved"] += 1
        elif second_correct:
            table["only second solved"] += 1
        else:
            table["none solved"] += 1
    return table


def count_counterexamples(answers, first, second):
    count = 0
    for student in answers:
        if student[second - 1] == 1 and student[first - 1] == 0:
            count += 1
    return count


def counterexample_table(answers):
    n_items = len(answers[0])
    table = {}
    for first in range(1, n_items + 1):
        for second in range(1, n_items + 1):
            if first != second:
                table[(first, second)] = count_counterexamples(answers, first, second)
    return table


def pairs_that_break_transitivity(relation):
    broken = []
    for (a, middle) in relation:
        for (middle_again, c) in relation:
            if middle_again == middle and c != a and (a, c) not in relation:
                broken.append((a, middle, c))
    return broken


def remove_pairs_that_break_transitivity(current, new_pairs):
    new_pairs = set(new_pairs)
    while True:
        combined = current | new_pairs
        broken = pairs_that_break_transitivity(combined)
        if not broken:
            return new_pairs
        for a, middle, c in broken:
            new_pairs.discard((a, middle))
            new_pairs.discard((middle, c))


def build_candidate_relations(table):
    n_items = max(pair[0] for pair in table)
    all_pairs_count = n_items * (n_items - 1)
    current = {pair for pair, count in table.items() if count == 0}
    candidates = [set(current)]
    for threshold in range(1, max(table.values()) + 1):
        new_pairs = {pair for pair, count in table.items() if count <= threshold and pair not in current}
        new_pairs = remove_pairs_that_break_transitivity(current, new_pairs)
        if new_pairs:
            current = current | new_pairs
            candidates.append(set(current))
        if len(current) == all_pairs_count:
            break
    return candidates


def estimate_error_rate(relation, table, shares, n_students):
    top = 0.0
    bottom = 0.0
    for (first, second), count in table.items():
        share_first = shares[first]
        share_second = shares[second]
        if (first, second) in relation:
            top += count * share_second * n_students
            bottom += (share_second * n_students) ** 2
        elif (second, first) in relation:
            top += share_first * n_students * (count - (share_second - share_first) * n_students)
            bottom += (share_first * n_students) ** 2
    if bottom == 0:
        return 0.0
    return top / bottom


def expected_counterexamples(pair, relation, shares, n_students, error_rate):
    first, second = pair
    share_first = shares[first]
    share_second = shares[second]
    if (first, second) in relation:
        return error_rate * share_second * n_students
    if (second, first) in relation:
        return (share_second - share_first + error_rate * share_first) * n_students
    return (1 - share_first) * share_second * n_students


def diff_score(relation, table, shares, n_students):
    error_rate = estimate_error_rate(relation, table, shares, n_students)
    total = 0.0
    for pair, observed in table.items():
        expected = expected_counterexamples(pair, relation, shares, n_students, error_rate)
        total += (observed - expected) ** 2
    n_items = len(shares)
    return total / (n_items * (n_items - 1)), error_rate


def run_iita(answers):
    n_students = len(answers)
    shares = share_correct(answers)
    table = counterexample_table(answers)
    candidates = build_candidate_relations(table)
    diffs = []
    error_rates = []
    for candidate in candidates:
        diff, error_rate = diff_score(candidate, table, shares, n_students)
        diffs.append(diff)
        error_rates.append(error_rate)
    best_index = diffs.index(min(diffs))
    return {
        "table": table,
        "candidates": candidates,
        "diffs": diffs,
        "error_rates": error_rates,
        "best_index": best_index,
        "relation": candidates[best_index],
    }
