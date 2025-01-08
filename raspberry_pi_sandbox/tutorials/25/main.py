import argparse
import time
import RPi.GPIO as GPIO
from raspberry_pi_sandbox.gpio import cleanup, setmode
import dht11


@setmode(GPIO.BCM)
@cleanup
def main():
    parser = argparse.ArgumentParser(description="DHT11 sensor")
    parser.add_argument("pin", type=int, help="GPIO pin number for the sensor")
    args = parser.parse_args()
    sensor = dht11.DHT11(pin=args.pin)
    while True:
        result = sensor.read()
        if result.is_valid():
            print(f"Temperature: {result.temperature}°C, Humidity: {result.humidity}%")
        time.sleep(0.2)


if __name__ == "__main__":
    main()
