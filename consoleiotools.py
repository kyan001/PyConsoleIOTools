from functools import wraps
import colorama
from colorama import Fore, Back, Style
colorama.init()


__version__ = '2.3.0'


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
    if exitable:
        echo(" {Fore.YELLOW}0) ** EXIT **{Fore.RESET}".format(Fore=Fore))
    for index, item in enumerate(choices, start=1):
        assemble_print = " {Fore.YELLOW}{num}){Fore.RESET} {Fore.WHITE}{itm}{Fore.RESET}".format(Fore=Fore, num=index, itm=item)
        echo(assemble_print)
    user_choice = get_input().strip()
    if user_choice in choices:
        return user_choice
    if user_choice == "0":
        return None
    elif user_choice.isdigit():
        index = int(user_choice) - 1
        if index >= len(choices):
            err("Invalid Choice")
            bye()
        return choices[index]
    else:
        err("Please enter a valid choice")
        return get_choice(choices)


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
