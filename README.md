# Pocket Ledger

Pocket Ledger is a small terminal expense tracker. I built it to learn how a command-line program can grow beyond a single script while keeping personal data local.

It stores monetary values as integer cents in SQLite, avoiding floating-point rounding surprises. Entries can be filtered, summarized by category, or exported to CSV.

## Try it

Python 3.10 or newer is required. The project has no runtime dependencies.

```powershell
$env:PYTHONPATH = "src"
python -m expense_tracker add 12.50 food --description "Lunch"
python -m expense_tracker list --category food
python -m expense_tracker summary
python -m expense_tracker export expenses.csv
```

Use `--database path/to/file.db` before the command to choose a different database. By default, data is stored in `~/.pocket-ledger/expenses.db`.

Run the test suite with:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

## What I learned

This project covers `argparse` subcommands, SQLite transactions, `Decimal` validation, CSV output, context-managed resources, and unit tests that use temporary databases.

A useful next step would be recurring expenses and date-range reports.

