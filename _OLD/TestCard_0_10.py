#! /usr/bin/env python
# Functionalization Controller
#
# Connects to a bunch of valves and syringe pumps and makes magic
#
# Fred Floyd
# Daktari Diagnostics
#
# ChangeLog
#               v0.01        20151007      Stripped Code from Functionator for test card
#               v0.02        20151015      Changed syringe size callout, reinstate debug
#               v0.03        20151019      Added pump stop time to manual operation
#               v0.04        20151020      Added ability to import parameters from csv
#               v0.05        20160907      Completely Changed for C1 Card (vs Card of the Month)
#               v0.06        20160908      Added pauses after each segment, adjusted volumes
#               v0.07        20160912      Adjusted Volumes from video, made valves open before closing other
#               v0.08        20160913      Changed from times to volume control
#               v0.09        20160915      Added Magnet Actuation
#               v0.010       20160915      Added Vibration Actuation
#               v0.011       20160919      Mix while filling / Pause 20 sec while emptying 100uL / Added Valve 4

VERSION="0.011"

import time
import csv
import DebugFunctions as db
from TestCardRig import TestCardRig

Debug = False # set this to True to enable debug by default. Can always toggle it with "d" command

Fakeout = False


##########
#
# ASSAY PARAMETERS
# 
##########

#Prime Parameters
PrimeRate=100
B1PrimeVol=0
B2PrimeVol=0
B3PrimeVol=0
B4PrimeVol=22
B5PrimeVol=30

#ASV PRIME PARAMETERS
ASVPrimeRate=100        #ASV Prime Flowrate (uL/min)
ASVPrimeVol=75          #ASV Prime Volume (uL)

#PLASMA FLOW PARAMETERS
PlasmaPushRate=100      #Flowrate for plasma being pushed to mixing chamber (uL/min)
PlasmaPushVol=71        #Plasma Push Volume (uL)

#DILLUTION AND MAG ADDITION PARAMETERS
MagFlowRate=100         #Flowrate for mag beads being pushed into mixing chamber (uL/min)
MagFlowVol=50           #Mag Bead volume (uL)

#MIX PARAMETERS
MagSweepTime = 30       #Magnet Mixing Sweep Time (sec)
MagStartFreq = 130      #Magnet Mixing Start Frequency (hz)
MagEndFreq = 175        #Magnet Mixing End Frequency  (hz)
MagCycles = 1           #Number of Sweep Cycles
MagMixingSteps = 2      #Number of mixing steps
MagMixingInc = 5        #Time between mixing steps (sec)

#PULLDOWN AND WASHOUT PARAMETERS
PulldownTime=60         #Time for mags to pull down
WashoutRate=100         #Air flowrate (uL/min)
WashoutVol=120          #Air Volume (uL)
PulldownTime1=10        #Time for mags to pull down
WashoutRate1=100        #Air flowrate (uL/min)
WashoutVol1=50

#WASH PARAMETERS
WashRate=100
WashVol=50
#hopefully use same mix parameters as before

#SILVER ADDITION PARAMETERS
SilverRate=100
SilverVol=50

#ASV PARAMETERS
SandwichRate=100     #Sandwich Resuspension Flowrate (uL/min)
SandwichVol=50       #Sandwich Resuspension Time (sec)
MoveRate=50          #Sandwich Move Flowrate (uL/min)
MoveVol=100          #Sandwich Move Flow Time (sec)
ElecRate=50          #Electrolyte Flowrate (uL/min)
ElecVol=25           #Electrolyte Flow Time (sec)

##########
#
# Syringe Sizes
#
##########
DiameterB1 = 11.99      # BD plastic 5ml syringe ID (mm)
DiameterB2 = 4.79       # BD plastic 5ml syringe ID (mm)
DiameterB3 = 11.99      # BD plastic 5ml syringe ID (mm)
DiameterB4 = 11.99      # BD plastic 5ml syringe ID (mm)
DiameterB5 = 11.99      # BD plastic 5ml syringe ID (mm)
#DiameterR6 = 11.99      # BD plastic 5ml syringe ID (mm)

