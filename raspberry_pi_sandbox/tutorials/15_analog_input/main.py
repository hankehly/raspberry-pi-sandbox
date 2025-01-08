import argparse
import time

import RPi.GPIO as GPIO

from raspberry_pi_sandbox.ADC0834 import ADC0834
from raspberry_pi_sandbox.gpio import cleanup


@cleanup
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clk", type=int, default=12, help="Clock pin")
    parser.add_argument("--dio", type=int, default=13, help="Data in/out pin")
    parser.add_argument("--cs", type=int, default=11, help="Chip select pin")
    parser.add_argument(
        "--mode", type=str, default="board", help="GPIO mode (board or bcm)"
    )
    parser.add_argument("--led", type=int, default=15, help="LED pin")
    args = parser.parse_args()
    GPIO.setmode(getattr(GPIO, args.mode.upper()))
    GPIO.setup(args.led, GPIO.OUT)
    adc = ADC0834(cs=args.cs, clk=args.clk, dio=args.dio).setup()
    pwm = GPIO.PWM(args.led, 60)
    pwm.start(0)
    try:
        while True:
            adc_val_raw = adc.read(channel=0)
            adc_val_pct = round(adc_val_raw / 255 * 100, 1)
            pwm.ChangeDutyCycle(adc_val_pct)
            print(f"{adc_val_pct}%")
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
