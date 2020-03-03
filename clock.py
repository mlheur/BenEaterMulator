#!/usr/bin/env python3

from enum import Enum
from sys import argv
from os.path import realpath, dirname
from time import time as now, sleep
from math import sqrt
from site import addsitedir
addsitedir(dirname(realpath(argv[0])))
from component import Component

class ClockMode(Enum):
    STEP = False
    RUN = True

class Clock(Component):
    def __init__(self, busses=None, lines=None, state={'mode': ClockMode.RUN, 'Hz': 1}):
        super().__init__(busses, lines, state)
        self.setspeed(state['Hz'])
        self.state['last_tick_time'] = now()

    def setspeed(self, Hz=1):
         self.state['sleeptime'] = 1.0 / sqrt(Hz)
         self.state['delaytime'] = 1.0 / Hz
         if 'Hz' in self.state.keys(): del self.state['Hz']

    def switchmode(self):
        self.state['mode'] = {False: ClockMode.RUN, True: ClockMode.STEP}[self.state['mode']]

    def getpulse(self,verbose=False):
        if self.state['mode'].value:
            while now() - self.state['last_tick_time'] < self.state['delaytime']:
                sleep(self.state['sleeptime'])
        self.state['last_tick_time'] = now()
        if verbose: print("tick")
        return not self.lines['hlt'].read()
    
 
if __name__ == "__main__":
    from bus import Bus
    clk = Clock(lines={'hlt':Bus()})
    print(clk)
    print("1. clk=[{}]".format(clk))
    clk.switchmode()
    print("2. clk=[{}]".format(clk))
    print(now())
    print("3. clk.getpulse() = [{}]".format(clk.getpulse()))
    print(now())
    clk.setspeed(0.1)
    print("4. clk.getpulse() = [{}]".format(clk.getpulse()))
    print(now())
    print("5. clk.getpulse() = [{}]".format(clk.getpulse()))
    print(now())
    clk.switchmode()
    print("6. clk=[{}]".format(clk))
    print("7. clk.getpulse() = [{}]".format(clk.getpulse()))
    print(now())
    print("8. clk.getpulse() = [{}]".format(clk.getpulse()))
    print(now())
    raise RuntimeError("this is meant to be imported")
 
