import time

from demo.demos import r
from demo.util import logging_setup


def main():
    print(
        f"""
    The following demo should print throttled iteration of the command 21
    times, {r.attempts} times within each {int(r.window_length/1000)} seconds separated with {int(r.break_length/1000)}
    seconds breaks.
    """
    )

    # Demo on throttling single commands
    # - put what you need into the explicit wrapper call
    start_time: float = time.time()
    for x in range(1, 22):
        r.throttle(print(f"Iterating through anything else: {x}, took {round(time.time() - start_time, 1)} seconds"))


if __name__ == "__main__":
    logging_setup.set_up_logging()
    main()
