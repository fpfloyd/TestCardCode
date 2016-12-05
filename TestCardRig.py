#
# Test Card Rig
#
# Connects to a bunch of valves and syringe pumps and makes magic
#
# Aaron Oppenheimer & Fred Floyd
# Daktari Diagnostics
#
# ChangeLog
#               v0.1    20151006        Stripped A.O. FxRig & Adapted for Test Card
#               v0.2    20151015        Pumps set to 5000uL at startup
#               v0.3    20160915        Added Magnet Actuation
#               v0.4    20160928        Added ASV and Haptic Motor Control
import DebugFunctions as db
from SyringePump import SyringePump
from VibVal import VibVal
from Magnet import Magnet
from ASV import ASV
from ASV_CLS_Parse import ParseASV


class TestCardRig:

        thePumps={}
        theValves={}
        theSentries={}
        theMagnet={}
        theVibration={}
        theSentriesInverse={}
        thePotentiostat={}
        theParser={}

        def __init__(self, vvcom,magcom,asvcom):
                # Need four syringe pumps, which we'll access by name
                
                # Now we need access to the valves
                self.theMagnetController=Magnet(magcom)
                self.theVibValController=VibVal(vvcom)
                self.thePotentiostat=ASV(asvcom)
                self.theParser=ParseASV()
                
        def Connect(self):
                success=True


                if not self.theMagnetController.Connect():
                        db.PrintDebug("Could not connect to Magnet")
                        success=False

                if not self.theVibValController.Connect():
                        db.PrintDebug("Cound not connect to Mixer")
                        success = False

                if not self.thePotentiostat.Connect():
                        db.PrintDebug("Could not Connect to Potentiostat")
                        success = False

                return success

        def Disconnect(self):
                for p in self.thePumps:
                        self.thePumps[p].Disconnect()
                self.theVibValController.Disconnect()
                self.thePotentiostat.Disconnect()
                self.theMagnetController.Disconnect()

        def PumpConfigure(self,which,port,diameter):
                db.PrintDebug("Configure pump "+port+" to diameter "+str(diameter))
                self.thePumps[which]=SyringePump(port)
                self.thePumps[which].Connect()
                self.thePumps[which].Configure(diameter)
                self.thePumps[which].SetVolume(1800)
                
        def PumpRate(self,which,rate):
                if which in self.thePumps:
                        db.PrintDebug("Set rate of pump "+which+" to "+str(rate))
                        self.thePumps[which].SetRate(rate)
                else:
                        db.PrintDebug("PumpStart FAIL No pump "+which)

        def PumpStart(self,which,rate,volume=None):
                if which in self.thePumps:
                        if (volume <> None):
                                db.PrintDebug("Set volume on pump "+which+" to "+str(volume))
                                self.thePumps[which].SetVolume(volume)
                        db.PrintDebug("Start pump "+which+" at rate "+str(rate))
                        self.thePumps[which].Start(rate)
                else:
                        db.PrintDebug("PumpStart FAIL No pump "+which)

        def PumpStop(self,which):
                if which in self.thePumps:
                        db.PrintDebug("Stop pump "+which)
                        self.thePumps[which].Stop()
                else:
                        db.PrintDebug("PumpStop FAIL No pump "+which)

        def PumpWithdraw(self,which):
                if which in self.thePumps:
                        db.PrintDebug("Withdraw pump "+which)
                        self.thePumps[which].EnableWithdraw()
                        self.thePumps[which].Start(200)
                else:
                        db.PrintDebug("PumpWidthdraw FAIL No pump "+which)
        
        def PumpStopWithdraw(self,which):
                if which in self.thePumps:
                        db.PrintDebug("Stop Withdraw pump "+which)
                        self.thePumps[which].Stop()
                        self.thePumps[which].DisableWithdraw()
                else:
                        db.PrintDebug("PumpStopWidthdraw FAIL No pump "+which)

        def AllPumpsStop(self):
                for i in self.thePumps:
                        self.PumpStop(i)
        
        def ValveConfigure(self, which, number):
                self.theValves[which]=number
        
        def ValveOpen(self,which):
                if which in self.theValves:
                        db.PrintDebug("Valve Open "+which)
                        self.theVibValController.Open(self.theValves[which])
                else:
                        db.PrintDebug("FAIL No valve "+which)

        def ValveClose(self,which):
                if which in self.theValves:
                        db.PrintDebug("Valve Close "+which)
                        self.theVibValController.Close(self.theValves[which])
                else:
                        db.PrintDebug("FAIL No valve "+which)

        def AllValvesClose(self):
                for i in self.theValves:
                        self.ValveClose(i)

        def MagnetEngage(self):
                db.PrintDebug("Magnet Engage")
                self.theMagnetController.Engage()

        def MagnetRetract(self):
                db.PrintDebug("Magnet Retract")
                self.theMagnetController.Retract()

        def MagnetHome(self):
                db.PrintDebug("Homing Magnet")
                self.theMagnetController.Home()

        def VibrationStart(self,SweepTime,StartFreq,EndFreq,TotalCycles):
                db.PrintDebug("Vibrating Mixer")
                self.theVibValController.Vibrate(SweepTime,StartFreq,EndFreq,TotalCycles)

        def SetupASV(self,DissVolt,DissTime,DepoVolt,DepoTime,StartSweep,EndSweep,SweepStep,SweepInc):
                db.PrintDebug("Passing ASV Parameters")
                self.thePotentiostat.SetupASV(DissVolt,DissTime,DepoVolt,DepoTime,StartSweep,EndSweep,SweepStep,SweepInc)

        def SetGains(self,DisGain,DepGain,SweGain):
                db.PrintDebug("Passing ASV Gains")
                self.thePotentiostat.SetGains(DisGain,DepGain,SweGain)

        def RunASV(self):
                db.PrintDebug('Running ASV')
                self.thePotentiostat.RunASV()

        def SaveASV(self,filepath,folder,filename):
                db.PrintDebug('Saving ASV File')
                self.thePotentiostat.SaveASV(filepath,folder,filename)

        def ParseASV(self,filepath,folder):
                db.PrintDebug('Parsing ASV Data')
                self.theParser.ParseASV(filepath,folder)




