#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
SainSmart 5-Axis Control Palletizing Robot Arm controller

In referring to rotation, "right" means clockwise, and "left" means counter-clockwise.
"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

#import logging
import sys
import time
import math

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


sys.dont_write_bytecode = True

# uncomment to enable logging
#logging.basicConfig(level=logging.DEBUG)
BASE_DEF_PER = 58
SHOULDER_DEF_PER = 30
ELBOW_DEF_PER = 20
WRIST_DEF_PER = 90
GRIPPER_DEF_PER = 50

SHOULDER_LENGTH = 10.5
ELBOW_LENGTH = 15

channels = {
		"Base": 3,
		"Shoulder": 15,
		"Elbow": 27,
		"Wrist": 10,
		"Gripper": 7
		}

positions = {
	"Max_Base": 100,
	"Min_Base": 0,
	"Max_Shoulder": 60,
	"Min_Shoulder": 28,
	"Max_Elbow": 80,
	"Min_Elbow": 0,
	"Max_Wrist": 100,
	"Min_Wrist": 0,
	"Max_Gripper": 95,
	"Min_Gripper": 0
	}


def pos2angle_1(percentage):
	aps = 60/(positions["Max_Shoulder"] - SHOULDER_DEF_PER)
	angle = -(percentage-SHOULDER_DEF_PER)*aps
	
	return angle

def pos2angle_2(percentage):
	aps = 90/(positions["Max_Elbow"] - ELBOW_DEF_PER)
	angle = -(percentage - ELBOW_DEF_PER)*aps
	
	return angle # + angle from pos2angle_1

def find_h(angle, length):
	height = math.sin(angle)*length
	return height
	

class Arm (object):

	def __init__(self):
		self.base = Base(channel=channels["Base"])
		self.shoulder = Shoulder(channel=channels["Shoulder"])
		self.elbow = Elbow(channel=channels["Elbow"])
		self.wrist = Wrist(channel=channels["Wrist"])
		self.gripper = Gripper(channel=channels["Gripper"])
		
	def reset(self):
	# extend to 45 degrees
		self.base.set_position_res(BASE_DEF_PER, speed = 75)
		self.shoulder.set_position_res(SHOULDER_DEF_PER, speed = 75)
		self.elbow.set_position_res(ELBOW_DEF_PER, speed = 75)
		self.wrist.set_position(WRIST_DEF_PER, speed = 75)
		self.gripper.set_position(GRIPPER_DEF_PER, speed = 75)
		time.sleep(0.1)
	
	def find_h(angle, length):
		height = math.sin(angle)*length
		return height
	
	def control(self):
		self.shoulder.angle = Shoulder.pos2angle_1(self.shoulder.position)
		self.elbow.angle = Elbow.pos2angle_2(self.shoulder.position) + self.shoulder.angle
		self.shoulder.height = find_h(self.shoulder.angle, SHOULDER_LENGTH)
		self.elbow.height = find_h(self.elbow.angle, ELBOW_LENGTH)
		
		if self.shoulder.height>ELBOW_LENGTH:
			pass
		else:
			#set_position for elbow
			pass
			
			
			

class DS3218(object):
	"""
	DS3218 servo motor
	
	(the single orange one)
	
	specifications
	---
	operating frequency: 50-330 Hz
	operating angle: 180 degrees (from 500 to 2500 usec)
	neutral position: 1500 usec
	deadband width: 3 usec
	pulse width range: 500 to 2500 usec
	"""
	def __init__(self, channel=0, frequency=50, min_pulse_width=500, max_pulse_width=2500, debug=False):
		"""
		initialize a servo object
		"""
		GPIO.setup(channel, GPIO.OUT)

		self.pwm = GPIO.PWM(channel, 50)
		self.pwm.start(0)

		self.channel = channel

		self.min_pulse_width = min_pulse_width
		self.max_pulse_width = max_pulse_width

	def set_specific_angle(self, percentage):
		if not isinstance(percentage, int):
			return
		elif not 0 <= percentage <= 100:
			return

		pulse = int(self.min_pulse_width + (percentage / 100) * (self.max_pulse_width - self.min_pulse_width))
		duty = int(angl / 18 + 2)
		GPIO.output(self.channel, True)
		self.pwm.ChangeDutyCycle(duty)


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
		self.pwm.start(0)

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
		duty = int(angl / 18 + 2)
		GPIO.output(self.channel, True)
		self.pwm.ChangeDutyCycle(duty)

class Base(object):
	"""
	goes from clockwise to counter-clockwise with low to high values
	"""
	min_pulse_width = 125
	max_pulse_width = 595

	def __init__(self, channel, debug=False, turn = 0):
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


