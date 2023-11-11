import time

import pigpio
import RPi.GPIO as GPIO
from raspberry_pi_sandbox.gpio import setmode, cleanup_pigpio
from gpiozero import LED


@setmode(GPIO.BCM)
@cleanup_pigpio
def main():
    pi = pigpio.pi()

    sensor_input_pin = 4
    pi.set_mode(sensor_input_pin, pigpio.INPUT)
    led = LED(21)
    led.off()

    servo_state_on = 130
    servo_state_off = 80
    servo_control_pin = 26

    # Setup servo control pin
    # The servo expects to see a pulse every 20 ms.
    # T = 20 ms
    # f = 1/T = 50 Hz
    servo_pwm_frequency = int(1 / 20 * 1000)
    pi.set_mode(servo_control_pin, pigpio.OUTPUT)
    pi.set_PWM_frequency(servo_control_pin, servo_pwm_frequency)
    pi.set_PWM_range(servo_control_pin, 1024)
    pi.set_PWM_dutycycle(servo_control_pin, servo_state_off)

    is_led_blinking = False

    print("Starting in...")
    for i in range(10, 0, -1):
        print(i)
        time.sleep(1)
    print("Starting now!")
    try:
        while True:
            if pi.read(sensor_input_pin) == pigpio.HIGH:
                print("Motion detected!")
                pi.set_PWM_dutycycle(servo_control_pin, servo_state_on)
                if not is_led_blinking:
                    led.blink(0.1, 0.1)
                    is_led_blinking = True
            else:
                print("No motion detected.")
                pi.set_PWM_dutycycle(servo_control_pin, servo_state_off)
                led.off()
                is_led_blinking = False
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
