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
    
        self.initUI()
        
    def initUI(self):               
        self.setWindowTitle('GreatFET Test Panel')

        label = QLabel(self)
        pixmap = QPixmap('icons/greatBLUE.png')
        label.setPixmap(pixmap)
        
        self.resize(pixmap.width(), pixmap.height())
        self.initButtons()
        center(self)
        self.show()

    def initButtons(self):
        h = 32
        w = 32
        x_offset = 43
        y_offset = 41
        self.j1_buttons = [None]
        self.j2_buttons = [None]
        self.j7_buttons = [None]

        # J1/J2/J7 Buttons
        x = 190
        ports = 3
        columns = 20
        rows = 2
        for i in range(ports):
            if i is 0:
                y = 802
                buttons = self.j1_buttons
            if i is 1:
                y = 27
                buttons = self.j2_buttons
            if i is 2:
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
                    button.clicked.connect(self.handleButton)
                    buttons.append(button)
                    y += y_offset
                y -= y_offset*rows
                x += x_offset
            x -= x_offset*20

        print("J1 buttons:", len(self.j1_buttons))
        print("J2 buttons:", len(self.j2_buttons))
        print("J7 buttons:", len(self.j7_buttons))


    def handleButton(self):
        self.dialog = OptionsWindow()
        self.dialog.show()


class OptionsWindow(QWidget):
    def __init__(self, parent=None):
        super(OptionsWindow, self).__init__(parent)
        
        self.setWindowTitle("Pin Options")
        self.resize(200,200)
        center(self)

        layout = QVBoxLayout()
        input_button = QRadioButton('Input')
        output_button = QRadioButton('Output')
        high_button = QRadioButton('High')
        low_button = QRadioButton('Low')
        input_button.clicked.connect(self.set_input)
        output_button.clicked.connect(self.set_output)
        high_button.clicked.connect(self.set_high)
        low_button.clicked.connect(self.set_low)
        layout.addWidget(input_button)
        layout.addWidget(output_button)
        layout.addWidget(high_button)
        layout.addWidget(low_button)
        self.setLayout(layout)
        self.show()

    def set_input(self):
        hardware.set_input_pin(hardware.j2, 8)  # configure board
    
    def set_output(self):
        hardware.set_output_pin(hardware.j2, 8)                 # configure board
        
    def set_high(self):
        hardware.set_pin_high(hardware.j2, 8)

    def set_low(self, ):
        hardware.set_pin_low(hardware.j2, 8)

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

