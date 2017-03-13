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

class VibVal:

        theComPort=""
        theConnection=None
        theListenThread=None
        theListenCallback=None
        theQuitSignal=False

        def __init__(self, ComPort):
                self.theComPort=ComPort

        def Connect(self):
                db.PrintDebug("Connecting mixer on port "+str(self.theComPort))
                success=True

                try:
                        self.theConnection=serial.Serial(self.theComPort,9600,serial.EIGHTBITS,serial.PARITY_NONE,serial.STOPBITS_ONE,writeTimeout=0)
                        x=""
                        while(x[:5]<>"Valid"):
                                x=self.theConnection.readline()
                                db.PrintDebug("waiting for go: "+x)

                except:
                        db.PrintDebug("No mixer connection!")
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

        def Open(self, which):
                db.PrintDebug("Opening valve " + str(which))
                if (self.theConnection):
                        self.theConnection.flushInput()
                        self.theConnection.write("vlv "+str(which)+" 1\r\n")  # arduino looks for \r
                        time.sleep(0.5)
                        raw = self.theConnection.readline()
                        if raw[:2] !='OK':
                            raise ValueError('!!!!VALVE ERROR!!!!')
                        else:
                            return

        def Close(self, which):
                db.PrintDebug("Closing valve " + str(which))
                if (self.theConnection):
                        self.theConnection.flushInput()
                        self.theConnection.write("vlv "+str(which)+" 0\r\n")  # arduino looks for \r
                        time.sleep(0.5)
                        raw = self.theConnection.readline()
                        if raw[:2] !='OK':
                            raise ValueError('!!!!VALVE ERROR!!!!')
                        else:
                            return


        def Vibrate(self,SweepTime,StartFreq,EndFreq,TotalCycles):
                db.PrintDebug("Vibrating Mixer")
                db.PrintDebug('vswp '+str(SweepTime)+' '+str(StartFreq)+' '+str(EndFreq)+' '+str(TotalCycles)+'\r\n')
                if (self.theConnection):
                        self.theConnection.flushInput()
                        self.theConnection.flushOutput()
                        self.theConnection.write("vswp "+str(SweepTime)+" "+str(StartFreq)+" "+str(EndFreq)+" "+str(TotalCycles)+"\r\n")
                        # if raw[:2] !='OK':
                        #     raise ValueError('!!!!VIBRATION ERROR!!!!')
                        # else:
                        #     return