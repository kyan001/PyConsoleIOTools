from functools import wraps
import sys

import rich.console
import rich.theme
import rich.panel
import rich.text
import rich.progress
import rich.traceback
import rich.markdown
import rich.box
import rich.markup

__version__ = "5.0.1"
__ascii__ = False
theme = rich.theme.Theme({
    "echo": "",
    "echo-bar": "",
    "echo-pre": "dim",
    "echo-indent": "dim",
    "info": "",
    "info-bar": "bright_white",
    "info-pre": "dim bright_white",
    "info-indent": "dim",
    "warn": "red",
    "warn-bar": "red",
    "warn-pre": "dim red",
    "warn-indent": "dim",
    "err": "bright_white on red",
    "err-bar": "bright_red",
    "err-pre": "dim bright_red",
    "err-indent": "dim",
    "ask": "yellow",
    "ask-bar": "yellow",
    "ask-pre": "dim yellow",
    "ask-indent": "dim",
    "muted": "dim bright_white",
    "muted-bar": "dim white",
    "muted-pre": "dim white",
    "muted-indent": "dim",
    "title": "bright_magenta",
    "pause": "bright_yellow",
    "choice-i": "yellow",
    "choice-cmd": "yellow underline",
})
console = rich.console.Console(theme=theme)  # main output printer


def debug(show_locals: bool = True) -> None:
    rich.traceback.install(show_locals=show_locals)


def as_session(name_or_func):  # decorator
    """print start/title/end info before and after the function call

    Args:
        title: title will show after the start, if has any
    """
    if callable(name_or_func):  # no name provided
        func = name_or_func
        name = func.__name__
        name = "".join([(" " + x) if x.isupper() else x for x in name])
        name = name.replace("_", " ")
        return as_session(name)(func)  # deco(func) -> deco(name)(func)
    else:
        name = name_or_func

    def get_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start()
            title(name)
            result = func(*args, **kwargs)
            end()
            return result
        return wrapper
    return get_func


def deprecated_by(new_func):  # decorator
    """print deprecated info before the function call

    Args:
        func (callable): the function that replace the deprecated one

    Returns:
        callable: the decorated function
    """
    import contextlib

    def call_new_func(old_func):
        @wraps(old_func)
        def wrapper(*args, **kwargs):
            with contextlib.redirect_stdout(sys.stderr):
                warn(f"DeprecationWarning: Function `{old_func.__name__}` is deprecated, now calling `{new_func.__name__}` instead.")
            return new_func(*args, **kwargs)
        return wrapper
    return call_new_func


def start():
    br()
    return sys.modules[__name__]  # chaining


def end():
    console.print("`" if __ascii__ else "╰")
    return sys.modules[__name__]  # chaining


def br(count=1):
    """print 1 to N blank lines"""
    print("\n" * (count - 1))
    return sys.modules[__name__]  # chaining


def echo(*args, pre: str = "", bar: str = "|" if __ascii__ else "│", style: str = "echo", indent: int = 0, **options):
    txt = rich.text.Text()
    if bar:
        txt.append(f"{bar}", style=f"{style}-bar" if f"{style}-bar" in theme.styles else style)
        txt.append(" ")
    if pre:
        txt.append(f"({pre.capitalize()})", style=f"{style}-pre" if f"{style}-pre" in theme.styles else style)
        txt.append(" ")
    if indent:
        indent_char_stem = "|   " if __ascii__ else "╷   "
        indent_char_branch = "|-- " if __ascii__ else "├── "
        indent_char_leaf = "`-- " if __ascii__ else "╰── "
        if indent < 0:
            indent = -indent
            indent_deco = indent_char_leaf
        else:
            indent_deco = indent_char_branch
        indent_deco = indent_char_stem * (indent - 1) + indent_deco
        txt.append(f"{indent_deco}", style=f"{style}-indent" if f"{style}-indent" in theme.styles else style)
    contents = rich.text.Text(" ").join(rich.text.Text.from_markup(f"{arg}") for arg in args)
    contents.stylize(style)
    txt.append(contents)
    console.print(txt, **options)
    return sys.modules[__name__]  # chaining


