import csv
import glob
import os
import shutil
import subprocess
import tempfile

from generator import generator, tatsuoka_zadaci

R_KOD = """
if (!requireNamespace("GDINA", quietly = TRUE)) {
  install.packages("GDINA", repos = "https://cloud.r-project.org")
}
library(GDINA)
e <- new.env()
nm <- data("realdata_Tatsuoka1990", package = "GDINA", envir = e)
message("Ucitani objekti: ", paste(nm, collapse = ", "))
obj <- get(nm[1], envir = e)
message("Klasa: ", paste(class(obj), collapse = ", "))
str(obj, max.level = 1)
if (is.list(obj) && !is.data.frame(obj) && all(c("dat", "Q") %in% names(obj))) {
  write.csv(obj$dat, "tatsuoka_odgovori.csv", row.names = FALSE)
  write.csv(obj$Q,   "tatsuoka_Q.csv",        row.names = FALSE)
} else {
  stop("Struktura nije lista sa dat i Q - posalji mi ispis str(obj) iznad.")
}
"""
RSCRIPT_PUTANJA = None


def nadji_rscript():
    if RSCRIPT_PUTANJA:
        return RSCRIPT_PUTANJA
    p = shutil.which("Rscript")
    if p:
        return p
    kandidati = []
    for disk in "CDEFGH":
        for obrazac in (
            rf"{disk}:\Program Files\R\R-*\bin\Rscript.exe",
            rf"{disk}:\Program Files\R\R-*\bin\x64\Rscript.exe",
            rf"{disk}:\R\R-*\bin\Rscript.exe",
            rf"{disk}:\R\R-*\bin\x64\Rscript.exe",
            rf"{disk}:\R-*\bin\Rscript.exe",
            rf"{disk}:\Programs\R\R-*\bin\Rscript.exe",
            rf"{disk}:\Users\*\AppData\Local\Programs\R\R-*\bin\Rscript.exe",
        ):
            kandidati += sorted(glob.glob(obrazac), reverse=True)
    if kandidati:
        return kandidati[0]
    raise SystemExit(
        "Rscript nije pronađen."
    )


def preuzmi_tatsuoka_iz_R():
    rscript = nadji_rscript()
    print("Koristim:", rscript)
    with tempfile.NamedTemporaryFile("w", suffix=".R", delete=False, encoding="utf-8") as f:
        f.write(R_KOD)
        r_fajl = f.name
    try:
        subprocess.run([rscript, r_fajl], check=True)
    finally:
        os.remove(r_fajl)

    with open("tatsuoka_odgovori.csv", newline="", encoding="utf-8") as f:
        r = csv.reader(f)
        header = next(r)
        rows = [list(map(float, x)) for x in r]
    print(f"tatsuoka_odgovori.csv: {len(rows)} učenika x {len(header)} stavki")
    for j, name in enumerate(header):
        print(f"  stavka {j + 1:2d} ({name}): udeo tačnih = "
              f"{sum(x[j] for x in rows) / len(rows):.2f}")


def main():
    generator(n_per_type=100, seed=0, out_path="zadaci.csv")

    tatsuoka_zadaci("tatsuoka_zadaci.csv")

    # preuzmi_tatsuoka_iz_R()


if __name__ == "__main__":
    main()