# Mar 7 2015

import RPi.GPIO as GPIO

PASS = 0
TURN_LEFT = 1
TURN_RIGHT = 2
FIRE = 3

READY = 2
CMDA = 3
CMDB = 4
CMD0 = 17
CMD1 = 27
CMD2 = 22
CMD3 = 10
pin_list = [CMDA, CMDB, CMD0, CMD1, CMD2, CMD3]


def gpio_setup():
    """ Define all the GPIO pins and prepare them for use.
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(READY, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    for pin in pin_list:
        GPIO.setup(pin, GPIO.out)
    pass


def send_command(arg):
    """ Send a command to Vex Cortex via GPIO pins.

        This is the function for generating the bit codes for output
        based on the given command to the function, and defining which pins to
        write them to.
        See code for pinout and protocol definition, subject to change.

        Params:
            arg - <tuple(int)> Command value and parameter to write to Cortex.
    """

    if arg[0] == 3:
        bit_arr = [(x,True) for x in pin_list[:2]] \
                + [(y,False) for y in pin_list[2:]]
    elif arg[0] == 2 or arg[0] == 3:
        bit_list = [int(x) for x in bin(arg[0] - 1)[2:]] \
                + [int(y) for y in bin(arg[1])[2:]]
        bit_arr = list(zip(pin_list, bit_list))
    else:
        bit_arr = [(x,False) for x in pin_list]

    for i in bit_arr:
        GPIO.output(i[0], i[1])


def read_ready():
    """ Read the ready signal from the Cortex.

        Returns:
            false if Cortex is busy executing command, else true
    """
    return GPIO.input(READY)
    # return GPIO.wait_for_edge(READY, GPIO.RISING)