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

VERSION="0.07"

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
#Pause Time
StepPauseTime=0         #Debug pause between each step

#PLASMA FLOW PARAMETERS
PlasmaPushRate=100      #Flowrate for plasma being pushed to mixing chamber (uL/min)
PlasmaPushTime=43     #Plasma Push Time (sec) = 71uL

#ASV PRIME PARAMETERS
ASVPrimeRate=100        #ASV Prime Flowrate (uL/min)
ASVPrimeTime=30         #ASV Prime Time (sec)


#DILLUTION AND MAG ADDITION PARAMETERS
MagFlowRate=100
MagFlowTime=54

#MIX PARAMETERS
#####

#PULLDOWN AND WASHOUT PARAMETERS
PulldownTime=60         #Time for mags to pull down
WashoutRate=100         #Air flowrate
WashoutTime=72

#WASH PARAMETERS
WashRate=100
WashTime=30
#hopefully use same mix parameters as before

#SILVER ADDITION PARAMETERS
SilverRate=100
SilverTime=30

#ASV PARAMETERS
SandwichRate=100       #Sandwich Resuspension Flowrate (uL/min)
SandwichTime=30        #Sandwich Resuspension Time (sec)
MoveRate=50            #Sandwich Move Flowrate (uL/min)
MoveTime=108            #Sandwich Move Flow Time (sec)
ElecRate=50            #Electrolyte Flowrate (uL/min)
ElecTime=30            #Electrolyte Flow Time (sec)

##########
#
# Syringe Sizes
#
##########
DiameterR1 = 11.99      # BD plastic 5ml syringe ID (mm)
DiameterR2 = 4.79       # BD plastic 5ml syringe ID (mm)
DiameterR3 = 11.99      # BD plastic 5ml syringe ID (mm)
DiameterR4 = 11.99      # BD plastic 5ml syringe ID (mm)
DiameterR5 = 11.99      # BD plastic 5ml syringe ID (mm)
#DiameterR6 = 11.99      # BD plastic 5ml syringe ID (mm)


