import logging
from functools import wraps
from threading import Semaphore
from time import sleep, time
from typing import Any, Callable, Iterable, Optional, Tuple, Union

from .__settings import ThrottleSettings


class Handle(ThrottleSettings):
    """Logic class for Registry functionality"""

    GO: bool = True
    HOLD: bool = False

    def __init__(self, *args, **kwargs):
        self.__semaphore: Semaphore = Semaphore()
        self.__timer_start: Optional[int] = None
        super().__init__(*args, **kwargs)

    def throttle(self, func: Callable):  # pragma: no cover
        def sleep_if_needed() -> None:
            self.__semaphore.acquire(blocking=True)
            __action, __length = self.stop_or_go()  # type: bool, float
            self.__semaphore.release()
            if __action == self.HOLD:
                logging.debug(
                    f"Handle.throttle.sleep_if_needed: sleeping for {__length} seconds because action is HOLD"
                )
                sleep(__length)
            # self.remove_concurrent()

        # We don't cover this in unit tests, but in integration tests. Hence no-cover
        @wraps(func)
        def wrapper_throttle(*args, **kwargs) -> Any:  # pragma: no cover
            def __throttle_iterative() -> Iterable[Any]:
                """Throttle call where func is iterative"""
                self.remove_attempt()
                for r in iter(b):
                    self.remove_concurrent()
                    yield r
                    sleep_if_needed()

            sleep_if_needed()
            b: Any = func(*args, **kwargs)

            if b is not None:
                try:
                    return __throttle_iterative()
                except TypeError:
                    self.remove_concurrent()
                    return b

            self.remove_concurrent()
            return b

        if func is None:
            sleep_if_needed()
            self.remove_concurrent()

        return wrapper_throttle

    def stop_or_go(self) -> Tuple[bool, Union[float, int]]:
        # Use this as base time
        current_mili: int = self.__miliseconds(time())

        # If window timer start not set, set it here now
        if not self.timer_start:
            self.timer_start = current_mili
            logging.debug(f"Handle.stop_or_go: Timer start set to {self.timer_start}")

        # Increase the usage counter
        self.add_attempt()
        logging.debug(f"Handle.stop_or_go: Increased count attempts to {self.count_attempts}")

        # Check if we are inside the valid window (curent militime - timer_start <= self.window_length)
        # if we are outside, reset the start time
        timer_start: int = self.timer_start if self.timer_start is not None else 0
        current_window: int = current_mili - timer_start
        if current_window > self.window_length:
            logging.debug(f"Handle.stop_or_go: Will reset the start time because of current window: {current_window}")
            self.timer_start = current_mili

        # Check if we didn't overuse (count attempts <= self.attempts)
        # If we are outside, set for hold
        if self.count_attempts > self.attempts:
            logging.debug(f"Handle.stop_or_go: Will signal hold because of count attempts: {self.count_attempts}")
            # - calculate hold time (remaining time for the window + self.break_length)
            negative_window: int = self.window_length - (current_mili - timer_start)
            hold_time: int = self.break_length + negative_window
            hold_time_seconds = hold_time / 1000 if hold_time > 0 else 0.0

            logging.debug(
                f"Handle.stop_or_go: Hold signaled. counter: {self.count_attempts}, hold_time: {hold_time}, "
                f"hold_time_seconds: {hold_time_seconds}, negative_window: {negative_window}"
            )
            time_due_queue: int = self.time_due_queue
            return self.HOLD, hold_time_seconds + (time_due_queue / 1000)

        if self.count_attempts == self.attempts:
            logging.debug(
                f"Handle.stop_or_go: count_attempts equals self.attempts ({self.count_attempts}={self.attempts}), "
                f"resetting attempts and timer."
            )
            # - reset counter, but to one - because if we've had to hold a call it happened in a new window
            #   (so next one will be no2)
            self.reset_attempts()
            # - unset timer start
            self.timer_start = None

            # Return if we are not running parallel tasks to throttle only
            if self.count_concurrent == 0:
                time_due_queue = self.time_due_queue
                negative_window = self.window_length - (current_mili - timer_start)
                hold_time = self.break_length + negative_window
                hold_time_seconds = hold_time / 1000 if hold_time > 0 else 0.0
                return self.HOLD, hold_time_seconds + (time_due_queue / 1000)

        # Get out
        sleep_due_queue: float = self.time_due_queue / 1000
        return self.GO if sleep_due_queue == 0.0 else self.HOLD, sleep_due_queue

    @staticmethod
    def __miliseconds(t: float) -> int:
        return int(round(t * 1000))

    @property
    def timer_start(self) -> Optional[int]:
        return self.__timer_start

    @timer_start.setter
    def timer_start(self, value: Union[int, None]) -> None:
        self.__timer_start = value

    @property
    def time_due_queue(self) -> int:
        # First calculate how many windows we have to break to do the queue
        concurrent_attempts: int = self.count_concurrent
        # We will need to count in the cooldown breaks we need to make
        self.add_concurrent()

        # If there is no concurrency in place, just return 0 (no queue for execution)
        if concurrent_attempts == 0:
            return 0

        allowed_attempts: int = self.attempts
        current_windows: int = int(concurrent_attempts / allowed_attempts)
        required_timeout: int = 0  # We will return this unless we've had current windows >0

        # So, windows to break times window length gives us intermediate time
        if current_windows > 0:
            required_timeout += current_windows * self.window_length
            cool_down_period_sum: int = current_windows * self.break_length
            required_timeout += cool_down_period_sum
            logging.debug(
                "throttle.settings.time_due_queue: "
                f"With concurrent_attempts={concurrent_attempts}, allowed_attempts={allowed_attempts}, "
                f"cool_down_period_sum={cool_down_period_sum} and current_windows={current_windows}, "
                f"required_timeout will be {required_timeout}"
            )
        else:
            logging.debug(
                "throttle.settings.time_due_queue: "
                f"With concurrent_attempts={concurrent_attempts} and allowed_attempts={allowed_attempts}, "
                f"hold time due queue will be 0"
            )

        return required_timeout
