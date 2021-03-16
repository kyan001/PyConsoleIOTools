# PyConsoleIOTools
[![Build Status](https://travis-ci.org/kyan001/PyConsoleIOTools.svg?branch=master)](https://travis-ci.org/kyan001/PyConsoleIOTools)
![PyPI - Downloads](https://img.shields.io/pypi/dm/consoleiotools.svg)
![GitHub release](https://img.shields.io/github/release/kyan001/PyConsoleIOTools.svg)
[![GitHub license](https://img.shields.io/github/license/kyan001/PyConsoleIOTools.svg)](https://github.com/kyan001/PyConsoleIOTools/blob/master/LICENSE)

## Installation

```sh
pip install consoleiotools  # install
pip install --upgrade consoleiotools  # update
```

## Get Started

```python
import consoleiotools as cit
print(cit.__version__)
```

## Prints on Screen

```python
>>> cit.start()
*

>>> cit.title('Session Name')
| __SESSION NAME__________________________

>>> cit.echo('Hello World')
| Hello World

>>> cit.echo('Hello World', pre='say')
| (Say) Hello World

>>> cit.ask('Hello World')
| (?) Hello World

>>> cit.info('Hello World')
| (Info) Hello World

>>> cit.warn('Hello World')
| (Warning) Hello World

>>> cit.err('Hello World')
| (Error) Hello World

>>> cit.dim('Hello World')
| Hello World  # gray

>>> cit.end()
`

>>> cit.br()
# blank line

>>> cit.br(2)
# blank line
# blank line
```

## Get User Input

```python
>>> cit.get_input()
> Hello World
'Hello World'

>>> cit.get_choice(['Apple', 'Google'])  # Enter number to select.
|  1) Apple
|  2) Google
> 2
'Google'

>>> cit.get_choice(['Apple', 'Google'])  # Enter string is ok too.
|  1) Apple
|  2) Google
> Google
'Google'

>>> cit.get_choice(['Apple', 'Google'], exitable=True)  # Add a choice of exit in menu.
|  0) ** EXIT **
|  1) Apple
|  2) Google
> 0
None

>>> cit.get_choices(['Apple', 'Google'])  # Multiple Selection
|  0) ** EXIT **
|  1) [ ] Apple
|  2) [ ] Google
> 1  # Enter number to check or uncheck selections
|  0) ** DONE **
|  1) [+] Apple
|  2) [ ] Google
> Google  # Enter string is ok too.
|  0) ** DONE **
|  1) [+] Apple
|  2) [+] Google
> 0  # Enter 0 when done.
['Apple', 'Google']  # return [] is no selections.

>>> cit.get_choices(['Apple', 'Google'], allable=True)  # Add a choice of select all in menu.
|  0) ** EXIT **
|  1) [ ] Apple
|  2) [ ] Google
|  a) ** ALL **
> a  # Enter `a` to check all. If `a` is in choices, enter `all`.
|  0) ** DONE **
|  1) [+] Apple
|  2) [+] Google
|  a) ** ALL **
> 0
['Apple', 'Google']
```

## File IO

```python
>>> cit.read_file('/path/to/file')
'File contents'

>>> cit.read_file('/path/to/file', with_encoding=True)
('File contents', 'utf-8')

>>> cit.write_file('/path/to/file', 'Contents')  # Append content to file.
8  # writed bytes

>>> cit.write_file('/path/to/file', 'Contents', overwrite=True)  # Overwrite if file exists.
8  # writed bytes
```

## Controls

```python
>>> cit.pause()
Press Enter to Continue...

>>> cit.bye()
# exit

>>> cit.bye(0)
# exit with code 0

>>> cit.bye('Seeya')
Seeya
# exit
```

## Decorators

```python
@cit.as_session('Hello')
def my_func():
    cit.echo('World')

>>> my_func()
*
| __HELLO__________________________
| World
`

@cit.as_session
def underscore_orCamel():
    pass

>>> underscore_orCamel()
*
| __UNDERSCORE OR CAMEL__________________________
`
```
