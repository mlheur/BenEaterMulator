#!/usr/bin/env python3

from enum import Enum
from sys import argv
from os.path import realpath, dirname
from time import time as now, sleep
from math import sqrt
from site import addsitedir
addsitedir(dirname(realpath(argv[0])))
from gate import OpenGate

class ClockMode(Enum):
    STEP = False
    RUN = True

class Clock(OpenGate):
    def __init__(self, id, bus, flags={}, state={'Hz': 1}):
        print("Clock Flags:[{}]".format(flags))
        flags.update({'hlt': False})
        self.state = {}
        self.state['last_tick_time'] = now()
        self.state['mode'] = ClockMode.RUN
        if "mode" in state.keys():
            self.state['mode'] = state['mode']
        if "Hz" in state.keys():
            self.setspeed(state['Hz'])
        print("Clock Flags:[{}]".format(flags))
        super().__init__(id, bus, bus, flags)
        del self.input
        del self.output
        print(str(self))

    def __str__(self):
        return("{0},{1},{2},{3}".format(type(self).__name__, self.id, self.flags, self.state))

    def hlt(self, state=None, verbose=False):
        return(self.flag('hlt', state, verbose))

    def setspeed(self, Hz=1):
        self.state['sleeptime'] = 1.0 / sqrt(Hz)
        self.state['delaytime'] = 1.0 / Hz
        if 'Hz' in self.state.keys(): del self.state['Hz']

    def switchmode(self):
        self.state['mode'] = {False: ClockMode.RUN, True: ClockMode.STEP}[self.state['mode'].value]

    def getpulse(self,verbose=False):
        if self.state['mode'].value:
            while now() - self.state['last_tick_time'] < self.state['delaytime']:
                sleep(self.state['sleeptime'])
        self.state['last_tick_time'] = now()
        if verbose: print("tick")
        return not self.hlt()
    
 
if __name__ == "__main__":
    from bus import Bus
    mb = Bus("mainbus", False)
    clk = Clock("clk", mb)
    print("  0 "+str(int(now()))+"\n    "+str(mb)+"\n    "+str(clk))
    clk.switchmode()
    print("  1 "+str(int(now()))+"\n    "+str(mb)+"\n    "+str(clk))
    clk.getpulse()
    print("  2 "+str(int(now()))+"\n    "+str(mb)+"\n    "+str(clk))
    clk.switchmode()
    print("  3 "+str(int(now()))+"\n    "+str(mb)+"\n    "+str(clk))
    clk.getpulse()
    print("  4 "+str(int(now()))+"\n    "+str(mb)+"\n    "+str(clk))
    clk.getpulse()
    print("  5 "+str(int(now()))+"\n    "+str(mb)+"\n    "+str(clk))
    clk.switchmode()
    print("  6 "+str(int(now()))+"\n    "+str(mb)+"\n    "+str(clk))
