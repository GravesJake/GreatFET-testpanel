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
		tk.Tk.__init__(self)
		self.black_button_image = tk.PhotoImage(file='black_button.png')
		self.green_button_image = tk.PhotoImage(file='green_button.png')
		self.green_zero_button_image = tk.PhotoImage(file='green_zero_button.png')
		self.green_one_button_image = tk.PhotoImage(file='green_one_button.png')
		self.red_button_image = tk.PhotoImage(file='red_button.png')
		self.red_zero_button_image = tk.PhotoImage(file='red_zero_button.png')
		self.red_one_button_image = tk.PhotoImage(file='red_one_button.png')

		# initialize the window
		self.wm_title("GreatFET Test Panel")
		self.geometry('1250x960')
		self.resizable(width=False, height=False)

		menubar = PanelMenu(self)
		self.config(menu=menubar)
		toolbar = PanelToolbar(self)
		self.canvas = PanelCanvas(self)
		status = StatusBar(self)

		self.gf = GreatFET()

	def open_options(self, port, pin):
		self.options = PinOptionsWindow(self, port, pin)

	def turn_on(self, port, pin):
		print("turn pin on")
		self.options.input_button.config(state='normal'), 
		self.options.output_button.config(state='normal')

	def turn_off(self, port, pin):
		print("turn pin off")
		canvas_buttons = self.canvas.buttons[port]
		canvas_buttons[pin].config(image=self.black_button_image)

		self.options.input_button.config(state='disabled'), 
		self.options.output_button.config(state='disabled')

	def set_input(self, port, pin):
		print("set pin to input")
		pin_attr = "P%d" % pin
		if port in globals():	# look for J1, J2, or J7 in globals all at once instead of checking individually
			# this will avoid the need to have three separate button mappings (one for each port)
			canvas_buttons = self.canvas.buttons[port]
			canvas_buttons[pin].config(image=self.green_button_image)

			if port == 'J1' and hasattr(J1, pin_attr):		# look for the pin in J1
				gf_pin = getattr(J1, pin_attr)
				self.gf.gpio.setup(gf_pin, Directions.IN)	# set the corresponding pin to input
				state = self.gf.gpio.input(gf_pin)			# read the state of the pin, low or high

			elif port == 'J2' and hasattr(J2, pin_attr):
				gf_pin = getattr(J2, pin_attr)
				self.gf.gpio.setup(gf_pin, Directions.IN)	# set the corresponding pin to input
				state = self.gf.gpio.input(gf_pin)			# read the state of the pin, low or high

			elif port == 'J7' and hasattr(J7, pin_attr):
				gf_pin = getattr(J7, pin_attr)
				self.gf.gpio.setup(gf_pin, Directions.IN)	# set the corresponding pin to input
				state = self.gf.gpio.input(gf_pin)			# read the state of the pin, low or high

			if state:
					canvas_buttons[pin].config(image=self.green_one_button_image)	# set image high
			else:
				canvas_buttons[pin].config(image=self.green_zero_button_image)		# set image low

		self.options.one_button.config(state='disabled')
		self.options.zero_button.config(state='disabled')

	def set_output(self, port, pin):
		print("set pin to output")
		pin_attr = "P%d" % pin
		if port in globals():
			canvas_buttons = self.canvas.buttons[port]

			if port == 'J1' and hasattr(J1, pin_attr):		# look for the pin in J1
				gf_pin = getattr(J1, pin_attr)
				self.gf.gpio.setup(gf_pin, Directions.OUT)	# set the corresponding pin to output

			elif port == 'J2' and hasattr(J2, pin_attr):
				gf_pin = getattr(J2, pin_attr)
				self.gf.gpio.setup(gf_pin, Directions.OUT)	# set the corresponding pin to output

			elif port == 'J7' and hasattr(J7, pin_attr):
				gf_pin = getattr(J7, pin_attr)
				self.gf.gpio.setup(gf_pin, Directions.OUT)	# set the corresponding pin to output

		canvas_buttons[pin].config(image=self.red_button_image)	# set image to output
		self.options.one_button.config(state='normal')
		self.options.zero_button.config(state='normal')

	def set_high(self, port, pin):
		print("set output high")
		pin_attr = "P%d" % pin
		if port in globals():
			canvas_buttons = self.canvas.buttons[port]

			if port == 'J1' and hasattr(J1, pin_attr):		# look for the pin in J1
				gf_pin = getattr(J1, pin_attr)
				self.gf.gpio.output(gf_pin, 1)	# set the corresponding pin's output to high

			elif port == 'J2' and hasattr(J2, pin_attr):
				gf_pin = getattr(J2, pin_attr)
				self.gf.gpio.output(gf_pin, 1)	# set the corresponding pin's output to high

			elif port == 'J7' and hasattr(J7, pin_attr):
				gf_pin = getattr(J7, pin_attr)
				self.gf.gpio.output(gf_pin, 1)	# set the corresponding pin's output to high

			canvas_buttons[pin].config(image=self.red_one_button_image)	# set image high

	def set_low(self, port, pin):
		print("set output low")
		pin_attr = "P%d" % pin
		if port in globals():
			canvas_buttons = self.canvas.buttons[port]

			if port == 'J1' and hasattr(J1, pin_attr):		# look for the pin in J1
				gf_pin = getattr(J1, pin_attr)
				self.gf.gpio.output(gf_pin, 0)	# set the corresponding pin's output to high

			elif port == 'J2' and hasattr(J2, pin_attr):
				gf_pin = getattr(J2, pin_attr)
				self.gf.gpio.output(gf_pin, 0)	# set the corresponding pin's output to high

			elif port == 'J7' and hasattr(J7, pin_attr):
				gf_pin = getattr(J7, pin_attr)
				self.gf.gpio.output(gf_pin, 0)	# set the corresponding pin's output to high

			canvas_buttons[pin].config(image=self.red_zero_button_image)	# set image high

	def knight_rider(self):
		gf = GreatFET()
		gf.vendor_request_out(vendor_requests.HEARTBEAT_STOP)
		gf.vendor_request_out(vendor_requests.GPIO_REGISTER, value=0, data=[3, 14, 2, 1, 3, 13, 3, 12])

		def set_led(gf, lednum, state):
		    gf.vendor_request_out(vendor_requests.GPIO_WRITE, data=[lednum, int(not(state))])

		pattern = [0, 1, 2, 3, 2, 1, 0]
		for led in pattern:
			set_led(gf, led, True)
			time.sleep(0.1)
			set_led(gf, led, False)

	def do_nothing(self):
		print("TestPanel do nothing")


