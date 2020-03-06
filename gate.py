#!/usr/bin/env python3      

# portable system imports
from sys import argv
from os.path import abspath, realpath, dirname
from site import addsitedir

# local imports
addsitedir(dirname(realpath(abspath(argv[0]))))
from bus import Trace

# exports
class OpenGate(object):
    def __init__(self, id, inbus, outbus=None, flags={}):
        self.id = id
        self.flags = {}
        self.flags.update(flags)
        self.input = Trace('{}.itrace'.format(self.id), inbus)
        if outbus is None: outbus = inbus
        self.output = Trace('{}.otrace'.format(self.id), outbus)

    def __str__(self):
        return("{0},{1},{2},{3}".format(self.id, self.flags, self.input, self.output))

    def flag(self, f, state=None, verbose=False):
        if state is not None:
            if not f in self.flags.keys(): self.flags[f] = None
            if verbose: print("   [verbose] {0}.flag: changing [{1}] flag from [{2}] to [{3}]".format(type(self).__name__, self.id, f, self.flags[f], state))
            self.flags[f] = state
        if verbose: print("   [verbose] {0}.flag: returning [{1}] flag as [{2}]".format(type(self).__name__, self.id, f, self.flags[f]))
        return self.flags[f]

    def gate_read(self, verbose=False):
        state = self.input.trace_read()
        if verbose: print("   [verbose] {0}.gate_read: returning [{1}] state as [{2}]".format(type(self).__name__, self.id, state))
        return state

    def gate_write(self, state, verbose=False):
        if verbose: print("   [verbose] {0}.gate_write: writing [{1}] state [{2}] to bus [{3}]".format(type(self).__name__, self.id, state, self.output))
        self.output.trace_write(state)

    def pulse(self, verbose=False):
        state = self.gate_read(verbose)
        if verbose: print("   [verbose] {0}.pulse: reading [{1}] from trace [{2}] as [{3}]".format(type(self).__name__, self.id, self.input, state))
        self.gate_write(state, verbose)
        if verbose: print("   [verbose] {0}.pulse: wrote [{1} state [{2}] to trace [{3}]".format(type(self).__name__, self.id, state, self.output))
        return(state)

class ToggleGate(OpenGate):
    def __init__(self, id, inbus, outbus=None, flags={}):
        if outbus is None: outbus = inbus
        flags.update({'oe': False})
        super().__init__(id, inbus, outbus, flags)
    def oe(self, state=None, verbose=False):
        return self.flag('oe', state, verbose)
    def pulse(self, verbose=False):
        state = self.gate_read(verbose)
        if verbose: print("   [verbose] {0}.pulse: reading [{1}] from trace [{2}] as [{3}]".format(type(self).__name__, self.id, self.input, state))
        if self.oe():
            self.gate_write(state, verbose)
            if verbose: print("   [verbose] {0}.pulse: wrote [{1} state [{2}] to trace [{3}]".format(type(self).__name__, self.id, state, self.output))
        return(state)

# main
if __name__ == "__main__":
    from bus import Bus
    mb = Bus("the_bus", "8-Bit-Bus")
    c = OpenGate("gate", mb)
    print("  0 "+str(c)+"\n    "+str(mb))
    c.pulse(True)
    print("  1 "+str(c)+"\n    "+str(mb))
    mb.bus_write("new data", True)
    c.pulse(True)
    print("  2 "+str(c)+"\n    "+str(mb))
