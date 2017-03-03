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

class Valves:

        theComPort=""
        theConnection=None
        theListenThread=None
        theListenCallback=None
        theQuitSignal=False

        def __init__(self, ComPort):
                self.theComPort=ComPort

        def Connect(self):
                db.PrintDebug("Connecting valves on port "+str(self.theComPort))
                success=True
                
                try:
                        self.theConnection=serial.Serial(self.theComPort,9600,serial.EIGHTBITS,serial.PARITY_NONE,serial.STOPBITS_ONE,timeout=1)        
                        x=""
                        while(x[:2]<>"GO"):
                                x=self.theConnection.readline()
                                db.PrintDebug("waiting for go: "+x)

                except:
                        db.PrintDebug("No valve connection!")
                        self.theConnection=None
                        success=False

                return success
        
        def Disconnect(self):
                db.PrintDebug("Disconnecting valves on port "+str(self.theComPort))
                if (self.theListenThread):
                        self.theQuitSignal=True
                        self.theListenThread.join()
                if (self.theConnection):
                        self.theConnection.close()
                        
        def Open(self, which):
                db.PrintDebug("Opening valve "+str(which))
                if (self.theConnection):
                        self.theConnection.flushInput()
                        self.theConnection.write(str(which)+",1\r") # arduino looks for \r
                        raw = self.theConnection.readline
                        if raw == 'OK':
                                return
                        else:
                                print '!!!!Valve Error!!!!'

        def Close(self, which):
                db.PrintDebug("Closing valve "+str(which))
                if (self.theConnection):
                        self.theConnection.flushInput()
                        self.theConnection.write(str(which)+",0\r") # arduino looks for \r
                        raw = self.theConnection.readline
                        if raw == 'OK':
                                return
                        else:
                                print '!!!!Valve Error!!!!'

        def SentryReport(self):
                if (self.theConnection):
                        self.theConnection.write("s"+"\r")
