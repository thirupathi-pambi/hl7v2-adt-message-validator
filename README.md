# HL7 v2 ADT Message Parser & Validator

![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green)

A lightweight Python tool that parses pipe-delimited HL7 v2 ADT messages and validates the structure that interfaces most commonly depend on, then writes a JSON report of errors and warnings.

> Built on synthetic messages only. This is an instructional validator, not a full HL7 standard implementation.

## Why this exists

ADT (admit / discharge / transfer) feeds are the backbone of hospital integrations, and malformed messages are a common cause of interface errors. This project shows how to parse HL7 v2 correctly (including the easy-to-miss detail that `MSH-1` *is* the field separator) and turn validation results into a structured, machine-readable report.

## What it checks

| Check | Result if it fails |
|---|---|
| Message starts with a well-formed `MSH` segment | Error (validation stops) |
| `PID` segment present | Error |
| `PV1` segment present | Error |
| `MSH-9` message type starts with `ADT^` | Error |
| `MSH-10` message control ID present | Error |
| `PID-3` patient identifier present | Error |
| `EVN` segment present | Warning |

The field separator is read from the message header rather than hard-coded.

## Project structure

```
.
├── data/
│   ├── valid_adt.hl7          # fictional message that passes
│   └── invalid_adt.hl7        # fictional message that fails validation
├── src/
│   └── main.py                # parser and validator
├── tests/
│   └── test_main.py
├── output/
│   └── validation_report.json # generated report
├── LICENSE
└── README.md
```

## Quick start

Requires Python 3.10+ (standard library only). Run from the repository root.

```bash
python src/main.py                      # validates every .hl7 file in data/
python -m unittest discover -s tests
```

## Example report (shape)

Each file in `data/` gets an entry like this (values illustrative):

```json
{
  "invalid_adt.hl7": {
    "valid": false,
    "errors": ["Missing patient identifier (PID-3)"],
    "warnings": ["EVN segment not found"],
    "message_type": "ADT^A01",
    "segments": ["MSH", "PID", "PV1"]
  }
}
```

## Limitations and next steps

- Does not validate data types, code tables, or segment cardinality from the HL7 specification.
- Validates ADT structure only; no ORU, ORM, or other message types.
- Possible extensions: per-trigger-event rules (A01, A03, A08), field-level format checks (dates, sex codes), an MLLP listener for live feeds, and use of an established parser library for full-spec coverage.

## License

MIT. See [LICENSE](LICENSE).
