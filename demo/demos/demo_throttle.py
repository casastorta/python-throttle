from time import sleep


def main():
    from throttle import Settings

    r: Settings = Settings(name="demo registry", window_length=5000, attempts=5, break_length=2000)

    # Demo on throttling the iterations
    # - create the function first, which is decorated with throttle registry instance throttle wrapper
    @r.throttle
    def do_print(iteration):
        print(f"Iteration through function: {iteration}")

    for x in range(1, 21):
        do_print(x)

    print("*" * 78)

    # Demo on throttling single commands
    # - put what you need into the explicit wrapper call
    for x in range(1, 21):
        r.throttle(print(f"Iterating through anything else: {x}"))

    print("*" * 78)

    # Demo on throttling iterative functions
    @r.throttle
    def demo_iteration():
        for x in range(1, 21):
            yield x

    for num in demo_iteration():
        print(f"Iterating through iterative type: {num}")

    print("*" * 78)

    # Always throttle every request for 0.5 seconds
    ra: Settings = Settings(name="Always throttle", attempts=1, window_length=0, break_length=500)

    @ra.throttle
    def demo_iteration():
        for x in range(1, 21):
            sleep(0.1)
            yield x

    for num in demo_iteration():
        print(f"Always throttling 0.5 seconds: {num}")
