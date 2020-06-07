from unittest import TestCase

import pytest
from throttle import throttle as th
from throttle.registry import DefaultRegistry, Registry, default_registry_name


class TestThrottle(TestCase):
    @staticmethod
    def helper_add_two_same_registries(registry_name: str, replace: bool) -> None:
        # Add first registry
        r: Registry = Registry(name=registry_name, window_length=1, attempts=2, break_length=3)
        th.add_registry(r)
        # Add second registry
        z: Registry = Registry(registry_name, window_length=4, attempts=5, break_length=6)
        th.add_registry(z, replace=replace)

    @staticmethod
    def helper_add_two_registries_some_and_other() -> None:
        r: Registry = Registry("some", 3, 4, 5)
        p: Registry = Registry("another", 1, 2, 3)
        th.add_registry(r)
        th.add_registry(p)

    @pytest.fixture(autouse=True)
    def setup(self):
        th.remove_all_registries()
        yield

    def test_get_default_registry(self):
        r: Registry = DefaultRegistry()
        th.add_registry(r)
        z: Registry = th.get_default_registry()
        assert r == z
        th.remove_registry(r.name)

    def test_add_default_registry_implicit(self):
        th.add_registry()
        r: Registry = th.get_registry(default_registry_name)
        z: Registry = th.get_default_registry()
        assert r == z

    def test_get_registry(self):
        r: Registry = Registry("abc", 4, 3, 2)
        th.add_registry(r)
        z: Registry = th.get_registry(r.name)
        assert r == z
        th.remove_registry(r.name)

    def test_add_registry(self):
        th.remove_all_registries()
        assert th.registries_evidence_length() == 0
        r: Registry = DefaultRegistry()
        th.add_registry(r)
        assert th.registries_evidence_length() == 1

    def test_add_two_registries(self):
        q: Registry = Registry("second", 1, 2, 3)
        th.add_registry()
        assert th.registries_evidence_length() == 1
        th.add_registry(q)
        assert th.registries_evidence_length() == 2

    def test_delete_registries(self):
        self.test_add_two_registries()
        assert th.registries_evidence_length() == 2
        th.remove_registry(th.get_default_registry().name)
        assert th.registries_evidence_length() == 1
        th.remove_registry("second")
        assert th.registries_evidence_length() == 0

    def test_adding_the_same_registry_name_not_replacing(self):
        # Prep work
        reg_name: str = "example"
        self.helper_add_two_same_registries(registry_name=reg_name, replace=False)
        # Length is still 1...
        assert th.registries_evidence_length() == 1
        # ...and it's still the first registry
        assert th.get_registry(reg_name).window_length == 1
        assert th.get_registry(reg_name).attempts == 2
        assert th.get_registry(reg_name).break_length == 3

    def test_adding_the_same_registry_name_replacing(self):
        # Prep work
        reg_name: str = "example"
        self.helper_add_two_same_registries(registry_name=reg_name, replace=True)
        # Length is still 1...
        assert th.registries_evidence_length() == 1
        # ...and it's second registry
        assert th.get_registry(reg_name).window_length == 4
        assert th.get_registry(reg_name).attempts == 5
        assert th.get_registry(reg_name).break_length == 6

    def test_delete_registry_from_empty_evidence(self):
        before: int = th.registries_evidence_length()
        th.remove_registry("random name")
        after: int = th.registries_evidence_length()
        assert before == 0 and after == 0

    def test_delete_registry_which_does_not_exist(self):
        # Add default registry
        th.add_registry()
        before: int = th.registries_evidence_length()
        th.remove_registry("random name")
        after: int = th.registries_evidence_length()
        assert before == 1 and after == 1

    def test_get_default_registry_with_no_default_registry_name(self):
        self.helper_add_two_registries_some_and_other()
        default_registry: Registry = th.get_default_registry()
        assert default_registry.name == "some"

    def test_get_default_registry_among_many(self):
        self.helper_add_two_registries_some_and_other()
        th.add_registry()
        default_registry: Registry = th.get_default_registry()
        assert default_registry.name == default_registry_name

    # Negative tests
    def test_retrieving_nonexisting_registry(self):
        with pytest.raises(KeyError):
            th.get_registry("random name")

    def test_get_default_registry_from_empty_evidence(self):
        with pytest.raises(ValueError):
            th.get_default_registry()
