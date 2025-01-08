import argparse
import time

from RPi import GPIO

from raspberry_pi_sandbox.gpio import cleanup, setmode


@setmode(GPIO.BOARD)
@cleanup
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-red",
        type=int,
        default=40,
        help="Red button input pin. This is a pull down button.",
    )
    parser.add_argument(
        "--input-green",
        type=int,
        default=38,
        help="Green button input pin. This is a pull down button.",
    )
    parser.add_argument(
        "--input-blue",
        type=int,
        default=36,
        help="Blue button input pin. This is a pull down button.",
    )
    parser.add_argument(
        "--output-red", type=int, default=37, help="Red led output pin."
    )
    parser.add_argument(
        "--output-green", type=int, default=35, help="Green led output pin."
    )
    parser.add_argument(
        "--output-blue", type=int, default=33, help="Blue led output pin."
    )
    args = parser.parse_args()

    # setup input and output pins
    GPIO.setup(args.input_red, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(args.input_green, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(args.input_blue, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(args.output_red, GPIO.OUT)
    GPIO.setup(args.output_green, GPIO.OUT)
    GPIO.setup(args.output_blue, GPIO.OUT)

    # turn off all leds
    GPIO.output(args.output_red, GPIO.LOW)
    GPIO.output(args.output_green, GPIO.LOW)
    GPIO.output(args.output_blue, GPIO.LOW)

    # define button callbacks
    def on_button_press_red(pin):
        print("Red button pressed")
        GPIO.output(args.output_red, not GPIO.input(args.output_red))

    def on_button_press_green(pin):
        print("Green button pressed")
        GPIO.output(args.output_green, not GPIO.input(args.output_green))

    def on_button_press_blue(pin):
        print("Blue button pressed")
        GPIO.output(args.output_blue, not GPIO.input(args.output_blue))

    # setup event detection
    GPIO.add_event_detect(
        args.input_red,
        GPIO.RISING,
        callback=on_button_press_red,
        bouncetime=200,
    )
    GPIO.add_event_detect(
        args.input_green,
        GPIO.RISING,
        callback=on_button_press_green,
        bouncetime=200,
    )
    GPIO.add_event_detect(
        args.input_blue, GPIO.RISING, callback=on_button_press_blue, bouncetime=200
    )

    # wait for keyboard interrupt
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
