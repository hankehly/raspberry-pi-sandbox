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