class PanelMenu(tk.Menu):
	def __init__(self, parent):
		tk.Menu.__init__(self, parent)
		sub_menu = tk.Menu(self, tearoff=0)							# tearoff removes the dotted line "button" located at 0
		self.add_cascade(label="File", menu=sub_menu) 				# sub_menu will appear as the dropdown under File
		sub_menu.add_command(label="New Project", command=parent.do_nothing)
		sub_menu.add_command(label="New", command=parent.do_nothing)
		sub_menu.add_separator()
		sub_menu.add_command(label="Exit", command=quit)

		edit_menu = tk.Menu(self, tearoff=0)
		self.add_cascade(label="Edit", menu=edit_menu)
		edit_menu.add_command(label="Redo", command=parent.do_nothing)

	def quit(self):
		sys.exit(0)


class PanelToolbar(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		question_button = tk.Button(self, text="Test Toolbar Question Button", command=self.question_func)
		question_button.pack(side=tk.LEFT, padx=2, pady=2)			# pad 2 pixels in the x and y direction on the button
		print_button = tk.Button(self, text="Knight Rider", command=parent.knight_rider)
		print_button.pack(side=tk.LEFT, padx=2, pady=2)
		self.pack(side=tk.TOP, fill=tk.X)

	def question_func(self):
		answer = tk.messagebox.askquestion('Question 1', 'Is your greatFET plugged in?')
		if answer == 'yes':
			print("congratulations")
		else:
			print("you should probably plug it in")


class PanelCanvas(tk.Canvas):
	def __init__(self, parent):
		tk.Canvas.__init__(self, parent)
		self.config(width=1250, height=910, bg='white')
		self.pack()
		self.board_image = tk.PhotoImage(file = 'greatBLUE.png')
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
		unclickable_pins = (1, 4, 5, 9, 10 , 11, 12, 19, 20)

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
		self.config(text="Test Status Bar", bd=1, relief=tk.SUNKEN, anchor='w')	# bd = border, SUNKEN is style, anchored West
		self.pack(side=tk.BOTTOM, fill=tk.X)


class PinOptionsWindow(tk.Toplevel):
	def __init__(self, parent, port, pin):
		tk.Toplevel.__init__(self)
		self.title("Pin Options")
		self.geometry("140x110")
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
panel.mainloop()
