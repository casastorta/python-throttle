from time import sleep, time
from typing import Callable, Optional

from .__settings import RegistrySettings


class Handle(RegistrySettings):
    """Logic class for Registry functionality"""

    def __init__(self, *args, **kwargs):
        self.__var_timer_start: Optional[int] = None
        self.__var_break_timer_start: Optional[int] = None
        self.__var_count_attempts: int = 0

        super().__init__(*args, **kwargs)

    def throttle(self, func: Optional[Callable]) -> Optional[Callable]:
        def wrapper(*args, **kwargs):
            self.__should_i_stay_or_should_i_go()
            func(*args, **kwargs)

        if func is None:
            self.__should_i_stay_or_should_i_go()

        return wrapper

    def __should_i_stay_or_should_i_go(self):
        if not self.__timer_start:
            # Nothing was happening yet, let's start fresh
            self.__timer_start = self.__miliseconds(time())
        # Circuit breaker functionality
        if self.__count_attempts >= self.attempts:
            sleep(self.break_length / 1000)
        current_militime: int = self.__miliseconds(time())
        if current_militime - self.__timer_start >= self.window_length:
            self.__timer_start = None
            self.__count_attempts = 0
        self.__count_attempts += 1

    @staticmethod
    def __miliseconds(t: float) -> int:
        return int(round(t * 1000))

    @property
    def __timer_start(self) -> Optional[int]:
        return self.__var_timer_start

    @__timer_start.setter
    def __timer_start(self, miliseconds: int) -> None:
        self.__var_timer_start = miliseconds

    @property
    def __break_timer_start(self) -> Optional[int]:
        return self.__var_break_timer_start

    @__break_timer_start.setter
    def __break_timer_start(self, miliseconds: int) -> None:
        self.__var_break_timer_start = miliseconds

    @property
    def __count_attempts(self) -> int:
        return self.__var_count_attempts

    @__count_attempts.setter
    def __count_attempts(self, counter: int) -> None:
        self.__var_count_attempts = counter
