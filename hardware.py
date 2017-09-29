#!/usr/bin/env python3

from greatfet import GreatFET
from greatfet.peripherals.gpio import J1, J2, J7, Directions
from greatfet.protocol import vendor_requests

class Board():
	def __init__(self, ports=[]):
		self.ports = ports


class Port():
	def __init__(self, name, gf_port, size, unclickable_pins=[]):
		self.pins = {}
		self.unclickable_pins = unclickable_pins
		for i in range(1, size):
			if i not in self.unclickable_pins:
				self.pins[i] = Pin(i, self, gf_port) # pin number needs to be a string


class Pin():
	def __init__(self, number, port, gf_port, mode=0, state=0):
		self.name = "P%d" % number
		self.number = number	# this is a string
		self.tuple = getattr(gf_port, self.name)
		self.port = port 
		self.mode = mode		# input/output
		self.state = state 		# high/low


j1 = Port('J1', J1, 40, (1,2,11,36,38))
j2 = Port('J2', J2, 40, (1,2,5,11,12,17,21,26,32,39,40))
j7 = Port('J7', J7, 20, (1,4,5,9,10,11,12,19,20))

b = Board((j1, j2, j7))
print("j1 pins tuple type")
print(type(j1.pins[3].tuple[0])) # tuple is made of two ints
print(j1.pins[3].tuple)

def _init_board(self):
	print('initializing board')
	for pin in j1.pins:		# pin is a string
		self.gf.gpio.setup(j1.pins[pin].tuple, Directions.IN)	# set the corresponding pin to input
		self.state = self.gf.gpio.input(j1.pins[pin].tuple)			# read the state of the pin, low or high
		j1.pins[pin].state = self.gf.gpio.input(j1.pins[pin].tuple)
		#self.j1_input_pins[pin_num] = self.state 			# store input pins for polling

	for pin in j2.pins:
		#print("j gf_pin type", type(gf_pin[0]))	# gf_pin is made of two ints, why does the new method not work?
		self.gf.gpio.setup(j2.pins[pin].tuple, Directions.IN)	# set the corresponding pin to input
		self.state = self.gf.gpio.input(j2.pins[pin].tuple)			# read the state of the pin, low or high
		#self.j2_input_pins[pin_num] = self.state 			# store input pins for polling

	for pin in j7.pins:
		self.gf.gpio.setup(j7.pins[pin].tuple, Directions.IN)	# set the corresponding pin to input
		self.state = self.gf.gpio.input(j7.pins[pin].tuple)			# read the state of the pin, low or high
		#self.j7_input_pins[pin_num] = self.state 			# store input pins for polling

def set_greatfet_input(self, port, pin):
	self.gf.gpio.setup(port.pins[pin].tuple, Directions.IN)
	port.pins[pin].mode = 0 			# 0 for input
	return port.pins[pin].state 		# not sure if this is still needed, leftover from pre-redesign
	#return self.state

def set_greatfet_output(self, port, pin):
	self.gf.gpio.setup(port.pins[pin].tuple, Directions.OUT)
	port.pins[pin].mode = 1 			# 1 for output

def set_greatfet_high(self, port, pin):
	self.gf.gpio.output(port.pins[pin].tuple, 1)
	port.pins[pin].state = 1 	# high

def set_greatfet_low(self, port, pin):
	self.gf.gpio.output(port.pins[pin].tuple, 0)
	port.pins[pin].state = 0 	#low
