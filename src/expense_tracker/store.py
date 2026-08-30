import sqlite3
from contextlib import contextmanager
from datetime import date
from decimal import Decimal
from pathlib import Path

from .models import Expense


class ExpenseStore:
    def __init__(self, database: Path) -> None:
        self.database = database

    def initialize(self) -> None:
        self.database.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY,
                    amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),
                    category TEXT NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    spent_on TEXT NOT NULL
                )
                """
            )

    def add(self, expense: Expense) -> int:
        cents = int(expense.amount * 100)
        with self._connect() as connection:
            cursor = connection.execute(
                "INSERT INTO expenses (amount_cents, category, description, spent_on) VALUES (?, ?, ?, ?)",
                (cents, expense.category.strip().lower(), expense.description.strip(), expense.spent_on.isoformat()),
            )
            return int(cursor.lastrowid)

    def list(self, *, category: str | None = None) -> list[Expense]:
        query = "SELECT id, amount_cents, category, description, spent_on FROM expenses"
        parameters: tuple[str, ...] = ()
        if category:
            query += " WHERE category = ?"
            parameters = (category.strip().lower(),)
        query += " ORDER BY spent_on DESC, id DESC"
        with self._connect() as connection:
            rows = connection.execute(query, parameters).fetchall()
        return [
            Expense(
                id=row["id"],
                amount=Decimal(row["amount_cents"]) / 100,
                category=row["category"],
                description=row["description"],
                spent_on=date.fromisoformat(row["spent_on"]),
            )
            for row in rows
        ]

    @contextmanager
    def _connect(self):
        connection = sqlite3.connect(self.database)
        connection.row_factory = sqlite3.Row
        try:
            with connection:
                yield connection
        finally:
            connection.close()
