#!/usr/bin/env python3

from enum import Enum
from sys import argv
from os.path import realpath, dirname
from time import time as now, sleep
from math import sqrt
from site import addsitedir
addsitedir(dirname(realpath(argv[0])))

class ClockMode(Enum):
    STEP = False
    RUN = True

class Clock:
    def __init__(self, haltbus, Hz=1, mode=ClockMode.RUN):
         self.inputs = {}
         self.inputs['halt'] = haltbus
         self.state = {}
         self.state['mode'] = mode
         self.setspeed(Hz)
         self.state['last_tick_time'] = 0

    def __str__(self):
         return("Clock: inputs=[{}], state=[{}]".format(self.inputs,self.state))
    
    def setspeed(self, Hz=1):
         self.state['sleeptime'] = 1.0 / sqrt(Hz)
         self.state['delaytime'] = 1.0 / Hz

    def toggle_mode(self):
        self.state['mode'] = {False:ClockMode.RUN,True:ClockMode.STEP}[self.state['mode'].value]

    def getpulse(self,verbose=False):
        if self.state['mode'].value:
            while now() - self.state['last_tick_time'] < self.state['delaytime']:
                sleep(self.state['sleeptime'])
        self.state['last_tick_time'] = now()
        if verbose: print("tick")
        return not self.inputs['halt'].read()
    
 
if __name__ == "__main__":
    from bus import Bus
    hlt = Bus()
    clk = Clock(hlt)
    print("1. clk=[{}]".format(clk))
    clk.toggle_mode()
    print("2. clk=[{}]".format(clk))
    print(now())
    print("3. clk.getpulse() = [{}]".format(clk.getpulse()))
    print(now())
    clk.setspeed(0.1)
    print("4. clk.getpulse() = [{}]".format(clk.getpulse()))
    print(now())
    print("5. clk.getpulse() = [{}]".format(clk.getpulse()))
    print(now())
    clk.toggle_mode()
    print("6. clk=[{}]".format(clk))
    print("7. clk.getpulse() = [{}]".format(clk.getpulse()))
    print(now())
    print("8. clk.getpulse() = [{}]".format(clk.getpulse()))
    print(now())
    raise RuntimeError("this is meant to be imported")
 
