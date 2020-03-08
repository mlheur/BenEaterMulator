#!/usr/bin/env python3      

# portable system imports
from sys import argv
from os.path import abspath, realpath, dirname
from site import addsitedir

# local imports
addsitedir(dirname(realpath(abspath(argv[0]))))
from bus import Bus
from gate import ToggleGate

# exports
class Register(ToggleGate):
    def __init__(self, id, bus, state=None, flags={}):
        if state is None: state = id
        self.state = state
        flags.update({'ie': False})
        super().__init__(id, bus, bus, flags)
    def __str__(self):
        return("{},{}".format(super().__str__(), self.state))
    def ie(self, state=None, verbose=False):
        return self.flag('ie', state, verbose)
    def rising_edge(self, verbose=False):
        if self.ie():
            self.state = self.gate_read(verbose)
    def falling_edge(self, verbose=False):
        if self.oe():
            self.gate_write(self.state, verbose)


class A_Register(Register):
    def __init__(self, id, bus, alu_a, state=None, flags={}):
        super().__init__(id, bus, state, flags)
        self.output.attach(alu_a)
    def rising_edge(self, verbose=False):
        if self.ie():
            self.state = self.gate_read(verbose)
        if self.oe():
            self.gate_write(self.state, verbose)
    def falling_edge(self, verbose=False):
        pass


class B_Register(Register):
    def __init__(self, id, bus, alu_b, state=None, flags={}):
        super().__init__(id, bus, state, flags)
        self.output.detach(bus)
        self.output.attach(alu_b)
        del self.flags['oe']
    def oe(self, state=None, verbose=False):
        return True
    def rising_edge(self, verbose=False):
        if self.ie():
            self.state = self.gate_read(verbose)
        self.gate_write(self.state, verbose)
    def falling_edge(self, verbose=False):
        pass


class OUT_Register(Register):
    def __init__(self, id, bus, state=None):
        super().__init__(id, bus, state)
        self.output.detach(bus)
        self.output = "SCREEN"
        self.ostate = self.state
    def rising_edge(self, verbose=False):
        if self.ie():
            self.ostate = self.state
            self.state = self.gate_read(verbose)
    def falling_edge(self, verbose=False):
        if self.ostate != self.state:
            print("OUT_Register output: {}".format(self.state))
            self.ostate = self.state


class INSTR_Register(Register):
    def __init__(self, id, bus, oprom_bus, state=None, flags={}):
        super().__init__(id, bus, state, flags)
        self.output.detach(bus)
        del self.output
        self.output = HiLoOutputSplitter(id, bus, oprom_bus, bus, state, flags)


class OPROM_Register(Register):
    def __init__(self, id, oprom_in, oprom_out, state=None, flags={}):
        super().__init__(id, oprom_out, decoder_bus, state, flags)
        self.input.detach(bus)
        del self.input
        self.input = HiTrace(id, oprom_bus)
    def ie(self, verbose=False):
        return True
    def oe(self, verbose=False):
        return True

# main
if __name__ == "__main__":
    bus = Bus("8-Bit-Bus", "8-Bit-data")
    alu_a = Bus("alu_a", "a output")
    A = A_Register("A", bus, alu_a)
    alu_b = Bus("alu_b", "b output")
    B = B_Register("B", bus, alu_b)

#    print("A.flags:[{}]".format(id(A.flags)))
#    print("B.flags:[{}]".format(id(B.flags)))



    print("  0 "+str(bus)+"\n    "+str(A)+"\n    "+str(B))

    # Load A immediate
    print("write to the bus")
    bus.bus_write("Put something on the bus")

    print("  1 "+str(bus)+"\n    "+str(A)+"\n    "+str(B))

    print("set ie oe flags")
    A.ie(True)
    A.oe(False)
    B.ie(False)
    B.oe(False)

    print("  2 "+str(bus)+"\n    "+str(A)+"\n    "+str(B))

    print("pulse")
    A.pulse(True)
    B.pulse(True)

    print("  3 "+str(bus)+"\n    "+str(A)+"\n    "+str(B))

