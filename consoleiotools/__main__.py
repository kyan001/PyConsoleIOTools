import sys
import io
import time

import consoleiotools as cit


def inspect(func_name, *args, **kwargs):
    cit.br()
    args_txt = ""
    if args:
        args_txt += ", ".join(f"{('`' + a + '`') if isinstance(a, str) else str(a)}" for a in args)
    if kwargs:
        args_txt += ", " + ", ".join(f"{k}=" + f"{('`' + v + '`') if isinstance(v, str) else str(v)}" for k, v in kwargs.items())
    cit.print(f"[dim bright_white]# {func_name}({args_txt})")
    return getattr(cit, func_name)(*args, **kwargs)


class fake_input:
    def __init__(self, user_input: str, double: bool = False):
        self.double = double
        self.user_input = user_input.strip().strip("\n") + "\n"
        if double:
            self.user_input += self.user_input

    def __enter__(self):
        sys.stdin = io.StringIO(self.user_input)

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdin = sys.__stdin__


def examples():
    inspect("start")
    inspect("title", "This is a title")
    inspect("echo", "This is a normal print.")
    inspect("ask", "This is a question.")
    inspect("info", "This is a info message.")
    inspect("warn", "This is a warning message.")
    inspect("err", "This is an error message.")
    inspect("mute", "This is a muted message.")
    inspect("end")
    inspect("print", "This is a [blue]COLORFUL[/] print.")
    inspect("markdown", "> *This* **is** a `markdown` print.")
    inspect(
        "panel",
        "This is a panel.",
        title="Title",
        subtitle="Subtitle",
        expand=False
    )
    inspect("br")
    inspect("rule", "This is a horizontal rule.")
    with fake_input("Apple"):
        result = inspect("get_input", "Get user input:")
        print("Apple")
        print(repr(result))
    with fake_input("1"):
        result = inspect(
            "get_choice",
            [
                "Apple",
                "Banana",
            ],
            exitable=True
        )
        print("2")
        print(repr(result))
    with fake_input("0"):
        result = inspect(
            "get_choices",
            [
                "Apple",
                "Banana",
            ],
            exitable=True,
            allable=True
        )
        print("0")
        print(result)
    inspect("track", "range(10), desc='Progress', unit='unit'")
    for i in cit.track(range(10), desc="Progress", unit="unit"):
        time.sleep(0.1)
    inspect("pause")


if __name__ == "__main__":
    cit.panel("\n".join([
        f"cit.__version__ = {cit.__version__}",
        f"cit.__ascii__ = {cit.__ascii__}"
    ]), title="ConsoleIOTools Features")
    examples()
