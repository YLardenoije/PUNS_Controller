from GRPCode.PSocInterface.AIPlayer.Flipper import Flipper



if __name__ == "__main__":
    # Create a DeviceInterface object
    DI = DI()
    # Create a Flipper object
    flipper = Flipper(1,DI)
    # Call the flip method
    flipper.flip()