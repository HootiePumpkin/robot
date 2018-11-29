#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import datetime
import readchar
import sys
import time

import oneservocontrol as controller
from oneservocontrol import channels

sys.dont_write_bytecode = True


def reset_arm(base):
	# extend to 45 degrees
	base.set_position_res(percentage = 58, speed = 75)
	time.sleep(0.1)
	
	
def main():
	
	arm = controller.Arm()
	arm.reset()

if __name__ == '__main__':
	main()
	