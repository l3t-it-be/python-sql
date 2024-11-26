import os
import sqlite3
from sqlite3 import Connection, Cursor
from typing import Self


class Initialization:
    def __init__(self, table_name: str):
        self.db_name: str = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'PaymentSystemDB.db'
        )
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
