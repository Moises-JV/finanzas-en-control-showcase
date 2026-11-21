"""Conservative amount parsing from synthetic OCR text (not OCR itself).

A deliberately standalone example. No image processing, files, network calls,
credentials, external integrations, or financial operations are implemented.
"""

from __future__ import annotations

from decimal import Decimal
import re


# Match complete, well-formed decimal amounts only. Guard both boundaries to
# prevent partial readings from malformed numbers or incidental text such as
# ``ABC250,000.00`` (where C is part of an unrelated word).
#
# A solitary "C" is an OCR substitution only when attached directly to digits.
# Grouped amounts use consistent, distinct thousands/decimal separators.
_AMOUNT_PATTERN = re.compile(
    r"(?<![\w₡¢])"
    r"(?:CRC[ \t]*|[₡¢][ \t]*|C(?=[0-9]))"
    r"(?P<number>"
    r"[0-9]{1,3}(?:,[0-9]{3})+\.[0-9]{2}"
    r"|[0-9]{1,3}(?:\.[0-9]{3})+,[0-9]{2}"
    r"|[0-9]+[.,][0-9]{2}"
    r")"
    r"(?![\w.,])",
    re.IGNORECASE,
)


def _to_decimal(number: str) -> Decimal:
    """Convert the structurally validated amount string to Decimal."""
    decimal_separator_at = max(number.rfind(","), number.rfind("."))
    integer_digits = number[:decimal_separator_at].replace(",", "").replace(".", "")
    cents = number[decimal_separator_at + 1 :]
    return Decimal(f"{integer_digits}.{cents}")


def extract_crc_amount(ocr_text: str) -> Decimal | None:
    """Return exactly one complete currency-marked amount, else ``None``.

    This intentionally narrow demo supports ``₡``, ``¢``, ``CRC``, and a
    directly attached ``C`` as a potential OCR substitution. It refuses
    malformed, unmarked, or multiple amounts; a human must review them.
    """
    candidates = [
        _to_decimal(match.group("number"))
        for match in _AMOUNT_PATTERN.finditer(ocr_text.replace("\u00a0", " "))
    ]
    return candidates[0] if len(candidates) == 1 else None
