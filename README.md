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
cit.start()
cit.title('Session Name')
cit.echo('Hello World')
cit.echo('Hello World', pre='Welcome', lvl=1)
cit.info('Hello World')
cit.info('Hello World', lvl=2)
cit.warn('Hello World')
cit.err('Hello World')
cit.end()
```

## Get User Input
```python
userinput = cit.get_input()
userchoice = cit.get_choice(['Apple', 'Google'])
```

## Controls
```python
cit.pause()
cit.bye()
cit.bye('Seeya')
```

## Decorators
```python
@cit.as_session('Session Name')
def my_func():
    do_stuff()
```
