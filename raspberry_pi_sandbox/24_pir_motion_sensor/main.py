from raspberry_pi_sandbox.gpio import setmode, cleanup
import time
import RPi.GPIO as GPIO


@setmode(GPIO.BCM)
@cleanup
def main():
    GPIO.setup(26, GPIO.IN)
    # wait 15 seconds, print a countdown
    print('Starting in...')
    for i in range(15, 0, -1):
        print(i)
        time.sleep(1)
    print('Starting now!')
    try:
        while True:
            if GPIO.input(26) == GPIO.HIGH:
                print('Motion detected!')
            else:
                print('No motion detected.')
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
