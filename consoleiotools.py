from functools import wraps
import colorama
from colorama import Fore, Back, Style
colorama.init()


__version__ = '2.7.1'


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
    err("Please enter a valid choice")
    return get_choice(choices)


def get_choices(choices, style="[+]", allable=False):
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
        echo("{Fore.YELLOW}{word:>2}) ** {done_or_exit} **{Fore.RESET}".format(Fore=Fore, word=DONE_WORD, done_or_exit="DONE" if user_choices else "EXIT"))
        for index, item in enumerate(choices, start=1):
            is_selected = item in user_choices
            if style == "[+]":
                markl = "[+] " if is_selected else "[ ] "
                markr = ""
            else:
                markl = "[ " if is_selected else "  "
                markr = " ]" if is_selected else "  "
            assemble_print = "{Fore.YELLOW}{num:>2}){Fore.RESET} {markl}{Fore.WHITE}{itm}{Fore.RESET}{markr}".format(Fore=Fore, num=index, itm=item, markl=markl, markr=markr)
            echo(assemble_print)
        if allable:
            echo("{Fore.YELLOW}{word:>2}) ** ALL **{Fore.RESET}".format(Fore=Fore, word=ALL_WORD))
        user_choice = get_input().strip()
        if user_choice == DONE_WORD:
            return user_choices
        if allable and user_choice == ALL_WORD:
            user_choices = choices
        elif user_choice in choices:
            user_choices = toggle_listitem(user_choice, user_choices)
        elif user_choice.isdigit() and 0 < int(user_choice) <= len(choices):
            index = int(user_choice) - 1
            user_choices = toggle_listitem(choices[index], user_choices)
        else:
            err("Please enter a valid choice")


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
