# HL7 v2 ADT Message Validator

This is a small Python validator for HL7 v2 ADT messages, the admit/discharge/transfer feed that most hospital interfaces depend on. I wanted to understand how these messages are put together field by field, and the best way to do that was to write the parser myself instead of using a library.

The messages here are made up. This isn't a full HL7 implementation. It checks the structure that interfaces most often break on.

## What an ADT message looks like

This is the valid sample from `data/valid_adt.hl7`:

```
MSH|^~\&|SIMAPP|CLINIC_A|SIM_EHR|NETWORK|202601151030||ADT^A01|MSG0001|P|2.5
EVN|A01|202601151030
PID|1||FAKE1001^^^SIM^MR||Taylor^Alex||19840312|U
PV1|1|O|OUTPATIENT^101
```

Each line is a segment. `MSH` is the header, `EVN` is the event, `PID` is the patient, and `PV1` is the visit. Fields are separated by `|`.

## What it checks

| Check                                     | If it fails                |
|-------------------------------------------|----------------------------|
| First segment is a well-formed `MSH`      | Error, and checking stops  |
| `PID` segment is present                  | Error                      |
| `PV1` segment is present                  | Error                      |
| `MSH-9` message type starts with `ADT^`   | Error                      |
| `MSH-10` message control ID isn't blank   | Error                      |
| `PID-3` patient identifier isn't blank    | Error                      |
| `EVN` segment is present                  | Warning                    |

## Running it

You need Python 3.10 or newer. There's nothing to install.

```bash
python src/main.py
python -m unittest discover -s tests
```

Run both commands from the repo root. The script validates every `.hl7` file in `data/` and writes the results to `output/validation_report.json`.

## Results

The valid message passes with no errors or warnings.

The invalid message, `data/invalid_adt.hl7`, has several problems built in:

```
MSH|^~\&|SIMAPP|CLINIC_A|SIM_EHR|NETWORK|202601151030||ADT^A01||P|2.5
PID|1||||Taylor^Alex
```

The validator catches all of them:

```json
"invalid_adt.hl7": {
  "valid": false,
  "errors": [
    "Missing PV1 segment",
    "Missing message control ID (MSH-10)",
    "Missing patient identifier (PID-3)"
  ],
  "warnings": ["EVN segment not found"],
  "message_type": "ADT^A01",
  "segments": ["MSH", "PID"]
}
```

## Things I learned building it

- **MSH counts its fields differently from every other segment.** In MSH, the `|` right after "MSH" *is* field 1 (MSH-1). So when you split the line on `|`, MSH-9 ends up at index 8, not 9. In every other segment, like PID, the index matches the field number. I got this wrong the first time, and it's a classic HL7 mistake.
- **The separator isn't always `|`.** The script reads the field separator from the 4th character of the MSH line instead of hard-coding it.
- **Real HL7 ends segments with `\r`, not a newline.** The script splits on both, so it handles messages from a real feed as well as files saved in a text editor.
- **A missing EVN is a warning, not an error.** Most receiving systems take the event type from MSH-9 anyway, so a missing EVN usually doesn't break anything. Missing PID or PV1 does.

## Files

```
data/valid_adt.hl7              sample message that passes
data/invalid_adt.hl7            sample message with problems built in
src/main.py                     parser and validator
tests/test_main.py              tests for valid, invalid and empty input
output/validation_report.json   generated report
```

## What I'd add next

- Different rules for each trigger event. An A03 (discharge) should require a discharge date in PV1-45, for example.
- Field format checks: valid dates in PID-7, allowed values in PID-8 (sex)
- Support for more than one message per file, since real batch files hold hundreds
- An MLLP listener, so it can validate messages from a live feed instead of files
