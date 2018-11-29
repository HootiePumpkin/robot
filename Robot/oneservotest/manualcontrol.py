import readchar
import sys
import time

import oneservocontrol as controller
from reset_arm import reset_arm
from pynput import keyboard

sys.dont_write_bytecode = True

def move_as(base, char):
	speed = 100
	if char == 's':
		base.set_position_res(base.position - 1, speed)
		print (base.position)
	elif char == 'f':
		base.set_position_res(base.position + 1, speed)
		print (base.position)
		
	else:
		pass

def main(): 
	arm = controller.Arm()
	arm.reset()
	
	def on_press(key):
		nkey = str(key)
		if nkey[1:2] == 'a':
			move_as(base, nkey[1:2])
		if nkey[1:2] == 'd':
			move_as(base, nkey[1:2])
	def on_release(key):
		nkey = str(key)
		if nkey[1:2] == 'f':
			sys.exit()
			
	with keyboard.Listener(on_press = on_press, on_release = on_release) as listener:
		listener.join()
	
if __name__ == '__main__':
	main()
	
	