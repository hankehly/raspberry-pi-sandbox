import argparse
import logging
import time

from RPi import GPIO

from raspberry_pi_sandbox.color import rgb_percentage_to_hex
from raspberry_pi_sandbox.gpio import LED, cleanup, setmode

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")


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
    led_red = LED(args.output_red, steps=20, freq=100)
    led_green = LED(args.output_green, steps=20, freq=100)
    led_blue = LED(args.output_blue, steps=20, freq=100)

    # define button callbacks
    def on_button_press_red(pin):
        result = led_red.brighten()
        if not result:
            led_red.reset()
        print_rgb()

    def on_button_press_green(pin):
        result = led_green.brighten()
        if not result:
            led_green.reset()
        print_rgb()

    def on_button_press_blue(pin):
        result = led_blue.brighten()
        if not result:
            led_blue.reset()
        print_rgb()

    def print_rgb():
        # convert to percentage
        red_percentage = round(led_red.brightness_ratio, 5) * 100
        green_percentage = round(led_green.brightness_ratio, 5) * 100
        blue_percentage = round(led_blue.brightness_ratio, 5) * 100
        # convert to hex
        hex = rgb_percentage_to_hex((red_percentage, green_percentage, blue_percentage))
        print(
            f"Current color: {hex} ({red_percentage}%, {green_percentage}%, {blue_percentage}%)"
        )

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


# Red
# Green
# Blue
# Yellow (red 100, green 100)
# Purple (red 100, blue 100)

# Turquoise:
# Hex: #40E0D0
# RGB Percentage: Red: 25.1%, Green: 87.84%, Blue: 81.57%

# Gold:
# Hex: #FFD700
# RGB Percentage: Red: 100%, Green: 84.31%, Blue: 0%

# Salmon: (not so much)
# Hex: #FA8072
# RGB Percentage: Red: 98.04%, Green: 50.98%, Blue: 45.1%

# Sky Blue:
# Hex: #87CEEB
# RGB Percentage: Red: 52.16%, Green: 80.39%, Blue: 92.55%

# Forest Green:
# Hex: #228B22
# RGB Percentage: Red: 13.33%, Green: 54.12%, Blue: 13.33%

# Tomato: (not so much)
# Hex: #FF6347
# RGB Percentage: Red: 100%, Green: 38.43%, Blue: 27.84%

# Peru:
# Hex: #CD853F
# RGB Percentage: Red: 80.39%, Green: 52.55%, Blue: 24.71%
