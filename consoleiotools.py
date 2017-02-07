from functools import wraps
import colorama
from colorama import Fore, Back, Style
colorama.init()


__version__ = '2.0.2'


def as_session(name=''):  # decorator
    """print start/title/end info before and after the function call

    Args:
        title: title will show after the start, if has any
    """
    def get_func(func):
        @wraps(func)
        def call_func(*args, **kwargs):
            start()
            if name:
                title(name)
            result = func(*args, **kwargs)
            end()
            return result
        return call_func
    return get_func


def start():
    print('*')


def end():
    print('!')


def br(count=1):
    """print 1 to N blank lines"""
    print('\n' * (count - 1))


def echo(msg, pre=""):
    prefix = Style.DIM + Fore.WHITE + '({}) '.format(pre.capitalize()) + Fore.RESET + Style.RESET_ALL if pre else ''
    print("| " + Back.BLACK + "{pf}{msg}".format(pf=prefix, msg=msg) + Back.RESET + Fore.RESET + Style.RESET_ALL)


def title(msg, **options):
    """print something like a title"""
    return echo(Style.BRIGHT + Fore.CYAN + "__{}__________________________".format(msg.upper()) + Style.RESET_ALL + Fore.RESET, **options)


def ask(msg, **options):
    return echo(Fore.YELLOW + msg, "?", **options)


def info(msg, **options):
    return echo(msg, "info", **options)


def warn(msg, **options):
    return echo(Fore.RED + msg, "warning", **options)


def err(msg, **options):
    return echo(Fore.RED + Style.BRIGHT + msg, "error", **options)


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


def get_choice(choices):
    for index, item in enumerate(choices):
        assemble_print = ""
        assemble_print += Fore.YELLOW + " {}) ".format(str(index + 1)) + Fore.RESET
        assemble_print += Fore.WHITE + str(item) + Fore.RESET
        echo(assemble_print)
    user_choice = get_input().strip()
    if user_choice in choices:
        return user_choice
    elif user_choice.isdigit():
        index = int(user_choice) - 1
        if index >= len(choices):
            err("Invalid Choice")
            bye()
        return choices[index]
    else:
        err("Please enter a valid choice")
        return get_choice(choices)