##########
#
# Run an Assay
#
##########
def assay(theRig):

        #StartUp
        stopAll(theRig)

        #Introduce Plasma into meander
        print ("Setting Valves, press ctrl+c to quit")
        theRig.ValveOpen("V1")
        theRig.ValveClose("V2")
        theRig.ValveClose("V3")
        time.sleep(StepPauseTime)
        #raw_input("Press enter to continue")
        
        #Push plasma to mixing chamber with lysis buffer
        print ("Pushing Plasma to Mixing Chamber, press ctrl+c to quit")
        theRig.PumpStart("R1", PlasmaPushRate)
        time.sleep(PlasmaPushTime)
        theRig.PumpStop("R1")
        time.sleep(StepPauseTime)
        #raw_input("Press enter to continue")
        
        #Prime ASV Channel
        print ("Priming ASV Channel, press ctrl+c to quit")
        theRig.ValveOpen("V3")
        theRig.ValveClose("V1")
        theRig.PumpStart("R3", ASVPrimeRate)
        time.sleep(ASVPrimeTime)
        theRig.PumpStop("R3")
        time.sleep(StepPauseTime)
        #raw_input("Press enter to continue")
        
        #Mix and Heat
        theRig.ValveClose("V3")
        ###

        #Add Mags
        print ("Diluting Lysis and Adding Mags, press ctrl+c to quit")
        theRig.ValveOpen("V1")
        theRig.PumpStart("R5", MagFlowRate)
        time.sleep(MagFlowTime)
        theRig.PumpStop("R5")
        time.sleep(StepPauseTime)
        #raw_input("Press enter to continue")

        #Mix and Pulldown
        ###

        #Empty Chamber
        print ("Emptying Chamber, press ctrl+c to quit")
        theRig.ValveOpen("V2")
        theRig.ValveClose("V1")
        theRig.PumpStart("R2", WashoutRate)
        time.sleep(WashoutTime)
        theRig.PumpStop("R2")
        time.sleep(StepPauseTime)
        #raw_input("Press enter to continue")

        #Wash and pull down
        print ("Washing half sandwiches, press ctrl+c to quit")
        theRig.ValveOpen("V1")
        theRig.ValveClose("V2")
        theRig.PumpStart("R5", WashRate)
        time.sleep(WashTime)
        theRig.PumpStop("R5")
        #add magnet move step here
        time.sleep(StepPauseTime)
        #raw_input("Press enter to continue")

        #Empty Chamber
        print ("Emptying Chamber, press ctrl+c to quit")
        theRig.ValveOpen("V2")
        theRig.ValveClose("V1")
        theRig.PumpStart("R2", WashoutRate)
        time.sleep(WashoutTime)
        theRig.PumpStop("R2")
        time.sleep(StepPauseTime)
        #raw_input("Press enter to continue")

        #Add Silver
        print ("Adding Silver, press ctrl+c to quit")
        theRig.ValveOpen("V1")
        theRig.ValveClose("V2")
        theRig.PumpStart("R4", MagFlowRate)
        time.sleep(MagFlowTime)
        theRig.PumpStop("R4")
        time.sleep(StepPauseTime)
        #raw_input("Press enter to continue")

        #Mix and Pulldown
        ###

        #Empty Chamber
        print ("Emptying Chamber, press ctrl+c to quit")
        theRig.ValveOpen("V2")
        theRig.ValveClose("V1")
        theRig.PumpStart("R2", WashoutRate)
        time.sleep(WashoutTime)
        theRig.PumpStop("R2")
        time.sleep(StepPauseTime)
        #raw_input("Press enter to continue")

        #Wash and pull down
        print ("Washing half sandwiches, press ctrl+c to quit")
        theRig.ValveOpen("V1")
        theRig.ValveClose("V2")
        theRig.PumpStart("R5", WashRate)
        time.sleep(WashTime)
        theRig.PumpStop("R5")
        #add magnet move step here
        time.sleep(StepPauseTime)
        #raw_input("Press enter to continue")

        #Empty Chamber
        print ("Emptying Chamber, press ctrl+c to quit")
        theRig.ValveOpen("V2")
        theRig.ValveClose("V1")
        theRig.PumpStart("R2", WashoutRate)
        time.sleep(WashoutTime)
        theRig.PumpStop("R2")
        time.sleep(StepPauseTime)
        #raw_input("Press enter to continue")

        #Resuspend Sandwiches
        print ("Resuspending Sandwiches, press ctrl+c to quit")
        theRig.ValveOpen("V1")
        theRig.ValveClose("V2")
        theRig.PumpStart("R5",SandwichRate)
        time.sleep(SandwichTime)
        theRig.PumpStop("R5")
        time.sleep(StepPauseTime)
        #raw_input("Press enter to continue")

        #Move to ASV Chamber
        print ("Moving Sandwiches to ASV Chamber, press ctrl+c to quit")
        theRig.ValveOpen("V3")
        theRig.ValveClose("V1")
        theRig.PumpStart("R2",MoveRate)
        time.sleep(MoveTime)
        theRig.PumpStop("R2")
        time.sleep(StepPauseTime)
        #raw_input("Press enter to continue")

        #Fill ASV Chamber with Electrolyte
        print("Filling ASV Chamber with Electrolyte, press ctrl+c to quit")
        theRig.PumpStart("R3",ElecRate)
        time.sleep(ElecTime)
        theRig.PumpStop("R3")
        time.sleep(StepPauseTime)

        print ("Assay Complete!")
        stopAll(theRig)
        beep()


##########
#
# Run a priming sequence
#
##########
def prime(theRig):
        print("Make Sure Card is Removed from Fixture (or Cleaning Card is in")
        ans=raw_input("Prime R1 path?")
        if (len(ans)>0) and ans[0]=="y":
                raw_input("Press enter to start")
                theRig.PumpStart("R1",300)
                raw_input("press enter to stop R1")
                theRig.PumpStop("R1")
                stopAll(theRig)

        ans=raw_input("Prime R3 path? (R2 is air)")
        if (len(ans)>0) and ans[0]=="y":
                raw_input("Press enter to start")
                theRig.PumpStart("R3",300)
                raw_input("press enter to stop R3")
                theRig.PumpStop("R3")
                stopAll(theRig)

        ans=raw_input("Prime R4 path?")
        if (len(ans)>0) and ans[0]=="y":
                raw_input("Press enter to start")
                theRig.PumpStart("R4",300)
                raw_input("press enter to stop R4")
                theRig.PumpStop("R4")
                stopAll(theRig)

        ans=raw_input("Prime R5 path?")
        if (len(ans)>0) and ans[0]=="y":
                raw_input("Press enter to start")
                theRig.PumpStart("R5",300)
                raw_input("press enter to stop R5")
                theRig.PumpStop("R5")
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
        theRig.PumpConfigure("R1","COM22",DiameterR1)
        theRig.PumpConfigure("R2","COM31",DiameterR2)
        theRig.PumpConfigure("R3","COM26",DiameterR3)
        theRig.PumpConfigure("R4","COM35",DiameterR4)
        theRig.PumpConfigure("R5","Com13",DiameterR5)
        #theRig.PumpConfigure("R5","Com28",DiameterR5)

        # Configure the valves. These numbers are the digital output line of the Arduino.
        theRig.ValveConfigure("V1",5)
        theRig.ValveConfigure("V2",6)
        theRig.ValveConfigure("V3",7)


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
