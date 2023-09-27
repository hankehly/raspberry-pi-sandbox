import time

import RPi.GPIO as GPIO

GPIO_OUT = 11
GPIO_IN = 29


def toggle_led():
    GPIO.output(GPIO_OUT, not GPIO.input(GPIO_OUT))


def on_button_press(*args):
    print("Button pressed!")
    toggle_led()


def setmode(mode):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"Setting mode to {mode}")
            GPIO.setmode(mode)
            func(*args, **kwargs)

        return wrapper

    return decorator


def cleanup_on_exit(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        finally:
            print("Cleaning up...")
            GPIO.cleanup()

    return wrapper


@setmode(GPIO.BOARD)
@cleanup_on_exit
def main():
    GPIO.setup(GPIO_IN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(GPIO_OUT, GPIO.OUT)
    GPIO.add_event_detect(GPIO_IN, GPIO.RISING, callback=on_button_press)
    while True:
        time.sleep(0.05)


if __name__ == "__main__":
    main()
