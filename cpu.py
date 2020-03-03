#!/usr/bin/env python3      

# portable system imports
from sys import argv
from os.path import abspath, realpath, dirname
from site import addsitedir

# local imports
addsitedir(dirname(realpath(abspath(argv[0]))))

from bus import Bus
from clock import Clock
from register import Register
from decoder import BenEaterDecoder

# exports
class CPU(object):
    def __init__(self):

        def mkreg(name):
            ie = Bus()
            oe = Bus()
            return Register({'bus': self.bus}, {'ie': ie, 'oe': oe})}

        self.hlt = Bus()
        self.bus = Bus()
        self.clk = Clock(self.control_lines['hlt'])
        self.components = {}
        self.A = mkreg("A")
        self.B = mkreg("B")
        self.decoder = BenEaterDecoder(self)

    def __str__(self):
        return("CPU:  A=[{}]   B=[{}]  BUS=[{}]  HLT=[{}]".format(
            self.components[0].state,
            self.components[1].state,
            self.bus.read(),
            self.control_lines['hlt'].read()
        ))

    def poweron(self, program=None, verbose=False):
        if program is None:
            program = [0]  # halt
        print("Before Poweron\n{}".format(self))
        while self.clk.getpulse(verbose):  # Wait for clock trigger
            if len(program):
                if verbose: print("fetch")
                instruction = program.pop(0)
                if verbose: print("decode")
                self.decoder.decode(instruction, verbose)
                if verbose: print("execute")
                for component in self.components:
                    component.pulse(verbose)
                if verbose: print(self)

# main
if __name__ == "__main__":
    cpu = CPU()
    cpu.poweron([3,1,4,7,4,5,3,4,2,5,4,6,1,0],True)
