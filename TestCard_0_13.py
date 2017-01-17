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
import ConfigParser
import param
import DebugFunctions as db
from TestCardRig import TestCardRig

Debug = False # set this to True to enable debug by default. Can always toggle it with 'd' command
Fakeout = False #Fakeout connections, use for debugging without full test rig
Pause = False #Adds pause between each assay step that requires user input
V2 = False
filepath = 'C:\C1_Output'


##########
#
# Run an Assay
#
##########
def assay(theRig):

        #StartUp
        filename = raw_input('Enter Filename for ASV Data (then press Enter):')
        stopAll(theRig)
        theRig.SetupASV(param.DissVolt,param.DissTime,param.DepoVolt,param.DepoTime,param.StartSweep,
                        param.EndSweep,param.SweepStep,param.SweepInc)
        theRig.SetGains(param.DissGain,param.DepoGain,param.SweepGain)

        #Open all Valves
        print time.strftime('%H:%M:%S -', time.localtime()), 'Starting Assay, Press ctrl+c at any time to quit'
        print time.strftime('%H:%M:%S -', time.localtime()), 'Setting Valves'
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
        print time.strftime('%H:%M:%S -', time.localtime()), 'Priming Blister Channels'
        #theRig.PumpStart('B1', param.PrimeRate, param.B1PrimeVol)
        #time.sleep(param.B1PrimeTime)
        #theRig.PumpStart('B6', param.PrimeRate, param.B6PrimeVol)
        #time.sleep(B6PrimeTime)
        #theRig.PumpStart('B2', param.PrimeRate, param.B2PrimeVol)
        #time.sleep(param.B2PrimeTime)
        theRig.PumpStart('B4', param.PrimeRate, param.B4PrimeVol)
        time.sleep(param.B4PrimeTime)
        theRig.PumpStart('B5', param.PrimeRate, param.B5PrimeVol)
        time.sleep(param.B5PrimeTime)
        if Pause == True:
            raw_input('Press enter to continue')

        #Prime ASV Channel
        print time.strftime('%H:%M:%S -', time.localtime()), 'Priming ASV Channel with ',param.ASVPrimeVol,'uL @',\
                param.ASVPrimeRate,'uL/min'
        theRig.ValveOpen('V3')
        time.sleep(0.5)
        theRig.ValveClose('V1')
        time.sleep(0.5)
        theRig.ValveClose('V4')
        time.sleep(0.5)
        theRig.ValveClose('V2')
        time.sleep(0.5)
        theRig.PumpStart('B2', param.ASVPrimeRate, param.ASVPrimeVol)
        time.sleep(param.ASVPrimeTime)
        if Pause == True:
            raw_input('Press enter to continue')

        #Ensure Chamber Is Empty
        print time.strftime('%H:%M:%S -', time.localtime()), 'Emptying Chamber with', param.WashoutVol50, 'uL @', \
                param.WashoutRate50, 'uL/min'
        theRig.MagnetRetract()
        time.sleep(0.5)
        theRig.ValveClose('V3')
        time.sleep(0.5)
        theRig.ValveOpen('V2')
        time.sleep(0.5)
        theRig.ValveClose('V1')
        time.sleep(0.5)
        theRig.ValveOpen('V4')
        theRig.PumpStart('B6', param.WashoutRate50, param.WashoutVol50)
        time.sleep(param.WashoutTime50)
        theRig.MagnetEngage()
        if Pause == True:
            raw_input('Press enter to continue')

        #Push Plasma to Mixing Chamber with Lysis Buffer
        print time.strftime('%H:%M:%S -', time.localtime()), 'Pushing Plasma to Mixing Chamber with ',\
                param.PlasmaPushVol,'uL @',param.PlasmaPushRate,'uL/min'
        theRig.ValveOpen('V1')
        time.sleep(0.5)
        theRig.ValveClose('V2')
        time.sleep(0.5)
        theRig.ValveClose('V3')
        time.sleep(0.5)
        theRig.PumpStart('B1', param.PlasmaPushRate, param.PlasmaPushVol)
        time.sleep(param.PlasmaPushTime)
        if Pause == True:
            raw_input('Press enter to continue')

        # Mix Lysis Buffer and Plasma
        print time.strftime('%H:%M:%S -', time.localtime()), 'Mixing Lysis Buffer and Plasma'
        theRig.VibrationStart(param.OtherSweepTime, param.OtherStartFreq, param.OtherEndFreq, param.OtherCycles)
        time.sleep(param.OtherMixingPause)

        if V2 == True:
                theRig.VibRetract()
                print time.strftime('%H:%M:%S -', time.localtime()), 'Disconnect Sample Port and Place in Eppendorf Tube, Then Press Enter'
                raw_input()
                theRig.AllValvesClose()
                time.sleep(0.5)
                theRig.ValveOpen('V4')
                time.sleep(0.5)
                print time.strftime('%H:%M:%S -', time.localtime()), 'Draining Sample Through V2 to Eppendorf Tube'
                theRig.PumpStart('B6', 100, 300)
                time.sleep(182)


        # #Add Mags to Chamber While Mixing
        # print time.strftime('%H:%M:%S -', time.localtime()), 'Adding Mags with',param.MagFlowVol,\
        #         'uL @',param.MagFlowRate,'uL/min. Mixing Step:', 1, 'of', param.MagMixingSteps
        # theRig.VibrationStart(param.MagFlowTime,param.MagStartFreq,param.MagEndFreq,param.MagCycles)
        # theRig.PumpStart('B4', param.MagFlowRate, param.MagFlowVol)
        # time.sleep(param.MagFlowTime)
        # if Pause == True:
        #     raw_input('Press enter to continue')
        #
        # # Mix and Incubate Mags
        # if param.EvenlySpaced == True:
        #     i = 2
        #     print time.strftime('%H:%M:%S -', time.localtime()), 'Mixing and Incubating Mags for', \
        #         str(param.MagMixingInc), 'seconds'
        #     while i <= param.MagMixingSteps:
        #         i = i + 1
        #         time.sleep((param.MagMixingInc / (param.MagMixingSteps-1))-param.MagMixingPause)
        #         print time.strftime('%H:%M:%S -', time.localtime()), 'Mixing Step:', i - 1, 'of', param.MagMixingSteps
        #         theRig.VibrationStart(param.MagSweepTime, param.MagStartFreq, param.MagEndFreq, param.MagCycles)
        #         time.sleep(param.MagMixingPause)
        #
        # if param.EvenlySpaced == False:
        #     i = 2
        #     print time.strftime('%H:%M:%S -', time.localtime()), 'Mixing and Incubating Mags for', \
        #         str(param.MagMixingInc), 'seconds'
        #     while i <= param.MagMixingSteps:
        #         i = i + 1
        #         theRig.VibrationStart(param.MagSweepTime, param.MagStartFreq, param.MagEndFreq, param.MagCycles)
        #         print time.strftime('%H:%M:%S -', time.localtime()), 'Mixing Step:', i - 1, 'of', param.MagMixingSteps
        #         time.sleep(param.MagMixingPause)
        #     time.sleep(param.MagMixingInc-(param.MagMixingPause*param.MagMixingSteps))
        #

        # # Pulldown Mags
        # print time.strftime('%H:%M:%S -', time.localtime()), 'Pulling Down Mags'
        # theRig.MagnetEngage()
        # time.sleep(0.5)
        # theRig.VibRetract()
        # time.sleep(param.PulldownTime)
        # if Pause == True:
        #         raw_input('Press enter to continue')
        #
        # #Empty Chamber
        # print time.strftime('%H:%M:%S -', time.localtime()), 'Emptying Chamber with',param.WashoutVol100,'uL @',param.WashoutRate100,'uL/min '
        # theRig.ValveOpen('V2')
        # time.sleep(0.5)
        # theRig.ValveClose('V1')
        # time.sleep(0.5)
        # theRig.PumpStart('B6', param.WashoutRate100, param.WashoutVol100)
        # time.sleep(param.WashoutTime100)
        # theRig.VibEngage()
        # if Pause == True:
        #     raw_input('Press enter to continue')
        #
        # #Add Wash Buffer to Chamber
        # print time.strftime('%H:%M:%S -', time.localtime()), 'Adding wash buffer to half sandwiches with',\
        #         param.WashVol,'uL @',param.WashRate,'uL/min'
        # theRig.ValveOpen('V1')
        # time.sleep(0.5)
        # theRig.ValveClose('V2')
        # time.sleep(0.5)
        # theRig.PumpStart('B4', param.WashRate, param.WashVol)
        # time.sleep(param.WashTime)
        # if Pause == True:
        #     raw_input('Press enter to continue')
        #
        # # Mixing and Resuspend Half Sandwiches
        # i = 1
        # print time.strftime('%H:%M:%S -', time.localtime()), 'Mixing/Washing Half Sandwiches'
        # theRig.MagnetRetract()
        # while i <= param.OtherMixingSteps:
        #     i = i + 1
        #     print time.strftime('%H:%M:%S -', time.localtime()), 'Mixing Step:', i - 1, 'of ', param.MagMixingSteps
        #     theRig.VibrationStart(param.OtherSweepTime, param.OtherStartFreq, param.OtherEndFreq, param.OtherCycles)
        #
        # # Pulldown Half Sandwiches
        # print time.strftime('%H:%M:%S -', time.localtime()), 'Pulling Down Half Sandwiches'
        # theRig.MagnetEngage()
        # time.sleep(0.5)
        # theRig.VibRetract()
        # time.sleep(param.PulldownTime)
        # if Pause == True:
        #     raw_input('Press enter to continue')
        #
        # #Empty Chamber
        # print time.strftime('%H:%M:%S -', time.localtime()), 'Emptying Chamber with',param.WashoutVol100,'uL @',\
        #         param.WashoutRate100,'uL/min'
        # theRig.ValveOpen('V2')
        # time.sleep(0.5)
        # theRig.ValveClose('V1')
        # time.sleep(0.5)
        # theRig.PumpStart('B6', param.WashoutRate100, param.WashoutVol100)
        # time.sleep(param.WashoutTime100)
        # theRig.VibEngage()
        # if Pause == True:
        #     raw_input('Press enter to continue')
        #
        # #Add Silver to Chamber
        # print time.strftime('%H:%M:%S -', time.localtime()), 'Adding Silver with',param.SilverVol,'uL @',\
        #         param.SilverRate,'uL/min'
        # theRig.ValveOpen('V1')
        # time.sleep(0.5)
        # theRig.ValveClose('V2')
        # time.sleep(0.5)
        # theRig.PumpStart('B5', param.SilverRate,param.SilverVol)
        # time.sleep(param.SilverTime)
        # if Pause == True:
        #     raw_input('Press enter to continue')
        #
        # #Mix Resuspend and Incubate Full Sandwiches
        # i = 1
        # print time.strftime('%H:%M:%S -', time.localtime()), 'Mixing & Incubating Full Sandwiches for',\
        #         param.SilverMixingInc,' seconds'
        # theRig.MagnetRetract()
        # while i <= param.SilverMixingSteps:
        #     i = i + 1
        #     print time.strftime('%H:%M:%S -', time.localtime()), 'Mixing/Incubation Step:', \
        #         i - 1, 'of ', param.SilverMixingSteps
        #     theRig.VibrationStart(param.SilverSweepTime, param.SilverStartFreq, param.SilverEndFreq, param.SilverCycles)
        #     time.sleep(param.SilverMixingInc/(param.SilverMixingSteps - 1))
        #
        # # Pulldown Sandwiches
        # print time.strftime('%H:%M:%S -', time.localtime()), 'Pulling Down Full Sandwiches'
        # theRig.MagnetEngage()
        # time.sleep(0.5)
        # theRig.VibRetract()
        # time.sleep(param.PulldownTime)
        # if Pause == True:
        #     raw_input('Press enter to continue')
        #
        # #Empty Chamber
        # print time.strftime('%H:%M:%S -', time.localtime()), 'Emptying Chamber with',param.WashoutVol50,\
        #         'uL @',param.WashoutRate50,'uL/min'
        # theRig.ValveOpen('V2')
        # time.sleep(0.5)
        # theRig.ValveClose('V1')
        # time.sleep(0.5)
        # theRig.PumpStart('B6', param.WashoutRate50, param.WashoutVol50)
        # time.sleep(param.WashoutTime50)
        # theRig.VibEngage()
        # if Pause == True:
        #     raw_input('Press enter to continue')
        #
        # #Add Wash to Chamber
        # print time.strftime('%H:%M:%S -', time.localtime()), 'Washing half sandwiches with',param.WashVol,\
        #         'uL @',param.WashRate,'uL/min'
        # theRig.ValveOpen('V1')
        # time.sleep(0.5)
        # theRig.ValveClose('V2')
        # time.sleep(0.5)
        # theRig.PumpStart('B4', param.WashRate, param.WashVol)
        # time.sleep(param.WashTime)
        # if Pause == True:
        #     raw_input('Press enter to continue')
        #
        # #Mix Resuspend and Wash Full Sandwiches
        # i = 1
        # print time.strftime('%H:%M:%S -', time.localtime()), 'Mixing/Washing Full Sandwiches'
        # theRig.MagnetRetract()
        # while i <= param.OtherMixingSteps:
        #     i = i + 1
        #     print time.strftime('%H:%M:%S -', time.localtime()), 'Mixing Step:', i - 1
        #     theRig.VibrationStart(param.OtherSweepTime, param.OtherStartFreq, param.OtherEndFreq, param.OtherCycles)
        #     time.sleep(param.OtherMixingPause)
        #
        # #Fix Mixing Beyond This Point
        #
        # # Pulldown Sandwiches
        # print time.strftime('%H:%M:%S -', time.localtime()), 'Pulling Down Full Sandwiches'
        # theRig.MagnetEngage()
        # time.sleep(param.PulldownTime)
        # if Pause == True:
        #     raw_input('Press enter to continue')
        #
        # #Empty Chamber
        # print time.strftime('%H:%M:%S -', time.localtime()), 'Emptying Chamber with',param.WashoutVol100,\
        #         'uL @',param.WashoutRate100,'uL/min '
        # theRig.ValveOpen('V2')
        # time.sleep(0.5)
        # theRig.ValveClose('V1')
        # time.sleep(0.5)
        # theRig.PumpStart('B6', param.WashoutRate100, param.WashoutVol100)
        # time.sleep(param.WashoutTime100)
        # if Pause == True:
        #     raw_input('Press enter to continue')
        #
        # #Add Wash to Chamber
        # print time.strftime('%H:%M:%S -', time.localtime()), 'Resuspending Full Sandwiches with',\
        #         param.SandwichVol,'uL @',param.SandwichRate,'uL/min '
        # theRig.ValveOpen('V1')
        # time.sleep(0.5)
        # theRig.ValveClose('V2')
        # time.sleep(0.5)
        # theRig.PumpStart('B4',param.SandwichRate,param.SandwichVol)
        # time.sleep(param.SandwichTime)
        # if Pause == True:
        #     raw_input('Press enter to continue')
        #
        # #Resuspend Sandwiches
        # i = 1
        # print time.strftime('%H:%M:%S -', time.localtime()), 'Resuspending Full Sandwiches'
        # theRig.MagnetRetract()
        # while i <= param.MagMixingSteps:
        #     i = i + 1
        #     print time.strftime('%H:%M:%S -', time.localtime()), 'Mixing Step:', i - 1
        #     theRig.VibrationStart(param.MagSweepTime, param.MagStartFreq, param.MagEndFreq, param.MagCycles)
        #
        if V2 == False:
                #Move to ASV Chamber
                print time.strftime('%H:%M:%S -', time.localtime()), 'Moving Sandwiches to ASV Chamber with',\
                        param.MoveVol,'uL @',param.MoveRate,'uL/min'
                theRig.ValveOpen('V3')
                time.sleep(0.5)
                theRig.ValveClose('V1')
                time.sleep(0.5)
                theRig.PumpStart('B6',param.MoveRate,param.MoveVol)
                time.sleep(param.MoveTime)
                if Pause == True:
                    raw_input('Press enter to continue')

                #PreFill Mix Chamber with Electrolyte to Stop Bubbles
                print time.strftime('%H:%M:%S -', time.localtime()), 'Priming Waste & Mixing Channels with Electrolyte'
                theRig.ValveClose('V3')
                time.sleep(0.5)
                theRig.ValveClose('V4')
                time.sleep(0.5)
                theRig.ValveOpen('V2')
                theRig.PumpStart('B2',param.ElecRate,10) #MAKE PARAMETER
                time.sleep(8)
                theRig.ValveOpen('V1')
                time.sleep(0.5)
                theRig.ValveClose('V2')
                theRig.PumpStart('B2',param.ElecRate,20) #MAKE PARAMETER
                time.sleep(30)

                #Fill ASV Chamber with Electrolyte
                print time.strftime('%H:%M:%S -', time.localtime()), 'Filling ASV Chamber with',param.ElecVol,\
                        'uL of Electrolyte at',param.ElecRate,'uL/min'
                theRig.ValveClose('V4')
                time.sleep(0.5)
                theRig.ValveOpen('V3')
                theRig.PumpStart('B2',param.ElecRate, param.ElecVol)
                theRig.ValveClose('V1')
                time.sleep(param.ElecTime-5)
                if Pause == True:
                    raw_input('Press enter to continue')

                #Run ASV
                print time.strftime('%H:%M:%S -', time.localtime()), 'Wetting Electrode for', param.PreASVWait, 'seconds'
                time.sleep(param.PreASVWait)
                print time.strftime('%H:%M:%S -', time.localtime()), 'Running ASV'
                theRig.RunASV()
                print time.strftime('%H:%M:%S -', time.localtime()), 'Saving ASV'
                theRig.SaveASV(filepath,folder,filename)

        print time.strftime('%H:%M:%S -', time.localtime()), 'Assay Complete!'
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
        time.sleep(0.5)
        theRig.PumpStart('B6', 1800, -1000)
        time.sleep(35)
        theRig.PumpRate('B6', 100)
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

        ans=raw_input('Prime B2 path?')
        if (len(ans)>0) and ans[0]=='y':
                raw_input('Press enter to start')
                theRig.PumpStart('B2',300)
                raw_input('press enter to stop B2')
                theRig.PumpStop('B2')
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
        theRig.MagnetHome()
        theRig.VibEngage()
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
        theRig.VibRetract()
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

        # Import Configuration from setup file
        config = ConfigParser.ConfigParser()
        config.read('setup.ini')
        config.sections()

        # Configure the Arduinos
        # (VibVal controller, Magnet Controller, Potentiostat)
        theRig=TestCardRig(config.get('ArduinoSetup','ComVibVal'),config.get('ArduinoSetup','ComMag'),
                           config.get('ArduinoSetup','ComASV'))

        # Configure the pumps
        theRig.PumpConfigure('B1',config.get('SyringeSetup','ComB1'),config.get('SyringeSetup','DiameterB1'))
        theRig.PumpConfigure('B2',config.get('SyringeSetup','ComB2'),config.get('SyringeSetup','DiameterB2'))
        #theRig.PumpConfigure('B3',config.get('SyringeSetup', 'ComB3'), config.get('SyringeSetup', 'DiameterB3'))
        theRig.PumpConfigure('B4',config.get('SyringeSetup','ComB4'),config.get('SyringeSetup','DiameterB4'))
        theRig.PumpConfigure('B5',config.get('SyringeSetup','ComB5'),config.get('SyringeSetup','DiameterB5'))
        theRig.PumpConfigure('B6',config.get('SyringeSetup', 'ComB6'), config.get('SyringeSetup', 'DiameterB6'))
        #theRig.PumpConfigure('B6',config.get('SyringePumpSetup','ComB6'),config.get('SyringeSetup','DiameterB6'))

        # Configure the valves. These numbers are the digital output line of the Arduino.
        theRig.ValveConfigure('V1',config.get('PortSetup','PortV1'))
        theRig.ValveConfigure('V2',config.get('PortSetup','PortV2'))
        theRig.ValveConfigure('V3',config.get('PortSetup','PortV3'))
        theRig.ValveConfigure('V4',config.get('PortSetup','PortV4'))

        #Configure the acctuators. These numbers are the steps for the vibration tip and magnet movements
        theRig.MagConfigure(config.get('AcctuatorSetup','MagEngage'))
        theRig.VibConfigure(config.get('AcctuatorSetup','VibEngage'),config.get('AcctuatorSetup','VibRetract'))


        if (Fakeout):
                print ('FAKING CONNECTION!')

        if (connect(theRig) or Fakeout):
                global folder
                folder = ''
                done=False
                while folder =='':
                        print time.strftime("%b %d %Y", time.localtime())
                        folder = raw_input('Enter Output Folder Name (then press ENTER):')

                while not done:
                        print 'Output will be saved in: {}\{}\ '.format(filepath, folder)
                        print time.strftime("%H:%M:%S", time.localtime())
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
