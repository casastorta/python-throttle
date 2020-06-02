from unittest import TestCase
from typing import Tuple
import pytest
from throttle.registry import Registry


class TestRegistryLogicHandler(TestCase, Registry):
    @pytest.fixture(autouse=True)
    def setup(self):
        if self.registry_instance:
            self.registry_instance = None
        self.registry_instance = Registry("Unit test registry", 1, 2, 3)
        yield

    def test_stop_or_go(self):
        timer_start, break_tiner_start, count_attempts = self._timer_start, self._break_timer_start, self._count_attempts
        assert timer_start is None

        assert True