import time

import RPi.GPIO as GPIO
import argparse

from raspberry_pi_sandbox.gpio import cleanup, setmode
from raspberry_pi_sandbox.utils import RollingAverageCalculator


@setmode(GPIO.BCM)
@cleanup
def main(trig_pin, echo_pin, led_pin):
    GPIO.setup(trig_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)
    GPIO.setup(led_pin, GPIO.OUT)
    pwm = GPIO.PWM(led_pin, 60)
    pwm.start(0)
    rolling_avg = RollingAverageCalculator(5)
    try:
        while True:
            GPIO.output(trig_pin, GPIO.LOW)
            time.sleep(2e-6)
            GPIO.output(trig_pin, GPIO.HIGH)
            time.sleep(10e-6)
            GPIO.output(trig_pin, GPIO.LOW)
            waiter1 = GPIO.wait_for_edge(echo_pin, GPIO.BOTH, timeout=100)
            if waiter1 is None:
                continue
            start = time.perf_counter()
            waiter2 = GPIO.wait_for_edge(echo_pin, GPIO.FALLING, timeout=100)
            if waiter2 is None:
                continue
            stop = time.perf_counter()
            # The speed of sound is 34300 cm/s.
            # The reason for dividing by 2 is because the ultrasonic sensor sends a sound wave and waits for it to bounce back.
            # The time it takes for the wave to travel to the object and back is measured.
            # However, the distance to the object is twice the distance traveled by the sound wave.
            # Therefore, dividing the time by 2 gives us the actual distance to the object.
            duration = stop - start
            cm = duration * 34300 / 2
            duty = 100 - min(100, max(0, cm / 10 * 100))
            duty = rolling_avg.rolling_average(duty)
            print(f"Distance: {cm:.2f} cm, Duty: {duty:.2f} %")
            pwm.ChangeDutyCycle(duty)
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ultrasonic sensor")
    parser.add_argument(
        "--trig", type=int, help="GPIO pin number for the trigger pin", default=26
    )
    parser.add_argument(
        "--echo", type=int, help="GPIO pin number for the echo pin", default=21
    )
    parser.add_argument(
        "--led", type=int, help="GPIO pin number for the LED pin", default=20
    )
    args = parser.parse_args()
    main(args.trig, args.echo, args.led)