##########
#
# Calculate Syringe Pump Times (No feedback from pump)
#
##########
ExtraTime=2             #Extra time after the syringe pump finishes
ASVPrimeTime=(ASVPrimeVol*60.0/ASVPrimeRate)+ExtraTime
PlasmaPushTime=(PlasmaPushVol*60.0/PlasmaPushRate)+ExtraTime
MagFlowTime=(MagFlowVol*60.0/MagFlowRate)+ExtraTime
WashoutTime=(WashoutVol*60.0/WashoutRate)+ExtraTime
WashoutTime1=(WashoutVol1*60.0/WashoutRate)+ExtraTime
WashTime=(WashVol*60.0/WashRate)+ExtraTime
SilverTime=(SilverVol*60.0/SilverRate)+ExtraTime
SandwichTime=(SandwichVol*60.0/SandwichRate)+ExtraTime
MoveTime=(MoveVol*60.0/MoveRate)+ExtraTime
ElecTime=(ElecVol*60.0/ElecRate)+ExtraTime
B1PrimeTime=(B1PrimeVol*60.0/PrimeRate)+ExtraTime
B2PrimeTime=(B2PrimeVol*60.0/PrimeRate)+ExtraTime
B3PrimeTime=(B3PrimeVol*60.0/PrimeRate)+ExtraTime
B4PrimeTime=(B4PrimeVol*60.0/PrimeRate)+ExtraTime
B5PrimeTime=(B5PrimeVol*60.0/PrimeRate)+ExtraTime





