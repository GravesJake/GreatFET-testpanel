#!/usr/bin/env python3

from tkinter import *
import tkinter.messagebox

from PIL import Image, ImageTk

def doNothing():
	print("do nothing")

window = Tk()
window.wm_title("greatFET Test Panel")
window.geometry('{}x{}'.format(1250, 960))
window.resizable(width=False, height=False)

# Message Box
#tkinter.messagebox.showinfo('Window Title', 'GSG is greeeeeeat')

def questionFunc():
	answer = tkinter.messagebox.askquestion('Question 1', 'Is your greatFET plugged in?')
	if answer == 'yes':
		print("congratulations")

load = Image.open('greatBLUE.png')
render = ImageTk.PhotoImage(load)

img = Label(image=render)
img.image = render
img.place(x=0, y=32)

# Main Menu
menu = Menu(window)
window.config(menu=menu)

subMenu = Menu(menu, tearoff=0)							# tearoff removes the annoying dotted line "button" located at 0
menu.add_cascade(label="File", menu=subMenu) 			# subMenu will appear as the dropdown under File

subMenu.add_command(label="New Project", command=doNothing)
subMenu.add_command(label="New", command=doNothing)
subMenu.add_separator()
subMenu.add_command(label="Exit", command=window.quit)

editMenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Redo", command=doNothing)


# Toolbar
toolbar = Frame(window, bg="blue")
insertButton = Button(toolbar, text="Test Toolbar Question Button", command=questionFunc)
insertButton.pack(side=LEFT, padx=2, pady=2)			# pad 2 pixels in the x and y direction on the button
printButton = Button(toolbar, text="Test Toolbar Button", command=doNothing)
printButton.pack(side=LEFT, padx=2, pady=2)
toolbar.pack(side=TOP, fill=X)


# Status Bar
status = Label(window, text="Test Status Bar", bd=1, relief=SUNKEN, anchor=W)	# bd = border, SUNKEN is style, anchored West
status.pack(side=BOTTOM, fill=X)


window.mainloop() # make it stay open
