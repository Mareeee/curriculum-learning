import glob
import os
import shutil
import subprocess
import tempfile

import project_paths as paths

RSCRIPT_PATH = None

R_SCRIPT_TEMPLATE = """
if (!requireNamespace("GDINA", quietly = TRUE)) {{
  install.packages("GDINA", repos = "https://cloud.r-project.org")
}}
library(GDINA)
env <- new.env()
object_names <- data("realdata_Tatsuoka1990", package = "GDINA", envir = env)
dataset <- get(object_names[1], envir = env)
write.csv(dataset$dat, "{answers_path}", row.names = FALSE)
write.csv(dataset$Q, "{q_matrix_path}", row.names = FALSE)
"""

WINDOWS_PATTERNS = [
    r"{drive}:\Program Files\R\R-*\bin\Rscript.exe",
    r"{drive}:\Program Files\R\R-*\bin\x64\Rscript.exe",
    r"{drive}:\R\R-*\bin\Rscript.exe",
    r"{drive}:\R\R-*\bin\x64\Rscript.exe",
    r"{drive}:\R-*\bin\Rscript.exe",
    r"{drive}:\Programs\R\R-*\bin\Rscript.exe",
    r"{drive}:\Users\*\AppData\Local\Programs\R\R-*\bin\Rscript.exe",
]


def find_rscript():
    if RSCRIPT_PATH:
        return RSCRIPT_PATH
    on_path = shutil.which("Rscript")
    if on_path:
        return on_path
    for drive in "CDEFGH":
        for pattern in WINDOWS_PATTERNS:
            matches = sorted(glob.glob(pattern.format(drive=drive)), reverse=True)
            if matches:
                return matches[0]
    raise SystemExit("Rscript not found. Install R or set RSCRIPT_PATH.")


def as_r_path(path):
    return str(path).replace("\\", "/")


def download_tatsuoka():
    rscript = find_rscript()
    print("Using:", rscript)
    paths.TATSUOKA_ANSWERS.parent.mkdir(parents=True, exist_ok=True)
    script = R_SCRIPT_TEMPLATE.format(
        answers_path=as_r_path(paths.TATSUOKA_ANSWERS),
        q_matrix_path=as_r_path(paths.TATSUOKA_Q_MATRIX),
    )
    with tempfile.NamedTemporaryFile("w", suffix=".R", delete=False, encoding="utf-8") as file:
        file.write(script)
        script_path = file.name
    try:
        subprocess.run([rscript, script_path], check=True)
    finally:
        os.remove(script_path)
    print("Wrote", paths.TATSUOKA_ANSWERS)
    print("Wrote", paths.TATSUOKA_Q_MATRIX)


if __name__ == "__main__":
    download_tatsuoka()
