import sys
import time
import math

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

sys.dont_write_bytecode = True

BASE_DEF_PER = 58

channels = {
		"Base": 3
		}
positions = {
	"Max_Base": 100,
	"Min_Base": 0
	}
	
class Arm (object):
	
	def __init__(self):
		self.base  = Base(channel = channels["Base"])
		
	def reset(self):
		self.base.set_position_res(BASE_DEF_PER, speed = 75)
		
class MG996R(object):
	"""
	TowerPro MG996R servo motor
	
	(the four purple ones)
	
	specifications
	---
	operating frequency: ?-? Hz
	operating angle: 270 degrees (from ? to ? usec)
	neutral position: ? usec
	deadband width: 1 usec
	pulse width range: ? to ? usec
	"""
	def __init__(self, channel, frequency=50, min_pulse_width=500, max_pulse_width=2500, debug=False):
		"""
		initialize a servo object
		"""
		GPIO.setup(channel, GPIO.OUT)

		self.pwm = GPIO.PWM(channel, 50)

		self.channel = channel

		self.min_pulse_width = min_pulse_width
		self.max_pulse_width = max_pulse_width

	def set_specific_angle(self, percentage):
		if not isinstance(percentage, int):
			return
		elif not 0 <= percentage <= 100:
			return

		pulse = int(self.min_pulse_width + (percentage / 100) * (self.max_pulse_width - self.min_pulse_width))
		angl = int((180 * pulse)/(self.max_pulse_width - self.min_pulse_width))
		duty = angl / 18 + 2
		self.pwm.ChangeDutyCycle(duty)

class Base(object):
	"""
	goes from clockwise to counter-clockwise with low to high values
	"""
	min_pulse_width = 125
	max_pulse_width = 595

	def __init__(self, channel=0, debug=False, turn = 0):
		"""
		initialize the object
		"""
		self.mg996r = MG996R(channel, min_pulse_width=Base.min_pulse_width, max_pulse_width=Base.max_pulse_width)
		self.turn = turn

	def set_position(self, percentage, speed=75):
		if 0 <= percentage <= 100:
			delay = 0.1 - speed * 0.001
			if self.turn == 0:
				for i in range(BASE_DEF_PER, percentage) :
					self.position = i
					self.mg996r.set_specific_angle(i)
					time.sleep(delay)
				time.sleep(delay*2)
				self.turn = 1
			else:
				if self.position<percentage:
					for i in range(self.position, percentage):
						self.position = i
						self.mg996r.set_specific_angle(i)
						time.sleep(delay)
					time.sleep(delay*2)
				elif self.position > percentage:
					for i in range(self.position, percentage, -1):
						self.position = i
						self.mg996r.set_specific_angle(i)
						time.sleep(delay)
					time.sleep(delay*2)

	def set_position_res(self, percentage, speed):
		"""
		used to reset position of arm component
		"""
		if 0 <= percentage <= 100:
			self.position = percentage
			self.mg996r.set_specific_angle(percentage)
		delay = 1 - speed*0.01
		time.sleep(delay)
		
