import logging
from typing import Dict, Optional, Set

from . import settings as rg

_settings_registry: Dict[str, rg.Settings] = {}
_settings_keys: Set[str] = set()


def registry_evidence_length() -> int:
    global _settings_keys
    return len(_settings_keys)


def add_settings(
    throttle_settings: Optional[rg.Settings] = None, name: Optional[str] = None, replace: bool = True,
) -> None:
    global _settings_registry, _settings_keys

    if not throttle_settings:
        throttle_settings = rg.DefaultSettings()

    settings_name: str = name if name else throttle_settings.name

    if settings_name in _settings_keys:
        if replace is False:
            logging.warning(f"Registry with the name {name} is already evidenced, you've asked not to replace")
            return

    _settings_registry[settings_name] = throttle_settings
    _settings_keys.add(settings_name)


def get_settings(name: str) -> rg.Settings:
    global _settings_registry, _settings_keys

    if name in _settings_keys:
        return _settings_registry[name]

    msg = f"Registry with the name {name} is not evidenced"
    logging.error(msg)
    raise KeyError(msg)


def remove_settings(name: str) -> None:
    global _settings_registry, _settings_keys

    if registry_evidence_length() == 0:
        logging.warning(f"Registry evidence is empty and request was to delete registry {name}, nothing to delete")
        return

    if name in _settings_keys:
        _settings_keys.remove(name)
        _settings_registry.pop(name)
    else:
        logging.warning(f"Registry with the name {name} is not evidenced, cannot remove")


def remove_all_settings() -> None:
    global _settings_registry, _settings_keys

    _settings_registry.clear()
    _settings_keys.clear()


def get_default_settings() -> rg.Settings:
    global _settings_registry, _settings_keys

    key: str

    if registry_evidence_length() == 0:
        msg = "No registries defined, cannot decide for default registry"
        logging.error(msg)
        raise ValueError(msg)

    if rg.default_registry_name in _settings_keys:
        key = rg.default_registry_name
    else:
        key = next(iter(_settings_registry))

    return get_settings(key)
