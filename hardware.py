#!/usr/bin/env python3

from greatfet import GreatFET
from greatfet.peripherals.gpio import J1, J2, J7, Directions
from greatfet.protocol import vendor_requests


def _init_board(self):
	print('initializing board')
	j1_pins = [pin for pin in dir(J1) if pin.startswith("P")]
	j2_pins = [pin for pin in dir(J2) if pin.startswith("P")]
	j7_pins = [pin for pin in dir(J7) if pin.startswith("P")]

	for pin in j1_pins:
		pin_str = ''.join(ch for ch in pin if ch.isdigit())
		pin_num = int(pin_str)
		gf_pin = getattr(J1, pin)
		self.gf.gpio.setup(gf_pin, Directions.IN)	# set the corresponding pin to input
		self.state = self.gf.gpio.input(gf_pin)			# read the state of the pin, low or high
		self.j1_input_pins[pin_num] = self.state 			# store input pins for polling

	for pin in j2_pins:
		pin_str = ''.join(ch for ch in pin if ch.isdigit())
		pin_num = int(pin_str)
		gf_pin = getattr(J2, pin)
		self.gf.gpio.setup(gf_pin, Directions.IN)	# set the corresponding pin to input
		state = self.gf.gpio.input(gf_pin)			# read the state of the pin, low or high
		self.j2_input_pins[pin_num] = self.state 			# store input pins for polling

	for pin in j7_pins:
		pin_str = ''.join(ch for ch in pin if ch.isdigit())
		pin_num = int(pin_str)
		gf_pin = getattr(J7, pin)
		self.gf.gpio.setup(gf_pin, Directions.IN)	# set the corresponding pin to input
		self.state = self.gf.gpio.input(gf_pin)			# read the state of the pin, low or high
		self.j7_input_pins[pin_num] = self.state 			# store input pins for polling

def set_greatfet_input(self, port, pin):
	pin_attr = "P%d" % pin
	if port in self.ports:	# look for J1, J2, or J7 in globals all at once instead of checking individually
		if port == 'J1' and hasattr(J1, pin_attr):		# look for the pin in J1
			if pin not in self.j1_input_pins:
				gf_pin = getattr(J1, pin_attr)
				self.gf.gpio.setup(gf_pin, Directions.IN)	# set the corresponding pin to input
				self.state = self.gf.gpio.input(gf_pin)			# read the state of the pin, low or high
				self.j1_input_pins[pin] = self.state 			# store input pins for polling

		elif port == 'J2' and hasattr(J2, pin_attr):
			if pin not in self.j2_input_pins:
				gf_pin = getattr(J2, pin_attr)
				self.gf.gpio.setup(gf_pin, Directions.IN)	# set the corresponding pin to input
				self.state = self.gf.gpio.input(gf_pin)			# read the state of the pin, low or high
				self.j2_input_pins[pin] = self.state 			# store input pins for polling

		elif port == 'J7' and hasattr(J7, pin_attr):
			if pin not in self.j7_input_pins:
				gf_pin = getattr(J7, pin_attr)
				self.gf.gpio.setup(gf_pin, Directions.IN)	# set the corresponding pin to input
				self.state = self.gf.gpio.input(gf_pin)			# read the state of the pin, low or high
				self.j7_input_pins[pin] = self.state 			# store input pins for polling

	return self.state

