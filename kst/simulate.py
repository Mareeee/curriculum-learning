import random


def close_under_prerequisites(selected, pairs):
    state = set(selected)
    changed = True
    while changed:
        changed = False
        for prerequisite, item in pairs:
            if item in state and prerequisite not in state:
                state.add(prerequisite)
                changed = True
    return state


def simulate_answers(pairs, n_items, n_students, slip, guess, select_prob, seed):
    rng = random.Random(seed)
    answers = []
    for _ in range(n_students):
        selected = {item for item in range(1, n_items + 1) if rng.random() < select_prob}
        known = close_under_prerequisites(selected, pairs)
        row = []
        for item in range(1, n_items + 1):
            if item in known:
                row.append(0 if rng.random() < slip else 1)
            else:
                row.append(1 if rng.random() < guess else 0)
        answers.append(row)
    return answers
