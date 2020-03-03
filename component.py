#!/usr/bin/env python3      

# portable system imports
from sys import argv
from os.path import abspath, realpath, dirname
from site import addsitedir

# local imports
addsitedir(dirname(realpath(abspath(argv[0]))))
from bus import InputBus as ib, OutputBus as ob

# exports
class Component(object):
    def __init__(self, mainbus):
        self.ib = ib("ib", mainbus)
        self.ib.enable()
        self.ob = ob("ob", mainbus)
        self.ob.disable()

    def input_enable(enabled=True):
        self.ib.enable(enabled)
    def input_disable():
        self.input_enable(False)

    def output_enable(enabled=True):
        self.ob.enable(enabled)
    def output_disable():
        self.output_enable(False)

    def __str__(self):
        return("Component:[ib:[{}], ob:[{}]]".format(self.ib, self.ob))

    def pulse(self,verbose=False):
        if verbose: print("PULSE!")
        self.ob.write(self.ib.read())

# main
if __name__ == "__main__":
    from bus import MainBus
    c = Component(MainBus("mainbus", "8 Bit Bus"))
    print(c)
    c.pulse(True)
