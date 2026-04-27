import duckdb
from pathlib import Path

DB_PATH = Path("data/crypto.duckdb")

def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    return duckdb.connect(str(DB_PATH))