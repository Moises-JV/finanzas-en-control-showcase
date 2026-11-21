# Security design

## Public showcase boundary

This repository contains newly written documentation and a small synthetic example. It excludes private source files, Git history, credentials, tokens, keys, `.env` files, databases, receipt images, financial records, logs, user identifiers, external-service configuration, deployment settings, OIDC material, allowlists, and authorization mechanisms.

## Defensive principles

1. **Least disclosure:** describe capabilities and boundaries without publishing implementation details that would expose private systems.
2. **Local, minimal example:** the runnable code uses only an input string and standard-library modules.
3. **No silent guessing:** an unmarked amount or multiple amount candidates yields no extracted value.
4. **Human accountability:** OCR output is a proposal requiring review, never sufficient authorization for a financial action.
5. **Duplicate awareness:** possible repeats should be surfaced for review. The private matching implementation and thresholds are intentionally not documented.
6. **No external side effects:** this showcase has no service clients, webhooks, database writes, or deployment actions.

## OCR error handling

OCR may substitute a currency mark (`₡` → `¢` or `C`), insert spaces, or vary decimal/grouping punctuation. The example accepts a narrow set of currency marks and validates full-token boundaries, number grouping and decimal structure. It does not infer currency from an arbitrary standalone number or `C` separated by whitespace, and it rejects multiple candidates.

This is a demonstration policy, not a complete fraud, accounting, compliance, or authorization control.

## Publication checklist

- [x] No private repository files or Git history copied.
- [x] No real receipts, financial data, or persistent databases included.
- [x] No secrets, keys, tokens, or local environment files included.
- [x] No external identifiers or integration configuration included.
- [x] No production infrastructure details included.
- [x] All examples are synthetic and make no external calls.
- [x] Included synthetic-demo screenshots independently reviewed and re-exported without inherited metadata.
- [ ] Future additional screenshots independently sanitized before adding.
- [ ] Future LinkedIn URL reviewed before adding.
