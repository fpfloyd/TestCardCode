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
#               v0.012       20160928      Added ASV control and output filepath
#               v0.13        20160930      Added Parser and Locked down Assay Parameters

VERSION='0.013'

import time
import csv
import DebugFunctions as db
from TestCardRig import TestCardRig

Debug = True # set this to True to enable debug by default. Can always toggle it with 'd' command
Fakeout = True #Fakeout connections, use for debugging without full test rig
Pause = False #Adds pause between each assay step that requires user input
filepath = '/Users/fredfloyd/Desktop/C1_Output'



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
MagStartFreq = 125      #Magnet Mixing Start Frequency (hz)
MagEndFreq = 250        #Magnet Mixing End Frequency  (hz)
MagCycles = 2           #Number of Sweep Cycles
MagMixingSteps = 1      #Number of mixing steps
MagMixingInc = 600      #Time between mag mixing steps (sec)
SilverMixingInc = 1800  #Time between Silver Mixing Steps (sec)
MagMixingPause = (MagCycles * MagSweepTime) + 10 #Sweep Time is not exact

#PULLDOWN AND WASHOUT PARAMETERS
PulldownTime=60         #Time for mags to pull down
WashoutRate100=100      #Air flowrate for 100 uL(uL/min)
WashoutVol100=125       #Air Volume for 100 uL (uL)
PulldownTime1=10        #Time for mags to pull down
WashoutRate50=100       #Air flowrate (uL/min)
WashoutVol50=75         #Air volume for 50uL (uL/min)

#WASH PARAMETERS
WashRate=100
WashVol=50
#hopefully use same mix parameters as before

#SILVER ADDITION PARAMETERS
SilverRate=100
SilverVol=50

#DETECTION CHAMBER PARAMETERS
SandwichRate=100     #Sandwich Resuspension Flowrate (uL/min)
SandwichVol=50       #Sandwich Resuspension Time (sec)
MoveRate=50          #Sandwich Move Flowrate (uL/min)
MoveVol=100          #Sandwich Move Flow Time (sec)
ElecRate=50          #Electrolyte Flowrate (uL/min)
ElecVol=40           #Electrolyte Flow Time (sec)

