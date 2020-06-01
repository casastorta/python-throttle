from throttle.registry import Registry

TwitterStandard: Registry = Registry(name="TwitterStandard", window_length=900000, attempts=15, break_length=0)
