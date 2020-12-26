import time
from time import sleep

from demo.util import logging_setup
from throttle.settings import Settings


def main():

    # Always throttle every request for 0.5 seconds
    ra: Settings = Settings(name="Always throttle", attempts=1, window_length=0, break_length=500)

    print(
        f"""
    The following demo should print 21 function calls each with {round(ra.break_length/1000, 1)} seconds
    break in between
    """
    )

    @ra.throttle
    def demo_iteration():
        for x in range(1, 22):
            sleep(0.1)
            yield x

    start_time: float = time.time()
    for num in demo_iteration():
        print(f"Always throttling 0.5 seconds: {num}, took {round(time.time() - start_time, 1)} seconds")


if __name__ == "__main__":
    logging_setup.set_up_logging()
    main()
