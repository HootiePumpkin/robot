#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
import readchar
import sys
import time

import controller as controller

sys.dont_write_bytecode = True

"""
def reset_arm(base, shoulder, elbow, wrist, gripper):
    # extend to 45 degrees
    base.set_position_res(percentage = 58, speed = 75)
    shoulder.set_position_res(30, speed = 75)
    elbow.set_position_res(20, speed = 75)
    wrist.set_position(90, speed = 75)
    gripper.set_position(50, speed = 75)
    time.sleep(0.1)
"""

def main():
    
    arm = controller.Arm()
    arm.reset()

if __name__ == '__main__':
    main()
