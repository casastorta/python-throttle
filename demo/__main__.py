from demo.demos import demo_throttle
from demo.setup.logging_setup import set_up_logging

set_up_logging()


def main():
    demo_throttle.main()


if __name__ == "__main__":
    main()
