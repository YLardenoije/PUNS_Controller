import sys
from enum import Enum

import time
import threading

import out.test_pb2 as test_pb2
import out.test_pb2_grpc as test_pb2_grpc
import google.protobuf.empty_pb2 as empty

import grpc

import msvcrt

from BallDetector import BallDetector
from DeviceInterface import DeviceInterface
from DeviceInterface import PinInput
from DeviceInterface import PinOutput

class pinballState(Enum):
    PLAYING = 1
    GAMEOVER = 2
    LAUNCHING = 3

class pinballEvent(Enum):
    BALL_LOSS = 1
    BUMPER_HIT = 2
    BALL_LAUNCHED = 3
    TIMER_TIMEOUT = 4

class MachineContainer():
    def __init__(self, leftButton, rightButton, leftBumper, rightBumper, launcherButton, launcherLed, VUK, launcher):
        self.leftButton = leftButton
        self.rightButton = rightButton
        self.leftBumper = leftBumper
        self.rightBumper = rightBumper
        self.launcherButton = launcherButton
        self.launcherLed = launcherLed
        self.VUK = VUK
        self.launcher = launcher

class pinballStateMachine():
    def __init__(self, stub, container):
        self.state = pinballState.PLAYING
        self.stub = stub
        self.container = container

        self.status = test_pb2.Status()
        self.status.ballsLeft = 3
        self.status.score.count = 0
        self.sendUpdate()
        self.stub.startGame(empty.Empty())

        self.eventQueue = []

    def sendUpdate(self):
        self.stub.setStatus(self.status)

    def queueEvent(self, event):
        self.eventQueue.append(event)

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

    def process(self):
        if (self.container.leftButton.ReadPin() == '0'):
            self.container.leftBumper.High()
        else:
            self.container.leftBumper.Low()

        if (self.container.rightButton.ReadPin() == '0'):
            self.container.rightBumper.High()
        else:
            self.container.rightBumper.Low()

        if self.state == pinballState.PLAYING:
            self.processPlaying()
        elif self.state == pinballState.GAMEOVER:
            self.processGameOver()
        elif self.state == pinballState.LAUNCHING:
            self.processLaunching()
        else:
            print("error")

        if len(self.eventQueue) > 0:
            print("pop event")
            event = self.eventQueue.pop(0)
            print(event)
            self.handleEvent(event)

    def handleEventPlaying(self, event):
        newState = self.state
        if event == pinballEvent.BALL_LOSS:
            if self.status.ballsLeft == 0:
                newState = pinballState.GAMEOVER
                self.stub.showGameOver(empty.Empty())
                threading.Timer(10, self.queueEvent, [pinballEvent.TIMER_TIMEOUT], {}).start()
            else:
                self.status.ballsLeft -= 1
                self.sendUpdate()

                newState = pinballState.LAUNCHING
                self.container.VUK.High()
                time.sleep(0.1)
                self.container.VUK.Low()
                threading.Timer(3, self.queueEvent, [pinballEvent.BALL_LAUNCHED], {}).start()

        elif event == pinballEvent.BUMPER_HIT:
            self.status.score.count += 100
            self.sendUpdate()

        return newState

    def processPlaying(self):
        if (self.container.launcherButton.ReadPin() == '0'):
            print("in")
            time.sleep(0.05)
            if (self.container.launcherButton.ReadPin() == '0'):
                self.queueEvent(pinballEvent.BALL_LOSS)
        return
    
    def handleEventGameOver(self, event):
        newState = self.state
        if event == pinballEvent.TIMER_TIMEOUT:
            self.status.ballsLeft = 3
            self.status.score.count = 0
            self.sendUpdate()
            newState = pinballState.PLAYING
            self.stub.startGame(empty.Empty())
            
        return newState

    def processGameOver(self):
        return
    
    def handleEventLaunching(self, event):
        newState = self.state
        if event == pinballEvent.BALL_LAUNCHED:
            newState = pinballState.PLAYING
            self.container.launcher.High()
            time.sleep(0.1)
            self.container.launcher.Low()
        return newState

    def processLaunching(self):
        return

if __name__ == "__main__":
    target = str(sys.argv[1])
    comport = str(sys.argv[2])
    # webcam = int(sys.argv[3])

    psoc = DeviceInterface(comport, 115200)
    leftButton = PinInput(26, psoc)
    rightButton = PinInput(27, psoc)

    leftBumper = PinOutput(20, psoc)
    rightBumper = PinOutput(17, psoc)

    launcherButton = PinInput(22, psoc)
    launcherLed = PinOutput(21, psoc)
    VUK = PinOutput(16, psoc)
    launcher = PinOutput(15, psoc)

    container = MachineContainer(leftButton, rightButton, leftBumper, rightBumper, launcherButton, launcherLed, VUK, launcher)

    channel = grpc.insecure_channel(target)
    pb = pinballStateMachine(test_pb2_grpc.testGRPCStub(channel), container)

    # detector = BallDetector(webcam)
    # threadDetector = threading.Thread(target=detector.detect_ball)
    # threadDetector.start()

    ballWasMissing = False

    while True:
        
        # if (detector.ballMissing and not ballWasMissing):
        #     pb.handleEvent(pinballEvent.BALL_LOSS)
        #     ballWasMissing = True
        
        # if (not detector.ballMissing):
        #     ballWasMissing = False

        if msvcrt.kbhit():
            c = msvcrt.getch()
            if (c == b'1'):
                pb.queueEvent(pinballEvent.BUMPER_HIT)
            elif (c == b'2'):
                pb.queueEvent(pinballEvent.BALL_LAUNCHED)
            elif (c == b'3'):
                pb.queueEvent(pinballEvent.BALL_LOSS)
            elif (c==b'q'):
                break
            else:
                print(c)
        
        pb.process()
    
    # detector.running = False
    # threadDetector.join()

