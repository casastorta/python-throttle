from typing import Optional
from unittest import TestCase

import pytest
from throttle.registry import Registry


class TestRegistryLogicHandler(TestCase):

    WINDOWS_LENGTH: int = 20000
    BREAK_LENGTH: int = 30000

    @pytest.fixture(autouse=True)
    def setup(self):
        self.registry_instance: Optional[Registry]
        self.registry_instance = Registry(
            "Unit test registry", attempts=3, window_length=self.WINDOWS_LENGTH, break_length=self.BREAK_LENGTH
        )
        yield
        self.registry_instance = None

    def test_stop_or_go_initialization(self):
        assert self.registry_instance._timer_start is None
        assert self.registry_instance._break_timer_start is None
        assert self.registry_instance._count_attempts == 0

    def test_stop_or_go_attempts_count_one(self):
        go_nogo, wait_time = self.registry_instance.stop_or_go()  # type: bool, float
        assert self.registry_instance._timer_start is not None
        assert self.registry_instance._break_timer_start is None
        assert self.registry_instance._count_attempts == 1
        assert go_nogo == self.registry_instance.GO
        assert wait_time == 0.0

    def test_stop_or_go_attempts_count_2(self):
        go_nogo: Optional[bool] = None
        wait_time: Optional[float] = None
        for i in range(1, 3):
            go_nogo, wait_time = self.registry_instance.stop_or_go()

        assert go_nogo == self.registry_instance.GO
        assert wait_time == 0.0

        assert self.registry_instance._timer_start is not None
        assert self.registry_instance._break_timer_start is None
        assert self.registry_instance._count_attempts == 2

    def test_stop_or_go_attempts_count_hit_attempts_limit(self):
        go_nogo: Optional[bool] = None
        wait_time: Optional[float] = None
        for i in range(1, 5):
            go_nogo, wait_time = self.registry_instance.stop_or_go()

        assert go_nogo == self.registry_instance.HOLD
        assert wait_time > 0 and wait_time < self.BREAK_LENGTH

        assert self.registry_instance._timer_start is not None
        assert self.registry_instance._break_timer_start is not None
        assert self.registry_instance._count_attempts == 4

    def test_stop_or_go_break_length_expiry(self):
        r: Registry = Registry("break length breaker", attempts=1, window_length=1, break_length=0)
        go_nogo: Optional[bool] = None
        wait_time: Optional[float] = None
        for i in range(1, 3):
            go_nogo, wait_time = r.stop_or_go()

        assert go_nogo == r.GO
        assert wait_time == 0 or wait_time == 1
