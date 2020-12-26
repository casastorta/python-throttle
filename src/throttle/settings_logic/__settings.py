import logging
from queue import Empty as ExceptionEmpty
from queue import Queue


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

        self.__count_attempts: Queue = Queue()
        self.__concurrent_counter: Queue = Queue()

        self.__name: str = name
        self.__window_length: int = window_length
        self.__attempts: int = attempts
        self.__break_length: int = break_length

        logging.debug(
            f"ThrottleSettings.__init__: instanced with parameters: name({self.__name}), "
            f"window_length({self.__window_length}), attempts({self.__attempts}), "
            f"break_length({self.__break_length})"
        )

    def __del__(self):
        logging.debug(f"Throttle settings {self} destroyed")

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

    @property
    def count_attempts(self) -> int:
        return self.__count_attempts.qsize()

    def add_attempt(self) -> None:
        """
        We are locking adding attempts to avoid simoultaneous clear of the count attempts while adding
        """
        self.__count_attempts.put(True)
        logging.debug(f"ThrottleSettings.add_attempts: called, new attempts count: {self.count_attempts}")

    def remove_attempt(self) -> None:
        try:
            self.__count_attempts.get()
            logging.debug(f"ThrottleSettings.remove_attempt: called, new attempt count: {self.count_attempts}")
        except ExceptionEmpty:
            logging.error("ThrottleSettings.remove_attempt: hit ExceptionEmpty")

    def reset_attempts(self) -> None:
        logging.debug("ThrottleSettings.reset_attempts: called")
        self.__count_attempts = Queue()

    def add_concurrent(self) -> None:
        self.__concurrent_counter.put(True)
        logging.debug(f"ThrottleSettings.add_concurrent: called, new concurrent count: {self.count_concurrent}")

    def remove_concurrent(self) -> None:
        try:
            self.__concurrent_counter.get()
            logging.debug(f"ThrottleSettings.remove_concurrent: called, new concurrent count: {self.count_concurrent}")
        except ExceptionEmpty:
            logging.error("ThrottleSettings.remove_concurrent: hit ExceptionEmpty")

    def reset_concurrent(self) -> None:
        logging.debug(f"ThrottleSettings.reset_concurrent: called, had concurrent count of: {self.count_concurrent}")
        self.__concurrent_counter = Queue()

    @property
    def count_concurrent(self) -> int:
        return self.__concurrent_counter.qsize()
