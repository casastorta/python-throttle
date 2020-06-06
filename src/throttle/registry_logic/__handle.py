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
        self.__break_timer_start: Optional[int] = None
        self.__count_attempts: int = 0
        super().__init__(*args, **kwargs)

    def throttle(self, func: Callable):
        @wraps(func)
        def wrapper_throttle(*args, **kwargs) -> Any:
            def __throttle_iterative() -> Iterable[Any]:
                """Throttle call where func is iterative"""
                for r in func(*args, **kwargs):
                    yield r
                    sleep_if_needed()

            sleep_if_needed()
            b = func(*args, **kwargs)
            if b is not None:
                try:
                    iter(b)
                except TypeError:
                    return __throttle_iterative()
            return b

        def sleep_if_needed() -> None:
            __action, __length = self.__stop_or_go()  # type: bool, float
            if __action == self.HOLD:
                sleep(__length)

        if func is None:
            sleep_if_needed()

        return wrapper_throttle

    def __stop_or_go(self) -> Tuple[bool, Union[float, int]]:
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
                hold_time: float = new_break_len / 1000
                return self.HOLD, hold_time
        new_militime: int = self.__miliseconds(time())

        # Check if we haven't broke count attempts for the window
        if self._count_attempts >= self.attempts:
            self._break_timer_start = new_militime
            _hold_time: float = self.break_length / 1000
            return self.HOLD, _hold_time

        # If we are outside of the window, reset count attempts and start of the window timer
        if (new_militime - self._timer_start) >= self.window_length:
            self._timer_start = None
            self._count_attempts = 0

        # We were allowed to run, so now we reset break timer start
        if self._break_timer_start:
            self._break_timer_start = None
        self._count_attempts += 1

        return self.GO, 0

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
