import contextlib
import io
import unittest
from expense_tracker.models import parse_amount
from expense_tracker.cli import build_parser

class NonfiniteAmountTests(unittest.TestCase):
    def test_nonfinite_amounts_raise_value_error(self):
        for value in ("NaN", "sNaN", "Infinity", "-Infinity"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_amount(value)

    def test_nan_produces_argument_error(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            build_parser().parse_args(["add", "NaN", "food"])
        self.assertEqual(error.exception.code, 2)
