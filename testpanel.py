#!/usr/bin/env python3

import hardware
import json

import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QLabel, QPushButton, QRadioButton, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize, QTimer


class PanelWindow(QWidget):
    def __init__(self, parent=None):
        super(PanelWindow, self).__init__(parent)
    
        hardware._init_board()
        self.init_ui()

    j1_buttons = [None]
    j2_buttons = [None]
    j7_buttons = [None]
        
    def init_ui(self):               
        self.setWindowTitle('GreatFET Test Panel')

        label = QLabel(self)
        pixmap = QPixmap('icons/greatBLUE.png')
        label.setPixmap(pixmap)
        
        self.resize(pixmap.width(), pixmap.height())
        self.init_buttons_ui()
        self.init_buttons_functions()
        center(self)
        self.show()

    def init_buttons_ui(self):
        # J1/J2/J7 button values
        h = 32
        w = 32
        x = 190
        x_offset = 43
        y_offset = 41
        num_of_ports = 3

        for port_num in range(num_of_ports):
            if port_num == 0:
                y = 843
                current_buttons = PanelWindow.j1_buttons
            elif port_num == 1:
                y = 68
                current_buttons = PanelWindow.j2_buttons
            elif port_num == 2:
                y = 112
                current_buttons = PanelWindow.j7_buttons

            for button_pair in range(20):
                button = QPushButton('', self)
                button.resize(w+4,h+4)
                button.setIcon(QIcon('icons/black_button.png'))
                button.setIconSize(QSize(w,h))
                button.move(x,y)
                current_buttons.append(button)
                if port_num != 2:
                    y -= y_offset
                    button = QPushButton('', self)
                    button.resize(w+4,h+4)
                    button.setIcon(QIcon('icons/black_button.png'))
                    button.setIconSize(QSize(w,h))
                    button.move(x,y)
                    current_buttons.append(button)
                    y += y_offset
                x += x_offset
            x -= x_offset*20

        PanelWindow.buttons = { 'J1': PanelWindow.j1_buttons,
                                'J2': PanelWindow.j2_buttons,
                                'J7': PanelWindow.j7_buttons}

        self.get_board_state()

    def init_buttons_functions(self):
        for i, pin_button in enumerate(PanelWindow.j1_buttons):
            if i not in hardware.j1.unclickable_pins and i != 0:
                pin_button.clicked.connect(self.make_handle_button(hardware.j1, i))

        for i, pin_button in enumerate(PanelWindow.j2_buttons):
            if i not in hardware.j2.unclickable_pins and i != 0:
                pin_button.clicked.connect(self.make_handle_button(hardware.j2, i))

        for i, pin_button in enumerate(PanelWindow.j7_buttons):
            if i not in hardware.j7.unclickable_pins and i != 0:
                pin_button.clicked.connect(self.make_handle_button(hardware.j7, i))

    # factory function to handle different port/pin combinations for buttons
    def make_handle_button(self, port, pin):
        def handle_button():
            self.dialog = OptionsWindow(port, pin)
            self.dialog.show()
        return handle_button

    def get_board_state(self):
        for port in hardware.b.ports:   # look through all the ports on the board
            for pin in port.pins:       # look through all the pins in each port
                if port.pins[pin].mode == "i": # i for input pins
                    port.pins[pin].state = hardware.gf.gpio.input(port.pins[pin].tuple) # read/set the state of the input pins (High/Low)
                    if port.pins[pin].state == True:
                        PanelWindow.buttons[port.name][pin].setIcon(QIcon('icons/green_one_button.png'))
                    else:
                        PanelWindow.buttons[port.name][pin].setIcon(QIcon('icons/green_zero_button.png'))
                

class OptionsWindow(QWidget):
    def __init__(self, port, pin, parent=None):
        super(OptionsWindow, self).__init__(parent)
        
        self.setWindowTitle("Pin Options")
        self.resize(200,200)
        center(self)

        layout = QVBoxLayout()
        input_button = QRadioButton('Input')
        output_button = QRadioButton('Output')
        high_button = QRadioButton('High')
        low_button = QRadioButton('Low')
        input_button.clicked.connect(lambda: self.set_input(port, pin))
        output_button.clicked.connect(lambda: self.set_output(port, pin))
        high_button.clicked.connect(lambda: self.set_high(port, pin))
        low_button.clicked.connect(lambda: self.set_low(port, pin))
        layout.addWidget(input_button)
        layout.addWidget(output_button)
        layout.addWidget(high_button)
        layout.addWidget(low_button)
        self.setLayout(layout)
        self.show()

    def set_input(self, port, pin):
        hardware.set_input_pin(port, pin)  # configure board

        # change the image on the button
        if port.pins[pin].state == True:
            PanelWindow.buttons[port.name][pin].setIcon(QIcon('icons/green_one_button.png'))
        else:
            PanelWindow.buttons[port.name][pin].setIcon(QIcon('icons/green_zero_button.png'))
    
    def set_output(self, port, pin):
        hardware.set_output_pin(port, pin)                 # configure board
        PanelWindow.buttons[port.name][pin].setIcon(QIcon('icons/red_button.png'))

        
    def set_high(self, port, pin):
        hardware.set_pin_high(port, pin)
        PanelWindow.buttons[port.name][pin].setIcon(QIcon('icons/red_one_button.png'))

    def set_low(self, port, pin):
        hardware.set_pin_low(port, pin)
        PanelWindow.buttons[port.name][pin].setIcon(QIcon('icons/red_zero_button.png'))


# this feels weird not being inside of a class and using self
def center(self):
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())

        
def main():
    app = QApplication(sys.argv)
    panel = PanelWindow()
    timer = QTimer()
    timer.timeout.connect(panel.get_board_state)
    timer.start(100)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

