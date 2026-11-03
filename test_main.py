import sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from main import validate
class HL7Tests(unittest.TestCase):
 def test_good(self):self.assertTrue(validate((ROOT/'data/valid_adt.hl7').read_text())['valid'])
 def test_bad(self):self.assertFalse(validate((ROOT/'data/invalid_adt.hl7').read_text())['valid'])
 def test_empty(self):self.assertFalse(validate('')['valid'])
