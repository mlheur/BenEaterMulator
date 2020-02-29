#!/usr/bin/env python3      

# portable system imports
from sys import argv
from os.path import abspath, realpath, dirname
from site import addsitedir

# local imports
addsitedir(dirname(realpath(abspath(argv[0]))))

# exports
class BenEaterDecoder(object):

    def __init__(self, control_lines, bus):
        self.cl = control_lines
        self.bus = bus

    def disable_all(self):
        for reg in self.cl['reg'].keys():
            for line in ["ie", "oe"]:
                self.cl['reg'][reg][line].write(False)

    def decode(self, instruction, verbose=False):
        self.disable_all()
        if instruction is None or instruction == 0:
            if verbose: print("0 halt")
            self.cl['hlt'].write(True)
            return
        if instruction == 1:
            if verbose: print("1 A register reads from the bus")
            self.cl['reg']["A"]['ie'].write(True)
            return
        if instruction == 2:
            if verbose: print("2 A register writes to the bus")
            self.cl['reg']["A"]['oe'].write(True)
            return
        if instruction == 3:
            if verbose: print("3 Write 'Hello' to the bus")
            self.bus.write("Hello")
            return
        if instruction == 4:
            if verbose: print("4 Write 'Goodbye' to the bus")
            self.bus.write("Goodbye")
            return
        if instruction == 5:
            if verbose: print("5 B register reads from the bus")
            self.cl['reg']["B"]['ie'].write(True)
            return
        if instruction == 6:
            if verbose: print("6 B register writes to the bus")
            self.cl['reg']["B"]['oe'].write(True)
            return
        if instruction == 7:
            if verbose: print("7 Copy A to B")
            self.cl['reg']["A"]['oe'].write(True)
            self.cl['reg']["B"]['ie'].write(True)
            return
        if instruction == 8:
            if verbose: print("8 Copy B to A")
            self.cl['reg']["A"]['ie'].write(True)
            self.cl['reg']["B"]['oe'].write(True)
            return

# main
if __name__ == "__main__":
    from sys import path as pylib

    print(pylib)
    raise RuntimeError("this is meant to be imported")

