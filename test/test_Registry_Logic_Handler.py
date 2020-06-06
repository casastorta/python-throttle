from typing import Optional
from unittest import TestCase

import pytest
from throttle.registry import Registry


class TestRegistryLogicHandler(TestCase):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.registry_instance: Optional[Registry]
        self.registry_instance = Registry("Unit test registry", 1, 2, 3)
        yield

    def test_stop_or_go(self):
        assert self.registry_instance._timer_start is None
        assert self.registry_instance._break_timer_start is None
        assert self.registry_instance._count_attempts == 0

        self.registry_instance.throttle(lambda: True)

        # assert self.registry_instance._timer_start is not None
        # assert self.registry_instance._break_timer_start is not None
        # assert self.registry_instance._count_attempts == 1
