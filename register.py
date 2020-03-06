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
    def ie(self, state=None, verbose=False):
        return self.flag('ie', state, verbose)
    def pulse(self, verbose=False):
        if self.ie():
            self.state = self.gate_read(verbose)
        if self.oe():
            self.gate_write(self.state, verbose)

class A_Register(Register):
    def __init__(self, id, bus, alu_a, state=None):
        super().__init__(id, bus, state)
        self.output.attach(alu_a)

class B_Register(Register):
    def __init__(self, id, bus, alu_b, state=None):
        super().__init__(id, bus, state)
        self.output.detach(bus)
        self.output.attach(alu_b)
        self.oe(True)

class OUT_Register(Register):
    def __init__(self, id, bus, state=None):
        super().__init__(id, bus, state)
        self.output.detach(bus)
        del self.output
    def oe(self, verbose=False):
        pass

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

