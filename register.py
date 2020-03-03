#!/usr/bin/env python3      

# portable system imports
from sys import argv
from os.path import abspath, realpath, dirname
from site import addsitedir

# local imports
addsitedir(dirname(realpath(abspath(argv[0]))))
from bus import Bus
from component import Component

# exports
class Register(Component):
    def __init__(self, busses, lines=None, state=False):
        if lines == None: lines = {}
        if not 'ie' in lines.keys():
            lines['ie'] = Bus()
        if not 'oe' in lines.keys():
            lines['oe'] = Bus()
        super().__init__(busses, lines, state)


    def pulse(self,verbose=False):
        if self.lines['ie'].read():
            self.state = self.busses['bus'].read()
        if self.lines['oe'].read():
            self.busses['bus'].write(self.state)

# main
if __name__ == "__main__":
    b = Bus()
    r = Register({'bus': b})
    print(r)
    raise RuntimeError("this is meant to be imported")
