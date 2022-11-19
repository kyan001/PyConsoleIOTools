from functools import wraps

import rich.console
import rich.theme
import rich.panel
import rich.live
import rich.text
import rich.progress

__version__ = "3.0.8"
theme = rich.theme.Theme({
    "echo": "on black",
    "info": "",
    "warn": "red",
    "err": "bright_white on red",
    "ask": "yellow",
    "title": "bright_cyan",
    "pre": "dim white",
    "pause": "yellow",
})
console = rich.console.Console(theme=theme)


def as_session(name_or_func):  # decorator
    """print start/title/end info before and after the function call

    Args:
        title: title will show after the start, if has any
    """
    if callable(name_or_func):  # no name provided
        func = name_or_func
        name = func.__name__
        name = "".join([(' ' + x) if x.isupper() else x for x in name])
        name = name.replace('_', ' ')
        return as_session(name)(func)  # deco(func) -> deco(name)(func)
    else:
        name = name_or_func

    def get_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            panel = rich.panel.Panel("123", title=name)
            with rich.live.Live(console=console) as live:
                result = func(*args, **kwargs)
                panel.subtitle = result
            return result
        return wrapper
    return get_func


def start():
    console.print('*')


def end():
    console.print('`')


def br(count=1):
    """print 1 to N blank lines"""
    print('\n' * (count - 1))


def echo(*arg, pre: str = "", style: str = "echo", **options):
    txt = rich.text.Text(style=style)
    if pre:
        txt.append(f"({pre.capitalize()}) ", style="pre")
    txt.append(" ".join(arg))
    console.print(txt, **options)


def title(*arg, **options):
    """print something like a title"""
    return console.rule((" ".join(arg)).upper().strip())


def ask(*arg, **options):
    return echo(*arg, pre="?", style="ask", **options)


def info(*arg, **options):
    return echo(*arg, pre="info", style="info", **options)


def warn(*arg, **options):
    return echo(*arg, pre="warning", style="warn", **options)


def err(*arg, **options):
    return echo(*arg, pre="error", style="err", **options)


def dim(*arg, **options):
    return echo(*arg, style="dim white", **options)


def pause(msg="Press [Enter] to Continue..."):
    """press to continue"""
    echo(f"\n{msg}", style="pause", end="")
    return input()


def bye(msg=""):
    """print msg and exit"""
    exit(msg)


def get_input(question="", prompt="> "):
    if question:
        ask(question)
    return str(input(prompt)).strip()


def get_choice(choices, exitable: bool = False):
    """Get user choice from a given list

    Args:
        choices: list. The list that user can choose from.
        exitable: bool. Does `exit` is an option for user to select.
    """
    EXIT_WORD = "exit" if "0" in choices else "0"
    for index, item in enumerate(choices, start=1):
        echo(f"[yellow]{index:>2})[/] [white]{item}[/]")
    if exitable:
        echo(f"[yellow]{EXIT_WORD:>2}) ** [b]EXIT[/] **")
    user_choice = get_input().strip()
    if exitable and user_choice == EXIT_WORD:
        return None
    if user_choice in choices:
        return user_choice
    if user_choice.isdigit():
        index = int(user_choice) - 1
        if 0 <= index < len(choices):
            return choices[index]
    err("Please enter a valid choice.")
    return get_choice(choices)


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
    user_choices = []
    while True:
        if allable:
            echo(f"[yellow]{ALL_WORD:>2}) ** [b]ALL[/] **")
        for index, item in enumerate(choices, start=1):
            mark = r"\[[green]+[/]]" if item in user_choices else rich.markup.escape("[ ]")  # item is selected or not
            echo(f"[yellow]{index:>2})[/] {mark} [white]{item}")
        if user_choices:  # user selections > 0
            echo(f"[yellow]{DONE_WORD:>2}) ** [b]DONE[/] **")
        elif exitable:  # no user selection, but exitable is on.
            echo(f"[yellow]{EXIT_WORD:>2}) ** [b]EXIT[/] **")
        user_choice = get_input().strip()
        if (user_choice == DONE_WORD or user_choice == EXIT_WORD):
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


def track(iterable, desc="", *arg, **options):
    return rich.progress.track(iterable, description=desc)


def read_file(path: str, with_encoding: bool = False, **kwargs):
    for enc in ("utf-8", 'gbk', 'cp1252', 'windows-1252', 'latin-1'):
        try:
            with open(path, mode='r', encoding=enc, **kwargs) as f:
                return (f.read(), enc) if with_encoding else f.read()
        except UnicodeDecodeError:
            pass


def write_file(path: str, content: str, overwrite: bool = False, **kwargs):
    mode = 'w' if overwrite else 'a'
    with open(path, mode=mode, encoding='utf-8', **kwargs) as fl:
        return fl.write(content)
