import matplotlib.pyplot as plt


def merge_equivalent_items(pairs, items):
    groups = []
    used = set()
    for item in items:
        if item in used:
            continue
        group = [item]
        for other in items:
            if other != item and (item, other) in pairs and (other, item) in pairs:
                group.append(other)
        used.update(group)
        groups.append(tuple(sorted(group)))
    return groups


def pairs_between_groups(pairs, groups):
    group_pairs = set()
    for first in groups:
        for second in groups:
            if first != second and (first[0], second[0]) in pairs:
                group_pairs.add((first, second))
    return group_pairs


def remove_shortcuts(group_pairs, groups):
    kept = set()
    for first, second in group_pairs:
        has_middle = any((first, m) in group_pairs and (m, second) in group_pairs for m in groups)
        if not has_middle:
            kept.add((first, second))
    return kept


def compute_levels(groups, cover_pairs):
    levels = {group: 0 for group in groups}
    changed = True
    while changed:
        changed = False
        for first, second in cover_pairs:
            if levels[second] < levels[first] + 1:
                levels[second] = levels[first] + 1
                changed = True
    return levels


def graph_from_pairs(pairs, items):
    groups = merge_equivalent_items(pairs, items)
    group_pairs = pairs_between_groups(pairs, groups)
    cover_pairs = remove_shortcuts(group_pairs, groups)
    return groups, cover_pairs


def draw_graph(groups, cover_pairs, title):
    levels = compute_levels(groups, cover_pairs)
    members_by_level = {}
    for group in groups:
        members_by_level.setdefault(levels[group], []).append(group)

    positions = {}
    for level, members in members_by_level.items():
        for index, group in enumerate(sorted(members)):
            positions[group] = (index - (len(members) - 1) / 2, -level)

    widest = max(len(members) for members in members_by_level.values())
    fig, ax = plt.subplots(figsize=(max(6, widest * 2.2), max(4, len(members_by_level) * 1.1)))
    for first, second in cover_pairs:
        ax.annotate("", xy=positions[second], xytext=positions[first],
                    arrowprops=dict(arrowstyle="->", color="gray", shrinkA=14, shrinkB=14))
    for group, (x, y) in positions.items():
        ax.text(x, y, ",".join(map(str, group)), ha="center", va="center", fontsize=9,
                bbox=dict(boxstyle="round", facecolor="#eff6ff", edgecolor="#3b82f6"))
    ax.set_xlim(-widest / 2 - 1, widest / 2 + 1)
    ax.set_ylim(-len(members_by_level), 1)
    ax.set_title(title)
    ax.axis("off")
    plt.show()
