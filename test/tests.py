import unittest
import re
from ocr.regex_builder import RegexBuilder

class Test_RegexTest(unittest.TestCase):
    def setUp(self):
        self.build = RegexBuilder()
    def test_number(self):
        lines = ['Facture N8 : 09-18','facture nO:']
        for line in lines:
            line = re.sub(self.build.compiled_factures,'facture :',line)
            self.assertIn('facture :',line)
