#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog
import hardware
import json


class TestPanel(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.black_button_image       = tk.PhotoImage(file='icons/black_button.png')
        self.green_button_image       = tk.PhotoImage(file='icons/green_button.png')
        self.green_zero_button_image  = tk.PhotoImage(file='icons/green_zero_button.png')
        self.green_one_button_image   = tk.PhotoImage(file='icons/green_one_button.png')
        self.red_button_image         = tk.PhotoImage(file='icons/red_button.png')
        self.red_zero_button_image    = tk.PhotoImage(file='icons/red_zero_button.png')
        self.red_one_button_image     = tk.PhotoImage(file='icons/red_one_button.png')
        self.icon_image               = tk.PhotoImage(file='icons/gsg.png')
        self.help_image               = tk.PhotoImage(file='icons/help_icon.png')

        # initialize the window
        w = 1250
        h = 930
        menubar = PanelMenu(self)
        self.wm_title("GreatFET Test Panel")        
        self.tk.call('wm', 'iconphoto', self._w, self.icon_image)
        # REVERT 500 BACK TO 0
        self.geometry("%dx%d+%d+%d" % (w, h, 500, 0)) # set size and position of window
        self.resizable(width=False, height=False)
        self.config(menu=menubar)
        self.canvas = PanelCanvas(self)
        self.status = StatusBar(self)
        
        hardware._init_board()

    def open_options(self, port, pin):
        self.options = PinOptionsWindow(self, port, pin)

    def open_help_menu(self):
        self.help_menu = HelpMenuWindow(self)

    def reset_board(self):
        hardware._init_board()

    def set_input(self, port, pin, file_flag):
        hardware.set_input_pin(port, pin)  # configure board
        self.set_input_image(port, pin, file_flag)                  # update UI

    def set_input_image(self, port, pin, file_flag):
        self.status.config(text="%s Pin %d set to Input" % (port.name, pin))
        self.canvas.buttons[port.name][pin].config(image=self.green_button_image)

        if port.pins[pin].state == True:        
            self.canvas.buttons[port.name][pin].config(image=self.green_one_button_image)   # set image high
        else:
            self.canvas.buttons[port.name][pin].config(image=self.green_zero_button_image)      # set image low

        # this doesn't need to happen when configuring pins from file so check for that
        if file_flag is False:
            self.options.one_button.config(state='disabled')
            self.options.zero_button.config(state='disabled')

    def set_output(self, port, pin, file_flag):
        hardware.set_output_pin(port, pin)                 # configure board
        self.set_output_image(port, pin, file_flag)                             # update UI

    def set_output_image(self, port, pin, file_flag):
        self.status.config(text="%s Pin %d set to Output" % (port.name, pin))
        self.canvas.buttons[port.name][pin].config(image=self.red_button_image) # set image to output

        # this doesn't need to happen when configuring pins from file
        if file_flag is False:
            self.options.one_button.config(state='normal')
            self.options.zero_button.config(state='normal')

    def set_high(self, port, pin):
        hardware.set_pin_high(port, pin)
        self.set_high_image(port, pin)

    def set_high_image(self, port, pin):
        self.status.config(text="%s Output Pin %d set to High" % (port.name, pin))
        self.canvas.buttons[port.name][pin].config(image=self.red_one_button_image) # set image high

    def set_low(self, port, pin):
        hardware.set_pin_low(port, pin)
        self.set_low_image(port, pin)

    def set_low_image(self, port, pin):
        self.status.config(text="%s Output Pin %d set to Low" % (port.name, pin))
        self.canvas.buttons[port.name][pin].config(image=self.red_zero_button_image)    # set image low

    # might want to separate this out further into a separate hardware funtion
    def get_board_state(self):
        for port in hardware.b.ports:   # look through all the ports on the board
            for pin in port.pins:       # look through all the pins in each port
                if port.pins[pin].mode == "i": # i for input pins
                    port.pins[pin].state = hardware.gf.gpio.input(port.pins[pin].tuple) # read/set the state of the input pins (High/Low)
                    if port.pins[pin].state == True: # True for high
                        self.canvas.buttons[port.name][pin].config(image=self.green_one_button_image) # port.name is a string linked to an actual hardware port
                    else:               # False for low
                        self.canvas.buttons[port.name][pin].config(image=self.green_zero_button_image)
        self.after(100, self.get_board_state)   # poll the board every 100ms

    def save_project(self):
        all_pins = self.serialize_board()
        config_file = filedialog.asksaveasfile(mode='w', defaultextension='.json')
        if config_file is None:
            return
        config_file.truncate(0)                     # clear the file each time we have to save to it
        json.dump(all_pins, config_file, indent=4)  # dump the JSON version of the board config to file
        config_file.close()
        self.status.config(text="Configuration saved to file")

    def load_project(self):
        config_file = filedialog.askopenfile(initialdir = "/GreatFET-testpanel",title = "Select File",filetypes = (("JSON files","*.json"),("all files","*.*")))
        if config_file is None:
            return
        loaded_pins = json.load(config_file)
        config_file.close()
        hardware._init_board()
        self.deserialize_board(loaded_pins)
        self.status.config(text="Configuration loaded from file")

    # create a JSON compatible version of the board
    def serialize_board(self): 
        json_ports = {"J1" : [], "J2" : [], "J7" : []}
        for port in hardware.b.ports:
            for pin in port.pins:
                json_ports[port.name].append({"pin_number" : port.pins[pin].number, "pin_mode" : port.pins[pin].mode, "pin_state" : port.pins[pin].state})
        return json_ports

    def deserialize_board(self, loaded_board):
        for loaded_port, loaded_pins in loaded_board.items():   # J1, J2, J3 are keys, the value for each is a list of dictionaries
            for loaded_pin in loaded_pins:      # each dictionary in the list of pins
                if loaded_port == "J1":
                    if loaded_pin["pin_mode"] == "i":
                        self.set_input(hardware.j1, loaded_pin["pin_number"], True)
                    if loaded_pin["pin_mode"] == "o":
                        self.set_output(hardware.j1, loaded_pin["pin_number"], True)
                        if loaded_pin["pin_state"] == True:
                            self.set_high(hardware.j1, loaded_pin["pin_number"])
                        else:
                            self.set_low(hardware.j1, loaded_pin["pin_number"])
                if loaded_port == "J2":
                    if loaded_pin["pin_mode"] == "i":
                        self.set_input(hardware.j2, loaded_pin["pin_number"], True)
                    if loaded_pin["pin_mode"] == "o":
                        self.set_output(hardware.j2, loaded_pin["pin_number"], True)
                        if loaded_pin["pin_state"] == True:
                            self.set_high(hardware.j2, loaded_pin["pin_number"])
                        else:
                            self.set_low(hardware.j2, loaded_pin["pin_number"])
                if loaded_port == "J7":
                    if loaded_pin["pin_mode"] == "i":
                        self.set_input(hardware.j7, loaded_pin["pin_number"], True)
                    if loaded_pin["pin_mode"] == "o":
                        self.set_output(hardware.j7, loaded_pin["pin_number"], True)
                        if loaded_pin["pin_state"] == True:
                            self.set_high(hardware.j7, loaded_pin["pin_number"])
                        else:
                            self.set_low(hardware.j7, loaded_pin["pin_number"])


class PanelMenu(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        file_menu = tk.Menu(self, tearoff=0)                        # tearoff removes the dotted line "button" located at 0
        self.add_cascade(label="File", menu=file_menu)              # sub_menu will appear as the dropdown under File
        file_menu.add_command(label="Save Project", command=parent.save_project)
        file_menu.add_command(label="Load Project", command=parent.load_project)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        edit_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Reset Board", command=parent.reset_board)
        self.add_command(label="Help", command=parent.open_help_menu)


class PanelCanvas(tk.Canvas):
    def __init__(self, parent):
        tk.Canvas.__init__(self, parent)
        self.config(width=1250, height=910, bg='white')
        self.pack()
        self.board_image = tk.PhotoImage(file = 'icons/greatBLUE.png')
        self.create_image(25, 5, image=self.board_image, anchor='nw')   # create an image (GreatFET) at position x, y on the canvas, anchored at the nw (top left) corner of the image

        self._init_j1_buttons(parent)
        self._init_j2_buttons(parent)
        self._init_j7_buttons(parent)
        self._init_button_dict()

    def _init_j1_buttons(self, parent):
        j1 = hardware.j1
        self.j1_buttons = [None]        # pin numbers start at 1
        x_coord = 233
        x_offset = 43   # pins are 43 pixels apart on the x axis
        y_coord = 865
        y_offset = 41   # pins are 41 pixels apart on the y axis
        pin_num = 1 

        for i in range(20):
            for j in range(2):
                self.j1_buttons.append(tk.Button(self, command=lambda pin_num=pin_num: parent.open_options(j1, pin_num), image=parent.black_button_image,
                                    highlightbackground='#afeeee', borderwidth=0))
                if pin_num not in j1.unclickable_pins:
                    self.create_window(x_coord, y_coord, window=self.j1_buttons[pin_num])
                y_coord -= y_offset
                pin_num += 1
            x_coord += x_offset
            y_coord = 865

    def _init_j2_buttons(self, parent):
        j2 = hardware.j2
        self.j2_buttons = [None]        # pin numbers start at 1
        x_coord = 233   
        x_offset = 43   # pins are 43 pixels apart on the x axis
        y_coord = 90    
        y_offset = 41   # pins are 41 pixels apart on the y axis
        pin_num = 1
        
        for i in range(20):
            for j in range(2):
                self.j2_buttons.append(tk.Button(self, command=lambda pin_num=pin_num: parent.open_options(j2, pin_num), image=parent.black_button_image,
                                        highlightbackground='#afeeee', borderwidth=0))
                if pin_num not in j2.unclickable_pins:  
                    self.create_window(x_coord, y_coord, window=self.j2_buttons[pin_num])
                y_coord -= y_offset
                pin_num += 1
            x_coord += x_offset
            y_coord = 90

    def _init_j7_buttons(self, parent):
        j7 = hardware.j7
        self.j7_buttons = [None]        # pin numbers start at 1
        x_coord = 233
        x_offset = 43   # pins are 43 pixels apart on the x axis
        y_coord = 135
        pin_num = 1

        for i in range(20):
            self.j7_buttons.append(tk.Button(self, command=lambda pin_num=pin_num: parent.open_options(j7, pin_num), image=parent.black_button_image,
                                highlightbackground='#afeeee', borderwidth=0))
            if pin_num not in j7.unclickable_pins:
                self.create_window(x_coord, y_coord, window=self.j7_buttons[pin_num])
            pin_num += 1
            x_coord += x_offset

    def _init_button_dict(self):
        self.buttons = {'J1': self.j1_buttons,
                        'J2': self.j2_buttons,
                        'J7': self.j7_buttons}
        self.addtag_all("all")

    def on_resize(self, event):
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.config(width=self.width, height=self.height)
        self.scale("all",0,0,wscale,hscale)


class StatusBar(tk.Label):
    def __init__(self, parent):
        tk.Label.__init__(self, parent)
        self.config(text="", bd=1, relief=tk.SUNKEN, anchor='w')
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
        self.geometry("%dx%d+%d+%d" % (w, h, x + x_offset, y + y_offset))
        self.resizable(width=False, height=False)
        self.grab_set()                     # prevent the main window from opening more windows while this one is open
        self.attributes("-topmost", True)   # force pin options popup window to stay on top
        self.tk.call('wm', 'iconphoto', self._w, parent.black_button_image)

        m = tk.IntVar() # mode
        v = tk.IntVar() # i/o value

        # create pin options buttons
        self.input_button = tk.Radiobutton(self, text="Input", state='normal', variable=m, value=1, 
                                            command=lambda: parent.set_input(port, pin, False))
        
        self.output_button = tk.Radiobutton(self, text="Output", state='normal', variable=m, value=0, 
                                            command=lambda: parent.set_output(port, pin, False))
        
        self.one_button = tk.Radiobutton(self, text="High", state='disabled', variable=v, value=1, 
                                            command=lambda: parent.set_high(port, pin))
        
        self.zero_button = tk.Radiobutton(self, text="Low", state='disabled', variable=v, value=0, 
                                            command=lambda: parent.set_low(port, pin))
        
        self.okay_button = tk.Button(self, text="Ok", command=self.destroy)

        # place buttons on pin options window
        self.input_button.grid(row=1, column=0, pady=5, sticky='w')
        self.output_button.grid(row=1, column=1, sticky='w')
        self.one_button.grid(row=2, column=0, sticky='w')
        self.zero_button.grid(row=2, column=1, sticky='w')
        self.okay_button.grid(row=3, column=1, pady=5, sticky='se')


class HelpMenuWindow(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self)
        x = parent.winfo_x()
        y = parent.winfo_y()
        x_offset = 20
        y_offset = 100
        w = 470
        h = 310

        self.title("Help")
        self.geometry("%dx%d+%d+%d" % (w, h, x + x_offset, y + y_offset))
        self.resizable(width=False, height=False)
        self.grab_set()
        self.attributes("-topmost", True)
        self.tk.call('wm', 'iconphoto', self._w, parent.help_image)

        help_message = """Welcome to the GreatFET Test Panel!

Here you will be able to configure any usable pin on the GreatFET and get realtime visual feedback.

- Input pins are shown by the green indicators and Output pins are shown in red.

- All usable pins on the board are initialized to Input on startup.

- You'll notice 1's and 0's on each indicator. This is the current value on the pin (high/low).
    
- Clicking on a pin will open up an options window for that pin, allowing you to configure it how you like.

- Setting pins to input will allow you to get values from things like buttons.

- Setting pins to output will allow you to set that pin to high or low and do things like toggle LEDs.

- If you have your pins configured in a way you'd like to reuse later, you can go to the File menu and save it and load it back in later."""

        msg = tk.Message(self, text=help_message)
        msg.pack()

panel = TestPanel()
panel.after(100, panel.get_board_state())   # poll the board every 100ms
panel.mainloop()
