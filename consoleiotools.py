from functools import wraps
import colorama
from colorama import Fore, Back, Style
colorama.init()

with open("VERSION") as f:
    __version__ = f.read().strip()


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
            start()
            title(name)
            result = func(*args, **kwargs)
            end()
            return result
        return wrapper
    return get_func


def start():
    print('*')


def end():
    print('`')


def br(count=1):
    """print 1 to N blank lines"""
    print('\n' * (count - 1))


def echo(msg, pre=""):
    prefix = Style.DIM + Fore.WHITE + '({}) '.format(pre.capitalize()) + Fore.RESET + Style.RESET_ALL if pre else ''
    print("| " + Back.BLACK + "{pf}{msg}".format(pf=prefix, msg=msg) + Back.RESET + Fore.RESET + Style.RESET_ALL)


def title(msg, **options):
    """print something like a title"""
    return echo(Style.BRIGHT + Fore.CYAN + "__{}__________________________".format(msg.upper().strip()) + Style.RESET_ALL + Fore.RESET, **options)


def ask(msg, **options):
    return echo(Fore.YELLOW + msg, "?", **options)


def info(msg, **options):
    return echo(msg, "info", **options)


def warn(msg, **options):
    return echo(Fore.RED + msg, "warning", **options)


def err(msg, **options):
    return echo(Back.RED + Fore.WHITE + Style.BRIGHT + msg, "error", **options)


def dim(msg, **options):
    return echo(Style.DIM + Fore.WHITE + msg, **options)


def pause(msg="Press Enter to Continue..."):
    """press to continue"""
    print('\n' + Fore.YELLOW + msg + Fore.RESET, end='')
    input()


def bye(msg=''):
    """print msg and exit"""
    exit(msg)


def get_input(question='', prompt='> '):
    if question:
        ask(question)
    return str(input(prompt)).strip()


def get_choice(choices, exitable: bool = False):
    """Get user choice from a given list

    Args:
        choices: list. The list that user can choose from.
        exitable: bool. Does `exit` is an option for user to select.
    """
    if exitable:
        exit_word = "0"
        echo("{Fore.YELLOW}{word:>2}) ** EXIT **{Fore.RESET}".format(Fore=Fore, word=exit_word))
    for index, item in enumerate(choices, start=1):
        assemble_print = "{Fore.YELLOW}{num:>2}){Fore.RESET} {Fore.WHITE}{itm}{Fore.RESET}".format(Fore=Fore, num=index, itm=item)
        echo(assemble_print)
    user_choice = get_input().strip()
    if exitable and user_choice == exit_word:
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

    DONE_WORD = "0"
    ALL_WORD = "all" if "a" in choices else "a"
    user_choices = []
    while True:
        if user_choices:  # user selections > 0
            echo("{Fore.YELLOW}{word:>2}) ** DONE **{Fore.RESET}".format(Fore=Fore, word=DONE_WORD))
        elif exitable:  # no user selection, but exitable is on.
            echo("{Fore.YELLOW}{word:>2}) ** EXIT **{Fore.RESET}".format(Fore=Fore, word=DONE_WORD))
        for index, item in enumerate(choices, start=1):
            mark = "[+]" if item in user_choices else "[ ]"  # item is selected or not
            assemble_print = "{Fore.YELLOW}{num:>2}){Fore.RESET} {mark} {Fore.WHITE}{itm}{Fore.RESET}".format(Fore=Fore, num=index, itm=item, mark=mark)
            echo(assemble_print)
        if allable:
            echo("{Fore.YELLOW}{word:>2}) ** ALL **{Fore.RESET}".format(Fore=Fore, word=ALL_WORD))
        user_choice = get_input().strip()
        if user_choice == DONE_WORD:
            if exitable or len(user_choices) > 0:
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
