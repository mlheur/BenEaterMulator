#!/usr/bin/env python3      

# portable system imports
from sys import argv
from os.path import abspath, realpath, dirname
from site import addsitedir

# local imports
addsitedir(dirname(realpath(abspath(argv[0]))))

from bus import Bus
from clock import Clock
from register import A_Register, B_Register, OUT_Register
from decoder import BenEaterDecoder

# exports
class CPU(object):
    def __init__(self, id):
        self.id = id
        self.mainbus = Bus("mainbus")
        self.alu_a = Bus("alu_a")
        self.alu_b = Bus("alu_b")
        self.clk = Clock("clk", self.mainbus)
        self.A = A_Register("A", self.mainbus, self.alu_a)
        self.B = B_Register("B", self.mainbus, self.alu_b)
        self.OUT = OUT_Register("OUT", self.mainbus)
        self.decoder = BenEaterDecoder(self)

    def __str__(self):
        return("CPU {}:\n  BUS=[{}]\n  A=[{}]\n  B=[{}]\n  CLK=[{}]".format(
            self.id,
            self.mainbus,
            self.A,
            self.B,
            self.clk
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
                for component in [self.A, self.B]:
                    component.pulse(verbose)
                if verbose: print(self)

# main
if __name__ == "__main__":
    cpu = CPU("TheCPU")
    program = []
    program.append(cpu.decoder.encode(0,1))
    program.append(cpu.decoder.encode(7,3))
    program.append(cpu.decoder.encode(0,2))
    program.append(cpu.decoder.encode(0xF,0))
    program.append(cpu.decoder.encode(0,4))
    cpu.poweron(program,True)

