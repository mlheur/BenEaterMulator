#!/usr/bin/env python3      

# portable system imports
from sys import argv
from os.path import abspath, realpath, dirname
from site import addsitedir

# local imports
addsitedir(dirname(realpath(abspath(argv[0]))))
from component import Component

# exports
class ALU(Component):

    def __init__(self, abus, bbus, obus, subenable, oenable, carryin, carryout):
        super().__init__(self, None, obus, None, oenable)
        del self.ienable
        del self.ibus
        self.subenable = subenable
        self.carryin = carryin
        self.carryout = carryout

    def pulse(self,verbose=False):
        A = self.abus.read() % 256
        B = self.bbus.read() % 256
	self.carryout.write(False)
	if self.subenable.read():
            B *= -1
        self.state = A + B
	if self.carryin.read():
            self.state += 1
        if self.state > 255 or self.state < 0:
            self.carryout.write(True)
            self.state %= 256
        
        if self.oenable.read():
             self.obus.write(self.state)


# main
if __name__ == "__main__":
    from sys import path as pylib

    print(pylib)
    raise RuntimeError("this is meant to be imported")

