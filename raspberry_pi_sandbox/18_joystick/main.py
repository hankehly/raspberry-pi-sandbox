import argparse
import time

import RPi.GPIO as GPIO

from raspberry_pi_sandbox.ADC0834 import ADC0834
from raspberry_pi_sandbox.gpio import cleanup


@cleanup
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--adc-clk", type=int, default=12, help="ADC0834 clock pin")
    parser.add_argument(
        "--adc-dio", type=int, default=13, help="ADC0834 data in/out pin"
    )
    parser.add_argument(
        "--adc-cs", type=int, default=11, help="ADC0834 chip select pin"
    )
    parser.add_argument(
        "--mode", type=str, default="board", help="GPIO mode (board or bcm)"
    )
    parser.add_argument("--joystick-sw", type=int, default=40, help="Joystick switch")
    args = parser.parse_args()
    GPIO.setmode(getattr(GPIO, args.mode.upper()))
    GPIO.setup(args.joystick_sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    adc = ADC0834(cs=args.adc_cs, clk=args.adc_clk, dio=args.adc_dio)
    adc.setup()

    try:
        while True:
            vrx = adc.read(channel=0)
            vry = adc.read(channel=1)
            sw = GPIO.input(args.joystick_sw)
            print(f"X: {vrx:03d}, Y: {vry:03d}, SW: {sw}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
