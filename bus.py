#!/usr/bin/env python3      

# portable system imports
from sys import argv
from os.path import abspath, realpath, dirname
from site import addsitedir

# local imports
addsitedir(dirname(realpath(abspath(argv[0]))))

# exports
class Bus(object):
    def __init__(self,id):
        self.id = id
        self.enabled = True
    def __str__(self):
        return("Bus:[enabled:{}, id:{}]".format(self.enabled, self.id))
    def enable(self, enabled=True):
        self.enabled = enabled
    def disable(self):
        self.enable(False)
    def read(self):
        if not hasattr(self, 'state'):
            return None
        if hasattr(self, 'enabled') and self.enabled:
            print("{} READ!".format(self.id))
            return(self.state)
    def write(self, state):
        if not hasattr(self, 'state'):
            return
        if hasattr(self, 'enabled') and self.enabled:
            print("{} WROTE! {}".format(self.id, state))
            self.state = state

class InputBus(Bus):
    def __init__(self, id, reads_from):
        super().__init__(id)
        self.reads_from = reads_from
    def __str__(self):
        return("InputBus:[reads_from:[{}], {}]".format(self.reads_from, super().__str__()))
    def read(self):
        if hasattr(self, 'enabled') and self.enabled:
            return self.reads_from.read()

class OutputBus(Bus):
    def __init__(self, id, writes_to):
        super().__init__(id)
        self.writes_to = writes_to
        self.disable()
    def __str__(self):
        return("OutputBus:[writes_to:[{}], {}]".format(self.writes_to, super().__str__()))
    def write(self, state):
        if hasattr(self, 'enabled') and self.enabled:
            self.writes_to.write(state)

class MainBus(Bus):
    def __init__(self, id, state=False):
        super().__init__(id)
        self.state = state
    def __str__(self):
        return("MainBus:[state:[{}], {}]".format(self.state, super().__str__()))
        
# main
if __name__ == "__main__":
    mybus = MainBus("mybus")
    myin = InputBus("myin", mybus)
    myout = OutputBus("myout", mybus)
    print(mybus)
    print(myin)
    print(myout)
    print("myin.read()={}".format(myin.read()))
    print("writing True to myout")
    myout.write(True)
    print(mybus)
    print("myin.read()={}".format(myin.read()))


