import datetime
import time
from unittest import TestCase

import pytest

from throttle import Settings


class IntegrationTest(TestCase):

    attempts: int = 5
    window_length: int = 1000
    break_length: int = 500

    @pytest.fixture(autouse=True)
    def setup(self):
        self.registry_instance: Settings = Settings(
            name="integration test registry",
            window_length=self.window_length,
            attempts=self.attempts,
            break_length=self.break_length,
        )
        yield
        self.registry_instance = None

    def helper_pass(self):
        pass

    def test_naive_within_limits(self):
        start_timer: float = time.time()
        for i in range(self.attempts):
            self.registry_instance.throttle(self.helper_pass())
            current_timer: float = time.time()
            diff = current_timer - start_timer
            """
            Passing this every time means we've managed to execute pass helper self.attempt times and didn't
            cross the self.window_length period
            """
            assert diff < self.window_length

    def test_naive_cross_attempts(self):
        start_timer: float = time.time()
        for i in range(self.attempts + 1):
            self.registry_instance.throttle(self.helper_pass())

        current_timer: float = time.time()
        diff = (current_timer - start_timer) * 1000

        """
        Execution time of self.attempts+1 of pass helper being equal or larger than self.attempts+self.break_length
        times means that the throttle block got activated
        """
        assert diff >= (self.window_length + self.break_length)
