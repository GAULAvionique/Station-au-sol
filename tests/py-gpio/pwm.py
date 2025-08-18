import RPi.GPIO as GPIO

FAN_PIN = 33  # FAN2
FREQ = 20000

GPIO.setmode(GPIO.BOARD)
GPIO.setup(FAN_PIN, GPIO.OUT)

# Create PWM
pwm = GPIO.PWM(FAN_PIN, FREQ)
pwm.start(0)  # Start at 0% duty cycle (fan off)

pwm.ChangeDutyCycle(10)
print("Fan speed: 10%")

# pwm.stop()
GPIO.cleanup()
