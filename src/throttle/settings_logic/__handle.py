import logging
from functools import wraps
from time import sleep, time
from typing import Any, Callable, Iterable, Optional, Tuple, Union

from .__settings import ThrottleSettings


class Handle(ThrottleSettings):
    """Logic class for Registry functionality"""

    GO: bool = True
    HOLD: bool = False

    def __init__(self, *args, **kwargs):
        self.__timer_start: Optional[int] = None
        self.__count_attempts: list = []
        super().__init__(*args, **kwargs)

    def throttle(self, func: Callable):  # pragma: no cover
        # We don't cover this in unit tests, but in integration tests. Hence no-cover

        @wraps(func)
        def wrapper_throttle(*args, **kwargs) -> Any:
            def __throttle_iterative() -> Iterable[Any]:
                """Throttle call where func is iterative"""
                for r in b:
                    sleep_if_needed()
                    yield r

            sleep_if_needed()
            b = func(*args, **kwargs)

            if b is not None:
                try:
                    iter(b)
                except TypeError:
                    return b
                else:
                    # yield step
                    return __throttle_iterative()
            return b

        def sleep_if_needed() -> None:
            __action, __length = self.stop_or_go()  # type: bool, float
            if __action == self.HOLD:
                logging.debug(f"Sleeping for {__length} seconds because action is HOLD")
                sleep(__length)

        if func is None:
            sleep_if_needed()

        return wrapper_throttle

    def stop_or_go(self) -> Tuple[bool, Union[float, int]]:
        go_or_hold: bool = self.GO
        hold_time_seconds: float = 0.0

        # Use this as base time
        current_mili: int = self.__miliseconds(time())

        # If window timer start not set, set it here now
        if not self.__timer_start:
            self.__timer_start = current_mili
            logging.debug(f"Timer start set to {self.__timer_start}")

        # Increase the usage counter
        self.__count_attempts.append(True)
        logging.debug(f"Increased count attempts to {self.count_attempts}")

        # Check if we didn't overuse (count attempts <= self.attempts)
        # If we are outside, set for hold
        if self.count_attempts > self.attempts:
            logging.debug(f"Will signal hold because of count attempts: {self.count_attempts}")
            go_or_hold = self.HOLD

        # Check if we are inside the valid window (curent militime - timer_start <= self.window_length)
        # if we are outside, reset the start time
        current_window: int = current_mili - self.__timer_start
        if current_window > self.window_length:
            logging.debug(f"Will reset the start time because of current window: {current_window}")
            self.__timer_start = current_mili

        # If we need to hold:
        if go_or_hold == self.HOLD:
            # - calculate hold time (remaining time for the window + self.break_length)
            negative_window: int = self.window_length - (current_mili - self.__timer_start)
            hold_time: int = self.break_length + negative_window
            hold_time_seconds = hold_time / 1000 if hold_time > 0 else 0.0

            logging.debug(
                f"Hold signaled. counter: {self.count_attempts}, hold_time: {hold_time}, "
                f"hold_time_seconds: {hold_time_seconds}, negative_window: {negative_window}"
            )

            # - reset counter, but to one - because if we've had to hold a call it happened in a new window
            #   (so next one will be no2)
            self.__count_attempts.clear()
            self.__count_attempts.append(True)
            # - unset timer start
            self.__timer_start = None

        # Get out
        return go_or_hold, hold_time_seconds

    @staticmethod
    def __miliseconds(t: float) -> int:
        return int(round(t * 1000))

    @property
    def timer_start(self) -> Optional[int]:
        return self.__timer_start

    @property
    def count_attempts(self) -> int:
        return len(self.__count_attempts)