#ASV PARAMETERS
DissTime = 30
DissVolt = 1.1
DepoTime = 120
DepoVolt = -1.0
StartSweep = -1
EndSweep = 0.1
SweepStep = 100
SweepInc = 10000


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
WashoutTime100=(WashoutVol100*60.0/WashoutRate100)+ExtraTime
WashoutTime50=(WashoutVol50*60.0/WashoutRate50)+ExtraTime
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
        filename = raw_input('Enter Filename for ASV Data (then press Enter)')
        stopAll(theRig)
        theRig.SetupASV(DissVolt,DissTime,DepoVolt,DepoTime,StartSweep,EndSweep,SweepStep,SweepInc)

        #Open all Valves
        print 'Setting Valves, press ctrl+c to quit'
        theRig.ValveOpen('V1')
        time.sleep(0.5)
        theRig.ValveOpen('V2')
        time.sleep(0.5)
        theRig.ValveOpen('V3')
        time.sleep(0.5)
        theRig.ValveClose('V4')
        time.sleep(0.5)
        if Pause == True:
                raw_input('Press enter to continue')

        #Prime Other Channels
        print'Priming Channels'
        #theRig.PumpStart('B1', PrimeRate, B1PrimeVol)
        #time.sleep(B1PrimeTime)
        #theRig.PumpStart('B2', PrimeRate, B2PrimeVol)
        #time.sleep(B2PrimeTime)
        #theRig.PumpStart('B3', PrimeRate, B3PrimeVol)
        #time.sleep(B3PrimeTime)
        theRig.PumpStart('B4', PrimeRate, B4PrimeVol)
        time.sleep(B4PrimeTime)
        theRig.PumpStart('B5', PrimeRate, B5PrimeVol)
        time.sleep(B5PrimeTime)
        if Pause == True:
            raw_input('Press enter to continue')

        #Prime ASV Channel
        print 'Priming ASV Channel with ',ASVPrimeVol,'uL @',ASVPrimeRate,'uL/min, press ctrl+c to quit'
        theRig.ValveOpen('V3')
        time.sleep(0.5)
        theRig.ValveClose('V1')
        time.sleep(0.5)
        theRig.ValveClose('V2')
        time.sleep(0.5)
        theRig.PumpStart('B3', ASVPrimeRate, ASVPrimeVol)
        time.sleep(ASVPrimeTime)
        if Pause == True:
            raw_input('Press enter to continue')

        #Ensure Chamber Is Empty
        print 'Emptying Chamber with', WashoutVol50, 'uL @', WashoutRate50, 'uL/min , press ctrl+c to quit'
        theRig.ValveClose('V3')
        time.sleep(1)
        theRig.ValveOpen('V2')
        time.sleep(0.5)
        theRig.ValveClose('V1')
        time.sleep(0.5)
        theRig.ValveOpen('V4')
        theRig.PumpStart('B2', WashoutRate50, WashoutVol50)
        time.sleep(WashoutTime50)
        if Pause == True:
            raw_input('Press enter to continue')

        #Push plasma to mixing chamber with lysis buffer
        print 'Pushing Plasma to Mixing Chamber with ',PlasmaPushVol,'uL @',PlasmaPushRate,'uL/min, press ctrl+c to quit'
        theRig.ValveOpen('V1')
        time.sleep(0.5)
        theRig.ValveClose('V2')
        time.sleep(0.5)
        theRig.ValveClose('V3')
        time.sleep(0.5)
        theRig.PumpStart('B1', PlasmaPushRate, PlasmaPushVol)
        time.sleep(PlasmaPushTime)
        if Pause == True:
            raw_input('Press enter to continue')

        # Mix Lysis and Plasma
        i = 1
        while i <= MagMixingSteps:
            i = i + 1
            theRig.VibrationStart(MagSweepTime, MagStartFreq, MagEndFreq, MagCycles)
            print 'Mixing Step:', i-1, 'of 2'
            time.sleep(MagMixingPause)

        #Add Mags while adding to chamber
        print 'Diluting Lysis and Adding Mags with',MagFlowVol,'uL @',MagFlowRate,'uL/min, press ctrl+c to quit'
        theRig.VibrationStart(MagFlowTime,MagStartFreq,MagEndFreq,1)
        theRig.PumpStart('B4', MagFlowRate, MagFlowVol)
        time.sleep(MagFlowTime+10)
        if Pause == True:
            raw_input('Press enter to continue')

        # Mix Mags While Adding
        i = 1
        print 'Mixing and Incubating Mags'
        while i <= MagMixingSteps:
                i = i + 1
                theRig.VibrationStart(MagSweepTime, MagStartFreq, MagEndFreq, MagCycles)
                print 'Mixing Step:', i-1
                time.sleep(MagMixingPause + MagMixingInc)

        # Pulldown Mags
        print 'Pulling Down Mags'
        theRig.MagnetEngage()
        time.sleep(PulldownTime)
        time.sleep(2)
        if Pause == True:
                raw_input('Press enter to continue')

        #Empty Chamber
        print 'Emptying Chamber with',WashoutVol100,'uL @',WashoutRate100,'uL/min , press ctrl+c to quit'
        theRig.ValveOpen('V2')
        time.sleep(0.5)
        theRig.ValveClose('V1')
        time.sleep(0.5)
        theRig.PumpStart('B2', WashoutRate100, WashoutVol100)
        time.sleep(WashoutTime100)
        if Pause == True:
            raw_input('Press enter to continue')

        #Wash and Resuspend
        print 'Washing half sandwiches with',WashVol,'uL @',WashRate,'uL/min, press ctrl+c to quit'
        theRig.ValveOpen('V1')
        time.sleep(0.5)
        theRig.ValveClose('V2')
        time.sleep(0.5)
        theRig.PumpStart('B4', WashRate, WashVol)
        time.sleep(WashTime)
        if Pause == True:
            raw_input('Press enter to continue')

        # Mixing Sandwiches
        i = 1
        print 'Mixing Sandwiches'
        theRig.MagnetRetract()
        while i <= MagMixingSteps:
            i = i + 1
            theRig.VibrationStart(MagSweepTime, MagStartFreq, MagEndFreq, MagCycles)
            print 'Mixing Step:', i-1
            time.sleep(MagMixingPause)

        # Pulldown Sandwiches
        print 'Pulling Down Sandwiches'
        theRig.MagnetEngage()
        time.sleep(PulldownTime)
        if Pause == True:
            raw_input('Press enter to continue')

        #Empty Chamber
        print 'Emptying Chamber with',WashoutVol50,'uL @',WashoutRate50,'uL/min, press ctrl+c to quit'
        theRig.ValveOpen('V2')
        time.sleep(0.5)
        theRig.ValveClose('V1')
        time.sleep(0.5)
        theRig.PumpStart('B2', WashoutRate50, WashoutVol50)
        time.sleep(WashoutTime50)
        if Pause == True:
            raw_input('Press enter to continue')

        #Add Silver and Resuspend
        print 'Adding Silver with',SilverVol,'uL @',SilverRate,'uL/min, press ctrl+c to quit'
        theRig.ValveOpen('V1')
        time.sleep(0.5)
        theRig.ValveClose('V2')
        time.sleep(0.5)
        theRig.PumpStart('B5', SilverRate,SilverVol)
        time.sleep(SilverTime)
        if Pause == True:
            raw_input('Press enter to continue')

        #Mix Sandwiches
        i = 1
        print 'Mixing Sandwiches'
        theRig.MagnetRetract()
        while i <= MagMixingSteps:
            i = i + 1
            theRig.VibrationStart(MagSweepTime, MagStartFreq, MagEndFreq, MagCycles)
            print 'Mixing/Incubation Step:', i-1
            time.sleep(MagMixingPause + SilverMixingInc)

        # Pulldown Sandwiches
        print 'Pulling Down Sandwiches'
        theRig.MagnetEngage()
        time.sleep(PulldownTime)
        if Pause == True:
            raw_input('Press enter to continue')

        #Empty Chamber
        print 'Emptying Chamber with',WashoutVol50,'uL @',WashoutRate50,'uL/min, press ctrl+c to quit'
        theRig.ValveOpen('V2')
        time.sleep(0.5)
        theRig.ValveClose('V1')
        time.sleep(0.5)
        theRig.PumpStart('B2', WashoutRate50, WashoutVol50)
        time.sleep(WashoutTime50)
        if Pause == True:
            raw_input('Press enter to continue')

        #Wash and pull down
        print 'Washing half sandwiches with',WashVol,'uL @',WashRate,'uL/min, press ctrl+c to quit'
        theRig.ValveOpen('V1')
        time.sleep(0.5)
        theRig.ValveClose('V2')
        time.sleep(0.5)
        theRig.PumpStart('B4', WashRate, WashVol)
        time.sleep(WashTime)
        if Pause == True:
            raw_input('Press enter to continue')

        #Mix Sandwiches
        i = 1
        print 'Mixing Sandwiches'
        theRig.MagnetRetract()
        while i <= MagMixingSteps:
            i = i + 1
            theRig.VibrationStart(MagSweepTime, MagStartFreq, MagEndFreq, MagCycles)
            print 'Mixing Step:', i-1
            time.sleep(MagMixingPause)

        # Pulldown Sandwiches
        print 'Pulling Down Sandwiches'
        theRig.MagnetEngage()
        time.sleep(PulldownTime)
        if Pause == True:
            raw_input('Press enter to continue')

        #Empty Chamber
        print 'Emptying Chamber with',WashoutVol50,'uL @',WashoutRate50,'uL/min , press ctrl+c to quit'
        theRig.ValveOpen('V2')
        time.sleep(0.5)
        theRig.ValveClose('V1')
        time.sleep(0.5)
        theRig.PumpStart('B2', WashoutRate50, WashoutVol50)
        time.sleep(WashoutTime50)
        if Pause == True:
            raw_input('Press enter to continue')

        #Resuspend Sandwiches
        print 'Resuspending Sandwiches with',SandwichVol,'uL @',SandwichRate,'uL/min , press ctrl+c to quit'
        theRig.ValveOpen('V1')
        time.sleep(0.5)
        theRig.ValveClose('V2')
        time.sleep(0.5)
        theRig.PumpStart('B4',SandwichRate,SandwichVol)
        time.sleep(SandwichTime)
        if Pause == True:
            raw_input('Press enter to continue')

        #Resuspend Sandwiches
        i = 1
        print 'Resuspending Sandwiches'
        theRig.MagnetRetract()
        while i <= MagMixingSteps:
            i = i + 1
            theRig.VibrationStart(MagSweepTime, MagStartFreq, MagEndFreq, MagCycles)
            print 'Mixing Step:', i-1
            time.sleep(MagMixingPause)

        #Move to ASV Chamber
        print 'Moving Sandwiches to ASV Chamber with',MoveVol,'uL @',MoveRate,'uL/min, press ctrl+c to quit'
        theRig.ValveOpen('V3')
        time.sleep(0.5)
        theRig.ValveClose('V1')
        time.sleep(0.5)
        theRig.PumpStart('B2',MoveRate,MoveVol)
        time.sleep(MoveTime)
        if Pause == True:
            raw_input('Press enter to continue')

        #Fill ASV Chamber with Electrolyte
        print'Filling ASV Chamber with',ElecVol,'uL of Electrolyte at',ElecRate,'uL/min, press ctrl+c to quit'
        theRig.ValveClose('V4')
        time.sleep(0.5)
        theRig.ValveOpen('V2')
        theRig.PumpStart('B3',ElecRate, ElecVol)
        time.sleep(2)
        theRig.ValveClose('V2')
        time.sleep(0.5)
        theRig.ValveOpen('V1')
        time.sleep(2)
        theRig.ValveOpen('V3')
        time.sleep(0.5)
        theRig.ValveClose('V1')
        time.sleep(ElecTime-5)
        if Pause == True:
            raw_input('Press enter to continue')

        #RUN ASV
        print 'Running ASV'
        theRig.RunASV()
        print 'Saving ASV'
        theRig.SaveASV(filepath,folder,filename)

        print 'Assay Complete!'
        stopAll(theRig)
        beep()
        time.sleep(0.1)
        beep()
        time.sleep(0.1)
        beep()

