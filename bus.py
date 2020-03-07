#!/usr/bin/env python3      

# portable system imports
from sys import argv
from os.path import abspath, realpath, dirname
from site import addsitedir

# local imports
addsitedir(dirname(realpath(abspath(argv[0]))))

# exports
class Bus(object):
    
    
    def __init__(self, id, state=None):
        self.id = id
        self.bus_write(state)
    
    def __str__(self):
        return("{0},{1}".format(self.id, self.state))
    
    def bus_read(self, verbose=False):
        if verbose: print("   [verbose] {0}.bus_read: returning [{1}] state [{2}]".format(type(self).__name__, self.id, self.state))
        return(self.state)
    
    def bus_write(self, state, verbose=False):
        if verbose: print("   [verbose] {0}.bus_write: changing [{1}] state from [{2}] to [{3}]".format(type(self).__name__, self.id, state, self.state))
        self.state = state


class Trace(object):


    def __init__(self, id, bus):
        self.id = id
        self.busses = bus
        if type(bus) != type([]):
            self.busses = [bus]

    def __str__(self):
        return("{0},{1}".format(self.id, self.busses))

    def trace_read(self, verbose=False):
        for bus in self.busses:
            return(bus.bus_read(verbose))

    def trace_write(self, state, verbose=False):
        for bus in self.busses:
            bus.bus_write(state, verbose)

    def attach(self, bus, verbose=False):
        if bus not in self.busses:
            self.busses.append(bus)

    def detach(self, bus, verbose=False):
        if bus in self.busses:
            for k, v in enumerate(self.busses):
                if v is bus:
                    del self.busses[k]
            

class HiTrace(Trace):

    def trace_read(self, verbose=False):
        for bus in self.busses:
            return((bus.bus_read(verbose)&0xF0)>>4)

    def trace_write(self, state, verbose=False):
        hipart = (state&0x0F) << 4
        for bus in self.busses:
            bus.bus_write(hipart|(bus.bus_read(verbose)&0xF), verbose)

class LoTrace(Trace):

    def trace_read(self, verbose=False):
        for bus in self.busses:
            return(bus.bus_read(verbose)&0x0F)

    def trace_write(self, state, verbose=False):
        lopart = state&0x0F
        for bus in self.busses:
            bus.bus_write((bus.bus_read(verbose) & 0xF0)|lopart, verbose)


# main
if __name__ == "__main__":
    bus = Bus("the_bus", False)
    print(bus, bus.bus_read(True))
    bus.bus_write(True)
    print(bus, bus.bus_read(True))

    t = Trace("the_trace", bus)
    t.trace_write(0b10100101, True)
    print(t, bus, bus.bus_read(True))
    print("reading from trace: {}".format(t.trace_read()))

    t.trace_write(0b11001010, True)
    lt = LoTrace("lo_trace", bus)
    ht = HiTrace("hi_trace", bus)
    print(t, lt, ht, bus, bus.bus_read(True), lt.trace_read(True), ht.trace_read(True))

    lt.trace_write(0b0011, True)
    print(t, lt, ht, bus, bus.bus_read(True), lt.trace_read(True), ht.trace_read(True))

    ht.trace_write(0b0101, True)
    print(t, lt, ht, bus, bus.bus_read(True), lt.trace_read(True), ht.trace_read(True))