def title(*args, **options):
    """print something like a title"""
    console.print(rich.panel.Panel((" ".join([f"{arg}" for arg in args])).upper().strip(), highlight=True, expand=False, box=rich.box.ASCII if __ascii__ else rich.box.ROUNDED), **options)
    return sys.modules[__name__]  # chaining


def ask(*args, **options):
    return echo(*args, pre="?", style="ask", **options)


def info(*args, **options):
    return echo(*args, pre="info", style="info", **options)


def warn(*args, **options):
    return echo(*args, pre="warning", style="warn", **options)


def err(*args, **options):
    return echo(*args, pre="error", style="err", **options)


def mute(*args, **options):
    return echo(*args, style="muted", **options)


def print(*args, **options):
    console.print(*args, **options)
    return sys.modules[__name__]  # chaining


def markdown(*args, **options):
    console.print(rich.markdown.Markdown(" ".join([f"{arg}" for arg in args])))
    return sys.modules[__name__]  # chaining


def rule(title: str, *args, **options):
    console.rule(title, *args, characters="-" if __ascii__ else "─", **options)
    return sys.modules[__name__]  # chaining


def panel(txt, title="", subtitle="", expand=True, highlight=True, style="", **options):
    console.print(
        rich.panel.Panel(
            txt,
            title=title,
            subtitle=subtitle,
            highlight=highlight,
            expand=expand,
            style=style,
            border_style=f"{style}-pre" if f"{style}-pre" in theme.styles else "",
            box=rich.box.ASCII if __ascii__ else rich.box.ROUNDED,
            **options
        )
    )
    return sys.modules[__name__]  # chaining


def escape(txt: str) -> str:
    """Escapes text so that it won't be interpreted as markup for rich.markup.

    Args:
        txt (str): The original text to escape.

    Returns:
        str: The escaped text. All squared brackets `[]` escaped.
    """
    return rich.markup.escape(txt)


def pause(msg="Press [Enter] to Continue..."):
    """press to continue"""
    with console.status(f"[pause]{escape(msg)}", spinner="point", spinner_style="pause"):
        input()
    return sys.modules[__name__]  # chaining


def bye(message: str = "", error: bool = False):
    """print a message and exit the program"""
    if error:
        if message:
            err(message)
        exit(1)
    else:
        if message:
            info(message)
        exit(0)


def get_input(question: str = "", prompt: str = "> ", default: str = "", strip: bool = True) -> str:
    """Get user input in stdin.

    Args:
        question: str. The question asked before get the answer.
        prompt: str. The prompt shows in the same line with the input field. Always ending with a space.
        default: str. If the answer is empty, default value returns.
        strip: bool. Remove leading and trailing whitespaces from user input or not. Default is True.
    """
    if default:
        prompt += f"[dim]({default})[/]"
    if question:
        ask(question)
    if prompt:
        console.print(prompt.strip(), end=" ")
    answer = input()
    if strip:
        answer = answer.strip()
    if answer == "":
        br()
        return default
    return answer


def get_choice(choices, exitable: bool = False, default: str = "") -> str:
    """Get user choice from a given list

    Args:
        choices: list. The list that user can choose from.
        exitable: bool. Does `exit` is an option for user to select.
    """
    EXIT_WORD = "exit" if "0" in choices else "0"
    DECO = f"[dim]{'--' if __ascii__ else '──'}[/]"
    BAR = "|" if __ascii__ else "│"
    CMD_TEXT = "[{color}]{icon}[/] [choice-cmd]{text}[/]"
    EXIT_TEXT = CMD_TEXT.format(color="red", icon='~' if __ascii__ else '✗', text="EXIT")
    fill = max(len(EXIT_WORD), 2)
    for index, item in enumerate(choices, start=1):
        console.print(f"{BAR} [choice-i]{index:>{fill}}[/][dim])[/] [white]{item}[/]")
    if exitable:
        console.print(f"{BAR} [choice-i]{EXIT_WORD:>{fill}}[/][dim])[/] {DECO} {EXIT_TEXT} {DECO}")
    user_choice = get_input(default=default).strip()
    if exitable and user_choice == EXIT_WORD:
        return ""
    if user_choice in choices:
        return user_choice
    if user_choice.isdigit():
        index = int(user_choice) - 1
        if 0 <= index < len(choices):
            return choices[index]
    err("Please enter a valid choice.")
    return get_choice(choices, exitable, default)


