#!/usr/bin/env python3      

# portable system imports
from sys import argv
from os.path import abspath, realpath, dirname
from site import addsitedir

# local imports
addsitedir(dirname(realpath(abspath(argv[0]))))
from register import Register
from bus import Trace

# exports
class ALU(Register):

    def __init__(self, id, a_bus, b_bus, out_bus, state=None, flags={}):
        super().__init__(id, out_bus, state, flags)
        self.ai_trace = Trace('{}.ai_trace'.format(self.id), a_bus)
        self.bi_trace = Trace('{}.bi_trace'.format(self.id), b_bus)
        self.subtract(False)
        self.carry(False)
        self.input = self.ai_trace
        if (state is None) or (type(state) != type(int(0))):
            self.state = 0
        del self.flags['ie']

    def __str__(self):
        return("{},{}".format(super().__str__(), self.bi_trace))

    def ie(self, state=None, verbose=False):
        return True

    def subtract(self, state=None, verbose=False):
        return(self.flag('subtract', state, verbose))

    def carry(self, state=None, verbose=False):
        return(self.flag('carry', state, verbose))

    def gate_read(self, verbose=False):
        return({'A':self.ai_trace.trace_read(), 'B':self.bi_trace.trace_read()})

    def pulse(self, verbose=False):
        inputs = self.gate_read()
        if verbose: print("   [verbose] {0}.pulse: ALU [{1}] received raw inputs [{2}]".format(type(self).__name__, self.id, inputs))

        for R,V in inputs.items():
            if (V is None) or (type(V) != type(int(0))):
                V = 0
                if verbose: print("   [verbose] {0}.pulse: ALU [{1}] input [{2}] is invalid [{3}], forcing to 0".format(type(self).__name__, self.id, R, V))
            inputs[R] = (int(V) & 0xFF)
            
        if self.subtract():
            inputs['B'] *= -1

        self.state = inputs['A'] + inputs['B']

        if self.carry():
            self.state += 1

        if verbose: print("   [verbose] {0}.pulse: ALU [{1}] has state [{2}]".format(type(self).__name__, self.id, self.state))

        if self.state > 255 or self.state < 0:
            self.carry(True)
            self.state %= 256
        
        if verbose: print("   [verbose] {0}.pulse: ALU [{1}] calculated self.state [{2}] with flags [{3}]".format(type(self).__name__, self.id, self.state, self.flags))

    def falling_edge(self, verbose=False):
        if self.oe():
            self.gate_write(self.state)


# main
if __name__ == "__main__":
    from bus import Bus
    from register import A_Register, B_Register
    mb = Bus("mainbus",0)
    alua = Bus("alua", 0)
    alub = Bus("alub", 0)
    A = A_Register("areg", mb, alua, 0)
    B = B_Register("breg", mb, alub, 0)
    ALU = ALU("me", alua, alub, mb, 0)

    order = [A,B,ALU]

    def dopulse():
        for c in order:
            c.rising_edge(True)
        for c in order:
            c.pulse(True)
        for c in order:
            c.falling_edge(True)

    print("  0 ALU:[{}]\n    A:[{}]\n    B:[{}]".format(ALU,A,B))
    dopulse()
    print("  1 ALU:[{}]\n    A:[{}]\n    B:[{}]".format(ALU,A,B))


    for _a in range(5):
        for _b in range(0,15,3):
            A.state = _a
            A.oe(True)
            B.state = _b
            dopulse()
            print("  _a=[{}]  _b[{}]\n    ALU:[{}]\n    A:[{}]\n    B:[{}]".format(_a,_b,ALU,A,B))