##########
#
# Run an Assay
#
##########
def assay(theRig):

        #StartUp
        stopAll(theRig)

        #Open all Valves
        print 'Setting Valves, press ctrl+c to quit'
        theRig.ValveOpen("V1")
        theRig.ValveOpen("V2")
        theRig.ValveOpen("V3")
        theRig.ValveClose("V4")
        if Debug == True:
                raw_input("Press enter to continue")

        #Prime Other Channels
        print'Priming Channels'
        #theRig.PumpStart("B1", PrimeRate, B1PrimeVol)
        #time.sleep(B1PrimeTime)
        #theRig.PumpStart("B2", PrimeRate, B2PrimeVol)
        #time.sleep(B2PrimeTime)
        #theRig.PumpStart("B3", PrimeRate, B3PrimeVol)
        #time.sleep(B3PrimeTime)
        theRig.PumpStart("B4", PrimeRate, B4PrimeVol)
        time.sleep(B4PrimeTime)
        theRig.PumpStart("B5", PrimeRate, B5PrimeVol)
        time.sleep(B5PrimeTime)
        if Debug == True:
            raw_input('Press enter to continue')

        #Prime ASV Channel
        print 'Priming ASV Channel with ',ASVPrimeVol,'uL @',ASVPrimeRate,'uL/min, press ctrl+c to quit'
        theRig.ValveOpen("V3")
        time.sleep(0.5)
        theRig.ValveClose("V1")
        time.sleep(0.5)
        theRig.ValveClose("V2")
        time.sleep(0.5)
        theRig.PumpStart("B3", ASVPrimeRate, ASVPrimeVol)
        time.sleep(ASVPrimeTime)
        if Debug == True:
            raw_input('Press enter to continue')

        raw_input('Remove B2 hemostat and press enter to continue')

        #Ensure Chamber Is Empty
        print 'Emptying Chamber with', WashoutVol1, 'uL @', WashoutRate1, 'uL/min , press ctrl+c to quit'
        theRig.ValveClose("V3")
        time.sleep(1)
        theRig.ValveOpen("V2")
        time.sleep(0.5)
        theRig.ValveClose("V1")
        time.sleep(0.5)
        theRig.ValveOpen("V4")
        theRig.PumpStart("B2", WashoutRate1, WashoutVol1)
        time.sleep(WashoutTime1)
        if Debug == True:
            raw_input('Press enter to continue')

        #Push plasma to mixing chamber with lysis buffer
        print 'Pushing Plasma to Mixing Chamber with ',PlasmaPushVol,'uL @',PlasmaPushRate,'uL/min, press ctrl+c to quit'
        theRig.ValveOpen("V1")
        time.sleep(0.5)
        theRig.ValveClose("V3")
        time.sleep(0.5)
        theRig.PumpStart("B1", PlasmaPushRate, PlasmaPushVol)
        time.sleep(PlasmaPushTime)
        theRig.PumpStop("B1")
        if Debug == True:
            raw_input('Press enter to continue')

        # Mix Mags
        i = 1
        while i <= MagMixingSteps:
            i = i + 1
            theRig.VibrationStart(MagSweepTime, MagStartFreq, MagEndFreq, MagCycles)
            print 'Mixing Step:', i-1
            time.sleep(MagSweepTime + MagMixingInc)
        
        #Mix and Heat
        theRig.ValveOpen("V1")
        time.sleep(0.5)
        theRig.ValveClose("V3")
        time.sleep(0.5)
        ###

        #Add Mags
        print 'Diluting Lysis and Adding Mags with',MagFlowVol,'uL @',MagFlowRate,'uL/min, press ctrl+c to quit'
        theRig.VibrationStart(MagFlowTime,MagStartFreq,MagEndFreq,1)
        theRig.PumpStart("B4", MagFlowRate, MagFlowVol)
        time.sleep(MagFlowTime)
        if Debug == True:
            raw_input('Press enter to continue')

        # Mix Mags
        i = 1
        while i <= MagMixingSteps:
                i = i + 1
                theRig.VibrationStart(MagSweepTime, MagStartFreq, MagEndFreq, MagCycles)
                print 'Mixing Step:', i-1
                time.sleep(MagSweepTime + MagMixingInc)

        # Pulldown Mags
        print 'Pulling Down Mags'
        theRig.MagnetEngage()
        time.sleep(PulldownTime)
        time.sleep(2)
        if Debug == True:
                raw_input('Press enter to continue')

        #Empty Chamber
        print 'Emptying Chamber with',WashoutVol,'uL @',WashoutRate,'uL/min , press ctrl+c to quit'
        theRig.ValveOpen("V2")
        time.sleep(0.5)
        theRig.ValveClose("V1")
        time.sleep(0.5)
        theRig.PumpStart("B2", WashoutRate, WashoutVol/2)
        time.sleep(WashoutTime/2+20)
        theRig.PumpStart("B2", WashoutRate, WashoutVol/2)
        if Debug == True:
            raw_input('Press enter to continue')

        #Wash and Resuspend
        print 'Washing half sandwiches with',WashVol,'uL @',WashoutRate,'uL/min, press ctrl+c to quit'
        theRig.ValveOpen("V1")
        time.sleep(0.5)
        theRig.ValveClose("V2")
        time.sleep(0.5)
        theRig.PumpStart("B4", WashRate, WashVol)
        time.sleep(WashTime)
        theRig.MagnetRetract()
        time.sleep(2)
        if Debug == True:
            raw_input('Press enter to continue')

        # Mixing Sandwiches
        i = 1
        print 'Mixing Sandwiches'
        while i <= MagMixingSteps:
            i = i + 1
            theRig.VibrationStart(MagSweepTime, MagStartFreq, MagEndFreq, MagCycles)
            print 'Mixing Step:', i-1
            time.sleep(MagSweepTime + MagMixingInc)

        # Pulldown Sandwiches
        print 'Pulling Down Sandwiches'
        theRig.MagnetEngage()
        time.sleep(PulldownTime)
        if Debug == True:
            raw_input('Press enter to continue')

        #Empty Chamber
        print 'Emptying Chamber with',WashoutVol,'uL @',WashoutRate,'uL/min, press ctrl+c to quit'
        theRig.ValveOpen("V2")
        time.sleep(0.5)
        theRig.ValveClose("V1")
        time.sleep(0.5)
        theRig.PumpStart("B2", WashoutRate, WashoutVol)
        time.sleep(WashoutTime)
        if Debug == True:
            raw_input('Press enter to continue')

        #Add Silver and Resuspend
        print 'Adding Silver with',MagFlowVol,'uL @',MagFlowRate,'uL/min, press ctrl+c to quit'
        theRig.ValveOpen("V1")
        time.sleep(0.5)
        theRig.ValveClose("V2")
        time.sleep(0.5)
        theRig.PumpStart("B5", MagFlowRate, MagFlowVol)
        time.sleep(MagFlowTime)
        theRig.MagnetRetract()
        time.sleep(2)
        if Debug == True:
            raw_input('Press enter to continue')

        #Mix Sandwiches
        i = 1
        print 'Mixing Sandwiches'
        while i <= MagMixingSteps:
            i = i + 1
            theRig.VibrationStart(MagSweepTime, MagStartFreq, MagEndFreq, MagCycles)
            print 'Mixing Step:', i-1
            time.sleep(MagSweepTime + MagMixingInc)

        # Pulldown Sandwiches
        print 'Pulling Down Sandwiches'
        theRig.MagnetEngage()
        time.sleep(PulldownTime)
        if Debug == True:
            raw_input('Press enter to continue')

        #Empty Chamber
        print 'Emptying Chamber with',WashoutVol,'uL @',WashoutRate,'uL/min, press ctrl+c to quit'
        theRig.ValveOpen("V2")
        time.sleep(0.5)
        theRig.ValveClose("V1")
        time.sleep(0.5)
        theRig.PumpStart("B2", WashoutRate, WashoutVol)
        time.sleep(WashoutTime)
        if Debug == True:
            raw_input('Press enter to continue')

        #Wash and pull down
        print 'Washing half sandwiches with',WashVol,'uL @',WashRate,'uL/min, press ctrl+c to quit'
        theRig.ValveOpen("V1")
        time.sleep(0.5)
        theRig.ValveClose("V2")
        time.sleep(0.5)
        theRig.PumpStart("B4", WashRate, WashVol)
        time.sleep(WashTime)
        theRig.MagnetRetract()
        time.sleep(2)
        if Debug == True:
            raw_input('Press enter to continue')

        #Mix Sandwiches
        i = 1
        print 'Mixing Sandwiches'
        while i <= MagMixingSteps:
            i = i + 1
            theRig.VibrationStart(MagSweepTime, MagStartFreq, MagEndFreq, MagCycles)
            print 'Mixing Step:', i-1
            time.sleep(MagSweepTime + MagMixingInc)

        # Pulldown Sandwiches
        print 'Pulling Down Sandwiches'
        theRig.MagnetEngage()
        time.sleep(PulldownTime)
        if Debug == True:
            raw_input('Press enter to continue')

        #Empty Chamber
        print 'Emptying Chamber with',WashoutVol,'uL @',WashoutRate,'uL/min , press ctrl+c to quit'
        theRig.ValveOpen("V2")
        time.sleep(0.5)
        theRig.ValveClose("V1")
        time.sleep(0.5)
        theRig.PumpStart("B2", WashoutRate, WashoutVol)
        time.sleep(WashoutTime)
        if Debug == True:
            raw_input('Press enter to continue')

        #Resuspend Sandwiches
        print 'Resuspending Sandwiches with',SandwichVol,'uL @',SandwichRate,'uL/min , press ctrl+c to quit'
        theRig.ValveOpen("V1")
        time.sleep(0.5)
        theRig.ValveClose("V2")
        time.sleep(0.5)
        theRig.PumpStart("B4",SandwichRate,SandwichVol)
        time.sleep(SandwichTime)
        theRig.MagnetRetract()
        time.sleep(2)
        if Debug == True:
            raw_input('Press enter to continue')

        #Resuspend Sandwiches
        i = 1
        print 'Resuspending Sandwiches'
        while i <= MagMixingSteps:
            i = i + 1
            theRig.VibrationStart(MagSweepTime, MagStartFreq, MagEndFreq, MagCycles)
            print 'Mixing Step:', i-1
            time.sleep(MagSweepTime + MagMixingInc)

        #Move to ASV Chamber
        print 'Moving Sandwiches to ASV Chamber with',MoveVol,'uL @',MoveRate,'uL/min, press ctrl+c to quit'
        theRig.ValveOpen("V3")
        time.sleep(0.5)
        theRig.ValveClose("V1")
        time.sleep(0.5)
        theRig.PumpStart("B2",MoveRate,MoveVol)
        time.sleep(MoveTime)
        if Debug == True:
            raw_input('Press enter to continue')

        #Fill ASV Chamber with Electrolyte
        print'Filling ASV Chamber with',ElecVol,'uL of Electrolyte at',ElecRate,'uL/min, press ctrl+c to quit'
        theRig.ValveClose("V4")
        theRig.PumpStart("B3",ElecRate, ElecVol)
        time.sleep(ElecTime)
        if Debug == True:
            raw_input('Press enter to continue')

        #RUN ASV

        print 'Assay Complete!'
        stopAll(theRig)
        beep()


