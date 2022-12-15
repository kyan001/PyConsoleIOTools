import sys
import io
import time

import consoleiotools as cit


def func_example(func_name, *args, **kwargs):
    cit.br()
    args_txt = ""
    if args:
        args_txt += ", ".join(f"{('`' + a + '`') if isinstance(a, str) else str(a)}" for a in args)
    if kwargs:
        args_txt += ", " + ", ".join(f"{k}=" + f"{('`' + v + '`') if isinstance(v, str) else str(v)}" for k, v in kwargs.items())
    cit.print(f"[dim bright_white]# {func_name}({args_txt})")
    return getattr(cit, func_name)(*args, **kwargs)


class fake_input():
    def __init__(self, user_input: str):
        self.user_input = user_input

    def __enter__(self):
        sys.stdin = io.StringIO(self.user_input)

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdin = sys.__stdin__


def examples():
    func_example("start")
    func_example("title", "This is a title")
    func_example("echo", "This is a normal print.")
    func_example("ask", "This is a question.")
    func_example("info", "This is a info message.")
    func_example("warn", "This is a warning message.")
    func_example("err", "This is an error message.")
    func_example("mute", "This is a muted message.")
    func_example("end")
    func_example("print", "This is a [blue]COLORFUL[/] print.")
    func_example("markdown", "> *This* **is** a `markdown` print.")
    func_example(
        "panel",
        "This is a panel.",
        title="Title",
        subtitle="Subtitle",
        expand=False
    )
    func_example("br")
    func_example("rule", "This is a horizontal rule.")
    with fake_input("Apple\n"):
        result = func_example("get_input", "Get user input:")
        print("Apple")
        print(repr(result))
    with fake_input("1\n"):
        result = func_example(
            "get_choice",
            [
                "Apple",
                "Banana",
            ],
            exitable=True
        )
        print("2")
        print(repr(result))
    with fake_input("0\n"):
        result = func_example(
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
    func_example("track", "range(10), desc='Progress', unit='unit'")
    for i in cit.track(range(10), desc="Progress", unit="unit"):
        time.sleep(0.1)
    func_example("pause")


if __name__ == "__main__":
    cit.panel(f"cit.__version__ = {cit.__version__}\ncit.__ascii__ = {cit.__ascii__}", title="ConsoleIOTools Features")
    examples()
