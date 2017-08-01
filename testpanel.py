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
		tk.Tk.wm_title(self, "GreatFET Test Panel")
		tk.Tk.geometry(self, '{}x{}'.format(1250, 960))
		tk.Tk.resizable(self, width=False, height=False)

		menuBar = PanelMenu(self)
		self.config(menu=menuBar)
		toolbar = PanelToolbar(self)
		canvas = PanelCanvas(self)
		status = StatusBar(self)

	def openOptions(self):
		options = PinOptions(self)

		
	def doNothing(self):
		print("do nothing")

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

class PanelMenu(tk.Menu):
	def __init__(self, parent):
		tk.Menu.__init__(self, parent)
		subMenu = tk.Menu(self, tearoff=0)							# tearoff removes the dotted line "button" located at 0
		self.add_cascade(label="File", menu=subMenu) 				# subMenu will appear as the dropdown under File
		subMenu.add_command(label="New Project", command=self.doNothing)
		subMenu.add_command(label="New", command=self.doNothing)
		subMenu.add_separator()
		subMenu.add_command(label="Exit", command=self.quit)

		editMenu = tk.Menu(self, tearoff=0)
		self.add_cascade(label="Edit", menu=editMenu)
		editMenu.add_command(label="Redo", command=self.doNothing)

	def doNothing(self):
		print("do nothing")

	def quit(self):
		sys.exit(0)

class PanelToolbar(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		self.config(bg="white")
		insertButton = tk.Button(self, text="Test Toolbar Question Button", command=self.questionFunc)
		insertButton.pack(side=tk.LEFT, padx=2, pady=2)			# pad 2 pixels in the x and y direction on the button
		printButton = tk.Button(self, text="Test Toolbar Button", command=self.doNothing)
		printButton.pack(side=tk.LEFT, padx=2, pady=2)
		self.pack(side=tk.TOP, fill=tk.X)
		#toolbar.grid(row=0, column=0, fill=column)

	def questionFunc(self):
		answer = tk.messagebox.askquestion('Question 1', 'Is your greatFET plugged in?')
		if answer == 'yes':
			print("congratulations")

	def doNothing(self):
		print("do nothing")

class PanelCanvas(tk.Canvas):
	def __init__(self, parent):
		tk.Canvas.__init__(self, parent)
		self.config(width=1250, height=910, bg='white')
		self.pack()
		self.board_image = tk.PhotoImage(file = 'greatBLUE.png')
		self.create_image(25, 0, image=self.board_image, anchor='nw')	# create an image (GreatFET) at position x, y on the canvas, anchored at the nw (top left) corner of the image

		# Pin Buttons
		self.pin_button1 = tk.Button(self, command=parent.knight_rider, 
								image=parent.black_button_image, highlightbackground='#afeeee', borderwidth=0)
		pin_button1_window = self.create_window(230, 44, window=self.pin_button1)	# create a button at x, y

		self.pin_button2 = tk.Button(self, command=parent.openOptions, 
								image=parent.black_button_image, highlightbackground='#afeeee', borderwidth=0)
		pin_button2_window = self.create_window(275, 44, window=self.pin_button2)	# create a button at x, y

class StatusBar(tk.Label):
	def __init__(self, parent):
		tk.Label.__init__(self, parent)
		self.config(text="Test Status Bar", bd=1, relief=tk.SUNKEN, anchor=tk.W)	# bd = border, SUNKEN is style, anchored West
		self.pack(side=tk.BOTTOM, fill=tk.X)

class PinOptions(tk.Toplevel):
	def __init__(self, parent):
		tk.Toplevel.__init__(self)
		self.title("Pin Options")
		self.geometry('400x300')
		self.resizable(width=False, height=False)
		self.config(bg='white')
		#self.pin_button1.config(image=self.red_button_image)

panel = TestPanel()
panel.mainloop()