##########
#
# Reset Air Syringe
#
##########
def airReset(theRig):
        ans = raw_input('Ensure card is removed from rig and press Enter')
        theRig.ValveOpen('V4')
        theRig.PumpStart('B2', 1000, 1000)
        time.sleep(60)
        theRig.PumpStop('B2')
        time.sleep(0.5)
        theRig.PumpStart('B2', 1800, -1000)
        time.sleep(35)
        theRig.PumpRate('B2', 100)
        return



##########
#
# Run a priming sequence
#
##########
def prime(theRig):
        print('Make Sure Card is Removed from Fixture (or Cleaning Card is in)')
        ans=raw_input('Prime B1 (Lysis Buffer) path?')
        if (len(ans)>0) and ans[0]=='y':
                raw_input('Press enter to start')
                theRig.PumpStart('B1',300)
                raw_input('press enter to stop B1')
                theRig.PumpStop('B1')
                stopAll(theRig)

        ans=raw_input('Prime or Reset B2 (Air) path?')
        if (len(ans)>0) and ans[0]=='y':
                theRig.ValveOpen('V4')
                raw_input('Press enter to start')
                theRig.PumpStart('B2',300)
                raw_input('press enter to stop B2')
                theRig.PumpStop('B2')
                stopAll(theRig)

        ans=raw_input('Prime B3 path?')
        if (len(ans)>0) and ans[0]=='y':
                raw_input('Press enter to start')
                theRig.PumpStart('B3',300)
                raw_input('press enter to stop B3')
                theRig.PumpStop('B3')
                stopAll(theRig)

        ans=raw_input('Prime B4 path?')
        if (len(ans)>0) and ans[0]=='y':
                raw_input('Press enter to start')
                theRig.PumpStart('B4',300)
                raw_input('press enter to stop B4')
                theRig.PumpStop('B4')
                stopAll(theRig)

        ans=raw_input('Prime B5 path?')
        if (len(ans)>0) and ans[0]=='y':
                raw_input('Press enter to start')
                theRig.PumpStart('B5',300)
                raw_input('press enter to stop B5')
                theRig.PumpStop('B5')
                stopAll(theRig)



        print('Priming Complete!')
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
                a=raw_input('command: v[name]-[0,1] p[name]-[rate, 0],seconds (r)eset (e)xit\n')
                if (len(a)==0):
                        pass
                elif (a[0]=='e'):
                        done=True
                elif (a[0]=='r'):
                        stopAll(theRig) 
                elif (a[0]=='v'):
                        l=a.find('-')
                        if (l>=2):
                                w=a[1:l]
                                s=a[-1:r]
                                if (s=='0'):
                                        theRig.ValveClose(w)
                                elif (s=='1'):
                                        theRig.ValveOpen(w)
                                else:
                                        print ('error')
                        else:
                                print ('error')
                elif (a[0]=='p'):
                        l=a.find('-')
                        s=a.find(',')
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
                                print ('error')
                else:
                        print ('unknown command!')
        
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
# Enter Folder Name
#
##########
def changeFolder(newfolder):
        global folder
        folder = newfolder

