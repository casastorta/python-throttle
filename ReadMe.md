[![Build Status](https://dev.azure.com/casastorta/vkrivokuca/_apis/build/status/casastorta.python-throttle?branchName=master)](https://dev.azure.com/casastorta/vkrivokuca/_build/latest?definitionId=1&branchName=develop)

# `Throttle` - Library to Throttle Anything

`Throttle` is a simple Python library for throttling... well, basically anything.

## How to use

Firstly, import `throttle.Settings` class and set up your own settings instance ("settings" is a settings
class instance for throttle functionality):

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

## Limitations

Library does not (can't?) really throttle iterations inside your functions. Please throttle singular actions inside
your iterative functionality.

## Future plans

See [to-do list here](doc/todo.md) list here
