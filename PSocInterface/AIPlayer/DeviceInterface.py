import serial
from singleton import Singleton

class DeviceInterface:
    def __init__(self, comPort = 'COM5', baudRate = 9600):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.ser = serial.Serial('comPort', baudRate)

    def WriteDigitalOut(self, pin, HighLow):
        self.ser.write(f"{pin} {HighLow}".encode())
    
    def readLine(self) -> str:
        return str(self.ser.readline().decode())