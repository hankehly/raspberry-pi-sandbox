import argparse
import time

import RPi.GPIO as GPIO

OUTPUT_PIN_NO = 11


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("times", type=int, help="How many times to blink the LED?")
    parser.add_argument(
        "-s",
        "--speed",
        choices={"slow", "normal", "fast", "sonic"},
        default="normal",
        help="How fast should the blinking be?",
    )
    args = parser.parse_args()
    speeds = {"slow": 1.0, "normal": 0.5, "fast": 0.25, "sonic": 0.125}
    delay = speeds[args.speed]
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(OUTPUT_PIN_NO, GPIO.OUT)
        for i in range(args.times):
            GPIO.output(OUTPUT_PIN_NO, True)
            time.sleep(delay)
            GPIO.output(OUTPUT_PIN_NO, False)
            is_last_time = i + 1 == args.times
            if is_last_time:
                break
            else:
                time.sleep(delay)
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
