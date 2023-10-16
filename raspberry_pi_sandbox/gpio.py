import logging
import sys
import threading
import time

import RPi.GPIO as GPIO


def setmode(mode):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"Setting mode to {mode}")
            GPIO.setmode(mode)
            func(*args, **kwargs)

        return wrapper

    return decorator


def cleanup(func):
    def wrapper(*args, **kwargs):
        GPIO.setwarnings(False)
        print("Cleaning up...")
        GPIO.cleanup()
        GPIO.setwarnings(True)
        try:
            func(*args, **kwargs)
        finally:
            print("Cleaning up...")
            GPIO.cleanup()

    return wrapper


class LoggingMixin:
    _log: logging.Logger = None

    @staticmethod
    def _get_log(self):
        if self._log is None:
            self._log = logging.getLogger(
                f"{self.__class__.__module__}.{self.__class__.__name__}"
            )
        return self._log

    @property
    def log(self):
        """Return a logger."""
        return LoggingMixin._get_log(self)


class LED(LoggingMixin):
    def __init__(self, pin, steps=5, freq=60):
        self._pin = pin
        GPIO.setup(self._pin, GPIO.OUT)
        self._freq = freq
        self._steps = steps
        self._pwm = GPIO.PWM(self._pin, self._freq)
        self._pwm_on = False
        # the higher the semaphore value, the dimmer the LED
        self._sem = threading.BoundedSemaphore(self._steps)
        self._sync()

    @property
    def steps(self) -> int:
        return self._steps

    @property
    def brightness_ratio(self) -> float:
        return 1 - self._sem._value / self._steps

    def dim(self) -> bool:
        try:
            self.log.debug("Dimming...")
            self._sem.release()
            self._sync()
            return True
        except ValueError:
            self.log.info("Already at min brightness!")
            return False

    def brighten(self) -> bool:
        self.log.debug("Brightening...")
        if self._sem.acquire(blocking=False):
            self._sync()
            return True
        self.log.info("Already at max brightness!")
        return False

    def reset(self):
        self._sem = threading.BoundedSemaphore(self._steps)
        self._sync()

    def set_brightness(self, brightness: float):
        """
        Set the brightness of the LED.

        :param brightness: A float between 0 and 1.
        """
        if brightness > 1:
            self.log.warning(
                f"Received brightness {brightness} but max is 1. Setting to 1."
            )
            brightness = 1
        elif brightness < 0:
            self.log.warning(
                f"Received brightness {brightness} but min is 0. Setting to 0."
            )
            brightness = 0
        self._sem = threading.BoundedSemaphore(
            self._steps - round(self._steps * brightness, 2)
        )
        self._sync()

    def _start_pwm(self, duty_cycle):
        self._pwm.start(duty_cycle)
        self._pwm_on = True
        self.log.info(f"Started PWM with duty cycle {duty_cycle}")

    def _stop_pwm(self):
        self._pwm.stop()
        self._pwm_on = False
        self.log.info("Stopped PWM")

    def _sync(self):
        self.log.debug("Syncing...")
        duty_cycle = self._freq - (self._freq * self._sem._value / self._steps)
        if duty_cycle == 0:
            self._stop_pwm()
            time.sleep(0.01)
            GPIO.output(self._pin, GPIO.LOW)
            self.log.info("Set pin to LOW")
        elif duty_cycle == self._freq:
            self._stop_pwm()
            time.sleep(0.01)
            GPIO.output(self._pin, GPIO.HIGH)
            self.log.info("Set pin to HIGH")
        else:
            if self._pwm_on:
                self._pwm.ChangeDutyCycle(duty_cycle)
                self.log.info(f"Changed duty cycle to {duty_cycle}")
            else:
                self._start_pwm(duty_cycle)
