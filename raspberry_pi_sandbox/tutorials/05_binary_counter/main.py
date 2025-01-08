import argparse
import time

import RPi.GPIO as GPIO

GPIO_01 = 11
GPIO_02 = 29
GPIO_03 = 16
GPIO_04 = 18
GPIO_05 = 40

# order matters
PINS = (
    GPIO_01,
    GPIO_02,
    GPIO_03,
    GPIO_04,
    GPIO_05,
)


def set_state(n: int):
    """
    Set the state of the GPIO pins to the
    """
    digits = bin(n)[2:].zfill(len(PINS))
    GPIO.output(PINS, list(map(int, digits)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--stop", type=int, default=32, help="Count until this number (default/max 32)"
    )
    args = parser.parse_args()
    if args.stop < 0 or args.stop > 32:
        raise ValueError("Please choose a number between 0 and 32")
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PINS, GPIO.OUT)
        for i in range(0, args.stop):
            print(str(i).zfill(len(str(args.stop))))
            set_state(i)
            time.sleep(1)
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
