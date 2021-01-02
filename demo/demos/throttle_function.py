import time

from demo.util import logging_setup

from . import r


def main():
    print(
        f"""
    The following demo should print throttled iteration of the function for 21
    times, {r.attempts} times within each {int(r.window_length/1000)} seconds separated with {int(r.break_length/1000)}
    seconds breaks.
    """
    )

    # Demo on throttling the iterations
    # - create the function first, which is decorated with throttle registry instance throttle wrapper
    @r.throttle
    def do_print(iteration: int):
        print(f"Iteration through function: {iteration}, took {round(time.time() - start_time, 1)} seconds")

    start_time: float = time.time()
    for x in range(1, 22):
        do_print(x)

    r.destroy()


if __name__ == "__main__":
    logging_setup.set_up_logging()
    main()