##########
#
# Run a priming sequence
#
##########
def prime(theRig):
        print("Make Sure Card is Removed from Fixture (or Cleaning Card is in")
        ans=raw_input("Prime B1 path?")
        if (len(ans)>0) and ans[0]=="y":
                raw_input("Press enter to start")
                theRig.PumpStart("B1",300)
                raw_input("press enter to stop B1")
                theRig.PumpStop("B1")
                stopAll(theRig)

        ans=raw_input("Prime B3 path? (B2 is air)")
        if (len(ans)>0) and ans[0]=="y":
                raw_input("Press enter to start")
                theRig.PumpStart("B3",300)
                raw_input("press enter to stop B3")
                theRig.PumpStop("B3")
                stopAll(theRig)

        ans=raw_input("Prime B4 path?")
        if (len(ans)>0) and ans[0]=="y":
                raw_input("Press enter to start")
                theRig.PumpStart("B4",300)
                raw_input("press enter to stop B4")
                theRig.PumpStop("B4")
                stopAll(theRig)

        ans=raw_input("Prime B5 path?")
        if (len(ans)>0) and ans[0]=="y":
                raw_input("Press enter to start")
                theRig.PumpStart("B5",300)
                raw_input("press enter to stop B5")
                theRig.PumpStop("B5")
                stopAll(theRig)



        print("Priming Complete!")
        beep()

