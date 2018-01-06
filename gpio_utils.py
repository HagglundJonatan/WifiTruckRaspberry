import RPi.GPIO as gpio
import time

# Handles GPIO operations

PIN_STEERING_SERVO = 03
IS_INITIALIZED = False

def initialize():
	gpio.setmode(gpio.BOARD)
	IS_INITIALIZED = True

def create_output_gpio(pin, frequencyHz):
	if not IS_INITIALIZED:
		initialize()
	gpio.setup(pin, gpio.OUT)
	return gpio.PWM(pin, frequencyHz)

def create_input(pin):
	if not IS_INITIALIZED:
		initialize()
	gpio.setup(pin, gpio.IN)

def create_output(gpio):
	if not IS_INITIALIZED:
		initialize()
	gpio.setup(pin, gpio.OUT)

def write(pin, value):
	if not IS_INITIALIZED:
		initialize()
	gpio.output(pin, value)

def read(pin):
	if not IS_INITIALIZED:
		initialize()
	return gpio.input(pin)

#Test
initialize()
pwmObject = create_output_gpio(PIN_STEERING_SERVO,50)
pwmObject.start(6.7) #Min
time.sleep(2)
pwmObject.start(7.5) #Neutral
time.sleep(2)
pwmObject.start(8.8) #Max

raw_input('Press return to stop:')

write(PIN_STEERING_SERVO, False)
pwmObject.ChangeDutyCycle(0)
pwmObject.stop()
gpio.cleanup()

































