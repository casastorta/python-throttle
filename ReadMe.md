# `Throttle` - Library to Throttle Anything

`Throttle` is a simple Python library for throttling... well, basically anything.

## How to use

Firstly, import `throttle.Registry` class and set up your own registry ("registry" is a settings
class instance for throttle functionality):

```python
from throttle import Settings

r: Settings = Settings(name="demo registry", window_length=10, attempts=3, break_length=2000)
```

### Throttle any function

Throttle any function by decorating it with `@throttle` wrapper of your registry instance:

```python
@r.throttle
def do_print(iteration):
    print(f"Iteration through function: {iteration}")

for x in range(1, 21):
    do_print(x)
```

### Or throttle just about anything else

Wrap anything inside a call for a `throttle` function of your registry instance:

```python
for x in range(1, 21):
    r.throttle(print(f"Iterating through anything else: {x}"))
```

## Limitations

We don't (can't?) really throttle iterations inside your functions. Please eiter throttle singular actions inside
your iterative functionality.

## Future plans

See [to-do list here](doc/todo.md) list here
