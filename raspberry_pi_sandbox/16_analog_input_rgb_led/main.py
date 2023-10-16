import argparse
import time

import RPi.GPIO as GPIO

from raspberry_pi_sandbox.ADC0834 import ADC0834
from raspberry_pi_sandbox.gpio import LED, cleanup


@cleanup
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clk", type=int, default=12, help="Clock pin")
    parser.add_argument("--dio", type=int, default=13, help="Data in/out pin")
    parser.add_argument("--cs", type=int, default=11, help="Chip select pin")
    parser.add_argument(
        "--mode", type=str, default="board", help="GPIO mode (board or bcm)"
    )
    parser.add_argument("--red-out", type=int, default=36, help="Red pin")
    parser.add_argument("--green-out", type=int, default=38, help="Green pin")
    parser.add_argument("--blue-out", type=int, default=40, help="Blue pin")
    parser.add_argument("--red-in", type=int, default=0, help="Red input channel")
    parser.add_argument("--green-in", type=int, default=1, help="Green input channel")
    parser.add_argument("--blue-in", type=int, default=2, help="Blue input channel")
    args = parser.parse_args()

    GPIO.setmode(getattr(GPIO, args.mode.upper()))

    GPIO.setup(args.red_out, GPIO.OUT)
    GPIO.setup(args.green_out, GPIO.OUT)
    GPIO.setup(args.blue_out, GPIO.OUT)

    led_red = LED(args.red_out, steps=20, freq=100)
    led_green = LED(args.green_out, steps=20, freq=100)
    led_blue = LED(args.blue_out, steps=20, freq=100)

    adc = ADC0834(cs=args.cs, clk=args.clk, dio=args.dio)

    try:
        while True:
            pct_red = round(adc.read(channel=args.red_in) / 255, 3)
            pct_green = round(adc.read(channel=args.green_in) / 255, 3)
            pct_blue = round(adc.read(channel=args.blue_in) / 255, 3)
            led_red.set_brightness(pct_red)
            led_green.set_brightness(pct_green)
            led_blue.set_brightness(pct_blue)
            print(f"R: {pct_red*100:.1f}%, G: {pct_green*100:.1f}%, B: {pct_blue*100:.1f}%")
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
