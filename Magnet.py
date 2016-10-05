#
# Class Valve
#
# A class allowing control of a set of valves through a serial interface
#
# Aaron Oppenheimer
# Daktari Diagnostics
#
# ChangeLog
#               20120726        Initial work
#               20120731        Added ability to read change to a sentry and report up the chain
#               20120821        Updated to align with Arduino code 1.0.2


import DebugFunctions as db
import serial
import time

class Magnet:

        theComPort=""
        theConnection=None
        theListenThread=None
        theListenCallback=None
        theQuitSignal=False

        def __init__(self, ComPort):
                self.theComPort=ComPort

        def Connect(self):
                db.PrintDebug("Connecting magnet on port "+str(self.theComPort))
                success=True

                try:
                        self.theConnection=serial.Serial(self.theComPort,9600,serial.EIGHTBITS,serial.PARITY_NONE,serial.STOPBITS_ONE,writeTimeout=0)
                        x=""
                        while(x[:5]<>"Valid"):
                                x=self.theConnection.readline()
                                db.PrintDebug("waiting for go: "+x)

                except:
                        db.PrintDebug("No magnet connection!")
                        self.theConnection=None
                        success=False

                return success

        def Disconnect(self):
                db.PrintDebug("Disconnecting Magnet on port "+str(self.theComPort))
                if (self.theListenThread):
                        self.theQuitSignal=True
                        self.theListenThread.join()
                if (self.theConnection):
                        self.theConnection.close()

        def Retract(self):
                db.PrintDebug("Retracting Magnet")
                if (self.theConnection):
                        self.theConnection.flushInput()
                        self.theConnection.write("fmov 2 500 b f \r\n") # arduino looks for \r
                        time.sleep(1)
                        self.theConnection.write("fmov 2 35 b s \r\n")


        def Engage(self):
                db.PrintDebug("Engaging Magnet")
                if (self.theConnection):
                        self.theConnection.flushInput()
                        self.theConnection.write("fmov 2 500 f f \r\n")
                        time.sleep(1)
                        self.theConnection.write("fmov 2 120 f s \r\n")

        def Home(self):
                db.PrintDebug("Homing Magnet")
                if (self.theConnection):
                        self.theConnection.flushInput()
                        self.theConnection.write("fmov 2 500 b s \r\n")
                        time.sleep(2)
                        self.theConnection.write("fmov 2 500 b s \r\n")


