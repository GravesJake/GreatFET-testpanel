#!/usr/bin/env python3

from greatfet.peripherals.gpio import J1, J2, J7, Directions

class Board():
	def __init__(self, ports=[]):
		self.ports = ports


class Port():
	def __init__(self, name, gf_port, size, unclickable_pins=[]):
		self.name = name
		self.pins = {}
		self.unclickable_pins = unclickable_pins
		for i in range(1, size):
			if i not in self.unclickable_pins:
				self.pins[i] = Pin(i, self, gf_port) # pin number needs to be a string


class Pin():
	def __init__(self, number, port, gf_port, mode=0, state=0):
		self.name = "P%d" % number
		self.tuple = getattr(gf_port, self.name)
		self.port = port 
		self.mode = mode		# input/output (0,1)
		self.state = state 		# high/low (1, 0)


j1 = Port('J1', J1, 40, (1,2,11,36,38))
j2 = Port('J2', J2, 40, (1,2,5,11,12,17,21,26,32,39,40))
j7 = Port('J7', J7, 20, (1,4,5,9,10,11,12,19,20))

b = Board((j1, j2, j7))

def _init_board(self):
	for port in b.ports:
		for pin in port.pins:
			self.gf.gpio.setup(port.pins[pin].tuple, Directions.IN)	# set the corresponding pin to input
			port.pins[pin].state = self.gf.gpio.input(port.pins[pin].tuple)
			port.pins[pin].mode = 0 # 0 for input
			
def set_greatfet_input(self, port, pin):	# set a pin as input
	self.gf.gpio.setup(port.pins[pin].tuple, Directions.IN)
	port.pins[pin].mode = 0 			# 0 for input
	port.pins[pin].state = self.gf.gpio.input(port.pins[pin].tuple) # read the high/low state from the board (True/False)

def set_greatfet_output(self, port, pin):	# set a pin as output
	self.gf.gpio.setup(port.pins[pin].tuple, Directions.OUT)
	port.pins[pin].mode = 1 			# 1 for output

def set_greatfet_high(self, port, pin):	# set an output pin to high
	self.gf.gpio.output(port.pins[pin].tuple, 1)	# 1 for high
	port.pins[pin].state = True 	# high

def set_greatfet_low(self, port, pin):	# set an output pin to low
	self.gf.gpio.output(port.pins[pin].tuple, 0)	# 0 for low
	port.pins[pin].state = False 	#low

# create a JSON compatible version of the board
def serialize_board(self): 
	all_pins = []
	port_pins = []
	for port in b.ports:
		for pin in port.pins:
			if port.pins[pin].mode == 0:		# input pin
				port_pins.append({"port" : port.name, "pin" : "P%d" % (pin), "pin_mode" : "input"})#port.pins[pin].mode})
				# dictionary containing input pin info
			if port.pins[pin].mode == 1:		# output pin
				# dictionary containing output pin info (includes high/low state)
				port_pins.append({"port" : port.name, "pin" : "P%d" % (pin), "pin_mode" : "output", "pin_state" : port.pins[pin].state})
	
		all_pins.append(port_pins)
		port_pins = []		# reset the pin list on each new GreatFET Port

	return all_pins
