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
    def __init__(self, busses=None, lines=None, state=False ):
        if busses == None: busses = {}
        if lines == None: lines = {}
        self.state = state
        self.busses = busses
        self.lines = lines

    def __str__(self):
        return("Component: state=[{}], busses=[{}], lines=[{}]".format(
            self.state,
            self.busses,
            self.lines))

    def pulse(self,verbose=False):
        raise RuntimeError("subclass must define pulse()")

# main
if __name__ == "__main__":
    c = Component()
    print(c)
    raise RuntimeError("this is meant to be imported")
