from functools import wraps


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


def echo(words, prefix="", lvl=0):
    words = str(words)
    if prefix:
        prefix = '({})'.format(prefix.capitalize()) + ' '
    tabs = '    ' * int(lvl) if int(lvl) else ''
    print("| {p}{t}{w}".format(p=prefix, t=tabs, w=words))


def title(words):
    return echo(words + ":")


def info(words, **options):
    return echo(words, "info", **options)


def warn(words, **options):
    return echo(words, "warning", **options)


def err(words, **options):
    return echo(words, "error", **options)


def pause(cls, msg="\nPress Enter to Continue...\n"):
    """press to continue"""
    input(msg)
