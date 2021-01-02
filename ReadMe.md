[![Build Status](https://dev.azure.com/casastorta/vkrivokuca/_apis/build/status/casastorta.python-throttle?branchName=master)](https://dev.azure.com/casastorta/vkrivokuca/_build/latest?definitionId=1&branchName=develop)

# `Throttle` - Library to Throttle Anything

`Throttle` is a simple Python library for throttling... well, basically anything.

Library can throttle your plain old functions and iterative implementations too. It knows how to handle multithreaded
logic.

## How to use

Firstly, import `throttle.Settings` class and set up your own settings instance ("settings" is a settings class instance
for throttle functionality):

```python
from throttle import Settings

ts: Settings = Settings(name="demo settings", window_length=10, attempts=3, break_length=2000)
```

### Throttle any function

Throttle any function by decorating it with `@throttle` wrapper of your registry instance:

```python
@ts.throttle
def do_print(iteration):
    print(f"Iteration through function: {iteration}")


for x in range(1, 21):
    do_print(x)
```

### Or throttle just about anything else

Wrap anything inside a call for a `throttle` function of your registry instance:

```python
for x in range(1, 21):
    ts.throttle(print(f"Iterating through anything else: {x}"))
```

## Gotchas

### Throttling (all members of) whole classes

You cannot simply decorate the whole `class` and expect for all the members to be throttled. While this as an
implementation did cross my mind, I could not think of a well-designed use-case which would benefit from this.

### Throttling `multiprocessing`

While this library supports throttling multithreaded logic, it does not supprot multiprocessing one (meaning: threading
is supported, `fork()` is not).

## Future plans

See [to-do list here](doc/todo.md) list here
