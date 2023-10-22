import time
import timeit

import RPi.GPIO as GPIO

from raspberry_pi_sandbox.gpio import cleanup, setmode


@setmode(GPIO.BCM)
@cleanup
def main():
    trig = 26
    echo = 21
    led = 20

    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)
    GPIO.setup(led, GPIO.OUT)

    try:
        while True:
            GPIO.output(trig, GPIO.LOW)
            time.sleep(2e-6)
            GPIO.output(trig, GPIO.HIGH)
            time.sleep(10e-6)
            GPIO.output(trig, GPIO.LOW)

            # Using wait_for_edge does not work here for some reason
            # GPIO.wait_for_edge(echo, GPIO.RISING)
            while GPIO.input(echo) == 0:
                pass
            start = time.perf_counter()
            # GPIO.wait_for_edge(echo, GPIO.FALLING)
            while GPIO.input(echo) == 1:
                pass
            stop = time.perf_counter()
            # The speed of sound is 34300 cm/s.
            # The reason for dividing by 2 is because the ultrasonic sensor sends a sound wave and waits for it to bounce back.
            # The time it takes for the wave to travel to the object and back is measured.
            # However, the distance to the object is twice the distance traveled by the sound wave.
            # Therefore, dividing the time by 2 gives us the actual distance to the object.
            cm = (stop - start) * 34300 / 2
            print(f"Distance: {cm:.2f} cm")
            GPIO.output(led, cm < 10)
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
