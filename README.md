# HL7 v2 ADT Message Parser & Validator

> **Portfolio demonstration | Synthetic / fictional data only**

A focused HL7 v2 pipe-delimited ADT exercise that parses MSH/PID/PV1 segments and checks common message requirements.

## What this demonstrates
- Parse line-oriented HL7 v2 messages with configurable field separator from MSH
- Validate essential ADT structure and identifiers
- Export JSON audit report with explicit errors and warnings

## Quick start
```bash
python src/main.py
python -m unittest discover -s tests
```

Python 3.10+ is recommended. Core functionality uses the Python standard library; no API keys or patient records are required. Run commands from the repository root.

## Repository contents
- `data/`: two fictional messages
- `src/main.py`: parser and validators
- `output/`: JSON report

## Relevant skills
HL7 v2, ADT messages, validation, healthcare interfaces, Python

## Data and privacy
All records, facilities, identifiers, events and organizations in this repository are fabricated for demonstrations. This is **not** a production clinical system and does not contain real protected health information (PHI). Do not upload real patient data or confidential employer files. Outputs do not substitute for clinical, privacy, security, or regulatory review.

## How to discuss in an interview
Explain the input, validations or transformations, measurable outputs, tests, and what you would change for a real deployment (authentication, audit logs, monitoring, regulatory review, and secure storage). Describe this as a **personal portfolio project**, not as an implementation at an employer.

## License
MIT — see [LICENSE](LICENSE).
