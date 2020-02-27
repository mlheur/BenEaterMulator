#!/usr/bin/env python3      

# portable system imports
from sys import argv
from os.path import abspath, realpath, dirname
from site import addsitedir

# local imports
addsitedir(dirname(realpath(abspath(argv[0]))))
from bus import Bus

# exports
class Component(object):
    def __init__(self, outbus, inbus=None):
        if outbus is None or isinstance(outbus, Bus):
            self.output = outbus
        else:
            raise RuntimeError("output bus is not a bus")
        self.inputs = []
        if inbus is not None:
            if type(inbus) == type([]):
                for i in inbus:
                    self.inputs.append(i)
            elif isinstance(inbus, Bus):
                self.inputs.append(inbus)
        self.state = False

    def clock_rise(self):
        n = len(self.inputs)
        if n == 0:
            self.state = False
            return
        if n > 1:
            self.state = []
            for i in self.inputs:
                self.state.append(i.sense())
            return
        self.state = self.inputs[0].sense()

    def clock_high(self):
        pass

    def clock_fall(self):
        if type(self.state) == type([]):
            if len(self.state) > 1:
                raise RuntimeError("multiple inputs, must override Component.clock_fall()")
            self.output.signal(self.state[0])
            return()
        self.output.signal(self.state)

    def clock_low(self):
        pass

    def __str__(self):
        return("state [{}], output [{}], inputs [{}]".format(self.state, self.output, self.inputs))

# main
if __name__ == "__main__":
    from sys import path as pylib
    mycomponent = Component(Bus(),Bus())
    print("1. mycomponent [{}]".format(mycomponent))
    mycomponent.clock_rise()
    print("2. mycomponent [{}]".format(mycomponent))
    mycomponent.clock_fall()
    print("3. mycomponent [{}]".format(mycomponent))
    mycomponent = Component(Bus(),[Bus(),Bus()])
    print("4. mycomponent [{}]".format(mycomponent))
    mycomponent.clock_rise()
    print("5. mycomponent [{}]".format(mycomponent))
    mycomponent.clock_fall()
    print("6. mycomponent [{}]".format(mycomponent))
    print(pylib)
    raise RuntimeError("this is meant to be imported")
