#!/usr/bin/env python3      

# portable system imports
from sys import argv
from os.path import abspath, realpath, dirname
from site import addsitedir

# local imports
addsitedir(dirname(realpath(abspath(argv[0]))))

# exports
class Bus(object):
    def __init__(self):
        self.state = False

    def signal(self,state):
        self.state = state

    def sense(self):
        return(self.state)

    def __str__(self):
        return("sense=[{}]".format(self.sense()))

# main
if __name__ == "__main__":
    from sys import path as pylib
    print(pylib)
    mybus = Bus()
    print("mybus [{}]".format(mybus))
    raise RuntimeError("this is meant to be imported")
