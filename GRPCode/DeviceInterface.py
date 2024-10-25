import serial
import time
class PinOutput:
    def __init__(self, pin, device):
        self.pin = pin
        self.device = device
        print(device.SetPinModeOutput(pin))
        print(device.WriteDigitalOutLow(pin))
    
    def High(self):
        self.device.WriteDigitalOutHigh(self.pin)

    def Low(self):
        self.device.WriteDigitalOutLow(self.pin)

class PinInput:
    def __init__(self, pin, device):
        self.pin = pin
        self.device = device
        print(device.SetPinModeInput(pin))

    def ReadPin(self):
        # returns last character in string
        return self.device.ReadDigitalIn(self.pin)[-1]

class DeviceInterface:
    def __init__(self, comPort, baudRate):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.ser = serial.Serial(comPort, baudRate, timeout=0.05)

    def SetPinModeOutput(self, pin):
        command = f"PIN SET MODE {pin} D_OUT\r\n".encode()
        self.ser.write(command)
        return self.readLine()

    def SetPinModeInput(self, pin):
        self.ser.write(f"PIN SET MODE {pin} D_IN_UP\r\n".encode())
        return self.readLine()

    def WriteDigitalOut(self, pin, HighLow):
        self.ser.write(f"PIN SET DIGITAL_OUT {pin} {HighLow}\r\n".encode())
        return self.readLine()

    def WriteDigitalOutHigh(self, pin):
        return self.WriteDigitalOut(pin, 1)
    
    def WriteDigitalOutLow(self, pin):
        return self.WriteDigitalOut(pin, 0)

    def ReadDigitalIn(self, pin):
        self.ser.write(f"PIN GET DIGITAL_IN {pin}\r\n".encode())
        return self.readLine()
    
    def readLine(self) -> str:
        return str(self.ser.readline().decode().strip())