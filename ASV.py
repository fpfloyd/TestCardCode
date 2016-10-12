#
# Class ASV
#
# A class allowing control of a set of celestica potentiostat through serial communication
#
# Fred Floyd
# Daktari Diagnostics
#
# ChangeLog
#               20160928        Initial Work


import DebugFunctions as db
import os
import serial
import time
import csv


class ASV:

        theComPort=""
        theConnection=None
        theListenThread=None
        theListenCallback=None
        theQuitSignal=False

        def __init__(self, ComPort):
                self.theComPort=ComPort

        def Connect(self):
                db.PrintDebug("Connecting ASV on port "+str(self.theComPort))
                success=True

                try:
                        self.theConnection=serial.Serial(self.theComPort,115200,serial.EIGHTBITS,serial.PARITY_NONE,serial.STOPBITS_ONE,writeTimeout=0)
                        x=""
                        while(x[:8]<>"Firmware"):
                                self.theConnection.write('ver \r\n')
                                x=self.theConnection.readline()
                                db.PrintDebug("waiting for go: "+x)

                except:
                        db.PrintDebug("No ASV connection!")
                        self.theConnection=None
                        success=False

                return success

        def Disconnect(self):
                db.PrintDebug("Disconnecting ASV on port "+str(self.theComPort))
                if (self.theListenThread):
                        self.theQuitSignal=True
                        self.theListenThread.join()
                if (self.theConnection):
                        self.theConnection.close()

        def SetupASV(self,DissVolt,DissTime,DepoVolt,DepoTime,StartSweep,EndSweep,SweepStep,SweepInc):
                db.PrintDebug("Setting ASV Parameters")
                if (self.theConnection):
                        self.theConnection.flushInput()
                        self.theConnection.flushOutput()
                        self.theConnection.write('{} {} {} {} {} {} {} {} {} {}\r\n'.format(
                            DissVolt,DissTime,DepoVolt,DepoTime,StartSweep,EndSweep,SweepStep,SweepInc))
                        return

        def RunASV(self):
                db.PrintDebug("run 1")
                if (self.theConnection):
                        self.theConnection.flushInput()
                        self.theConnection.flushOutput()
                        self.theConnection.write('run 1 \r\n')
                        raw = ''
                        while (raw[:25] != 'Running dissolution phase'):
                                raw = self.theConnection.readline()
                                db.PrintDebug(str(raw))
                        print (str(raw))
                        print self.theConnection.readline()

                        while (raw[:24] != 'Running deposition phase'):
                                raw = self.theConnection.readline()
                                db.PrintDebug(str(raw))
                        print str(raw)
                        print self.theConnection.readline()

                        while (raw[:19] != 'Running sweep phase'):
                                raw = self.theConnection.readline()
                                db.PrintDebug(str(raw))
                        print str(raw)

                        while (raw[:14] != 'Assay complete'):
                                raw = self.theConnection.readline()
                                db.PrintDebug(str(raw))
                        print "ASV Complete"
                        print str(raw)
                        return


        def SaveASV(self,filepath,folder,filename):
                db.PrintDebug("Downloading ASV File")
                if (self.theConnection):
                        filename_txt = '{}\{}\{}{}'.format(filepath, folder, filename, ".txt")
                        directory = '{}\{}'.format(filepath,folder)
                        if not os.path.exists(directory):
                                os.makedirs(directory)
                        f = open(str(filename_txt), 'w')
                        self.theConnection.flushInput()
                        self.theConnection.flushOutput()
                        self.theConnection.write('dld \r\n')
                        raw = ''
                        while (raw[:17] <> 'Download complete'):
                                raw = self.theConnection.readline()
                                f.writelines(str(raw))
                                db.PrintDebug(str(raw))
                        f.close()
                        time.sleep(1)
                        print 'Download Complete'
                        return







