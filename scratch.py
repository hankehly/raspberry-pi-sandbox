import time

import RPi.GPIO as GPIO

GPIO_01 = 1
GPIO_40 = 40
GPIO_38 = 38


def set_led_state(on: bool):
    if on:
        GPIO.output(GPIO_38, GPIO.HIGH)
    else:
        GPIO.output(GPIO_38, GPIO.LOW)


def main():
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(GPIO_40, GPIO.IN)
        GPIO.setup(GPIO_38, GPIO.OUT)
        while True:
            on = GPIO.input(GPIO_40)
            set_led_state(on)
            print(on)
            time.sleep(0.05)
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
