"""
https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/
"""

import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library

GPIO.setwarnings(False)  # Ignore warning for now
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
# Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:  # Run forever
    if GPIO.input(10) == GPIO.HIGH:
        print("Button was pushed!")
