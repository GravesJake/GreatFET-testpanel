#!/usr/bin/env python3

import sys
import tkinter as tk
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk

# GreatFET 
import time
from greatfet import GreatFET
from greatfet.peripherals.gpio import J1, J2, J7, Directions
from greatfet.protocol import vendor_requests

class TestPanel(tk.Tk):
	def __init__(self):
		self.ports = {'J1': J1, 'J2': J2, 'J7': J7}

		tk.Tk.__init__(self)
		self.black_button_image = tk.PhotoImage(file='icons/black_button.png')
		self.green_button_image = tk.PhotoImage(file='icons/green_button.png')
		self.green_zero_button_image = tk.PhotoImage(file='icons/green_zero_button.png')
		self.green_one_button_image = tk.PhotoImage(file='icons/green_one_button.png')
		self.red_button_image = tk.PhotoImage(file='icons/red_button.png')
		self.red_zero_button_image = tk.PhotoImage(file='icons/red_zero_button.png')
		self.red_one_button_image = tk.PhotoImage(file='icons/red_one_button.png')

		# initialize the window
		self.wm_title("GreatFET Test Panel")
		self.geometry('1250x960')
		self.resizable(width=False, height=False)

		menubar = PanelMenu(self)
		self.config(menu=menubar)
		toolbar = PanelToolbar(self)
		self.canvas = PanelCanvas(self)
		self.status = StatusBar(self)

		self.j1_input_pins = {}		# used for board polling
		self.j2_input_pins = {}
		self.j7_input_pins = {}

		self.gf = GreatFET()

	def open_options(self, port, pin):
		self.options = PinOptionsWindow(self, port, pin)

	def turn_on(self, port, pin):
		self.status.config(text="Turn Pin On")
		self.options.input_button.config(state='normal'), 
		self.options.output_button.config(state='normal')

	def turn_off(self, port, pin):
		self.status.config(text="Turn Pin Off")
		self.canvas_buttons = self.canvas.buttons[port]
		self.canvas_buttons[pin].config(image=self.black_button_image)

		self.options.input_button.config(state='disabled'), 
		self.options.output_button.config(state='disabled')

	def set_input(self, port, pin):
		self.status.config(text="Set Pin to Input")
		pin_attr = "P%d" % pin
		if port in self.ports:	# look for J1, J2, or J7 in globals all at once instead of checking individually
			# this will avoid the need to have three separate button mappings (one for each port)
			self.canvas_buttons = self.canvas.buttons[port]
			self.canvas_buttons[pin].config(image=self.green_button_image)

			if port == 'J1' and hasattr(J1, pin_attr):		# look for the pin in J1
				gf_pin = getattr(J1, pin_attr)
				self.gf.gpio.setup(gf_pin, Directions.IN)	# set the corresponding pin to input
				state = self.gf.gpio.input(gf_pin)			# read the state of the pin, low or high
				self.j1_input_pins[pin] = state 			# store input pins for polling
				print(self.j1_input_pins)

			elif port == 'J2' and hasattr(J2, pin_attr):
				gf_pin = getattr(J2, pin_attr)
				self.gf.gpio.setup(gf_pin, Directions.IN)	# set the corresponding pin to input
				state = self.gf.gpio.input(gf_pin)			# read the state of the pin, low or high
				self.j2_input_pins[pin] = state 			# store input pins for polling
				print(self.j2_input_pins)

			elif port == 'J7' and hasattr(J7, pin_attr):
				gf_pin = getattr(J7, pin_attr)
				self.gf.gpio.setup(gf_pin, Directions.IN)	# set the corresponding pin to input
				state = self.gf.gpio.input(gf_pin)			# read the state of the pin, low or high
				self.j7_input_pins[pin] = state 			# store input pins for polling
				print(self.j7_input_pins)

			if state:
				self.canvas_buttons[pin].config(image=self.green_one_button_image)	# set image high
			else:
				self.canvas_buttons[pin].config(image=self.green_zero_button_image)		# set image low

		self.options.one_button.config(state='disabled')
		self.options.zero_button.config(state='disabled')

	def set_output(self, port, pin):
		self.status.config(text="Set Pin to Output")
		pin_attr = "P%d" % pin
		if port in self.ports:
			self.canvas_buttons = self.canvas.buttons[port]

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

		self.canvas_buttons[pin].config(image=self.red_button_image)	# set image to output
		self.options.one_button.config(state='normal')
		self.options.zero_button.config(state='normal')

	def set_high(self, port, pin):
		self.status.config(text="Set Output Pin to High")
		pin_attr = "P%d" % pin
		obj = self.ports[port]
		if hasattr(obj, pin_attr):
			gf_pin = getattr(obj, pin_attr)
			self.gf.gpio.output(gf_pin, 1)	# set the corresponding pin's output to high
			self.canvas_buttons[pin].config(image=self.red_one_button_image)	# set image high

	def set_low(self, port, pin):
		'''port is a string like "J1", pin is an int like 5 for P5'''
		self.status.config(text="Set Output Pin to Low")
		pin_attr = "P%d" % pin
		
		self.canvas_buttons = self.canvas.buttons[port]
		self.canvas_buttons[pin].config(image=self.red_zero_button_image)	# set image high

		obj = self.ports[port]
		if hasattr(obj, pin_attr):
			gf_pin = getattr(obj, pin_attr)
			self.gf.gpio.output(gf_pin, 0)	# set the corresponding pin's output to high

	def get_state(self, j1_pins, j2_pins, j7_pins):
		for pin in j1_pins:
			pin_num = int(pin)
			pin_attr = "P%d" % pin_num			
			gf_j1_pin = getattr(J1, pin_attr)
			state = self.gf.gpio.input(gf_j1_pin)	# read the state of the pin, low or high
			if state:
				self.canvas.j1_buttons[pin].config(image=self.green_one_button_image)		# set image high
			else:
				self.canvas.j1_buttons[pin].config(image=self.green_zero_button_image)		# set image low

		for pin in j2_pins:
			pin_num = int(pin)
			pin_attr = "P%d" % pin_num			
			gf_j2_pin = getattr(J2, pin_attr)
			state = self.gf.gpio.input(gf_j2_pin) 	# read the state of the pin, low or high
			if state:
				self.canvas.j2_buttons[pin].config(image=self.green_one_button_image)		# set image high
			else:
				self.canvas.j2_buttons[pin].config(image=self.green_zero_button_image)		# set image low

		for pin in j7_pins:
			pin_num = int(pin)
			pin_attr = "P%d" % pin_num		
			gf_j7_pin = getattr(J7, pin_attr)
			state = self.gf.gpio.input(gf_j7_pin)	# read the state of the pin, low or high
			if state:
				self.canvas.j7_buttons[pin].config(image=self.green_one_button_image)		# set image high
			else:
				self.canvas.j7_buttons[pin].config(image=self.green_zero_button_image)		# set image low

		self.after(100, self.get_state, j1_pins, j2_pins, j7_pins)

	def knight_rider(self):
		self.status.config(text="David Hasselhoff")
		led1 = (3, 14)
		led2 = (2, 1)
		led3 = (3, 13)
		led4 = (3, 12)

		for led in (led1, led2, led3, led4):
			self.gf.gpio.setup(led, Directions.OUT)

		pattern = (led1, led2, led3, led4, led3, led2, led1)
		for led in pattern:
			self.gf.gpio.output(led, False) # on
			time.sleep(0.1)
			self.gf.gpio.output(led, True) # on

	def do_nothing(self):
		print("TestPanel do nothing")


