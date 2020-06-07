from .registry_logic import __handle as rh

default_registry_name: str = "Default Registry"


class Settings(rh.Handle):
    """Interface class for Settings handling"""
    ...


__DefaultThrottleSettings: Settings = Settings(
    name=default_registry_name, window_length=6000, attempts=100, break_length=1000
)


def DefaultSettings() -> Settings:
    return __DefaultThrottleSettings
