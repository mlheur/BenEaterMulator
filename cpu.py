#!/usr/bin/env python3      

# portable system imports
from sys import argv
from os.path import abspath, realpath, dirname
from site import addsitedir

# local imports
addsitedir(dirname(realpath(abspath(argv[0]))))

from bus import Bus
from clock import Clock
from component import Component
from decoder import BenEaterDecoder

# exports
class CPU(object):
    def __init__(self):

        def mkreg(name):
            ie = Bus()
            oe = Bus()
            self.control_lines['reg'][name] = {'ie': ie, 'oe': oe}
            return Component(self.bus, self.bus, ie, oe)

        self.control_lines = {}
        self.control_lines['hlt'] = Bus()
        self.control_lines['reg'] = {}
        self.bus = Bus()
        self.clk = Clock(self.control_lines['hlt'])
        self.components = []
        self.components.append(mkreg("A"))
        self.components.append(mkreg("B"))
        self.decoder = BenEaterDecoder(self.control_lines, self.bus)

    def __str__(self):
        return("CPU:  A=[{}]   B=[{}]  BUS=[{}]  HLT=[{}]".format(
            self.components[0].state,
            self.components[1].state,
            self.bus.read(),
            self.control_lines['hlt'].read()
        ))

    def poweron(self, program=None):
        if program is None:
            program = [0]  # halt
        print("Before Poweron\n{}".format(self))
        while self.clk.getpulse():  # Wait for clock trigger
            if len(program):
                self.decoder.decode(program.pop(0))
                for component in self.components:
                    component.pulse()
                print(self)

# main
if __name__ == "__main__":
    cpu = CPU()
    cpu.poweron([3,1,4,7,4,5,3,4,2,5,4,6,1,0])
