# PyConsoleIOTools
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
| Session Name:

>>> cit.echo('Hello World')
| Hello World

>>> cit.echo('Hello World', pre='say', lvl=1)
| (Say)     Hello World

>>> cit.ask('Hello World')
| (?) Hello World

>>> cit.info('Hello World')
| (Info) Hello World

>>> cit.info('Hello World', lvl=2)
| (Info)         Hello World

>>> cit.warn('Hello World')
| (Warning) Hello World

>>> cit.err('Hello World')
| (Error) Hello World

>>> cit.end()
!

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

## Controls
```python
>>> cit.pause()
Press Enter to Continue...

>>> cit.bye()
# exit

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
| Hello:
| World
!
```
