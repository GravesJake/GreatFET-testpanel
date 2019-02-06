#!/usr/bin/env python3

import hardware
import json

import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QLabel, QPushButton, QRadioButton, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
    
        self.init_ui()
        
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
        h = 32
        w = 32
        x_offset = 43
        y_offset = 41
        self.j1_buttons = []
        self.j2_buttons = []
        self.j7_buttons = []

        # J1/J2/J7 Buttons
        x = 190
        ports = 3
        columns = 20
        rows = 2

        for i in range(ports):
            if i == 0:
                y = 843
                buttons = self.j1_buttons
            if i == 1:
                y = 68
                buttons = self.j2_buttons
            if i == 2:
                y = 112
                buttons = self.j7_buttons
                rows = 1
            for j in range(columns):
                for k in range(rows):
                    button = QPushButton('', self)
                    button.resize(w+4,h+4)
                    button.setIcon(QIcon('icons/black_button.png'))
                    button.setIconSize(QSize(w,h))
                    button.move(x,y)
                    buttons.append(button)
                    y -= y_offset
                y += y_offset*rows
                x += x_offset
            x -= x_offset*20

    def init_buttons_functions(self):
        for i, pin_button in enumerate(self.j1_buttons, start=1):
            if i not in hardware.j1.unclickable_pins:
                pin_button.clicked.connect(self.make_handle_button(hardware.j1, i))

        for i, pin_button in enumerate(self.j2_buttons, start=1):
            if i not in hardware.j2.unclickable_pins:
                pin_button.clicked.connect(self.make_handle_button(hardware.j2, i))

        for i, pin_button in enumerate(self.j7_buttons, start=1):
            if i not in hardware.j7.unclickable_pins:
                pin_button.clicked.connect(self.make_handle_button(hardware.j7, i))

    # factory function to handle different port/pin combinations for buttons
    def make_handle_button(self, port, pin):
        def handle_button():
            print("handle_button")
            print(port)
            print(pin)
            self.dialog = OptionsWindow(port, pin)
            self.dialog.show()
        return handle_button


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
    
    def set_output(self, port, pin):
        hardware.set_output_pin(port, pin)                 # configure board
        
    def set_high(self, port, pin):
        hardware.set_pin_high(port, pin)

    def set_low(self, port, pin):
        hardware.set_pin_low(port, pin)

# this feels weird not being inside of a class and using self
def center(self):
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())

        
def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