##########
#
# Operate manually
#
##########

def doManual(theRig):
        global ReportingImpedance
        
        done=False
        while not done:
                a=raw_input("command: v[name]-[0,1] p[name]-[rate, 0],seconds (r)eset (e)xit\n")
                if (len(a)==0):
                        pass
                elif (a[0]=="e"):
                        done=True
                elif (a[0]=="r"):
                        stopAll(theRig) 
                elif (a[0]=="v"):
                        l=a.find("-")
                        if (l>=2):
                                w=a[1:l]
                                s=a[-1:r]
                                if (s=="0"):
                                        theRig.ValveClose(w)
                                elif (s=="1"):
                                        theRig.ValveOpen(w)
                                else:
                                        print ("error")
                        else:
                                print ("error")
                elif (a[0]=="p"):
                        l=a.find("-")
                        s=a.find(",")
                        if (l>=2):
                                w=a[1:l]
                                r=int(a[l+1:s])
                                t=int(a[s+1:])
                                if (r==0):
                                        theRig.PumpStop(w)
                                else:
                                        theRig.PumpStart(w,r)
                                        time.sleep(t)
                                        theRig.PumpStop(w)
                        else:
                                print ("error")
                else:
                        print ("unknown command!")
        
##########
#
# UTILITIES
#
##########

##########
#
# Connect it all up
#
##########
def connect(theRig):
        if (theRig.Connect()):
                theRig.AllPumpsStop()
                theRig.AllValvesClose()
                return True
        else:
                return False
        
##########
#
# Shut it down
#
##########
def disconnect(theRig):
        theRig.AllPumpsStop()
        theRig.AllValvesClose() 
        theRig.Disconnect()
        theRig.MagnetHome()

##########
#
# Stop everything
#
##########
def stopAll(theRig):
        theRig.AllPumpsStop()
        theRig.AllValvesClose()
        theRig.MagnetHome()

##########
#
# a better timing function than time.wait()
#
##########
def Delay(wait):
        nowtime=time.time()
        while ((time.time()-nowtime) < wait):
                pass

##########
#
# Make a noise
#
##########
def beep():
        print ('\a')

##########
#
# Make the magic here
#
##########
def main():
        global VERSION

        db.setDebug(Debug)

        print ("Test Card v"+VERSION)
        
        theRig=TestCardRig("COM32","COM36","COM29") # valve controller, Magnet Controller, Vibration Controller

        # Configure the pumps
        theRig.PumpConfigure("B1","COM22",DiameterB1)
        theRig.PumpConfigure("B2","COM31",DiameterB2)
        theRig.PumpConfigure("B3","COM26",DiameterB3)
        theRig.PumpConfigure("B4","COM35",DiameterB5)
        theRig.PumpConfigure("B5","Com13",DiameterB4)
        #theRig.PumpConfigure("B6","Com28",DiameterB4)

        # Configure the valves. These numbers are the digital output line of the Arduino.
        theRig.ValveConfigure("V1",5)
        theRig.ValveConfigure("V2",6)
        theRig.ValveConfigure("V3",7)
        theRig.ValveConfigure("V4",8)


        if (Fakeout):
                print ("FAKING CONNECTION!")

        if (connect(theRig) or Fakeout):
                done=False

                while not done:
                        a=raw_input("key to start: (a)ssay, (p)rime, (m)anual operation, (q)uit\n")
                        # secretly, we can also turn debug messages on and off with "d"
                        try:
                                if (a=="a"):
                                        assay(theRig)
                                elif(a=="p"):
                                        prime(theRig)
                                elif (a=="m"):
                                        doManual(theRig)
                                elif (a=="d"):
                                        db.toggleDebug()
                                elif (a=="q"):
                                        done=True
                                else:
                                        print "Unknown Command!"
                        except KeyboardInterrupt:
                                print ("Keyboard interrupt!")
                                stopAll(theRig)
                                

                disconnect(theRig)
        else:
                print "No connection to rig!"
                raw_input("Press Enter to exit")

if __name__ == "__main__":
    main()
