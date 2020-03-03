#!/usr/bin/env python3      

# portable system imports
from sys import argv
from os.path import abspath, realpath, dirname
from site import addsitedir

# local imports
addsitedir(dirname(realpath(abspath(argv[0]))))

# exports
class Bus(object):
    def __init__(self, state=False):
        self.state = state
	self.peers = {}

    def write(self, state):
        self.state = state
        for peer in peers.values():
            peer.write(sate)

    def read(self):
        return(self.state)
    
    def leave(self,peername):
        if peername in self.peers:
            del self.peers[peername]

    def board(self,peer=None,peername=None,peerbus=None):
        if peer is None:
            if peername is not None and peerbus is not None:
                peer = {peername:peerbus}
        if peer is not None:
	    if type(peer) != type({}):
                raise RuntimeError("Bus.board(peer=[{}]) is expecting a dictionary".format(peer))
            if isinstance(peer.values()[0],Bus):
                self.peers.extend(peer)
                return
	raise RuntimeError("Bus.board(peer=[{}], peername=[{}], peerbus=[{}]) called with invalid parameters".format(peer,peerbus,peername))
        
    def __str__(self):
        return("Bus{state=[{}]}".format(self.read()))

# main
if __name__ == "__main__":
    from sys import path as pylib
    print(pylib)
    mybus = Bus()
    print("mybus [{}]".format(mybus))
    raise RuntimeError("this is meant to be imported")

