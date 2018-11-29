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
from reset_arm import reset_arm
from test_arm import test_arm


sys.dont_write_bytecode = True


def move_as(base, shoulder, elbow, wrist, gripper, char):
    speed = 100

    if char == 's':
        base.set_position_res(base.position - 1, speed)
        print (base.position)
    elif char == 'f':
        base.set_position_res(base.position + 1, speed)
        print (base.position)
    elif char == 'e':
        shoulder.set_position_res(shoulder.position + 1, speed)
        print (shoulder.position)
    elif char == 'd':
        shoulder.set_position_res(shoulder.position - 1, speed)
        print (shoulder.position)
    elif char == 'g':
        elbow.set_position_res(elbow.position - 1, speed)
        print (elbow.position)
    elif char == 't':
        elbow.set_position_res(elbow.position + 1, speed)
        print (elbow.position)
    elif char == 'u':
        wrist.set_position(wrist.position + 1, speed)
        print (wrist.position)
    elif char == 'i':
        wrist.set_position(wrist.position - 1, speed)
        print (wrist.position)
    elif char == 'j':
        gripper.set_position(gripper.position + 3, speed)
        print (gripper.position)
    elif char == 'k':
        gripper.set_position(gripper.position - 3, speed)
        print (gripper.position)
    elif char == ' ':
        if gripper.position == 0:
            gripper.set_position(100, speed)
        else:
            gripper.set_position(0, speed)
    else:
        pass

    # time.sleep(0.5)

def main():
    arm = controller.Arm()
    arm.reset()

    path = []
    while True:
    # for char in path:
        char = readchar.readchar()
        hex_char = hex(ord(char))

        if hex_char == '0x3':
            print("path followed: {}".format(path))

            print("received {} in hex, exiting".format(hex_char))

            sys.exit()

        print(char)

        path.append(char)

        move_as(arm.base, arm.shoulder, arm.elbow, warm.rist, arm.gripper, char)

        if char == 'r':
            reset_arm(arm.base, arm.shoulder, arm.elbow, warm.rist, arm.gripper)

            for char in path:
                move_as(arm.base, arm.shoulder, arm.elbow, warm.rist, arm.gripper, char)

            path = []
        elif char == 'v':
            # filename = 'path_' + str(datetime.datetime.now()).replace(' ', '_')[:-3] + '.txt'
            filename = 'path.txt'

            with open(filename, 'w') as f:
                f.write(''.join(path)[:-1])

        elif char == 'c':
            filename = 'path.txt'

            with open(filename, 'r') as f:
                path = f.readlines()
                print(path)

                reset_arm(arm.base, arm.shoulder, arm.elbow, warm.rist, arm.gripper)

                for char in path[0]:
                    move_as(arm.base, arm.shoulder, arm.elbow, warm.rist, arm.gripper, char)

                path = []


if __name__ == '__main__':
    main()

