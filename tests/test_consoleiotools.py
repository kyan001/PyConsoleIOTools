from typing import List
import unittest
import sys
import os
from unittest.mock import patch

from ansiesc import StringIO

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import consoleiotools as cit  # noqa: linter (pycodestyle) should not lint this line.


class test_consoleiotools(unittest.TestCase):
    """For testing consoleiotools"""
    TMP_FILE = "tmp.txt"

    def setUp(self):
        pass

    def tearDown(self):
        if os.path.isfile(self.TMP_FILE):
            os.remove(self.TMP_FILE)

    def test_version(self):
        self.assertTrue(isinstance(cit.__version__, str))

    def test_start(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            cit.start()
            self.assertEqual(fake_out.getvalue(), '\n')

    def test_end(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            cit.end()
            self.assertTrue('\n' in fake_out.getvalue())

    def test_br(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            cit.br(2)
            self.assertEqual(fake_out.getvalue(), '\n\n')

    def test_echo(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            cit.echo("ABC")
            self.assertEqual(fake_out.getvalue(), "│ ABC\n")

    def test_echo_pre(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            cit.echo("ABC", pre="prefix")
            self.assertEqual(fake_out.getvalue(), "│ (Prefix) ABC\n")

    def test_echo_bar(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            cit.echo("ABC", bar="BAR")
            self.assertEqual(fake_out.getvalue(), "BAR ABC\n")

    def test_markdown(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            cit.markdown("### ABC")
            self.assertEqual(fake_out.getvalue().strip(), "ABC")

    def test_title(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            cit.title("ABC")
            self.assertEqual(fake_out.getvalue().strip(), """
╭─────╮
│ ABC │
╰─────╯
            """.strip())

    def test_ask(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            cit.ask("ABC")
            self.assertEqual(fake_out.getvalue(), "│ (?) ABC\n")

    def test_info(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            cit.info("ABC")
            self.assertEqual(fake_out.getvalue(), "│ (Info) ABC\n")

    def test_warn(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            cit.warn("ABC")
            self.assertEqual(fake_out.getvalue(), "│ (Warning) ABC\n")

    def test_err(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            cit.err("ABC")
            self.assertEqual(fake_out.getvalue(), "│ (Error) ABC\n")

    def test_dim(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            cit.dim("ABC")
            self.assertEqual(fake_out.getvalue(), "│ ABC\n")

    def test_pause(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("\n")):  # simulate press enter
            cit.pause()
            expect_word = "\nPress [Enter] to Continue..."
            self.assertEqual(fake_out.getvalue(), expect_word)

    def test_bye(self):
        self.assertRaises(SystemExit, cit.bye, None)

    def test_get_input(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("ABC\n")):
            userinput = cit.get_input()
            self.assertEqual(fake_out.getvalue(), "> ")
            self.assertEqual(userinput, "ABC")

    def test_get_choice_index(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("1\n")):
            self.assertEqual(cit.get_choice(["ABC", "DEF"]), "ABC")
            expect_word = "   1) ABC\n   2) DEF\n> "
            self.assertEqual(fake_out.getvalue(), expect_word)

    def test_get_choice_string(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("ABC\n")):
            self.assertEqual(cit.get_choice(["ABC", "DEF"]), "ABC")
            expect_word = "   1) ABC\n   2) DEF\n> "
            self.assertEqual(fake_out.getvalue(), expect_word)

    def test_get_choices_done(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("1\n0\n")):
            self.assertEqual(cit.get_choices(["ABC", "DEF"]), ["ABC", ])
            expect_word = "0) ** DONE **"
            self.assertTrue(expect_word in fake_out.getvalue())

    def test_get_choices_done_esc(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("1\ndone\n")):
            self.assertEqual(cit.get_choices(["ABC", "0"]), ["ABC", ])
            expect_word = "done) ** DONE **"
            self.assertTrue(expect_word in fake_out.getvalue())

    def test_get_choices_exitable_esc(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("exit\n")):
            self.assertEqual(cit.get_choices(["ABC", "0"], exitable=True), [])
            expect_word = "exit) ** EXIT **"
            self.assertTrue(expect_word in fake_out.getvalue())

    def test_get_choices_exitable(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("0\n")):
            self.assertEqual(cit.get_choices(["ABC", "DEF"], exitable=True), [])
            expect_word = "0) ** EXIT **"
            self.assertTrue(expect_word in fake_out.getvalue())

    def test_get_choices_allable_off(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("a\n0\n")):  # allable off
            self.assertEqual(cit.get_choices(["ABC", "DEF"], exitable=True), [])
            expect_word = "Please enter a valid choice."
            self.assertTrue(expect_word in fake_out.getvalue())

    def test_get_choices_allable_esc(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("all\n0\n")):  # allable off
            self.assertEqual(cit.get_choices(["a", "DEF"], allable=True, exitable=True), ["a", "DEF"])
            expect_word = "all) ** ALL **"
            self.assertTrue(expect_word in fake_out.getvalue())

    def test_get_choices_allable_select(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("a\n0\n")):  # allable on
            self.assertEqual(cit.get_choices(["ABC", "DEF"], allable=True), ["ABC", "DEF"])
            expect_word = "a) ** ALL **"
            self.assertTrue(expect_word in fake_out.getvalue())

    def test_get_choices_allable_unselect(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("a\na\n0\n")):  # allable on, unselect all.
            self.assertEqual(cit.get_choices(["ABC", "DEF"], allable=True, exitable=True), [])
            expect_word = "[+] ABC"
            self.assertTrue(expect_word in fake_out.getvalue())

    def test_as_session_1(self):
        @cit.as_session
        def func():
            print('ABC')

        with patch("sys.stdout", new=StringIO()) as fake_out:
            func()
            expect_word = """
╭────────╮
│ FUNC() │
╰────────╯
ABC
╰
            """
            self.assertEqual(fake_out.getvalue().strip(), expect_word.strip())

    def test_as_session_2(self):
        @cit.as_session('DEF')
        def func():
            print('ABC')

        with patch("sys.stdout", new=StringIO()) as fake_out:
            func()
            expect_word = """
╭───────╮
│ DEF() │
╰───────╯
ABC
╰
            """
            self.assertEqual(fake_out.getvalue().strip(), expect_word.strip())

    def test_as_session_3(self):
        @cit.as_session
        def underscore_orCamel():
            print('ABC')

        with patch("sys.stdout", new=StringIO()) as fake_out:
            underscore_orCamel()
            expect_word = """
╭───────────────────────╮
│ UNDERSCORE OR CAMEL() │
╰───────────────────────╯
ABC
╰
            """
            self.assertEqual(fake_out.getvalue().strip(), expect_word.strip())

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
