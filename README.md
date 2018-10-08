# PyConsoleIOTools
[![Build Status](https://travis-ci.org/kyan001/PyConsoleIOTools.svg?branch=master)](https://travis-ci.org/kyan001/PyConsoleIOTools)

## Installation
```
pip install consoleiotools
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

>>> cit.get_choice(['Apple', 'Google'])
|  1) Apple
|  2) Google
> 2
'Google'

>>> cit.get_choice(['Apple', 'Google'])
|  1) Apple
|  2) Google
> Google
'Google'
```

## File IO
```python
>>> cit.read_file('/path/to/file')
'File contents'

>>> cit.read_file('/path/to/file', with_encoding=True)
('File contents', 'utf-8')

>>> cit.write_file('/path/to/file', "Contents")
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
