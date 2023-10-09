import time

import RPi.GPIO as GPIO

from raspberry_pi_sandbox.ADC0834 import ADC0834
from raspberry_pi_sandbox.gpio import cleanup, setmode


@setmode(GPIO.BOARD)
@cleanup
def main():
    adc = ADC0834(cs=11, clk=12, dio=13)
    GPIO.setup(15, GPIO.OUT)
    pwm = GPIO.PWM(15, 100)
    pwm.start(0)
    try:
        while True:
            adc_val = adc.read(channel=0)
            adv_val_as_pct = round(adc_val / 255 * 100, 1)
            pwm.ChangeDutyCycle(adv_val_as_pct)
            print(f"{adv_val_as_pct}%")
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
