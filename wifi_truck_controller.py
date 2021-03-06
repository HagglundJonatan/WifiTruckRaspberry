#The controller class of the wifi truck!

from Adafruit_PWM_Servo_Driver import PWM
import time

class WifiTruckController(object):

	# Initialises the controller with all gpio's and stuff
	def __init__(self, pwm = None, servoMin = 0, servoNeutral = 0, servoMax = 0, servoOutputSpan = 0) :
		
		#Initialise the PWM device using the default address (Adafruit)
		self.pwm = PWM(0x40)
		self.pwm.setPWMFreq(50)

		self.servoMinSteering = 230 #Min pulse length out of 4096
		self.servoNeutralSteering = 307 #Neutral -||-
		self.servoMaxSteering = 415 #Max -||-
		self.servoOutputSpanSteering = self.servoMaxSteering - self.servoMinSteering

		self.servoMinDCMotor = 230 	 	#Min pulse length out of 4096
		self.servoNeutralDCMotor = 315 		#Neutrall -||- ?
		self.servoMaxDCMotor = 400 	 	#Max -||-
		self.servoOutputSpanDCMotor = self.servoMaxDCMotor - self.servoMinDCMotor
		
	# Sets a the pwm value by input (percentage)
	def setServoPulse(self, channel, inputPercentage):
#		print("setServoPules - input:%f" % inputPercentage )
		if ( 0.0 <= inputPercentage <= 1.0 ):
			if ( channel == 0 ):
				pwmOutput = int(self.servoMinSteering + self.servoOutputSpanSteering * inputPercentage) # starting at min add the input times the span (min + 165 * 1 == 100%)
#				print("setServoPulse - pwmOutput:%d" %pwmOutput)
				self.pwm.setPWM(channel, 0, pwmOutput)
			elif ( channel == 1 ):
				pwmOutput = int(self.servoMinDCMotor + self.servoOutputSpanDCMotor * inputPercentage) # starting at min add the input times the span (min + 165 * 1 == 100%)
#				print("setServoPulse - pwmOutput:%d" %pwmOutput)
				self.pwm.setPWM(channel, 0, pwmOutput)	
		else:
			self.pwm.setPWM(channel, 0, 0)

	def stop(self):
		self.releaseMovement()
		self.releaseSteering()
#		print("WTC - STOP")

	def releaseSteering(self):
		self.setServoPulse(0, 0.5)
		time.sleep(0.5)
		self.pwm.setPWM(0, 0, 0)

	def releaseMovement(self):
		self.setServoPulse(1, 0.25)
		time.sleep(0.5)
		self.pwm.setPWM(1, 0, 0)

	def releaseAllServos(self):
		self.pwm.setAllPWM(0, 0)

	def move(self, percent):
		# Since the speed regulator doesn't map to the joystick divide by 2
		# when reversing. The reverse is active in the 0-25% area
		if ( percent < 0.35 ):
			percent = 0
		elif ( 0.4 < percent < 0.5 ):
			percent = 0.25
		elif ( 0.5 < percent < 0.6 ):
			percent *= 0.75
		self.setServoPulse(1, percent)
#		print("WTC - MOVE")

	def steer(self, percent):
		self.setServoPulse(0, percent)
#		print("WTC - STEER")

#	def left(self, percent):
#		self.setServoPulse(0, percent)
#		#self.pwm.setPWM(0, 0, self.servoMax)
#		print("WTC - LEFT")
#
#	def neutral(self):
#		self.setServoPulse(0, 0.5)
#		#self.pwm.setPWM(0, 0, 307)
#		print("WTC - STRAIGHT")



#testController = WifiTruckController()

#testController.steer(0.0)
#time.sleep(1)
#testController.steer(1.0)
#time.sleep(1)
#testController.stop()

