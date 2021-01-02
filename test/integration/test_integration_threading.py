import logging
import threading
import time
from unittest import TestCase

import pytest

from throttle import Settings


class ThreadingIntegrationTest(TestCase):

    attempts: int = 3
    window_length: int = 500
    break_length: int = 500

    @pytest.fixture(autouse=True)
    def setup(self):
        self.registry_instance: Settings = Settings(
            name=f"integration test registry for {self._testMethodName}",
            window_length=self.window_length,
            attempts=self.attempts,
            break_length=self.break_length,
        )
        yield
        self.registry_instance = None

    def helper_pass(self):
        pass

    def test_thread_overcount(self):
        @self.registry_instance.throttle
        def worker(num: int, start_time: int, end_times: list):
            logging.debug(f"Launching worker {num} started at {start_time}")
            time.sleep(0.02)
            pass
            end_time: int = time.time()
            duration: int = end_time - start_time
            end_times.append(round(duration, 3))
            logging.debug(f"Worker {num} ran for {duration}")

        threads: list = []
        end_times: list = []
        for i in range(22):
            start_time: int = time.time()
            t = threading.Thread(target=worker, args=(i, start_time, end_times))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        logging.debug(f"Thread end times: {end_times}")

        end_tuple = tuple(int(end_time) for end_time in end_times)
        del end_times

        assert end_tuple.count(0) == 3, "0 does not repeat 3 times"
        assert end_tuple.count(1) == 3, "1 does not repeat 3 times"
        assert end_tuple.count(2) == 3, "2 does not repeat 3 times"
        assert end_tuple.count(3) == 3, "3 does not repeat 3 times"
        assert end_tuple.count(4) == 3, "4 does not repeat 3 times"
        assert end_tuple.count(5) == 3, "5 does not repeat 3 times"
        assert end_tuple.count(6) == 3, "6 does not repeat 3 times"
        assert end_tuple.count(7) == 1, "7 does not repeat 1 time"

        assert len(end_tuple) == 22, "There have been different number than 22 tries"
