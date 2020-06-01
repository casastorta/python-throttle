import logging
from typing import Dict, Optional, Set

from . import registry as rg

_registries: Dict[str, rg.Registry] = {}
_registries_keys: Set[str] = set()


def registries_evidence_length() -> int:
    global _registries_keys
    return len(_registries_keys)


def add_registry(
    registry_settings: Optional[rg.Registry] = None, name: Optional[str] = None, replace: bool = True,
) -> None:
    global _registries, _registries_keys

    if not registry_settings:
        registry_settings = rg.DefaultRegistry()

    registry_name: str = name if name else registry_settings.name

    if registry_name in _registries_keys:
        if replace is False:
            logging.warning(f"Registry with the name {name} is already evidenced, you've asked not to replace")
            return

    _registries[registry_name] = registry_settings
    _registries_keys.add(registry_name)


def get_registry(name: str) -> rg.Registry:
    global _registries, _registries_keys

    if name in _registries_keys:
        return _registries[name]

    msg = f"Registry with the name {name} is not evidenced"
    logging.error(msg)
    raise KeyError(msg)


def remove_registry(name: str) -> None:
    global _registries, _registries_keys

    if registries_evidence_length() == 0:
        logging.warning(f"Registry evidence is empty and request was to delete registry {name}, nothing to delete")
        return

    if name in _registries_keys:
        _registries_keys.remove(name)
        _registries.pop(name)
    else:
        logging.warning(f"Registry with the name {name} is not evidenced, cannot remove")


def remove_all_registries() -> None:
    global _registries, _registries_keys

    _registries.clear()
    _registries_keys.clear()


def get_default_registry() -> rg.Registry:
    global _registries, _registries_keys

    key: str

    if registries_evidence_length() == 0:
        msg = "No registries defined, cannot decide for default registry"
        logging.error(msg)
        raise ValueError(msg)

    if rg.default_registry_name in _registries_keys:
        key = rg.default_registry_name
    else:
        key = next(iter(_registries))

    return get_registry(key)
