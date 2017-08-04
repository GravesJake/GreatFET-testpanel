#!/usr/bin/env python3

import sys
import tkinter as tk
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk

# GreatFET 
import time
from greatfet import GreatFET
from greatfet.protocol import vendor_requests

class TestPanel(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self.black_button_image = tk.PhotoImage(file='black_button.png')
		self.green_button_image = tk.PhotoImage(file='green_button.png')
		self.red_button_image = tk.PhotoImage(file='red_button.png')

		# initialize the window
		self.wm_title("GreatFET Test Panel")
		self.geometry('1250x960')
		self.resizable(width=False, height=False)

		menubar = PanelMenu(self)
		self.config(menu=menubar)
		toolbar = PanelToolbar(self)
		self.canvas = PanelCanvas(self)
		status = StatusBar(self)

	def open_options(self):
		options = PinOptions(self)
		
	def do_nothing(self):
		print("TestPanel do nothing")

	def knight_rider(self):
		gf = GreatFET()
		gf.vendor_request_out(vendor_requests.HEARTBEAT_STOP)
		gf.vendor_request_out(vendor_requests.REGISTER_GPIO, value=0, data=[14, 3, 1, 2, 13, 3, 12, 3])

		def set_led(gf, lednum, state):
		    gf.vendor_request_out(vendor_requests.WRITE_GPIO, data=[int(not(state)), lednum])

		pattern = [0, 1, 2, 3, 2, 1, 0]
		for led in pattern:
		    set_led(gf, led, True)
		    time.sleep(0.1)
		    set_led(gf, led, False)

	def change_red(self):
		print("change red")
		self.canvas.pin_button1.config(image=self.red_button_image)

	def change_green(self):
		print("change green")
		self.canvas.pin_button1.config(image=self.green_button_image)

	def change_black(self):
		print("change black")
		self.canvas.pin_button1.config(image=self.black_button_image)


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
		self.config(bg="white")
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

	def _init_j1_buttons(self, parent):
		j1 = 'j1'
		self.j1_buttons = [None]		# pin numbers start at 1
		x_coord = 233
		x_offset = 43	# pins are 43 pixels apart on the x axis
		y_coord = 865
		y_offset = 41 	# pins are 41 pixels apart on the y axis
		pin_num = 1	
		unclickable_pins = (1,2,11,36,38)

		for i in range(20):
			for j in range(2):
				self.j1_buttons.append(tk.Button(self, command=lambda pin_num=pin_num: self.print_num(j1, pin_num), image=parent.black_button_image,
									highlightbackground='#afeeee', borderwidth=0))
				# skip button creation on unusable pins: 1, 2, 11, 36, 38

				if pin_num not in unclickable_pins:
					self.create_window(x_coord, y_coord, window=self.j1_buttons[pin_num])
				y_coord -= y_offset
				pin_num += 1
			x_coord += x_offset
			y_coord = 865

	def _init_j2_buttons(self, parent):
		j2 = 'j2'
		self.j2_buttons = [None]			# pin numbers start at 1
		x_coord = 233	
		x_offset = 43	# pins are 43 pixels apart on the x axis
		y_coord = 90	
		y_offset = 41 	# pins are 41 pixels apart on the y axis
		pin_num = 1
		unclickable_pins = (1,2,5,11,12,17,21,26,32,39,40)
		
		for i in range(20):
			for j in range(2):
				self.j2_buttons.append(tk.Button(self, command=lambda pin_num=pin_num: self.print_num(j2, pin_num), image=parent.black_button_image,
										highlightbackground='#afeeee', borderwidth=0))
				# skip button creation on unusable pins: 1, 2, 11, 36, 38
				if pin_num not in unclickable_pins:	
					self.create_window(x_coord, y_coord, window=self.j2_buttons[pin_num])
				y_coord -= y_offset
				pin_num += 1
			x_coord += x_offset
			y_coord = 90

	def _init_j7_buttons(self, parent):
		j7 = 'j7'
		self.j7_buttons = [None]		# pin numbers start at 1
		x_coord = 233
		x_offset = 43	# pins are 43 pixels apart on the x axis
		y_coord = 135
		pin_num = 1
		unclickable_pins = (1, 4, 5, 9, 10 , 11, 12, 19, 20)

		for i in range(20):
			self.j7_buttons.append(tk.Button(self, command=lambda pin_num=pin_num: self.print_num(j7, pin_num), image=parent.black_button_image,
								highlightbackground='#afeeee', borderwidth=0))
			if pin_num not in unclickable_pins:
				self.create_window(x_coord, y_coord, window=self.j7_buttons[pin_num])
			pin_num += 1
			x_coord += x_offset

	def print_num(self, header, pin):
		print(header, ' p', pin, sep='')


class StatusBar(tk.Label):
	def __init__(self, parent):
		tk.Label.__init__(self, parent)
		self.config(text="Test Status Bar", bd=1, relief=tk.SUNKEN, anchor='w')	# bd = border, SUNKEN is style, anchored West
		self.pack(side=tk.BOTTOM, fill=tk.X)


class PinOptions(tk.Toplevel):
	def __init__(self, parent):
		tk.Toplevel.__init__(self)
		self.title("Pin Options")
		self.geometry("200x160")
		self.configure(bg="white")

		# on/off buttons
		p = tk.IntVar()
		m = tk.IntVar()
		self.on_button = tk.Radiobutton(self, text="On", bg='white', variable=p, value=1, command=parent.do_nothing)
		self.on_button.pack(anchor='nw', padx=5, pady=5)
		self.off_button = tk.Radiobutton(self, text="Off", bg='white', variable=p, value=0, command=parent.change_black)
		self.off_button.pack(anchor='nw', padx=5, pady=5)
		self.input_button = tk.Radiobutton(self, text="Input", bg='white', variable=m, value=1, command=parent.change_green)
		self.input_button.pack(anchor='ne', padx=5, pady=5)
		self.output_button = tk.Radiobutton(self, text="Output", bg='white', variable=m, value=0, command=parent.change_red)
		self.output_button.pack(anchor='ne', padx=5, pady=5)

		self.okay_button = tk.Button(self, text="Ok", command=self.destroy)
		self.okay_button.pack(anchor='se', padx=5, pady=10)

	def set_input(self):
		print("input")

	def quit(self):
		print("quit")

panel = TestPanel()
panel.mainloop()