class PanelMenu(tk.Menu):
	def __init__(self, parent):
		tk.Menu.__init__(self, parent)
		sub_menu = tk.Menu(self, tearoff=0)							# tearoff removes the dotted line "button" located at 0
		self.add_cascade(label="File", menu=sub_menu) 				# sub_menu will appear as the dropdown under File
		sub_menu.add_separator()
		sub_menu.add_command(label="Exit", command=quit)

		edit_menu = tk.Menu(self, tearoff=0)
		self.add_cascade(label="Edit", menu=edit_menu)

	def quit(self):
		sys.exit(0)


class PanelToolbar(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		knight_rider_button = tk.Button(self, text="Knight Rider", command=parent.knight_rider)
		knight_rider_button.pack(side=tk.LEFT, padx=2, pady=2)
		self.pack(side=tk.TOP, fill=tk.X)


class PanelCanvas(tk.Canvas):
	def __init__(self, parent):
		tk.Canvas.__init__(self, parent)
		self.config(width=1250, height=910, bg='white')
		self.pack()
		self.board_image = tk.PhotoImage(file = 'icons/greatBLUE.png')
		self.create_image(25, 5, image=self.board_image, anchor='nw')	# create an image (GreatFET) at position x, y on the canvas, anchored at the nw (top left) corner of the image

		self._init_j1_buttons(parent)
		self._init_j2_buttons(parent)
		self._init_j7_buttons(parent)
		self._init_button_dict()

	def _init_j1_buttons(self, parent):
		j1 = 'J1'
		self.j1_buttons = [None]		# pin numbers start at 1
		x_coord = 233
		x_offset = 43	# pins are 43 pixels apart on the x axis
		y_coord = 865
		y_offset = 41 	# pins are 41 pixels apart on the y axis
		pin_num = 1	
		unclickable_pins = (1,2,11,36,38)

		for i in range(20):
			for j in range(2):
				self.j1_buttons.append(tk.Button(self, command=lambda pin_num=pin_num: parent.open_options(j1, pin_num), image=parent.black_button_image,
									highlightbackground='#afeeee', borderwidth=0))
				if pin_num not in unclickable_pins:
					self.create_window(x_coord, y_coord, window=self.j1_buttons[pin_num])
				y_coord -= y_offset
				pin_num += 1
			x_coord += x_offset
			y_coord = 865

	def _init_j2_buttons(self, parent):
		j2 = 'J2'
		self.j2_buttons = [None]			# pin numbers start at 1
		x_coord = 233	
		x_offset = 43	# pins are 43 pixels apart on the x axis
		y_coord = 90	
		y_offset = 41 	# pins are 41 pixels apart on the y axis
		pin_num = 1
		unclickable_pins = (1,2,5,11,12,17,21,26,32,39,40)
		
		for i in range(20):
			for j in range(2):
				self.j2_buttons.append(tk.Button(self, command=lambda pin_num=pin_num: parent.open_options(j2, pin_num), image=parent.black_button_image,
										highlightbackground='#afeeee', borderwidth=0))
				if pin_num not in unclickable_pins:	
					self.create_window(x_coord, y_coord, window=self.j2_buttons[pin_num])
				y_coord -= y_offset
				pin_num += 1
			x_coord += x_offset
			y_coord = 90

	def _init_j7_buttons(self, parent):
		j7 = 'J7'
		self.j7_buttons = [None]		# pin numbers start at 1
		x_coord = 233
		x_offset = 43	# pins are 43 pixels apart on the x axis
		y_coord = 135
		pin_num = 1
		unclickable_pins = (1,4,5,9,10,11,12,19,20)

		for i in range(20):
			self.j7_buttons.append(tk.Button(self, command=lambda pin_num=pin_num: parent.open_options(j7, pin_num), image=parent.black_button_image,
								highlightbackground='#afeeee', borderwidth=0))
			if pin_num not in unclickable_pins:
				self.create_window(x_coord, y_coord, window=self.j7_buttons[pin_num])
			pin_num += 1
			x_coord += x_offset

	def _init_button_dict(self):
		self.buttons = {'J1': self.j1_buttons,
						'J2': self.j2_buttons,
						'J7': self.j7_buttons}

	def print_num(self, header, pin):
		print(header, ' p', pin, sep='')


class StatusBar(tk.Label):
	def __init__(self, parent):
		tk.Label.__init__(self, parent)
		self.config(text="", bd=1, relief=tk.SUNKEN, anchor='w')	# bd = border, SUNKEN is style, anchored West
		self.pack(side=tk.BOTTOM, fill=tk.X)


class PinOptionsWindow(tk.Toplevel):
	def __init__(self, parent, port, pin):
		tk.Toplevel.__init__(self)
		x = parent.winfo_x()
		y = parent.winfo_y()
		x_offset = 20
		y_offset = 100
		w = 140
		h = 110

		self.title("Pin Options")
		self.geometry("%dx%d+%d+%d" % (w, h, x + x_offset, y + y_offset)) # set size and position of window
		self.resizable(width=False, height=False)
		self.grab_set()	# prevents the main window from opening more windows while this one is open

		# on/off buttons
		p = tk.IntVar()	# power
		m = tk.IntVar()	# mode
		v = tk.IntVar() # i/o value

		# create pin options buttons
		self.on_button = tk.Radiobutton(self, text="On", variable=p, value=1, 
											command=lambda: parent.turn_on(port, pin))
		
		self.off_button = tk.Radiobutton(self, text="Off", variable=p, value=0, 
											command=lambda: parent.turn_off(port, pin))
		
		self.input_button = tk.Radiobutton(self, text="Input", state='disabled', variable=m, value=1, 
											command=lambda: parent.set_input(port, pin))
		
		self.output_button = tk.Radiobutton(self, text="Output", state='disabled', variable=m, value=0, 
											command=lambda: parent.set_output(port, pin))
		
		self.one_button = tk.Radiobutton(self, text="1", state='disabled', variable=v, value=1, 
											command=lambda: parent.set_high(port, pin))
		
		self.zero_button = tk.Radiobutton(self, text="0", state='disabled', variable=v, value=0, 
											command=lambda: parent.set_low(port, pin))
		
		self.okay_button = tk.Button(self, text="Ok", command=self.destroy)

		# place buttons on pin options window
		self.on_button.grid(row=0, column=0, sticky='w')
		self.off_button.grid(row=0, column=1, sticky='w')
		self.input_button.grid(row=1, column=0, pady=5, sticky='w')
		self.output_button.grid(row=1, column=1, sticky='w')
		self.one_button.grid(row=2, column=0, sticky='w')
		self.zero_button.grid(row=2, column=1, sticky='w')
		self.okay_button.grid(row=3, column=1, pady=5, sticky='se')

panel = TestPanel()
panel.after(100, panel.get_state(panel.j1_input_pins, panel.j2_input_pins, panel.j7_input_pins)) # keep window updated based on GreatFET physical pins
panel.mainloop()
