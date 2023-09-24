import time

import RPi.GPIO as GPIO


def main():
    try:
        GPIO.setmode(GPIO.BOARD)
        # GPIO.setup(?, GPIO.IN|OUT)
        while True:
            print("Hello")
            time.sleep(1)
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
