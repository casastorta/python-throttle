import logging
from functools import wraps
from time import sleep, time
from typing import Any, Callable, Iterable, Optional, Tuple, Union

from .__settings import RegistrySettings


class Handle(RegistrySettings):
    """Logic class for Registry functionality"""

    GO = True
    HOLD = False

    def __init__(self, *args, **kwargs):
        self.__timer_start: Optional[int] = None
        self.__count_attempts: int = 0
        super().__init__(*args, **kwargs)

    def throttle(self, func: Callable):  # pragma: no cover
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
                    return __throttle_iterative()
            return b

        def sleep_if_needed() -> None:
            __action, __length = self.stop_or_go()  # type: bool, float
            if __action == self.HOLD:
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

        # Increase the usage counter
        self.__count_attempts = self.__count_attempts + 1

        # Check if we didn't overuse (count attempts <= self.attempts)
        # If we are outside, set for hold
        if self.__count_attempts > self.attempts:
            logging.debug(f"Will signal hold because of count attempts: {self.__count_attempts}")
            go_or_hold = self.HOLD

        # Check if we are inside the valid window (curent militime - timer_start <= self.window_length)
        # if we are outside, set for hold!
        current_window: int = current_mili - self.__timer_start
        if current_window > self.window_length:
            logging.debug(f"Will signal hold because of current window: {current_window}")
            go_or_hold = self.HOLD

        # If we need to hold:
        if go_or_hold == self.HOLD:
            # - calculate hold time (remaining time for the window + self.break_length)
            negative_window: int = current_mili - self.__timer_start
            hold_time: int = self.break_length + negative_window
            hold_time_seconds = hold_time / 1000 if hold_time > 0 else 0.0

            logging.debug(
                f"Hold signaled. counter: {self.__count_attempts}, hold_time: {hold_time_seconds}, "
                f"negative_window: {negative_window}"
            )

            # - reset counter
            self.__count_attempts = 1
            # - unset timer start
            self.__timer_start = None

        # Get out
        return go_or_hold, hold_time_seconds

    @staticmethod
    def __miliseconds(t: float) -> int:
        return int(round(t * 1000))

    @property
    def _timer_start(self) -> Optional[int]:
        return self.__timer_start

    @_timer_start.setter
    def _timer_start(self, miliseconds: int) -> None:
        self.__timer_start = miliseconds

    @property
    def _count_attempts(self) -> int:
        return self.__count_attempts

    @_count_attempts.setter
    def _count_attempts(self, counter: int) -> None:
        self.__count_attempts = counter
