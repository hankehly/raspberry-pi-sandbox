import argparse
import time

import RPi.GPIO as GPIO
import pigpio

from raspberry_pi_sandbox.gpio import cleanup
from raspberry_pi_sandbox.ADC0834 import ADC0834


@cleanup
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--control-pin", type=int, default=21, help="control pin")
    parser.add_argument("--adc-clk", type=int, default=22, help="ADC0834 clock pin")
    parser.add_argument(
        "--adc-dio", type=int, default=27, help="ADC0834 data in/out pin"
    )
    parser.add_argument(
        "--adc-cs", type=int, default=17, help="ADC0834 chip select pin"
    )
    args = parser.parse_args()

    # Assumes BCM mode!!
    GPIO.setmode(GPIO.BCM)

    # Setup ADC0834
    adc = ADC0834(cs=args.adc_cs, clk=args.adc_clk, dio=args.adc_dio)
    adc.setup()

    # Setup servo control pin
    # GPIO.setup(args.control_pin, GPIO.OUT)

    # The servo expects to see a pulse every 20 ms.
    # T = 20 ms
    # f = 1/T = 50 Hz
    # pwm = GPIO.PWM(args.control_pin, 50)
    # pwm.start(0)
    pi = pigpio.pi()
    pi.set_mode(args.control_pin, pigpio.OUTPUT)
    pi.set_PWM_frequency(args.control_pin, 50)
    pi.set_PWM_range(args.control_pin, 1024)

    try:
        while True:
            adc_value = adc.read(channel=0)  # between 0 and 255
            # Translate range 0 ~ 255 to 25 ~ 125
            duty = round(25 + (adc_value / 255) * 100)
            pi.set_PWM_dutycycle(args.control_pin, duty)
            # pwm.ChangeDutyCycle(duty)
            print(f"adc_value: {adc_value}, duty: {duty}")
            time.sleep(0.05)
    except KeyboardInterrupt:
        pi.stop()


if __name__ == "__main__":
    main()