class Shoulder(object):
	"""
	goes from the front to the back with high to low values
	
	NOTE
	can't reach the min range, goes into negative values,
	might require tuning in respect of the frequency
	"""
	min_pulse_width = 10
	max_pulse_width = 370

	def __init__(self, channel, debug=False, turn = 0):
		"""
		initialize the object
		"""
		self.ds3218 = DS3218(channel, min_pulse_width=Shoulder.min_pulse_width, max_pulse_width=Shoulder.max_pulse_width)
		self.turn = turn
		self.position = None
		self.angle = None
		self.height = None
		
	def pos2angle_1(percentage):
		aps = 60/(positions["Max_Shoulder"] - SHOULDER_DEF_PER)
		angle = -(percentage-SHOULDER_DEF_PER)*aps
		
		return angle
		
	def set_position_res(self, percentage, speed=75):
		"""
		used to reset position of arm component
		"""
		if 0 <= percentage <= 100:
			self.position = percentage
			self.ds3218.set_specific_angle(percentage)
		delay = 1 - speed * 0.01
		time.sleep(delay)

	def set_position(self, percentage, speed=75):
		if 0 <= percentage <= 100:
			delay = 0.1 - speed * 0.001
			if self.turn == 0:
				for i in range(SHOULDER_DEF_PER, percentage) :
					self.position = i
					self.angle = pos2angle_1(self.position)
					self.height = find_h(self.angle, SHOULDER_LENGTH)
					if self.height>ELBOW_DEF_PER:
						self.ds3218.set_specific_angle(i)
						time.sleep(delay)
				time.sleep(delay*2)
				self.turn = 1
			else:
				if self.position<percentage:
					for i in range(self.position, percentage):
						self.position = i
						self.ds3218.set_specific_angle(i)
						time.sleep(delay)
					time.sleep(delay*2)
				elif self.position > percentage:
					for i in range(self.position, percentage, -1):
						self.position = i
						self.ds3218.set_specific_angle(i)
						time.sleep(delay)
					time.sleep(delay*2)



class Elbow(object):
	"""
	goes from the front to the back with high to low values
	
	NOTE
	there is a kind of non smooth motion when reaching the min range
	"""
	min_pulse_width = 127
	max_pulse_width = 608

	def __init__(self, channel, debug=False, turn = 0):
		"""
		initialize the object
		"""
		self.mg996r = MG996R(channel, min_pulse_width=Elbow.min_pulse_width, max_pulse_width=Elbow.max_pulse_width)
		self.turn = turn
		self.position = None
		self.angle = None
		self.height = None
		
	def pos2angle_2(percentage):
		aps = 90/(positions["Max_Elbow"] - ELBOW_DEF_PER)
		angle = -(percentage - ELBOW_DEF_PER)*aps
		
		return angle # + angle from pos2angle_1
		
	def set_position_res(self, percentage, speed=75):
		"""
		used to reset position of arm component
		"""
		if 0 <= percentage <= 100:
			self.position = percentage
			self.mg996r.set_specific_angle(percentage)
		delay = 1 - speed * 0.01
		time.sleep(delay)

	def set_position(self, percentage, speed=75):
		if 0 <= percentage <= 100:
			delay = 0.1 - speed * 0.001
			if self.turn == 0:
				for i in range(ELBOW_DEF_PER, percentage) :
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


class Wrist(object):
	"""
	goes from clockwise to counter-clockwise with low to high values

	NOTE
	can move beyond its max value manually but not programmatically,
	must be a mechanical manufacturing issue
	"""
	min_pulse_width = 150
	max_pulse_width = 600

	def __init__(self, channel, debug=False, turn = 0):
		"""
		initialize the object
		"""
		self.mg996r = MG996R(channel, min_pulse_width=Wrist.min_pulse_width, max_pulse_width=Wrist.max_pulse_width)
		self.turn = turn
		
	def set_position(self, percentage, speed=75):
		"""
		used to reset position of arm component
		"""
		if 0 <= percentage <= 100:
			self.position = percentage
			self.mg996r.set_specific_angle(percentage)
		delay = 1 - speed * 0.01
		time.sleep(delay)


class Gripper(object):
	"""
	opens and closes with low to high values
	"""
	min_pulse_width = 420
	max_pulse_width = 570

	def __init__(self, channel, debug=False, turn = 0):
		"""
		initialize the object
		"""
		self.mg996r = MG996R(channel, min_pulse_width=Gripper.min_pulse_width, max_pulse_width=Gripper.max_pulse_width)
		self.turn = turn
		
	def set_position(self, percentage, speed=75):
		"""
		used to reset position of arm component
		"""
		if (0 <= percentage <= 100):
			self.position = percentage
			self.mg996r.set_specific_angle(percentage)
		delay = 1 - speed * 0.01
		time.sleep(delay)
		
if __name__ == "__main__":
	print("this is a library file meant to be imported, not run")

	
	