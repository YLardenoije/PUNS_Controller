import sys
from enum import Enum

import time
import threading

import out.test_pb2 as test_pb2
import out.test_pb2_grpc as test_pb2_grpc
import google.protobuf.empty_pb2 as empty

import grpc

import msvcrt

class pinballState(Enum):
    PLAYING = 1
    GAMEOVER = 2
    LAUNCHING = 3

class pinballEvent(Enum):
    BALL_LOSS = 1
    BUMPER_HIT = 2
    BALL_LAUNCHED = 3
    TIMER_TIMEOUT = 4

class pinballStateMachine():
    def __init__(self, stub):
        self.state = pinballState.LAUNCHING
        self.stub = stub

        self.status = test_pb2.Status()
        self.status.ballsLeft = 3
        self.status.score.count = 0
        self.sendUpdate()
        self.stub.startGame(empty.Empty())

    def sendUpdate(self):
        self.stub.setStatus(self.status)

    def handleEvent(self, event):
        print(self.state)
        print(event)
        if self.state == pinballState.PLAYING:
            self.state = self.handleEventPlaying(event)
        elif self.state == pinballState.GAMEOVER:
            self.state = self.handleEventGameOver(event)
        elif self.state == pinballState.LAUNCHING:
            self.state = self.handleEventLaunching(event)
        print(self.state)  

    def handleEventPlaying(self, event):
        newState = self.state
        if event == pinballEvent.BALL_LOSS:
            if self.status.ballsLeft == 0:
                newState = pinballState.GAMEOVER
                self.stub.showGameOver(empty.Empty())
                threading.Timer(10, self.handleEvent, [pinballEvent.TIMER_TIMEOUT], {}).start()
            else:
                newState = pinballState.LAUNCHING
                #TODO: Ready ball

        elif event == pinballEvent.BUMPER_HIT:
            self.status.score.count += 100
            self.sendUpdate()

        return newState
    
    def handleEventGameOver(self, event):
        newState = self.state
        if event == pinballEvent.TIMER_TIMEOUT:
            self.status.ballsLeft = 3
            self.status.score.count = 0
            self.sendUpdate()
            newState = pinballState.LAUNCHING
            #TODO: Ready ball
            self.stub.startGame(empty.Empty())
            
        return newState
    
    def handleEventLaunching(self, event):
        newState = self.state
        if event == pinballEvent.BALL_LAUNCHED:
            newState = pinballState.PLAYING
            self.status.ballsLeft -= 1
            self.sendUpdate()
            #TODO: Launch ball
        return newState

if __name__ == "__main__":
    target = str(sys.argv[1])
    channel = grpc.insecure_channel(target)
    pb = pinballStateMachine(test_pb2_grpc.testGRPCStub(channel))
    while True:
        if msvcrt.kbhit():
            c = msvcrt.getch()
            if (c == b'1'):
                pb.handleEvent(pinballEvent.BUMPER_HIT)
            elif (c == b'2'):
                pb.handleEvent(pinballEvent.BALL_LAUNCHED)
            elif (c == b'3'):
                pb.handleEvent(pinballEvent.BALL_LOSS)
            else:
                print(c)

