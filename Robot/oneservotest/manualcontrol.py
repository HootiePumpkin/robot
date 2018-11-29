import readchar
import sys
import time

import oneservocontrol as controller
from reset_arm import reset_arm

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

		move_as(base, char)

		if char == 'r':
			reset_arm(base)

			for char in path:
				move_as(base, char)

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
				
				reset_arm(base)
				
				for char in path[0]:
					move_as(base, char)

				path = []


if __name__ == '__main__':
	main()
	
	