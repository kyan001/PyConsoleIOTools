import unittest
import sys
import os

import FakeIn
import FakeOut

sys.path.insert(0, '../')
import consoleiotools as cit


class test_consoleiotools(unittest.TestCase):
    """For testing consoleiotools"""
    cit_version = '2.3.0'
    TMP_FILE = "tmp.txt"

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
        if os.path.isfile(self.TMP_FILE):
            os.remove(self.TMP_FILE)

    def test_version(self):
        self.assertEqual(self.cit_version, cit.__version__)

    def test_start(self):
        cit.start()
        self.assertEqual(self.fakeout.readline(ansi=False), '*\n')

    def test_end(self):
        cit.end()
        self.assertEqual(self.fakeout.readline(ansi=False), '`\n')

    def test_br(self):
        cit.br(2)
        self.assertEqual(self.fakeout.readline(ansi=False), '\n\n')

    def test_echo(self):
        cit.echo("ABC")
        self.assertEqual(self.fakeout.readline(ansi=False), "| ABC\n")

    def test_echo_pre(self):
        cit.echo("ABC", pre="prefix")
        self.assertEqual(self.fakeout.readline(ansi=False), "| (Prefix) ABC\n")

    def test_title(self):
        cit.title("ABC")
        self.assertEqual(self.fakeout.readline(ansi=False), '| __ABC__________________________\n')

    def test_ask(self):
        cit.ask("ABC")
        self.assertEqual(self.fakeout.readline(ansi=False), "| (?) ABC\n")

    def test_info(self):
        cit.info("ABC")
        self.assertEqual(self.fakeout.readline(ansi=False), "| (Info) ABC\n")

    def test_warn(self):
        cit.warn("ABC")
        self.assertEqual(self.fakeout.readline(ansi=False), "| (Warning) ABC\n")

    def test_err(self):
        cit.err("ABC")
        self.assertEqual(self.fakeout.readline(ansi=False), "| (Error) ABC\n")

    def test_pause(self):
        self.fakein.write()  # simulate press enter
        cit.pause()
        expect_word = "\nPress Enter to Continue..."
        self.assertEqual(self.fakeout.readline(ansi=False), expect_word)

    def test_bye(self):
        self.assertRaises(SystemExit, cit.bye, None)

    def test_get_input(self):
        self.fakein.write("ABC")
        userinput = cit.get_input()
        self.assertEqual(self.fakeout.readline(ansi=False), "> ")
        self.assertEqual(userinput, "ABC")

    def test_get_choice_1(self):
        self.fakein.write("1")
        self.assertEqual(cit.get_choice(["ABC", "DEF"]), "ABC")
        expect_word = "|  1) ABC\n|  2) DEF\n> "
        self.assertEqual(self.fakeout.readline(ansi=False), expect_word)

    def test_get_choice_2(self):
        self.fakein.write("ABC")
        self.assertEqual(cit.get_choice(["ABC", "DEF"]), "ABC")
        expect_word = "|  1) ABC\n|  2) DEF\n> "
        self.assertEqual(self.fakeout.readline(ansi=False), expect_word)

    def test_as_session_1(self):
        @cit.as_session
        def func():
            print('ABC')

        func()
        expect_word = "*\n| __FUNC__________________________\nABC\n`\n"
        self.assertEqual(self.fakeout.readline(ansi=False), expect_word)

    def test_as_session_2(self):
        @cit.as_session('DEF')
        def func():
            print('ABC')

        func()
        expect_word = "*\n| __DEF__________________________\nABC\n`\n"
        self.assertEqual(self.fakeout.readline(ansi=False), expect_word)

    def test_as_session_3(self):
        @cit.as_session
        def underscore_orCamel():
            print('ABC')

        underscore_orCamel()
        expect_word = "*\n| __UNDERSCORE OR CAMEL__________________________\nABC\n`\n"
        self.assertEqual(self.fakeout.readline(ansi=False), expect_word)

    def test_write_file(self):
        content = "3.1415926"
        len_write = cit.write_file(self.TMP_FILE, content)
        self.assertEqual(len_write, len(content))

    def test_write_file_overwrite(self):
        content = "3.1415926"
        len_write = cit.write_file(self.TMP_FILE, content, overwrite=True)
        self.assertEqual(len_write, len(content))

    def test_read_file(self):
        content = "3.1415926"
        len_write = cit.write_file(self.TMP_FILE, content)
        content_read = cit.read_file(self.TMP_FILE)
        self.assertEqual(content_read, content)

    def test_read_file_with_encoding(self):
        content = "3.1415926"
        len_write = cit.write_file(self.TMP_FILE, content)
        content_read, encoding = cit.read_file(self.TMP_FILE, with_encoding=True)
        self.assertEqual(encoding, "utf-8")


if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)
