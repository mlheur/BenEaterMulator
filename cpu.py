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
        self.control_lines = {}
        self.control_lines['hlt'] = Bus()
        self.bus = Bus()
        self.clk = Clock(self.control_lines['hlt'])
        self.components = []
        a_reg_ie = Bus()
        self.control_lines['a_reg_ie'] = a_reg_ie
        self.control_lines['a_reg_oe'] = a_reg_oe
        self.components.append(Component(self.bus, self.bus, a_reg_ie, a_reg_oe)) # a register
        self.decoder = BenEaterDecoder()

    def poweron(self):
        while self.clk.getpulse():
            # fetch
            # decode
            # execute
            for component in self.components:
                component.pulse()

# main
if __name__ == "__main__":
    cpu = CPU()
    cpu.poweron()
