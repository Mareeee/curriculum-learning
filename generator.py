import csv
import random
from fractions import Fraction
from math import gcd


def int_add_nocarry(rng):
    while True:
        a, b = rng.randint(10, 99), rng.randint(10, 99)
        if all(x + y < 10 for x, y in zip(map(int, str(a)[::-1]), map(int, str(b)[::-1]))):
            return f"{a}+{b}=", str(a + b)


def int_add_carry(rng):
    while True:
        a, b = rng.randint(10, 99), rng.randint(10, 99)
        if (a % 10) + (b % 10) >= 10:
            return f"{a}+{b}=", str(a + b)


def int_sub_noborrow(rng):
    while True:
        a, b = rng.randint(10, 99), rng.randint(10, 99)
        if a > b and (a % 10) >= (b % 10) and (a // 10) >= (b // 10):
            return f"{a}-{b}=", str(a - b)


def int_sub_borrow1(rng):
    while True:
        a, b = rng.randint(10, 99), rng.randint(10, 99)
        if a > b and (a % 10) < (b % 10):
            return f"{a}-{b}=", str(a - b)


def int_sub_borrow_multi(rng):
    while True:
        a, b = rng.randint(100, 999), rng.randint(10, 999)
        if a > b and (a % 10) < (b % 10) and ((a // 10) % 10) < ((b // 10) % 10 + 1):
            return f"{a}-{b}=", str(a - b)


def int_mul_1d(rng):
    a, b = rng.randint(2, 9), rng.randint(2, 9)
    return f"{a}*{b}=", str(a * b)


def int_mul_2d1d(rng):
    a, b = rng.randint(11, 99), rng.randint(2, 9)
    return f"{a}*{b}=", str(a * b)


def frac_sub_same_den(rng):
    d = rng.randint(3, 12)
    while True:
        a, b = rng.randint(1, d - 1), rng.randint(1, d - 1)
        if a < b:
            a, b = b, a
        if a == b or gcd(a - b, d) == 1:
            return f"{a}/{d}-{b}/{d}=", str(Fraction(a - b, d))


def frac_sub_diff_den(rng):
    while True:
        d1, d2 = rng.choice([2, 3, 4, 5, 6, 8, 9]), rng.choice([2, 3, 4, 5, 6, 8, 9])
        if d1 == d2:
            continue
        a, b = rng.randint(1, d1 * 2), rng.randint(1, d2)
        f1, f2 = Fraction(a, d1), Fraction(b, d2)
        if 0 < f1 < 1 and f1 > f2 > 0:
            return f"{a}/{d1}-{b}/{d2}=", str(f1 - f2)


def frac_whole_minus_frac(rng):
    w, d = rng.randint(1, 5), rng.randint(2, 8)
    n = rng.randint(1, d - 1)
    return f"{w}-{n}/{d}=", str(w - Fraction(n, d))


def mixed_sub_noborrow(rng):
    while True:
        d = rng.randint(3, 12)
        w1, w2 = rng.randint(2, 7), rng.randint(1, 7)
        n1, n2 = rng.randint(1, d - 1), rng.randint(1, d - 1)
        if w1 >= w2 and n1 >= n2:
            r = (w1 + Fraction(n1, d)) - (w2 + Fraction(n2, d))
            if r > 0:
                return f"{w1} {n1}/{d}-{w2} {n2}/{d}=", str(r)


def mixed_sub_borrow(rng):
    while True:
        d = rng.randint(3, 12)
        w1, w2 = rng.randint(2, 7), rng.randint(1, 6)
        n1, n2 = rng.randint(1, d - 1), rng.randint(1, d - 1)
        if w1 > w2 and n1 < n2:
            r = (w1 + Fraction(n1, d)) - (w2 + Fraction(n2, d))
            return f"{w1} {n1}/{d}-{w2} {n2}/{d}=", str(r)


def frac_sub_improper(rng):
    d1 = rng.randint(2, 9)
    a = rng.randint(d1 + 1, 2 * d1 + 3)
    if rng.random() < 0.5:
        b, d2 = rng.randint(1, d1 - 1), d1
    else:
        d2 = rng.choice([x for x in range(2, 10) if x != d1])
        b = rng.randint(1, d2 - 1)
    return f"{a}/{d1}-{b}/{d2}=", str(Fraction(a, d1) - Fraction(b, d2))


def mixed_minus_whole(rng):
    w1 = rng.randint(2, 9)
    w2 = rng.randint(1, w1)
    d = rng.randint(3, 9)
    n = rng.randint(1, d - 1)
    return f"{w1} {n}/{d}-{w2}=", str(w1 + Fraction(n, d) - w2)


def whole_minus_mixed(rng):
    w1 = rng.randint(3, 9)
    w2 = rng.randint(1, w1 - 1)
    d = rng.randint(3, 9)
    n = rng.randint(1, d - 1)
    return f"{w1}-{w2} {n}/{d}=", str(w1 - w2 - Fraction(n, d))


def mixed_sub_diff_den(rng):
    dens = [2, 3, 4, 5, 6, 8, 10, 12]
    while True:
        d1, d2 = rng.choice(dens), rng.choice(dens)
        if d1 == d2:
            continue
        w1, w2 = rng.randint(2, 7), rng.randint(1, 6)
        n1, n2 = rng.randint(1, d1 - 1), rng.randint(1, d2 - 1)
        r = (w1 + Fraction(n1, d1)) - (w2 + Fraction(n2, d2))
        if w1 >= w2 and r > 0:
            return f"{w1} {n1}/{d1}-{w2} {n2}/{d2}=", str(r)


def mixed_sub_improper(rng):
    while True:
        d = rng.randint(2, 6)
        w1, w2 = rng.randint(3, 7), rng.randint(1, 4)
        n2 = rng.randint(d + 1, 2 * d - 1) if d > 2 else 3
        m = Fraction(w1)
        txt1 = f"{w1}"
        if rng.random() > 0.25:
            n1 = rng.randint(1, d - 1)
            m += Fraction(n1, d)
            txt1 = f"{w1} {n1}/{d}"
        r = m - (w2 + Fraction(n2, d))
        if r >= 0:
            return f"{txt1}-{w2} {n2}/{d}=", str(r)


def frac_sub_simplify(rng):
    while True:
        d = rng.choice([4, 6, 8, 9, 10, 12])
        a, b = rng.randint(2, d - 1), rng.randint(1, d - 2)
        if a > b and gcd(a - b, d) > 1:
            return f"{a}/{d}-{b}/{d}=", str(Fraction(a - b, d))


def frac_mul(rng):
    d1, d2 = rng.randint(2, 8), rng.randint(2, 8)
    n1, n2 = rng.randint(1, d1 - 1), rng.randint(1, d2 - 1)
    return f"{n1}/{d1}*{n2}/{d2}=", str(Fraction(n1, d1) * Fraction(n2, d2))


TYPES = {
    "int_add_nocarry":       (int_add_nocarry, "celi"),
    "int_add_carry":         (int_add_carry, "celi"),
    "int_sub_noborrow":      (int_sub_noborrow, "celi"),
    "int_sub_borrow1":       (int_sub_borrow1, "celi"),
    "int_sub_borrow_multi":  (int_sub_borrow_multi, "celi"),
    "int_mul_1d":            (int_mul_1d, "celi"),
    "int_mul_2d1d":          (int_mul_2d1d, "celi"),
    "frac_sub_same_den":     (frac_sub_same_den, "razlomci"),
    "frac_sub_diff_den":     (frac_sub_diff_den, "razlomci"),
    "frac_whole_minus_frac": (frac_whole_minus_frac, "razlomci"),
    "mixed_sub_noborrow":    (mixed_sub_noborrow, "razlomci"),
    "mixed_sub_borrow":      (mixed_sub_borrow, "razlomci"),
    "frac_sub_simplify":     (frac_sub_simplify, "razlomci"),
    "frac_mul":              (frac_mul, "razlomci"),
    "frac_sub_improper":     (frac_sub_improper, "razlomci"),
    "mixed_minus_whole":     (mixed_minus_whole, "razlomci"),
    "whole_minus_mixed":     (whole_minus_mixed, "razlomci"),
    "mixed_sub_diff_den":    (mixed_sub_diff_den, "razlomci"),
    "mixed_sub_improper":    (mixed_sub_improper, "razlomci"),
}


def generate(type_name, n, seed):
    rng = random.Random(f"{seed}-{type_name}")
    fn = TYPES[type_name][0]
    return [(type_name,) + fn(rng) for _ in range(n)]


def mixed_batch(n_per_type, seed):
    out = []
    for t in TYPES:
        out += generate(t, n_per_type, seed)
    random.Random(seed).shuffle(out)
    return out


COLUMNS = ["id", "seed", "tip", "oblast", "zapis", "resenje",
           "duzina_zapisa", "duzina_resenja", "resenje_je_ceo_broj",
           "resenje_veci_od_1", "duplikat"]


def generator(n_per_type=100, seed=0, out_path="zadaci.csv", types=None):
    types = types or list(TYPES)
    rows, seen = [], set()
    i = 0
    for t in types:
        for _, zapis, resenje in generate(t, n_per_type, seed):
            val = Fraction(resenje)
            rows.append({
                "id": i,
                "seed": seed,
                "tip": t,
                "oblast": TYPES[t][1],
                "zapis": zapis,
                "resenje": resenje,
                "duzina_zapisa": len(zapis),
                "duzina_resenja": len(resenje),
                "resenje_je_ceo_broj": int(val.denominator == 1),
                "resenje_veci_od_1": int(val > 1),
                "duplikat": int(zapis in seen),
            })
            seen.add(zapis)
            i += 1

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)

    print(f"Upisano {len(rows)} zadataka u {out_path}")
    for t in types:
        r = [x for x in rows if x["tip"] == t]
        d = sum(x["duplikat"] for x in r)
        print(f"  {t:24s} n={len(r):4d}  duplikata={d}")
    return rows


TATSUOKA = [
    ("5/3-3/4=", "frac_sub_improper"),       ("3/4-3/8=", "frac_sub_diff_den"),
    ("5/6-1/9=", "frac_sub_diff_den"),       ("3 1/2-2 3/2=", "mixed_sub_improper"),
    ("4 3/5-3 4/10=", "mixed_sub_diff_den"), ("6/7-4/7=", "frac_sub_same_den"),
    ("3-2 1/5=", "whole_minus_mixed"),       ("2/3-2/3=", "frac_sub_same_den"),
    ("3 7/8-2=", "mixed_minus_whole"),       ("4 4/12-2 7/12=", "mixed_sub_borrow"),
    ("4 1/3-2 4/3=", "mixed_sub_improper"),  ("11/8-1/8=", "frac_sub_improper"),
    ("3 3/8-2 5/6=", "mixed_sub_diff_den"),  ("3 4/5-3 2/5=", "mixed_sub_noborrow"),
    ("2-1/3=", "frac_whole_minus_frac"),     ("4 5/7-1 4/7=", "mixed_sub_noborrow"),
    ("7 3/5-2 4/5=", "mixed_sub_borrow"),    ("4 1/10-2 8/10=", "mixed_sub_borrow"),
    ("4-1 4/3=", "mixed_sub_improper"),      ("4 1/3-1 5/3=", "mixed_sub_improper"),
]


def _num(t):
    tot = Fraction(0)
    for p in t.split():
        tot += Fraction(p)
    return tot


def tatsuoka_zadaci(out_path="tatsuoka_zadaci.csv", proveri_n=0):
    cache, rows = {}, []
    for i, (zapis, tip) in enumerate(TATSUOKA, 1):
        a, b = zapis[:-1].split("-", 1)
        row = {"stavka": i, "zapis": zapis, "resenje": str(_num(a) - _num(b)), "tip": tip}
        if proveri_n > 0:
            if tip not in cache:
                cache[tip] = {z for _, z, _ in generate(tip, proveri_n, seed=12345)}
            row["vidjen_u_uzorku_generatora"] = int(zapis in cache[tip])
        rows.append(row)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return rows


if __name__ == "__main__":
    generator()