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

        def Configure(self,MagEngage):
                global magSteps
                magSteps = float(MagEngage)


        def Disconnect(self):
                db.PrintDebug("Disconnecting Magnet on port "+str(self.theComPort))
                if (self.theListenThread):
                        self.theQuitSignal=True
                        self.theListenThread.join()
                if (self.theConnection):
                        self.theConnection.close()

        def MagRetract(self):
                db.PrintDebug("Retracting Magnet")
                if (self.theConnection):
                        self.theConnection.flushInput()
                        self.theConnection.write("fmov 2 500 b f \r\n") # arduino looks for \r
                        time.sleep(1)
                        self.theConnection.write("fmov 2 500 b s \r\n")


        def MagEngage(self):
                global magSteps
                db.PrintDebug("Engaging Magnet")
                if (self.theConnection):
                        self.theConnection.flushInput()
                        if magSteps > 1000:
                                'Magnet Engagement Too High'
                                return False
                        if magSteps > 500:
                                magSteps = magSteps - 500
                                self.theConnection.write("fmov 2 500 f f \r\n")
                                time.sleep(1)
                                self.theConnection.write("fmov 2 " + str(magSteps) + " f s \r\n")
                        if magSteps < 500:
                                self.theConnection.write("fmov 2 " + str(magSteps) + " f s \r\n")

        def MagHome(self):
                db.PrintDebug("Homing Magnet")
                if (self.theConnection):
                        self.theConnection.flushInput()
                        self.theConnection.write("fmov 2 500 b s \r\n")
                        time.sleep(2)
                        self.theConnection.write("fmov 2 500 b s \r\n")

        def VibConfigure(self,VibEngage,VibRetract):
                global VibEngageAng
                global VibRetractAng
                VibEngageAng = VibEngage
                VibRetractAng = VibRetract

        def VibEngage(self):
                global VibEngageAng
                db.PrintDebug("Engaging Vibration Tip")
                if (self.theConnection):
                        self.theConnection.flushInput()
                        self.theConnection.write("serv " + VibEngageAng + " \r\n")

        def VibRetract(self):
                global VibEngageAng
                db.PrintDebug("Retracting Vibration Tip")
                if (self.theConnection):
                        self.theConnection.flushInput()
                        self.theConnection.write("serv " + VibRetractAng + " \r\n")


