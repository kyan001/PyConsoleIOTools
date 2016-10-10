import unittest
import sys

import FakeIn
import FakeOut

sys.path.insert(0, '../')
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

    def test_start(self):
        cit.start()
        self.assertEqual(self.fakeout.readline(), '*\n')

    def test_end(self):
        cit.end()
        self.assertEqual(self.fakeout.readline(), '!\n')

    def test_echo(self):
        cit.echo("ABC")
        self.assertEqual(self.fakeout.readline(), "| ABC\n")

    def test_echo_pre(self):
        cit.echo("ABC", pre="prefix")
        self.assertEqual(self.fakeout.readline(), "| (Prefix) ABC\n")

    def test_echo_lvl(self):
        cit.echo("ABC", lvl=2)
        expect_word = "| {t}ABC\n".format(t='    ' * 2)
        self.assertEqual(self.fakeout.readline(), expect_word)

    def test_title(self):
        cit.title("ABC")
        self.assertEqual(self.fakeout.readline(), '| ABC:\n')

    def test_info(self):
        cit.info("ABC")
        self.assertEqual(self.fakeout.readline(), "| (Info) ABC\n")

    def test_warn(self):
        cit.warn("ABC")
        self.assertEqual(self.fakeout.readline(), "| (Warning) ABC\n")

    def test_err(self):
        cit.err("ABC")
        self.assertEqual(self.fakeout.readline(), "| (Error) ABC\n")

    def test_pause(self):
        self.fakein.write()  # simulate press enter
        cit.pause()
        expect_word = "\nPress Enter to Continue..."
        self.assertEqual(self.fakeout.readline(), expect_word)

    def test_bye(self):
        self.assertRaises(SystemExit, cit.bye, None)

    def test_get_input(self):
        self.fakein.write("ABC")
        userinput = cit.get_input()
        self.assertEqual(self.fakeout.readline(), "> ")
        self.assertEqual(userinput, "ABC")

    def test_get_choice_1(self):
        self.fakein.write("1")
        self.assertEqual(cit.get_choice(["ABC", "DEF"]), "ABC")
        expect_word = "|  1) ABC\n|  2) DEF\n> "
        self.assertEqual(self.fakeout.readline(), expect_word)

    def test_get_choice_2(self):
        self.fakein.write("ABC")
        self.assertEqual(cit.get_choice(["ABC", "DEF"]), "ABC")
        expect_word = "|  1) ABC\n|  2) DEF\n> "
        self.assertEqual(self.fakeout.readline(), expect_word)

if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)
    cit.pause()
