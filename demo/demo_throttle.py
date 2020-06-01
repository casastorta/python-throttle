import os
import sys


def main():
    from throttle import Registry

    r: Registry = Registry(name="demo registry", window_length=10, attempts=3, break_length=2000)

    # Demo on throttling the iterations
    # - create the function first, which is decorated with throttle registry instance throttle wrapper

    @r.throttle
    def do_print(iteration):
        print(f"Iteration through function: {iteration}")

    for x in range(1, 21):
        do_print(x)

    # Demo on throttling single commands
    # - wrap them in a lambda. and put into the explicit wrapper call
    for x in range(1, 21):
        r.throttle(print(f"Iterating through anything else: {x}"))


if __name__ == "__main__":
    print(os.getcwd())
    sys.path.append(os.path.abspath(os.getcwd() + "/src/"))
    main()
