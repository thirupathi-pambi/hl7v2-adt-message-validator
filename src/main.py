"""Minimal instructional HL7 v2 ADT validator, not a full standards implementation."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def validate(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    errors, warnings = [], []
    if not lines or not lines[0].startswith('MSH') or len(lines[0]) < 4:
        return {'valid': False, 'errors': ['MSH segment missing or malformed'], 'warnings': [], 'message_type': None}
    separator = lines[0][3]
    segments = {}
    for line in lines:
        parts = line.split(separator)
        segments.setdefault(parts[0], []).append(parts)
    if 'PID' not in segments: errors.append('Missing PID segment')
    if 'PV1' not in segments: errors.append('Missing PV1 segment')
    msh = segments['MSH'][0]
    # MSH-1 is the field separator, represented by character index 3, not a split token.
    def field(parts, index): return parts[index] if len(parts) > index else ''
    msg_type = field(msh, 8)
    if not msg_type.startswith('ADT^'): errors.append('Expected ADT message in MSH-9')
    if not field(msh, 9): errors.append('Missing message control ID (MSH-10)')
    if 'PID' in segments and not field(segments['PID'][0], 3): errors.append('Missing patient identifier (PID-3)')
    if 'EVN' not in segments: warnings.append('EVN segment not found')
    return {'valid': not errors, 'errors': errors, 'warnings': warnings, 'message_type': msg_type,
            'segments': list(segments)}

def main():
    report = {path.name: validate(path.read_text()) for path in sorted((ROOT/'data').glob('*.hl7'))}
    out = ROOT/'output/validation_report.json';out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__ == '__main__': main()
