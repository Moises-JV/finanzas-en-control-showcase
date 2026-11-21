"""Synthetic-only regression tests for the public showcase parser."""

from decimal import Decimal
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from safe_ocr_example import extract_crc_amount  # noqa: E402


class SafeOcrExampleTests(unittest.TestCase):
    def test_extracts_synthetic_receipt_amount(self) -> None:
        fixture = ROOT / "examples" / "synthetic-receipt" / "receipt_ocr.txt"
        self.assertEqual(
            extract_crc_amount(fixture.read_text(encoding="utf-8")),
            Decimal("250000.00"),
        )

    def test_accepts_attached_c_substitution(self) -> None:
        self.assertEqual(extract_crc_amount("TOTAL C250,000.00"), Decimal("250000.00"))

    def test_accepts_cent_symbol_substitution(self) -> None:
        self.assertEqual(extract_crc_amount("TOTAL ¢250,000.00"), Decimal("250000.00"))

    def test_accepts_explicit_crc(self) -> None:
        self.assertEqual(extract_crc_amount("TOTAL CRC 250,000.00"), Decimal("250000.00"))

    def test_accepts_european_separators(self) -> None:
        self.assertEqual(extract_crc_amount("TOTAL ₡250.000,00"), Decimal("250000.00"))

    def test_accepts_ungrouped_decimal(self) -> None:
        self.assertEqual(extract_crc_amount("TOTAL ₡250000.00"), Decimal("250000.00"))

    def test_accepts_nbsp_after_symbol(self) -> None:
        self.assertEqual(extract_crc_amount("TOTAL ₡\u00a0250,000.00"), Decimal("250000.00"))

    def test_requires_human_review_for_multiple_amounts(self) -> None:
        self.assertIsNone(extract_crc_amount("Antes ₡100.00; total ₡250,000.00"))

    def test_rejects_unmarked_number(self) -> None:
        self.assertIsNone(extract_crc_amount("TOTAL 250,000.00"))

    def test_rejects_marker_inside_unrelated_word(self) -> None:
        self.assertIsNone(extract_crc_amount("TOTAL ABC250,000.00"))

    def test_rejects_spaced_c_marker(self) -> None:
        self.assertIsNone(extract_crc_amount("TOTAL C 250,000.00"))

    def test_rejects_trailing_digit(self) -> None:
        self.assertIsNone(extract_crc_amount("TOTAL ₡250,000.001"))

    def test_rejects_trailing_decimal_group(self) -> None:
        self.assertIsNone(extract_crc_amount("TOTAL ₡250,000.00.99"))

    def test_rejects_trailing_word(self) -> None:
        self.assertIsNone(extract_crc_amount("TOTAL ₡250,000.00bad"))

    def test_rejects_inconsistent_number_separators(self) -> None:
        self.assertIsNone(extract_crc_amount("TOTAL ₡250.000.00"))

    def test_rejects_missing_decimals(self) -> None:
        self.assertIsNone(extract_crc_amount("TOTAL ₡250,000"))

    def test_rejects_broken_grouping(self) -> None:
        self.assertIsNone(extract_crc_amount("TOTAL ₡25,00.00"))


if __name__ == "__main__":
    unittest.main()