def set_greatfet_output(self, port, pin):
	pin_attr = "P%d" % pin
	if port in self.ports:
		

		if port == 'J1' and hasattr(J1, pin_attr):		# look for the pin in J1
			gf_pin = getattr(J1, pin_attr)
			self.gf.gpio.setup(gf_pin, Directions.OUT)	# set the corresponding pin to output
			if pin in self.j1_input_pins:
				self.j1_input_pins.pop(pin)		# remove pin from tracked input pins to avoid trying to read an output pin

		elif port == 'J2' and hasattr(J2, pin_attr):
			gf_pin = getattr(J2, pin_attr)
			self.gf.gpio.setup(gf_pin, Directions.OUT)	# set the corresponding pin to output
			if pin in self.j2_input_pins:
				self.j2_input_pins.pop(pin)		# remove pin from tracked input pins to avoid trying to read an output pin

		elif port == 'J7' and hasattr(J7, pin_attr):
			gf_pin = getattr(J7, pin_attr)
			self.gf.gpio.setup(gf_pin, Directions.OUT)	# set the corresponding pin to output
			if pin in self.j7_input_pins:
				self.j7_input_pins.pop(pin)		# remove pin from tracked input pins to avoid trying to read an output pin

def set_greatfet_high(self, port, pin):
	pin_attr = "P%d" % pin
	# obj = self.ports[port]
	# if hasattr(obj, pin_attr):
	# 	gf_pin = getattr(obj, pin_attr)
	# 	self.gf.gpio.output(gf_pin, 1)	# set the corresponding pin's output to high
	# 	self.canvas_buttons[pin].config(image=self.red_one_button_image)	# set image high
	if port == 'J1' and hasattr(J1, pin_attr):
		gf_j1_pin = getattr(J1, pin_attr)
		self.gf.gpio.output(gf_j1_pin, 1)	# set the corresponding pin's output to high
		#self.canvas.j1_buttons[pin].config(image=self.red_one_button_image)	# set image high
		self.state = 1
		self.j1_output_pins[pin] = self.state 			# store input pins for polling

	if port == 'J2' and hasattr(J2, pin_attr):
		gf_j2_pin = getattr(J2, pin_attr)
		self.gf.gpio.output(gf_j2_pin, 1)	# set the corresponding pin's output to high
		#self.canvas.j2_buttons[pin].config(image=self.red_one_button_image)	# set image high
		self.state = 1
		self.j2_output_pins[pin] = self.state 			# store input pins for polling

	if port == 'J7' and hasattr(J7, pin_attr):
		gf_j7_pin = getattr(J7, pin_attr)
		self.gf.gpio.output(gf_j7_pin, 1)	# set the corresponding pin's output to high
		#self.canvas.j7_buttons[pin].config(image=self.red_one_button_image)	# set image high
		self.state = 1
		self.j7_output_pins[pin] = self.state 			# store input pins for polling

def set_greatfet_low(self, port, pin):
	pin_attr = "P%d" % pin
	
	''' v this was for avoiding checking for port string match cases, should try to revert to this v '''
	# self.canvas_buttons = self.canvas.buttons[port]
	# self.canvas_buttons[pin].config(image=self.red_zero_button_image)	# set image high

	# obj = self.ports[port]
	# if hasattr(obj, pin_attr):
	# 	gf_pin = getattr(obj, pin_attr)
	# 	self.gf.gpio.output(gf_pin, 0)	# set the corresponding pin's output to high
	''' ^ this was for avoiding checking for port string match cases, should try to revert to this ^ '''

	if port == 'J1' and hasattr(J1, pin_attr):
		gf_j1_pin = getattr(J1, pin_attr)
		self.gf.gpio.output(gf_j1_pin, 0)	# set the corresponding pin's output to high
		self.state = 0
		self.j1_output_pins[pin] = self.state 			# store input pins for polling

	if port == 'J2' and hasattr(J2, pin_attr):
		gf_j2_pin = getattr(J2, pin_attr)
		self.gf.gpio.output(gf_j2_pin, 0)	# set the corresponding pin's output to high
		self.state = 0
		self.j2_output_pins[pin] = self.state 			# store input pins for polling

	if port == 'J7' and hasattr(J7, pin_attr):
		gf_j7_pin = getattr(J7, pin_attr)
		self.gf.gpio.output(gf_j7_pin, 0)	# set the corresponding pin's output to high
		self.state = 0
		self.j7_output_pins[pin] = self.state 			# store input pins for polling