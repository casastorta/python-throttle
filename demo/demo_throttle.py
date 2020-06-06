import os
import sys


def main():
    from throttle import Registry

    r: Registry = Registry(name="demo registry", window_length=5000, attempts=5, break_length=2000)

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


if __name__ == "__main__":
    print(os.getcwd())
    sys.path.append(os.path.abspath(os.getcwd() + os.sep + "src"))
    main()
