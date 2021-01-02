import time

from demo.util import logging_setup

from . import r


def main():
    print(
        f"""
    The following demo should print throttled iterations of the iterative
    object for 21 times, {r.attempts} times within each {int(r.window_length/1000)} seconds separated with
    {int(r.break_length/1000)} seconds breaks.
    """
    )

    # Demo on throttling iterative functions
    @r.throttle
    def demo_iteration():
        for x in range(1, 22):
            yield x

    start_time = time.time()
    for num in demo_iteration():
        print(f"Iterating through iterative type: {num}, took {round(time.time() - start_time, 1)} seconds")
    r.destroy()


if __name__ == "__main__":
    logging_setup.set_up_logging()
    main()
