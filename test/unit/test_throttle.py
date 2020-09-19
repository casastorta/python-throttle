from unittest import TestCase

import pytest
from throttle import throttle as th
from throttle.settings import DefaultSettings, Settings, default_registry_name


class TestThrottle(TestCase):
    @staticmethod
    def helper_add_two_same_settings(registry_name: str, replace: bool) -> None:
        # Add first registry
        r: Settings = Settings(
            name=registry_name, window_length=1, attempts=2, break_length=3
        )
        th.add_settings(r)
        # Add second registry
        z: Settings = Settings(
            registry_name, window_length=4, attempts=5, break_length=6
        )
        th.add_settings(z, replace=replace)

    @staticmethod
    def helper_add_two_settings_some_and_other() -> None:
        r: Settings = Settings("some", 3, 4, 5)
        p: Settings = Settings("another", 1, 2, 3)
        th.add_settings(r)
        th.add_settings(p)

    @pytest.fixture(autouse=True)
    def setup(self):
        th.remove_all_settings()
        yield

    def test_get_default_settings(self):
        r: Settings = DefaultSettings()
        th.add_settings(r)
        z: Settings = th.get_default_settings()
        assert r == z
        th.remove_settings(r.name)

    def test_add_default_settings_implicit(self):
        th.add_settings()
        r: Settings = th.get_settings(default_registry_name)
        z: Settings = th.get_default_settings()
        assert r == z

    def test_get_settings(self):
        r: Settings = Settings("abc", 4, 3, 2)
        th.add_settings(r)
        z: Settings = th.get_settings(r.name)
        assert r == z
        th.remove_settings(r.name)

    def test_add_settings(self):
        th.remove_all_settings()
        assert th.registry_evidence_length() == 0
        r: Settings = DefaultSettings()
        th.add_settings(r)
        assert th.registry_evidence_length() == 1

    def test_add_two_settings(self):
        q: Settings = Settings("second", 1, 2, 3)
        th.add_settings()
        assert th.registry_evidence_length() == 1
        th.add_settings(q)
        assert th.registry_evidence_length() == 2

    def test_delete_settings(self):
        self.test_add_two_settings()
        assert th.registry_evidence_length() == 2
        th.remove_settings(th.get_default_settings().name)
        assert th.registry_evidence_length() == 1
        th.remove_settings("second")
        assert th.registry_evidence_length() == 0

    def test_adding_the_same_settings_name_not_replacing(self):
        # Prep work
        reg_name: str = "example"
        self.helper_add_two_same_settings(registry_name=reg_name, replace=False)
        # Length is still 1...
        assert th.registry_evidence_length() == 1
        # ...and it's still the first registry
        assert th.get_settings(reg_name).window_length == 1
        assert th.get_settings(reg_name).attempts == 2
        assert th.get_settings(reg_name).break_length == 3

    def test_adding_the_same_settings_name_replacing(self):
        # Prep work
        reg_name: str = "example"
        self.helper_add_two_same_settings(registry_name=reg_name, replace=True)
        # Length is still 1...
        assert th.registry_evidence_length() == 1
        # ...and it's second registry
        assert th.get_settings(reg_name).window_length == 4
        assert th.get_settings(reg_name).attempts == 5
        assert th.get_settings(reg_name).break_length == 6

    def test_delete_settings_from_empty_evidence(self):
        before: int = th.registry_evidence_length()
        th.remove_settings("random name")
        after: int = th.registry_evidence_length()
        assert before == 0 and after == 0

    def test_delete_settings_which_does_not_exist(self):
        # Add default registry
        th.add_settings()
        before: int = th.registry_evidence_length()
        th.remove_settings("random name")
        after: int = th.registry_evidence_length()
        assert before == 1 and after == 1

    def test_get_default_settings_with_no_default_settings_name(self):
        self.helper_add_two_settings_some_and_other()
        default_registry: Settings = th.get_default_settings()
        assert default_registry.name == "some"

    def test_get_default_settings_among_many(self):
        self.helper_add_two_settings_some_and_other()
        th.add_settings()
        default_registry: Settings = th.get_default_settings()
        assert default_registry.name == default_registry_name

    # Negative tests
    def test_retrieving_nonexisting_settings(self):
        with pytest.raises(KeyError):
            th.get_settings("random name")

    def test_get_default_settings_from_empty_evidence(self):
        with pytest.raises(ValueError):
            th.get_default_settings()
