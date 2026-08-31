from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation


@dataclass(frozen=True)
class Expense:
    amount: Decimal
    category: str
    description: str
    spent_on: date
    id: int | None = None


def parse_amount(value: str) -> Decimal:
    try:
        # Keep every amount at two decimal places.
        amount = Decimal(value).quantize(Decimal("0.01"))
    except InvalidOperation as exc:
        raise ValueError("amount must be a number") from exc
    if amount <= 0:
        raise ValueError("amount must be greater than zero")
    return amount
