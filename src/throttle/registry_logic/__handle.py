from functools import wraps
from collections.abc import Iterable
from time import sleep, time
from typing import Any, Callable, Optional, Set

from .__settings import RegistrySettings


class Handle(RegistrySettings):
    """Logic class for Registry functionality"""

    def __init__(self, *args, **kwargs):
        self.__timer_start: Optional[int] = None
        self.__break_timer_start: Optional[int] = None
        self.__count_attempts: int = 0

        super().__init__(*args, **kwargs)

    def throttle(self, func):
        @wraps(func)
        def wrapper_throttle(*args, **kwargs):

            args_repr = [repr(a) for a in args]  # 1
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
            signature = ", ".join(args_repr + kwargs_repr)  # 3
            print(f"Calling {func.__name__}({signature})")

            def __throttle_iterative():
                """Throttle call where func is iterative"""
                for r in func(*args, **kwargs):  # type: Any
                    yield r
                    self.__stop_or_go()

            self.__stop_or_go()
            b = func(*args, **kwargs)
            if b is not None:
                try:
                    iter(b)
                except TypeError:
                    return __throttle_iterative()
            return b

        if func is None:
            self.__stop_or_go()

        return wrapper_throttle

    def __stop_or_go(self) -> None:
        if not self._timer_start:
            # Nothing was happening yet, let's start fresh
            self._timer_start = self.__miliseconds(time())

        # Circuit breaker functionality
        current_militime: int = self.__miliseconds(time())

        # Check if we should be on hold still
        if self._break_timer_start:
            end_of_break: int = self._break_timer_start + self.break_length
            if current_militime <= end_of_break:
                new_break_len: int = end_of_break - current_militime
                sleep(new_break_len / 1000)
        new_militime: int = self.__miliseconds(time())

        # Check if we haven't broke count attempts for the window
        if self._count_attempts >= self.attempts:
            self._break_timer_start = new_militime
            sleep(self.break_length / 1000)

        # If we are outside of the window, reset count attempts and start of the window timer
        if (new_militime - self._timer_start) >= self.window_length:
            self._timer_start = None
            self._count_attempts = 0

        # We were allowed to run, so now we reset break timer start
        if self._break_timer_start:
            self._break_timer_start = None
        self._count_attempts += 1

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
    def _break_timer_start(self) -> Optional[int]:
        return self.__break_timer_start

    @_break_timer_start.setter
    def _break_timer_start(self, miliseconds: int) -> None:
        self.__break_timer_start = miliseconds

    @property
    def _count_attempts(self) -> int:
        return self.__count_attempts

    @_count_attempts.setter
    def _count_attempts(self, counter: int) -> None:
        self.__count_attempts = counter
