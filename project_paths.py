from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

GENERATED_TASKS = DATA_DIR / "generated" / "tasks.csv"

TATSUOKA_ITEMS = DATA_DIR / "tatsuoka" / "items.csv"
TATSUOKA_ANSWERS = DATA_DIR / "tatsuoka" / "answers.csv"
TATSUOKA_Q_MATRIX = DATA_DIR / "tatsuoka" / "q_matrix.csv"
