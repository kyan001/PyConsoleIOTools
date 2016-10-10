import unittest
import sys
sys.path.insert(0, '../')

import FakeIn
import FakeOut
import consoleiotools as cit


class test_consoleiotools(unittest.TestCase):
    """For testing consoleiotools"""
    cit_version = '1.0.0'

    def setUp(self):
        self.console_out = sys.stdout
        self.fakeout = FakeOut.FakeOut()
        sys.stdout = self.fakeout
        self.console_in = sys.stdin
        self.fakein = FakeIn.FakeIn()
        sys.stdin = self.fakein

    def tearDown(self):
        self.fakeout.clean()
        self.fakein.clean()
        sys.stdout = self.console_out
        sys.stdin = self.console_in

    def test_version(self):
        self.assertEqual(self.cit_version, cit.__version__)


if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)
