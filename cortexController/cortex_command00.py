# Mar 7 2015

import RPi.GPIO as GPIO

PASS = 0
TURN_LEFT = 1
TURN_RIGHT = 2
FIRE = 3

def send_command(arg):
    """ Send a command to Vex Cortex via GPIO pins.

        This is the function for generating the bit codes for output
        based on the given command to the function, and defining which pins to
        write them to.
        See code for pinout and protocol definition, subject to change.

        Params:
            arg - <List<int>> keyval(s) and parameters of command to be executed.
    """

    bits = []


    write_pins(bit_arr)

def write_pins(bits):
    """ Set the given GPIO pins to their respective on/off values.

        This is the mechanical part of the code, just dumbly setting the
        GPIO pins it's told to

        Params:
            bits - <List<2-tuple>> GPIO pin # and desired set value pairs to write
    """

    pass