from pathlib import Path
import sqlite3
from sqlite3 import Connection, Cursor
from typing import Self

BASE_DIR = Path(__file__).resolve().parent


class Initialization:
    """Создание БД"""

    def __init__(self, table_name: str):
        db_path = BASE_DIR / 'PaymentSystemDB.db'
        self.db_name: str = db_path.as_posix()
        self.table_name: str = table_name
        self.db: Connection | None = None
        self.cursor: Cursor | None = None

    def __enter__(self) -> Self:
        self.db = sqlite3.connect(self.db_name, isolation_level=None)
        self.cursor = self.db.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db is not None:
            self.db.close()
