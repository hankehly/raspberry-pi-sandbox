import argparse
import logging
import threading
import time

from RPi import GPIO

from raspberry_pi_sandbox.gpio import cleanup, setmode

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class LED:
    def __init__(self, pin, steps=5, freq=60):
        self._pin = pin
        GPIO.setup(self._pin, GPIO.OUT)
        self._freq = freq
        self._steps = steps
        self._pwm = GPIO.PWM(self._pin, self._freq)
        self._pwm_on = False
        self._sem = threading.BoundedSemaphore(self._steps)
        self._sync()

    def dim(self):
        try:
            logging.debug("Dimming...")
            self._sem.release()
            self._sync()
        except ValueError:
            logging.info("Already at min brightness!")

    def brighten(self):
        logging.debug("Brightening...")
        if self._sem.acquire(blocking=False):
            self._sync()
        else:
            logging.info("Already at max brightness!")

    def _start_pwm(self, duty_cycle):
        self._pwm.start(duty_cycle)
        self._pwm_on = True
        logging.info(f"Started PWM with duty cycle {duty_cycle}")

    def _stop_pwm(self):
        self._pwm.stop()
        self._pwm_on = False
        logging.info("Stopped PWM")

    def _sync(self):
        logging.debug("Syncing...")
        duty_cycle = self._freq - (self._freq * self._sem._value / self._steps)
        if duty_cycle == 0:
            self._stop_pwm()
            time.sleep(0.01)
            GPIO.output(self._pin, GPIO.LOW)
            logging.info("Set pin to LOW")
        elif duty_cycle == self._freq:
            self._stop_pwm()
            time.sleep(0.01)
            GPIO.output(self._pin, GPIO.HIGH)
            logging.info("Set pin to HIGH")
        else:
            if self._pwm_on:
                self._pwm.ChangeDutyCycle(duty_cycle)
                logging.info(f"Changed duty cycle to {duty_cycle}")
            else:
                self._start_pwm(duty_cycle)


@setmode(GPIO.BOARD)
@cleanup
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--led-pin", type=int, default=36)
    parser.add_argument(
        "--brighten-pin",
        type=int,
        default=38,
        help=(
            "GPIO pin that the brighten button is connected to. "
            "Pressing this button will increase the brightness of the LED. "
            "The GPIO pin is pulled down, so the button should connect the pin to 3.3V when pressed."
        ),
    )
    parser.add_argument(
        "--dim-pin",
        type=int,
        default=40,
        help=(
            "GPIO pin that the dim button is connected to. "
            "Pressing this button will decrease the brightness of the LED. "
            "The GPIO pin is pulled down, so the button should connect the pin to 3.3V when pressed."
        ),
    )
    parser.add_argument(
        "--steps", type=int, default=5, help="Number of brightness steps"
    )
    parser.add_argument("--freq", type=int, default=60, help="PWM frequency in Hz")
    args = parser.parse_args()

    logging.info("Starting LED PWM demo...")
    logging.info(
        f"LED pin: {args.led_pin}, Brighten pin: {args.brighten_pin}, "
        f"Dim pin: {args.dim_pin}, Steps: {args.steps}, Freq: {args.freq} Hz"
    )

    GPIO.setup(args.brighten_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(args.dim_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    led = LED(args.led_pin, args.steps, args.freq)

    def on_dim_button_press(*args):
        logging.debug("Dim button pressed!")
        led.dim()

    def on_brighten_button_press(*args):
        logging.debug("Brighten button pressed!")
        led.brighten()

    GPIO.add_event_detect(
        args.brighten_pin,
        GPIO.RISING,
        callback=on_brighten_button_press,
        bouncetime=200,
    )
    GPIO.add_event_detect(
        args.dim_pin, GPIO.RISING, callback=on_dim_button_press, bouncetime=200
    )
    while True:
        time.sleep(0.05)


if __name__ == "__main__":
    main()
