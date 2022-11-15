import unittest

from printer import Printer

class TestPrinter(unittest.TestCase):

    def setUp(self):
        self.printer = Printer()

    def test_printer(self):
        self.printer.print()

