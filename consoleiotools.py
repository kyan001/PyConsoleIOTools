from functools import wraps

__version__ = '1.0.0'


def as_session(title=''):  # decorator
    """print start/title/end info before and after the function call

    Args:
        title: title will show after the start, if has any
    """
    def get_func(func):
        @wraps(func)
        def call_func(*args, **kwargs):
            start()
            if title:
                title(title)
            result = func(*args, **kwargs)
            end()
            return result
        return call_func
    return get_func


def start():
    print('*')


def end():
    print('!')


def echo(msg, prefix="", lvl=0):
    msg = str(msg)
    if prefix:
        prefix = '({})'.format(prefix.capitalize()) + ' '
    tabs = '    ' * int(lvl) if int(lvl) else ''
    print("| {pf}{tabs}{msg}".format(pf=prefix, tabs=tabs, msg=msg))


def title(msg):
    return echo(msg + ":")


def info(msg, **options):
    return echo(msg, "info", **options)


def warn(msg, **options):
    return echo(msg, "warning", **options)


def err(msg, **options):
    return echo(msg, "error", **options)


def pause(cls, msg="Press Enter to Continue..."):
    """press to continue"""
    input('\n' + msg)


def bye(cls, msg=''):
    """print msg and exit"""
    exit(msg)


def get_input(question='', prompt='> '):
    if question:
        print(question)
    return str(input(prompt)).strip()


def get_choice(choices):
    assemble_print = ""
    for index, item in enumerate(choices):
        assemble_print += '\n' if index else ''
        assemble_print += "| " + " {}) ".format(str(index + 1)) + str(item)
    user_choice = get_input(assemble_print)
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
