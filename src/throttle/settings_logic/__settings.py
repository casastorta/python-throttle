import logging


class ThrottleSettings:
    """Settings class for all registry related"""

    def __init__(self, name: str, window_length: int, attempts: int, break_length: int):
        """
        :param name:            Name of the registry
        :param window_length:   Time frame length (ms)
        :param attempts:        Attempts within time frame before throttle
        :param break_length:    Time which circuit breaker needs to stay open (ms)
        """

        if not all(isinstance(i, int) for i in [window_length, attempts, break_length]):
            raise ValueError("Registry settings for numerical parameters must be int's")

        if not all(abs(i) == i for i in [window_length, attempts, break_length]):
            raise ValueError("Registry settings for numerical parameters must be 0 or greater")

        self.__name: str = name
        self.__window_length: int = window_length
        self.__attempts: int = attempts
        self.__break_length: int = break_length

        logging.debug(
            f"ThrottleSettings instanced with parameters: name({self.__name}), "
            f"window_length({self.__window_length}), attempts({self.__attempts}), "
            f"break_length({self.__break_length})"
        )

    def __del__(self):
        logging.debug(f"Throttle settings of name {self.__name} destroyed")

    @property
    def name(self) -> str:
        return self.__name

    @property
    def window_length(self) -> int:
        return self.__window_length

    @property
    def attempts(self) -> int:
        return self.__attempts

    @property
    def break_length(self) -> int:
        return self.__break_length
