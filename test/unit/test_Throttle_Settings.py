from unittest import TestCase

import pytest
from throttle.settings import DefaultSettings, Settings, default_registry_name


class TestSettings(TestCase):
    def test_default_builtin_settings(self):
        r: Settings = DefaultSettings()
        assert r.name == default_registry_name

    def test_full_init(self):
        r: Settings = Settings(name="abc", window_length=1, attempts=2, break_length=3)
        assert r.name == "abc"
        assert r.window_length == 1
        assert r.attempts == 2
        assert r.break_length == 3

    # Negative tests
    def test_empty_init(self):
        with pytest.raises(TypeError):
            r: Settings = Settings()
            del r

    def test_invalid_type_length(self):
        with pytest.raises(ValueError):
            r: Settings = Settings(
                name="abc", window_length="z", attempts=2, break_length=3
            )
            del r

    def test_negative_param_length(self):
        with pytest.raises(ValueError):
            r: Settings = Settings(
                name="abc", window_length=-3, attempts=2, break_length=3
            )
            del r

    def test_invalid_type_attempts(self):
        with pytest.raises(ValueError):
            r: Settings = Settings(
                name="abc", window_length=1, attempts="z", break_length=3
            )
            del r

    def test_negative_param_attempts(self):
        with pytest.raises(ValueError):
            r: Settings = Settings(
                name="abc", window_length=1, attempts=-2, break_length=3
            )
            del r

    def test_invalid_type_break_length(self):
        with pytest.raises(ValueError):
            r: Settings = Settings(
                name="abc", window_length=1, attempts=2, break_length="z"
            )
            del r

    def test_negative_break_length(self):
        with pytest.raises(ValueError):
            r: Settings = Settings(
                name="abc", window_length=1, attempts=2, break_length=-1
            )
            del r
