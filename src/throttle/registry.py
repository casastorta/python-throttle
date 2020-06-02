from .registry_logic import __handle as rh

default_registry_name: str = "Default Registry"


class Registry(rh.Handle):
    """Interface class for Registry handling"""

    ...


__DefaultRegistrySettings: Registry = Registry(
    name=default_registry_name, window_length=6000, attempts=100, break_length=1000
)


def DefaultRegistry() -> Registry:
    return __DefaultRegistrySettings
