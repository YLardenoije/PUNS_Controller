import serial
import time
from DeviceInterface import DeviceInterface as DI
class Flipper:
    def __init__(self, pin, DeviceInterface):
        self.m_pin = pin
        self.DI = DeviceInterface

    def flip(self):
        self.DI.WriteDigitalOut(self.m_pin, 1)
        time.sleep(0.1)
        self.DI.WriteDigitalOut(self.m_pin, 0)
        
if __name__ == "__main__":
    DI = DI()
    flipper = Flipper(1,DI)
    flipper.flip()