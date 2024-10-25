import serial

class DeviceInterface:
    def __init__(self, comPort = 'COM5', baudRate = 9600):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.ser = serial.Serial(comPort, baudRate)

    def WriteDigitalOut(self, pin, HighLow):
        self.ser.write(f"PIN SET DIGITAL_OUT {pin} {HighLow}".encode())

    def WriteDigitalOutHigh(self, pin):
        self.WriteDigitalOut(pin, 1)
    
    def WriteDigitalOutLow(self, pin):
        self.WriteDigitalOut(pin, 0)
    
    def readLine(self) -> str:
        return str(self.ser.readline().decode())