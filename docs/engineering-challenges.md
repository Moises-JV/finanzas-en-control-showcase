# Engineering challenges

## OCR is probabilistic, financial interpretation must be cautious

Receipt OCR can return visually similar characters in different forms. For example, the intended value `₡250,000.00` might appear as `¢250,000.00` or `C250,000.00`. Thousands and decimal separators can also vary by receipt layout.

The showcase example separates this presentation cleanup from the financial decision:

- It recognizes only directly prefixed currency marks: `₡`, `¢`, `CRC`, or a tightly attached `C`.
- It accepts complete, valid grouped or ungrouped amounts with exactly two decimal digits, supporting `250,000.00` and `250.000,00` conventions.
- It checks both token boundaries and requires distinct, consistent grouping and decimal separators; it refuses partial matches inside malformed values or unrelated words.
- It returns `None` when no complete marked candidate or more than one candidate exists. A standalone `C` must be attached directly to the number.

That conservative behavior is intentional. A real workflow should show unresolved information to a reviewer rather than choose a value based on weak OCR evidence.

## Duplicate prevention without overclaiming

Duplicate protection is important because message-and-receipt workflows can be retried. A possible match should create a visible review signal, preserving human context and auditability. The specific comparison strategy, fields, thresholds, and any external lookup details are private and deliberately excluded from this public material.

## Containerized OCR validation

The private project validated real Tesseract in Docker. This showcase does not reproduce the image, dependency manifest, or CI workflow, because the aim is to demonstrate the architectural reasoning without publishing operational configuration. The Python example remains runnable everywhere a supported Python interpreter is available.

## Evidence boundary

The private project’s reported 597 passing tests are not presented as results for this repository. The tests here validate only the standalone synthetic parser and should be reported separately.
