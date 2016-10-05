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

VERSION="0.04"

import time
import csv
import DebugFunctions as db
from TestCardRig import TestCardRig

Debug = True # set this to True to enable debug by default. Can always toggle it with "d" command

Fakeout = True


##########
#
# ASSAY PARAMETERS
# 
##########
#Pause Time
StepPauseTime=5         #Debug pause between each step
#PRIMING PARAMETERS
R1PrimeRate=100         #R1 Prime Flowrate (uL/min)
R1PrimeTime=30          #R1 Prime Time (sec)
R2PrimeRate=0           #R2 Prime Flowrate (uL/min)
R2PrimeTime=0           #R2 Prime Time (sec)
R3PrimeRate=50          #R3 Prime Flowrate (uL/min)
R3PrimeTime=60          #R3 Prime Time (sec)
R4PrimeRate=100         #R4 Prime Flowrate (uL/min)
R4PrimeTime=60          #R4 Prime Time (sec)

#WASHOUT PARAMETERS
WashoutRate=480         #Loading Pad Mixing Flowrate (uL/min)
WashoutTime=30          #Loading Pad Mixing Time (sec)

#CAPTURE PARAMETERS
PulldownRate=100       #Pulldonw Flowrate (uL/min)
PulldownTime=180       #Pulldown Time (sec)

#LYSE PARAMETERS
LyseRate=50            #Lysis Flowrate (uL/min)
LyseFlowTime=60        #Lysis Flow Time (sec)
LyseIncubate=30        #Lysis Incubation Time (sec)

#SANDWICH FORMATION AND WASH PARAMETERS
SilverRate=100         #Silver Pickup Flowate (uL/min)
SilverTime=30          #Silver Pickup Flow Time (sec)
SilverPause=60         #Silver Incubate Time(sec)
MagRate=50             #Mag Bead Flowrate (uL/min)
MagTime=30             #Mag Bead Flow Time (sec)
MagPause=60            #Mag Bead Incubate Time (sec)

#ASV PARAMETERS
asvRate=50             #Electrolyte Flowrate (uL/min)
asvTime=240            #Electrolyte Flow Time (sec)

##########
#
# Syringe Size
#
##########
DiameterR1 = 4.78       # BD plastic 1ml syringe ID (mm)
DiameterR2 = 4.78       # BD plastic 1ml syringe ID (mm)
DiameterR3 = 4.78       # BD plastic 1ml syringe ID (mm)
DiameterR4 = 4.78       # BD plastic 1ml syringe ID (mm)


##########
#
# Run a priming sequence
#
##########
def assay(theRig):

        #StartUp
        stopAll(theRig)

        #Prime R1
        print ("Priming R1, press ctrl+c to quit")
        theRig.ValveOpen("V1")
        theRig.ValveClose("V2")
        theRig.ValveClose("V3")
        theRig.ValveClose("V4")
        time.sleep(StepPauseTime)
        theRig.PumpStart("R1", R1PrimeRate)
        time.sleep(R1PrimeTime)
        theRig.PumpStop("R1")
        time.sleep(StepPauseTime)
        
        #Prime R2
        #print ("Priming R2, press ctrl+c to quit")
        #theRig.ValveClose("V1")
        #time.sleep(StepPauseTime)
        #theRig.ValveOpen("V2")
        #time.sleep(StepPauseTime)
        #theRig.PumpStart("R2", R2PrimeRate)
        #time.sleep(R2PrimeTime)
        #theRig.PumpStop("R2")
        #time.sleep(StepPauseTime)
        
        #Prime R4
        print ("Priming R4, press ctrl+c to quit")
        theRig.PumpStart("R4", R4PrimeRate)
        time.sleep(R4PrimeTime)
        theRig.PumpStop("R4")
        time.sleep(StepPauseTime)
        
        #Prime R3
        print ("Priming R3, press ctrl+c to quit")
        theRig.ValveClose("V2")
        time.sleep(StepPauseTime)
        theRig.ValveOpen("V3")
        time.sleep(StepPauseTime)
        theRig.PumpStart("R3", R3PrimeRate)
        time.sleep(R3PrimeTime)
        theRig.PumpStop("R3")
        time.sleep(StepPauseTime)
        
        #Virioun Washout
        print ("Washing Out Sample, press ctrl+c to quit")
        theRig.ValveClose("V3")
        time.sleep(StepPauseTime)
        theRig.ValveOpen("V2")
        time.sleep(StepPauseTime)
        theRig.PumpStart("R1", WashoutRate)
        time.sleep(WashoutTime)
        theRig.PumpStop("R1")
        time.sleep(StepPauseTime)
        
        #Virion Pull Down
        print ("Pulling Down Virions, press ctrl+c to quit")
        theRig.PumpStart("R1", PulldownRate)
        time.sleep(PulldownTime)
        theRig.PumpStop("R1")
        time.sleep(StepPauseTime)

        
        #Lyse Virions
        print ("Lysing Virions, press ctrl+c to quit")
        theRig.PumpStart("R2", LyseRate)
        time.sleep(LyseFlowTime)
        theRig.PumpStop("R2")
        time.sleep(LyseIncubate)
        time.sleep(StepPauseTime)

        #Form Sandwhiches
        print ("Forming Sandwiches, press ctrl+c to quit")
        theRig.PumpStart("R2", SilverRate)
        time.sleep(SilverTime)
        theRig.PumpStop("R2")
        time.sleep(SilverPause)
        theRig.PumpStart("R2", MagRate)
        time.sleep(MagTime)
        theRig.PumpStop("R2")

        
        #Flow to ASV chamber 
        print ("Flowing to ASV Chamber, press ctrl+c to quit")
        theRig.ValveClose("V3")
        theRig.ValveOpen("V4")
        theRig.PumpStart("R3", asvRate)
        time.sleep(asvTime)
        stopAll(theRig)             

        print ("Done!")
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

##########
#
# Stop everything
#
##########
def stopAll(theRig):
        theRig.AllPumpsStop()
        theRig.AllValvesClose() 

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

        print ("Test Card "+VERSION)
        
        theRig=TestCardRig("COM32") # valve controller,

        # Configure the pumps
        theRig.PumpConfigure("R1","COM31",DiameterR1)
        theRig.PumpConfigure("R2","COM26",DiameterR2)
        theRig.PumpConfigure("R3","COM22",DiameterR3)
        theRig.PumpConfigure("R4","COM27",DiameterR4)

        # Configure the valves. These numbers are the digital output line of the Arduino.
        theRig.ValveConfigure("V1",5)
        theRig.ValveConfigure("V2",6)
        theRig.ValveConfigure("V3",7)
        theRig.ValveConfigure("V4",8)
        theRig.ValveConfigure("V5",9)
        theRig.ValveConfigure("V6",10)

        if (Fakeout):
                print ("FAKING CONNECTION!")

        if (connect(theRig) or Fakeout):
                done=False

                while not done:
                        a=raw_input("key to start: (a)ssay, (m)anual, (q)uit\n")
                        # secretly, we can also turn debug messages on and off with "d"
                        try:
                                if (a=="a"):
                                        assay(theRig)
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
