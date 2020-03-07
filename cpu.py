#!/usr/bin/env python3      

# portable system imports
from sys import argv
from os.path import abspath, realpath, dirname
from site import addsitedir

# local imports
addsitedir(dirname(realpath(abspath(argv[0]))))

from bus import Bus
from clock import Clock, ClockMode as CM
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
        self.decoder = BenEaterDecoder(self)
        self.components = []
        self.A = A_Register("A", self.mainbus, self.alu_a)
        self.components.append(self.A)
        self.B = B_Register("B", self.mainbus, self.alu_b)
        self.components.append(self.B)
        self.OUT = OUT_Register("OUT", self.mainbus)
        self.components.append(self.OUT)

    def __str__(self):
        return("CPU {}:\n  BUS=[{}]\n  A=[{}]\n  B=[{}]\n  CLK=[{}]".format(
            self.id,
            self.mainbus,
            self.A,
            self.B,
            self.clk
        ))

    def poweron(self, program=None, mode=CM.RUN, verbose=False):
        self.clk.hlt(False)
        self.clk.state['mode'] = mode
        if (program is None) or (len(program)==0):
            program = [cpu.decoder.encode("HLT",0)]
        if verbose: print("program: {}".format(program))
        if verbose: print("Before Poweron\n{}".format(self))
        while self.clk.getpulse(verbose):  # Wait for clock trigger, returns False on HLT
            for instruction in program:
                if verbose: print("fetch")
                if verbose: print("decode")
                self.decoder.decode(instruction, verbose)
                if verbose: print("execute")
                for component in self.components:
                    if hasattr(component, "rising_edge"):
                        component.rising_edge(verbose)
                for component in self.components:
                    if hasattr(component, "pulse"):
                        component.pulse(verbose)
                for component in self.components:
                    if hasattr(component, "falling_edge"):
                        component.falling_edge(verbose)
                if verbose: print(self)

# main
if __name__ == "__main__":
    cpu = CPU("TheCPU")
    program = []
    program.append(cpu.decoder.encode("NOP",1))
    program.append(cpu.decoder.encode("LDI",3))
    program.append(cpu.decoder.encode(0,2))
    program.append(cpu.decoder.encode("HLT",0))
    cpu.poweron(program,CM.RUN)
    cpu.poweron([],CM.RUN,True)