##########
#
# Make the magic here
#
##########
def main():
        global VERSION

        db.setDebug(Debug)

        print ('Test Card v'+VERSION)

        # Configure the Arduinos
        # (valve controller, Magnet Controller, Vibration Controller, Potentiostat)
        theRig=TestCardRig('COM32','COM36','COM29','COM38')

        # Configure the pumps
        theRig.PumpConfigure('B1','COM22',DiameterB1)
        theRig.PumpConfigure('B2','COM31',DiameterB2)
        theRig.PumpConfigure('B3','COM26',DiameterB3)
        theRig.PumpConfigure('B4','COM35',DiameterB5)
        theRig.PumpConfigure('B5','Com13',DiameterB4)
        #theRig.PumpConfigure('B6','Com28',DiameterB4)

        # Configure the valves. These numbers are the digital output line of the Arduino.
        theRig.ValveConfigure('V1',8)
        theRig.ValveConfigure('V2',9)
        theRig.ValveConfigure('V3',10)
        theRig.ValveConfigure('V4',11)


        if (Fakeout):
                print ('FAKING CONNECTION!')

        if (connect(theRig) or Fakeout):
                global folder
                folder = ''
                done=False
                while folder =='':
                        folder = raw_input('Enter Output Folder Name (then press ENTER):')

                while not done:
                        print 'Output will be saved in: {}\{}\ '.format(filepath, folder)
                        a=raw_input('key to start: (a)ssay, (p)rime, (c)hange folder name, pa(r)se folder, a(i)r reset, (m)anual operation, (q)uit\n')
                        # secretly, we can also turn debug messages on and off with 'd'
                        try:
                                if (a=='a'):
                                        assay(theRig)
                                elif(a=='p'):
                                        prime(theRig)
                                elif (a=='c'):
                                        folder = raw_input('Enter Output Folder Name (then press ENTER):')
                                elif (a=='r'):
                                        theRig.ParseASV(filepath,folder)
                                elif (a=='i'):
                                        airReset(theRig)
                                elif (a=='m'):
                                        doManual(theRig)
                                elif (a=='v'):
                                        theRig.RunASV()
                                elif (a=='d'):
                                        db.toggleDebug()
                                elif (a=='q'):
                                        done=True
                                else:
                                        print 'Unknown Command!'

                        except KeyboardInterrupt:
                                print ('Keyboard interrupt!')
                                stopAll(theRig)


                disconnect(theRig)
        else:
                print 'No connection to rig!'
                raw_input('Press Enter to exit')

if __name__ == '__main__':
    main()
