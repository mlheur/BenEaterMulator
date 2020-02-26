#!/usr/bin/env python3

from enum import Enum
from sys import argv
from os.path import realpath, dirname
from time import sleep
from site import addsitedir
addsitedir(dirname(realpath(argv[0])))

class Clock:
 class ClockMode(Enum):
  STEP = False
  RUN = True

 def __init__(self, mode=Clock.ClockMode.STEP):
  self.inputs = {}
  self.inputs['halt'] = False
  self.inputs['switchmode'] = False
  self.inputs['step'] = False


if __name__ == "__main__":
 clk = clock()
 
