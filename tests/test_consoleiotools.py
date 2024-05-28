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
            self.assertEqual('╰', fake_out.getvalue().strip())

    def test_ascii(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            cit.__ascii__ = True
            cit.end()
            cit.__ascii__ = False
            self.assertEqual("`", fake_out.getvalue().strip())

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

    def test_echo_indent(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            cit.echo("ABC", indent=1)
            self.assertEqual(fake_out.getvalue(), "│ ├── ABC\n")

    def test_echo_indent_leaf(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            cit.echo("ABC", indent=-1)
            self.assertEqual(fake_out.getvalue(), "│ ╰── ABC\n")

    def test_echo_indent_stem(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            cit.echo("ABC", indent=2)
            self.assertEqual(fake_out.getvalue(), "│ ╷   ├── ABC\n")

    def test_markdown(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            cit.markdown("### ABC")
            self.assertEqual(fake_out.getvalue().strip(), "ABC")

    def test_panel(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            cit.panel("ABC", title="ABC", subtitle="ABC", expand=False, style="dim")
            self.assertEqual(fake_out.getvalue().strip(), "\n".join([
                "╭─ ABC ─╮",
                "│ ABC   │",
                "╰─ ABC ─╯",
            ]))

    def test_title(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            cit.title("ABC")
            self.assertEqual(fake_out.getvalue().strip(), "\n".join([
                "╭─────╮",
                "│ ABC │",
                "╰─────╯",
            ]))

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

    def test_mute(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            cit.mute("ABC")
            self.assertEqual(fake_out.getvalue(), "│ ABC\n")

    def test_print(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            cit.print("ABC")
            self.assertEqual(fake_out.getvalue(), "ABC\n")

    def test_print_escape(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            cit.print(cit.escape("[test]ABC"))
            self.assertEqual(fake_out.getvalue(), "[test]ABC\n")

    def test_pause(self):
        with patch("sys.stdin", new=StringIO("\n")):  # simulate press enter
            cit.pause()

    def test_track(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            for i in cit.track(range(5), disable=True):
                print(i)
            self.assertEqual("0\n1\n2\n3\n4\n\n", fake_out.getvalue())

    def test_bye(self):
        self.assertRaises(SystemExit, cit.bye, None)

    def test_get_input(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("ABC\n")):
            userinput = cit.get_input()
            self.assertIn("> ", fake_out.getvalue())
            self.assertEqual(userinput, "ABC")

    def test_get_input_question(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("ABC\n")):
            userinput = cit.get_input(question="question")
            self.assertIn("question", fake_out.getvalue())
            self.assertEqual(userinput, "ABC")

    def test_get_input_prompt(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("ABC\n")):
            userinput = cit.get_input(prompt=": ")
            self.assertIn(": ", fake_out.getvalue())
            self.assertEqual(userinput, "ABC")

    def test_get_input_default(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("\n")):
            userinput = cit.get_input(default="answer")
            self.assertIn("> (answer) ", fake_out.getvalue())
            self.assertEqual(userinput, "answer")

    def test_get_input_strip(self):
        with patch("sys.stdout", new=StringIO()), patch("sys.stdin", new=StringIO("  ABC  \n")):
            userinput = cit.get_input(strip=True)
            self.assertEqual(userinput, "ABC")
        with patch("sys.stdout", new=StringIO()), patch("sys.stdin", new=StringIO("  ABC  \n")):
            userinput = cit.get_input(strip=False)
            self.assertEqual(userinput, "  ABC  ")

    def test_get_choice(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("1\n")):
            self.assertEqual(cit.get_choice(["ABC", "DEF"]), "ABC")
            self.assertIn("1) ABC", fake_out.getvalue())
            self.assertIn("2) DEF", fake_out.getvalue())

    def test_get_choice_string(self):
        with patch("sys.stdout", new=StringIO()), patch("sys.stdin", new=StringIO("ABC\n")):
            self.assertEqual(cit.get_choice(["ABC", "DEF"]), "ABC")

    def test_get_choices_done(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("1\n0\n")):
            self.assertEqual(cit.get_choices(["ABC", "DEF"]), ["ABC", ])
            self.assertIn("DONE", fake_out.getvalue())

    def test_get_choices_done_esc(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("1\ndone\n")):
            self.assertEqual(cit.get_choices(["ABC", "0"]), ["ABC", ])
            self.assertIn("done)", fake_out.getvalue())

    def test_get_choices_exitable_esc(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("exit\n")):
            self.assertEqual(cit.get_choices(["ABC", "0"], exitable=True), [])
            self.assertIn("exit)", fake_out.getvalue())

    def test_get_choices_exitable(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("0\n")):
            self.assertEqual(cit.get_choices(["ABC", "DEF"], exitable=True), [])
            self.assertIn("EXIT", fake_out.getvalue())

    def test_get_choices_allable_off(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("a\n0\n")):  # allable off
            self.assertEqual(cit.get_choices(["ABC", "DEF"], exitable=True), [])
            self.assertIn("Please enter a valid choice.", fake_out.getvalue())

    def test_get_choices_allable_esc(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("all\n0\n")):  # allable off
            self.assertEqual(cit.get_choices(["a", "DEF"], allable=True, exitable=True), ["a", "DEF"])
            self.assertIn("all)", fake_out.getvalue())

    def test_get_choices_allable_select(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("a\n0\n")):  # allable on
            self.assertEqual(cit.get_choices(["ABC", "DEF"], allable=True), ["ABC", "DEF"])
            expect_word = "ALL"
            self.assertIn(expect_word, fake_out.getvalue())

    def test_get_choices_allable_unselect(self):
        with patch("sys.stdout", new=StringIO()) as fake_out, patch("sys.stdin", new=StringIO("a\na\n0\n")):  # allable on, unselect all.
            self.assertEqual(cit.get_choices(["ABC", "DEF"], allable=True, exitable=True), [])
            self.assertIn("[✓] ABC", fake_out.getvalue())

    def test_as_session_1(self):
        @cit.as_session
        def func():
            print('ABC')

        with patch("sys.stdout", new=StringIO()) as fake_out:
            func()
            self.assertEqual(fake_out.getvalue().strip(), "\n".join([
                "╭──────╮",
                "│ FUNC │",
                "╰──────╯",
                "ABC",
                "╰",
            ]))

    def test_as_session_2(self):
        @cit.as_session('DEF')
        def func():
            print('ABC')

        with patch("sys.stdout", new=StringIO()) as fake_out:
            func()
            self.assertEqual(fake_out.getvalue().strip(), "\n".join([
                "╭─────╮",
                "│ DEF │",
                "╰─────╯",
                "ABC",
                "╰",
            ]))

    def test_as_session_3(self):
        @cit.as_session
        def underscore_orCamel():
            print('ABC')

        with patch("sys.stdout", new=StringIO()) as fake_out:
            underscore_orCamel()
            self.assertEqual(fake_out.getvalue().strip(), "\n".join([
                "╭─────────────────────╮",
                "│ UNDERSCORE OR CAMEL │",
                "╰─────────────────────╯",
                "ABC",
                "╰",
            ]))

    def test_deprecated_by(self):
        @cit.deprecated_by(print)
        def old_func(s: str):
            print("Calling old_func()")

        with patch("sys.stderr", new=StringIO()) as fake_err, patch("sys.stdout", new=StringIO()) as fake_out:
            old_func("ABC")
            self.assertEqual(fake_out.getvalue().strip(), "ABC")
            self.assertIn("DeprecationWarning: Function `old_func` is deprecated, now calling `print` instead.", fake_err.getvalue().strip())

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
        self.assertGreater(len_write, 0)
        self.assertEqual(content_read, content)

    def test_read_file_with_encoding(self):
        content = "3.1415926"
        len_write = cit.write_file(self.TMP_FILE, content)
        content_read, encoding = cit.read_file(self.TMP_FILE, with_encoding=True)
        self.assertGreater(len_write, 0)
        self.assertEqual(content_read, content)
        self.assertEqual(encoding, "utf-8")


if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)
