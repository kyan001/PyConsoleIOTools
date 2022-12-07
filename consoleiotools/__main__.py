import sys
import io
import time

import consoleiotools as cit


def func_example(func_name, *args, **kwargs):
    cit.br()
    cit.print(f"{'*' if cit.__ascii__ else '•'} [cyan u]{func_name}[dim]()")
    if args or kwargs:
        return getattr(cit, func_name)(*args, **kwargs)
    else:
        return getattr(cit, func_name)()


class fake_input():
    def __init__(self, user_input: str):
        self.user_input = user_input

    def __enter__(self):
        sys.stdin = io.StringIO(self.user_input)

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdin = sys.__stdin__


def examples():
    func_example("start")
    func_example("title", "This is title(...)")
    func_example("echo", "This is echo(...)")
    func_example("ask", "This is ask(...)")
    func_example("info", "This is info(...)")
    func_example("warn", "This is warn(...)")
    func_example("err", "This is err(...)")
    func_example("mute", "This is mute(...)")
    func_example("end")
    func_example("print", "This is print(...)")
    func_example("markdown", "> *This* **is** `markdown(...)`")
    func_example(
        "panel",
        "This is panel(..., title='Title', subtitle='Subtitle', expand=False)",
        title="Title",
        subtitle="Subtitle",
        expand=False
    )
    func_example("br")
    func_example("rule", "This is rule(...)")
    with fake_input("Apple\n"):
        result = func_example("get_input", "This is get_input(...)")
        print("Apple")
        print(repr(result))
    with fake_input("2\n"):
        result = func_example(
            "get_choice",
            [
                "get_choice(..., exitable=True)",
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
                "get_choices(..., exitable=True, allable=True)",
                "Apple",
                "Banana",
            ],
            exitable=True,
            allable=True
        )
        print("0")
        print(result)
    func_example("track", [])
    for i in cit.track(range(10), desc="Progress", unit="unit"):
        time.sleep(0.1)
    func_example("pause")


if __name__ == "__main__":
    cit.panel(f"cit.__version__ = {cit.__version__}\ncit.__ascii__ = {cit.__ascii__}", title="ConsoleIOTools Features")
    examples()
