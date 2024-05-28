# PyConsoleIOTools
![PyPI - Downloads](https://img.shields.io/pypi/dm/consoleiotools.svg)
![GitHub release](https://img.shields.io/github/release/kyan001/PyConsoleIOTools.svg)
[![GitHub license](https://img.shields.io/github/license/kyan001/PyConsoleIOTools.svg)](https://github.com/kyan001/PyConsoleIOTools/blob/master/LICENSE)

## Installation

```sh
pip install consoleiotools  # install
pip install --upgrade consoleiotools  # update
python -m consoleiotools  # examples
```

## Get Started

```python
import consoleiotools as cit
print(cit.__version__)
```

## Prints on Screen

```python
>>> cit.start()
# blank line

>>> cit.title("Session Name")
+--------------+
| SESSION NAME |
+--------------+

>>> cit.echo("Hello World")
| Hello World

>>> cit.echo("Hello World", pre="say", bar="!")
! (Say) Hello World

>>> cit.echo("Hello World", indent="+")  # indent, `+` means 1 level of indents
| |-- Hello World

>>> cit.echo("Hello World", indent="-")  # `-` means last line of indents.
| `-- Hello World

>>> cit.echo("Hello World", indent="+-+-")  # 4 levels of indents
| |       |   `-- Hello World
# |   |   |   |   |
# |   |   |   |   `-- The content
# |   |   |   `------ The last char `-` in `indent=`
# |   |   `---------- The 3rd char `+` in `indent=`
# |   `-------------- The 2nd char `-` in `indent=`
# `------------------ The 1st char `+` in `indent=`

>>> cit.ask("Hello World")
| (?) Hello World

>>> cit.info("Hello World")
| (Info) Hello World

>>> cit.warn("Hello World")
| (Warning) Hello World

>>> cit.err("Hello World")
| (Error) Hello World

>>> cit.mute("Hello World")
| Hello World  # muted by dim

>>> cit.print("[yellow]Hello World[/]")  # print with styles
Hello World  # yellow

>>> cit.print(cit.escape("[yellow]Hello World[/]"))  # escape `[` -> `\[` if not escaped. escape `\` -> `\\` if not used as escape char.
[yellow]Hello World[/]

>>> cit.markdown("# Header")  # print markdown
+--------------+
|    Header    |
+--------------+

>>> cit.rule()  # print horizontal rule
----------------------------------------

>>> cit.rule("Title", style="blue", align="center")  # print horizontal rule with Title. align = center|left|right
---------------- Title ----------------


>>> cit.panel("Panel", title="Panel Title", subtitle="Panel Subtitle")  # print text in a panel
+---------- Panel Title ----------+
| Panel                           |  # full width
+-------- Panel Subtitle ---------+

>>> cit.panel("Panel", title="Panel Title", subtitle="Panel Subtitle", expand=False, style="blue")  # fit panel to text
+- Panel Title -+  # blue
| Panel         |
+- Panel Subtit-+

>>> cit.end()
`

>>> cit.br()
# blank line

>>> cit.br(2)
# blank line
# blank line

>>> for var in cit.track(iterables, "Progress"): pass
| : Progress ---------------------===================  52% 0:00:52 - 52/100

>>> cit.__ascii__ = True  # use ascii chars only.
```

## Get User Input

```python
>>> cit.get_input()  # Get user input from stdin
> Hello World
'Hello World'

>>> cit.get_input("Question?")  # With a question
| (?) Question?
> Yes
'Yes'

>>> cit.get_input(prompt="Answer:")  # With a customized prompt.
Answer: Apple
'Apple'

>>> cit.get_input("Continue?", default="yes")  # With a default answer.
| (?) Continue?
> (yes)  # Entered nothing
'yes'

>>> cit.get_input(strip=False)  # Do not remove leading and trailing whitespaces from user input.
>       # Whitespaces
'    '

>>> cit.get_choice(["Apple", "Google"])  # Enter number to select.
|  1) Apple
|  2) Google
> 2
'Google'

>>> cit.get_choice(["Apple", "Google"])  # Enter string is ok too.
|  1) Apple
|  2) Google
> Google
'Google'

>>> cit.get_choice(["Apple", "Google"], exitable=True)  # Add a choice of exit in menu.
|  1) Apple
|  2) Google
|  0) ** EXIT **
> 0
None

>>> cit.get_choices(["Apple", "Google"])  # Multiple Selection
|  1) [ ] Apple
|  2) [ ] Google
> 1  # Enter number to check or uncheck selections
|  1) [+] Apple
|  2) [ ] Google
|  0) ** DONE **
> Google  # Enter string is ok too.
|  1) [+] Apple
|  2) [+] Google
|  0) ** DONE **
> 0  # Enter 0 when done.
['Apple', 'Google']  # return [] is no selections.

>>> cit.get_choices(["Apple", "Google"], allable=True)  # Add a choice of select all in menu.
|  a) ** ALL **
|  1) [ ] Apple
|  2) [ ] Google
> a  # Enter `a` to check all. If `a` is in choices, enter `all`.
|  a) ** ALL **
|  1) [+] Apple
|  2) [+] Google
|  0) ** DONE **
> 0
['Apple', 'Google']

>>> cit.get_choices(["Apple", "Google"], exitable=True)  # Add a choice of exit in menu.
|  1) [ ] Apple
|  2) [ ] Google
|  0) ** EXIT **
> 0
[]  # Empty list returned.
```

## File IO

```python
>>> cit.read_file("/path/to/file")
'Hello World'

>>> cit.read_file("/path/to/file", with_encoding=True)
('Hello World', 'utf-8')

>>> cit.write_file("/path/to/file", "Hello World")  # Append content to file.
11  # writed bytes

>>> cit.write_file("/path/to/file", "Hello World", overwrite=True)  # Overwrite if file exists.
11  # writed bytes
```

## Controls

```python
>>> cit.pause()
| Press [Enter] to Continue...

>>> cit.bye()
# exit

>>> cit.bye(0)
# exit with code 0

>>> cit.bye("Seeya")
Seeya
# exit
```

## Decorators

```python
@cit.as_session("Hello")  # String as the Title of the session.
def my_func():
    cit.echo("World")

>>> my_func()
+---------+
| HELLO() |
+---------+
| World
`

@cit.as_session  # Use function name as the Title of the session.
def underscore_orCamel():
    pass

>>> underscore_orCamel()
+-----------------------+
| UNDERSCORE OR CAMEL() |
+-----------------------+
`

@cit.deprecated_by(new_func):  # A function object as argument.
def old_func(...):
    pass  # code here won't be actually executed.

>>> old_func(...)
Function `old_func` is deprecated, now calling `new_func` instead.  # Warning printed to stderr.
# new_func(...) is called
```