def get_choices(choices, allable: bool = False, exitable: bool = False) -> list:
    def toggle_listitem(itm, lst: list):
        if itm in lst:
            lst.remove(itm)
        else:
            lst.append(itm)
        return lst

    EXIT_WORD = "exit" if "0" in choices else "0"
    DONE_WORD = "done" if "0" in choices else "0"
    ALL_WORD = "all" if "a" in choices else "a"
    DECO_WORD = f"[dim]{'--' if __ascii__ else '──'}[/]"
    BAR_WORD = "|" if __ascii__ else "│"
    BRACKET_WORD = "[cyan]" + escape("[{}]") + "[/]"
    CMD_TEXT = "[{color}]{icon}[/] [choice-cmd]{text}[/]"
    ALL_TEXT = CMD_TEXT.format(color="yellow", icon='+' if __ascii__ else '❍', text="ALL")
    EXIT_TEXT = CMD_TEXT.format(color="red", icon='~' if __ascii__ else '✗', text="EXIT")
    DONE_TEXT = CMD_TEXT.format(color="green", icon='=' if __ascii__ else '✓', text="DONE")
    fill = max(len(EXIT_WORD), len(DONE_WORD), len(ALL_WORD), 2)
    user_choices = []
    while True:
        if allable:
            console.print(f"{BAR_WORD} [choice-i]{ALL_WORD:>{fill}}[/][dim])[/] {DECO_WORD} {ALL_TEXT} {DECO_WORD}")
        for index, item in enumerate(choices, start=1):
            mark = BRACKET_WORD.format(f"[bright_green]{'+' if __ascii__ else '✓'}[/]") if item in user_choices else BRACKET_WORD.format(" ")  # item is selected or not
            console.print(f"{BAR_WORD} [choice-i]{index:>{fill}}[/][dim])[/] {mark} [white]{item}")
        if user_choices:  # user selections > 0
            console.print(f"{BAR_WORD} [choice-i]{DONE_WORD:>{fill}}[/][dim])[/] {DECO_WORD} {DONE_TEXT} {DECO_WORD}")
        elif exitable:  # no user selection, but exitable is on.
            console.print(f"{BAR_WORD} [choice-i]{EXIT_WORD:>{fill}}[/][dim])[/] {DECO_WORD} {EXIT_TEXT} {DECO_WORD}")
        user_choice = get_input().strip()
        if (user_choice == DONE_WORD or user_choice == EXIT_WORD or user_choice == ""):
            if exitable or len(user_choices) > 0:  # keep looping when not exitable and no user choices.
                return user_choices
        if allable and user_choice == ALL_WORD:
            if len(user_choices) == len(choices):
                user_choices = []
            else:
                user_choices = choices.copy()
        elif user_choice in choices:
            user_choices = toggle_listitem(user_choice, user_choices)
        elif user_choice.isdigit() and 0 < int(user_choice) <= len(choices):
            index = int(user_choice) - 1
            user_choices = toggle_listitem(choices[index], user_choices)
        else:
            err("Please enter a valid choice.")


def track(iterable, desc="", unit="", *args, **options):
    with rich.progress.Progress("|" if __ascii__ else "│", rich.progress.SpinnerColumn(), *rich.progress.Progress.get_default_columns(), "·", rich.progress.MofNCompleteColumn(), unit, *args, **options) as progress:
        task = progress.add_task(desc, total=None if not iterable or not len(iterable) else len(iterable))
        while not progress.finished:
            for item in iterable:
                yield item
                progress.update(task, advance=1)


def read_file(path: str, with_encoding: bool = False, **kwargs) -> tuple[str, str] | str:
    for enc in ("utf-8", "gbk", "cp1252", "windows-1252", "latin-1"):
        try:
            with open(path, mode="r", encoding=enc, **kwargs) as f:
                return (f.read(), enc) if with_encoding else f.read()
        except UnicodeDecodeError:
            pass
    return ("", "") if with_encoding else ""


def write_file(path: str, content: str, overwrite: bool = False, **kwargs):
    mode = "w" if overwrite else "a"
    with open(path, mode=mode, encoding="utf-8", **kwargs) as fl:
        return fl.write(content)


if __name__ == "__main__":
    markdown(read_file("README.md"))
