#!/usr/bin/env python3

from greatfet import GreatFET
from greatfet.peripherals.gpio import DIRECTION_IN, DIRECTION_OUT
from greatfet.boards.one import GreatFETOne

gf = GreatFET()


class Board():
    def __init__(self, ports={}):
        self.ports = ports


class Port():
    def __init__(self, name, size, unclickable_pins=[]):
        self.name = name
        self.pins = {}
        self.unclickable_pins = unclickable_pins
        for i in range(1, size):
            if i not in self.unclickable_pins:
                self.pins[i] = Pin(i, self) # pin number needs to be a string


class Pin():
    def __init__(self, number, port, mode=0, state=0):
        self.name = "P%d" % number
        self.number = number
        self.port = port 
        self.tuple = GreatFETOne.GPIO_MAPPINGS.get(port.name + "_" + self.name)
        self.mode = mode        # input/output (i, o)
        self.state = state      # high/low (1, 0)


j1 = Port('J1', 40, (1,2,11,36,38))
j2 = Port('J2', 40, (1,2,5,11,12,17,21,26,32,39,40))
j7 = Port('J7', 20, (1,4,5,9,10,11,12,19,20))
b = Board((j1, j2, j7))


# initialize the board: set all pins to input
def _init_board():
    for port in b.ports:
        for pin in port.pins:
            set_input_pin(port, pin)
            

# set a pin as input
def set_input_pin(port, pin):
    gf.gpio.set_up_pin(port.pins[pin].tuple, DIRECTION_IN)
    port.pins[pin].mode = "i" 
    port.pins[pin].state = gf.gpio.read_pin_state(port.pins[pin].tuple) # read the high/low state from the board (True/False)


# set a pin as output
def set_output_pin(port, pin):
    gf.gpio.set_up_pin(port.pins[pin].tuple, DIRECTION_OUT)
    port.pins[pin].mode = "o"   


# set an output pin high
def set_pin_high(port, pin):
    gf.gpio.set_pin_state(port.pins[pin].tuple, 1) # 1 for high
    port.pins[pin].state = True             # high


# set an output pin low
def set_pin_low(port, pin):
    gf.gpio.set_pin_state(port.pins[pin].tuple, 0) # 0 for low
    port.pins[pin].state = False            #low

