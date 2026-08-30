import argparse
import csv
from collections import defaultdict
from datetime import date
from decimal import Decimal
from pathlib import Path

from .models import Expense, parse_amount
from .store import ExpenseStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pocket-ledger", description="Track expenses from the terminal")
    parser.add_argument("--database", type=Path, default=Path.home() / ".pocket-ledger" / "expenses.db")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="record an expense")
    add_parser.add_argument("amount", type=parse_amount)
    add_parser.add_argument("category")
    add_parser.add_argument("--description", "-d", default="")
    add_parser.add_argument("--date", type=date.fromisoformat, default=date.today())

    list_parser = subparsers.add_parser("list", help="show recorded expenses")
    list_parser.add_argument("--category")

    subparsers.add_parser("summary", help="total spending by category")
    export_parser = subparsers.add_parser("export", help="write expenses to CSV")
    export_parser.add_argument("path", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    store = ExpenseStore(args.database)
    store.initialize()
    if args.command == "add":
        expense_id = store.add(Expense(args.amount, args.category, args.description, args.date))
        print(f"Added expense #{expense_id}")
    elif args.command == "list":
        _print_expenses(store.list(category=args.category))
    elif args.command == "summary":
        _print_summary(store.list())
    elif args.command == "export":
        _export(store.list(), args.path)
        print(f"Exported expenses to {args.path}")
    return 0


def _print_expenses(expenses: list[Expense]) -> None:
    if not expenses:
        print("No expenses found.")
        return
    for expense in expenses:
        print(f"{expense.spent_on}  ${expense.amount:>8.2f}  {expense.category:<15} {expense.description}")


def _print_summary(expenses: list[Expense]) -> None:
    totals: dict[str, Decimal] = defaultdict(Decimal)
    for expense in expenses:
        totals[expense.category] += expense.amount
    if not totals:
        print("No expenses found.")
        return
    for category, total in sorted(totals.items(), key=lambda item: item[1], reverse=True):
        print(f"{category:<20} ${total:.2f}")
    print(f"{'Total':<20} ${sum(totals.values()):.2f}")


def _export(expenses: list[Expense], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.writer(output)
        writer.writerow(["id", "date", "amount", "category", "description"])
        for expense in expenses:
            writer.writerow([expense.id, expense.spent_on, expense.amount, expense.category, expense.description])


if __name__ == "__main__":
    raise SystemExit(main())

