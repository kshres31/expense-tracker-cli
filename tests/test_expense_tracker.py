import tempfile
import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path

from expense_tracker.models import Expense, parse_amount
from expense_tracker.store import ExpenseStore


class AmountTests(unittest.TestCase):
    def test_rounds_amount_to_cents(self) -> None:
        self.assertEqual(parse_amount("4.999"), Decimal("5.00"))

    def test_rejects_non_positive_amount(self) -> None:
        with self.assertRaisesRegex(ValueError, "greater than zero"):
            parse_amount("0")


class StoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.store = ExpenseStore(Path(self.temp_dir.name) / "expenses.db")
        self.store.initialize()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_adds_and_filters_expenses(self) -> None:
        self.store.add(Expense(Decimal("8.25"), "Food", "breakfast", date(2026, 8, 30)))
        self.store.add(Expense(Decimal("20.00"), "Travel", "train", date(2026, 8, 29)))

        food = self.store.list(category="FOOD")

        self.assertEqual(len(food), 1)
        self.assertEqual(food[0].description, "breakfast")
        self.assertEqual(food[0].amount, Decimal("8.25"))

    def test_lists_newest_expense_first(self) -> None:
        self.store.add(Expense(Decimal("1"), "other", "old", date(2026, 1, 1)))
        self.store.add(Expense(Decimal("2"), "other", "new", date(2026, 2, 1)))

        self.assertEqual([item.description for item in self.store.list()], ["new", "old"])


if __name__ == "__main__":
    unittest.main()

