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
    def __init__(self, ibus, obus, ienable, oenable):
        self.ibus = ibus
        self.obus = obus
        self.ienable = ienable
        self.oenable = oenable
        self.state = False

    def __str__(self):
        return("Component: state=[{}], ibus=[{}], obus=[{}], ienable=[{}], oenable=[{}]".format(
            self.state,
            self.ibus,
            self.obus,
            self.ienable,
            self.oenable))

    def pulse(self):
        if self.ienable.read():
             self.state = self.ibus.read()
        if self.oenable.read():
             self.obus.write(self.state)

# main
if __name__ == "__main__":
    from sys import path as pylib
    print(pylib)
    thebus = Bus()
    ie = Bus()
    oe = Bus()
    thecomp = Component(thebus,thebus,ie,oe)
    print("1. thebus=[{}],thecomp=[{}]".format(thebus,thecomp))
    thebus.write(True)
    print("2. thebus=[{}],thecomp=[{}]".format(thebus,thecomp))
    ie.write(True)
    print("3. thebus=[{}],thecomp=[{}]".format(thebus,thecomp))
    oe.write(False)
    print("4. thebus=[{}],thecomp=[{}]".format(thebus,thecomp))
    thecomp.pulse()
    print("5. thebus=[{}],thecomp=[{}]".format(thebus,thecomp))
    ie.write(False)
    print("6. thebus=[{}],thecomp=[{}]".format(thebus,thecomp))
    thebus.write(False)
    print("7. thebus=[{}],thecomp=[{}]".format(thebus,thecomp))
    thecomp.pulse()
    print("8. thebus=[{}],thecomp=[{}]".format(thebus,thecomp))
    oe.write(False)
    print("9. thebus=[{}],thecomp=[{}]".format(thebus,thecomp))
    thecomp.pulse()
    print("10. thebus=[{}],thecomp=[{}]".format(thebus,thecomp))
    raise RuntimeError("this is meant to be imported")
