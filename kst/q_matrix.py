import csv


def load_q_matrix(path):
    with open(path) as file:
        rows = list(csv.reader(file))[1:]
    return [[int(value) for value in row] for row in rows]


def skills_of_item(q_matrix, item):
    row = q_matrix[item - 1]
    skills = set()
    for skill_index, flag in enumerate(row):
        if flag == 1:
            skills.add(skill_index + 1)
    return skills


def q_prerequisite_pairs(q_matrix):
    n_items = len(q_matrix)
    pairs = set()
    for first in range(1, n_items + 1):
        for second in range(1, n_items + 1):
            if first == second:
                continue
            first_skills = skills_of_item(q_matrix, first)
            second_skills = skills_of_item(q_matrix, second)
            if first_skills <= second_skills:
                pairs.add((first, second))
    return pairs
