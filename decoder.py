#!/usr/bin/env python3      

# portable system imports
from sys import argv
from os.path import abspath, realpath, dirname
from site import addsitedir

# local imports
addsitedir(dirname(realpath(abspath(argv[0]))))
from bus import Trace
from register import Register

# exports
class BenEaterDecoder(Register):

    def __init__(self, cpu):
        self.cpu = cpu
        self.output = Trace("out_to_mainbus", cpu.mainbus)

    def disable_all(self):
        self.cpu.clk.hlt(False)
        for component in [self.cpu.A, self.cpu.B]:
            for flag in 'ie', 'oe':
                component.flag(flag, False)

    def encode(self, INSTR, VALUE):
        if type(INSTR) == type(''):
            if (INSTR == "NOP"): INSTR = 0
            if (INSTR == "LDA"): INSTR = 1
            if (INSTR == "ADD"): INSTR = 2
            if (INSTR == "SUB"): INSTR = 3
            if (INSTR == "STA"): INSTR = 4
            if (INSTR == "OUT"): INSTR = 5
            if (INSTR == "JMP"): INSTR = 6
            if (INSTR == "LDI"): INSTR = 7
            if (INSTR == "JC" ): INSTR = 8
            if (INSTR == "HLT"): INSTR = 15
        return( ((INSTR & 0x0F)<<4) | (VALUE & 0x0F) )
###
# 0000#### NOP No Operation
# 0001#### LDA Load memory into A
# 0010#### ADD Load A+B into A
# 0011#### SUB Load A-B into A
# 0100#### STA Load A into Memory
# 0101#### OUT Load A into Out
# 0110#### JMP Load MAR into IR
# 0111#### LDI Load #### into A
# 1000#### JC  
# 
# 
# 
# 
# 
# 
# 1111#### HLT
###
    def decode(self, instruction, verbose=False):
        self.disable_all()
        if instruction is None or type(instruction) != type(0xFF) or instruction < 0 or instruction > 0xFF:
            raise RuntimeError("faulty instruction format: {}".format(instruction))
        INSTR = (instruction & 0xF0) >> 4
        VALUE = (instruction & 0x0F)
        if INSTR == 0x0:
            if verbose: print("00: NOP")
            return
        if INSTR == 0x1:
            if verbose: print("01: LDA")
            return
        if INSTR == 0x2:
            if verbose: print("02: ADD")
            return
        if INSTR == 0x3:
            if verbose: print("03: SUB")
            return
        if INSTR == 0x4:
            if verbose: print("04: STA")
            return
        if INSTR == 0x5:
            if verbose: print("05: OUT")
            return
        if INSTR == 0x6:
            if verbose: print("06: JMP")
            return
        if INSTR == 0x7:
            if verbose: print("07: LDI")
            self.cpu.A.ie(True)
            self.output.trace_write(VALUE)
            return
        if INSTR == 0x8:
            if verbose: print("08: JC ")
            return
        if INSTR == 0xF:
            if verbose: print("15: HLT")
            self.cpu.clk.hlt(True)
            return

# main
if __name__ == "__main__":
    pass

