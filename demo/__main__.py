from demo.demos import (throttle_command, throttle_every, throttle_function,
                        throttle_iterative)
from demo.util.logging_setup import set_up_logging

set_up_logging()


def main():
    for module in (
        throttle_every,
        throttle_command,
        throttle_function,
        throttle_iterative,
    ):
        module.main()
        print(f"\n{'*'*76}\n")


if __name__ == "__main__":
    main()
