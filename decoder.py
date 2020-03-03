#!/usr/bin/env python3      

# portable system imports
from sys import argv
from os.path import abspath, realpath, dirname
from site import addsitedir

# local imports
addsitedir(dirname(realpath(abspath(argv[0]))))

# exports
class BenEaterDecoder(object):

    def __init__(self, cpu):
        self.cpu = cpu

    def disable_all(self):
        for reg in self.cl['reg'].keys():
            for line in ["ie", "oe"]:
                self.cl['reg'][reg][line].write(False)

    def decode(self, instruction, verbose=False):
        self.disable_all()
        if instruction is None or instruction == 0:
            if verbose: print("0: Halt")
            self.cpu.control_lines['hlt'].write(True)
            return

# main
if __name__ == "__main__":
    from sys import path as pylib

    print(pylib)
    raise RuntimeError("this is meant to be imported")

