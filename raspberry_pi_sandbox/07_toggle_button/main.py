import time

import RPi.GPIO as GPIO

from raspberry_pi_sandbox.gpio import cleanup, setmode

GPIO_OUT = 11
GPIO_IN = 29


def toggle_led():
    GPIO.output(GPIO_OUT, not GPIO.input(GPIO_OUT))


def on_button_press(*args):
    print("Button pressed!")
    toggle_led()


@setmode(GPIO.BOARD)
@cleanup
def main():
    GPIO.setup(GPIO_IN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(GPIO_OUT, GPIO.OUT)
    GPIO.add_event_detect(GPIO_IN, GPIO.RISING, callback=on_button_press, bouncetime=200)
    while True:
        time.sleep(0.05)


if __name__ == "__main__":
    main()
