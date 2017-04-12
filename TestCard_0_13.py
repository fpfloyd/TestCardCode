#! /usr/bin/env python
# C1 Test Card Fixture
#
# Runs assay on C1 cards
# Connects to syringe pumps, valves, actuators and potentiostat through various microcontrollers
#
# Fred Floyd
# Daktari Diagnostics


import time
import csv
import ConfigParser
import param
import git
import DebugFunctions as db
from TestCardRig import TestCardRig

Debug = False # set this to True to enable debug by default. Can always toggle it with 'd' command
Fakeout = True #Fakeout connections, use for debugging without full test rig
Pause = False #Adds pause between each assay step that requires user input
filepath = 'C:\C1_Output'


##########
#
# Run an Assay
#
##########
def assay(theRig):

        #StartUp
        filename = ''
        while filename == '':
            filename = raw_input('Enter Filename for ASV Data (then press Enter):')
            if len(filename)==0:
                print 'Filename needed'
        stopAll(theRig)
        startTime = time.time()
        theRig.SetupASV(param.DissVolt,param.DissTime,param.DepoVolt,param.DepoTime,param.StartSweep,
                        param.EndSweep,param.SweepStep,param.SweepInc)
        theRig.SetGains(param.DissGain,param.DepoGain,param.SweepGain)

        #Open all Valves
        print time.strftime('%H:%M:%S -', time.localtime()), 'Starting Assay, Press ctrl+c at any time to quit'
        print time.strftime('%H:%M:%S -', time.localtime()), 'Setting Valves'
        theRig.ValveOpen('V1')
        theRig.ValveOpen('V2')
        theRig.ValveOpen('V3')
        theRig.ValveClose('V4')
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
        if param.B3 == False:
            #Prime ASV Channel
            print time.strftime('%H:%M:%S -', time.localtime()), 'Priming ASV Channel with ',param.ASVPrimeVol,'uL @',\
                    param.ASVPrimeRate,'uL/min'
            theRig.ValveOpen('V3')
            theRig.ValveClose('V1')
            theRig.ValveClose('V4')
            theRig.ValveClose('V2')
            theRig.PumpStart('B2', param.ASVPrimeRate, param.ASVPrimeVol)
            time.sleep(param.ASVPrimeTime)
            if Pause == True:
                raw_input('Press enter to continue')

            #Ensure Chamber Is Empty
            print time.strftime('%H:%M:%S -', time.localtime()), 'Emptying Chamber with', param.WashoutVol50, 'uL @', \
                    param.WashoutRate50, 'uL/min'
            theRig.VibRetract()
            time.sleep(0.5)
            theRig.ValveClose('V3')
            theRig.ValveOpen('V2')
            theRig.ValveClose('V1')
            theRig.ValveOpen('V4')
            theRig.PumpStart('B6', param.WashoutRate50, param.WashoutVol50)
            time.sleep(param.WashoutTime50)
            theRig.ValveClose('V4')
            theRig.VibEngage()
            if Pause == True:
                raw_input('Press enter to continue')

        if param.B3 == True:
            # Prime ASV Channel
            print time.strftime('%H:%M:%S -', time.localtime()), 'Priming ASV Channel with ', param.ASVPrimeVol, 'uL @', \
                param.ASVPrimeRate, 'uL/min'
            theRig.ValveOpen('V1')
            theRig.ValveClose('V3')
            theRig.ValveClose('V4')
            theRig.ValveClose('V2')
            theRig.PumpStart('B2', param.ASVPrimeRate, param.ASVPrimeVol)
            time.sleep(param.ASVPrimeTime)
            if Pause == True:
                raw_input('Press enter to continue')

            # Prime V3
            print time.strftime('%H:%M:%S -', time.localtime()), 'Priming V3 with ', param.V3PrimeVol, 'uL @', \
                param.ASVPrimeRate, 'uL/min'
            theRig.ValveOpen('V3')
            theRig.ValveClose('V1')
            theRig.ValveClose('V4')
            theRig.ValveClose('V2')
            theRig.PumpStart('B2', param.PrimeRate, param.V3PrimeVol)
            time.sleep(param.V3PrimeTime)
            if Pause == True:
                raw_input('Press enter to continue')

            # Ensure Chamber Is Empty
            print time.strftime('%H:%M:%S -', time.localtime()), 'Emptying Chamber with', param.WashoutVol50, 'uL @', \
                param.WashoutRate50, 'uL/min'
            theRig.VibRetract()
            time.sleep(0.5)
            theRig.ValveClose('V3')
            theRig.ValveOpen('V2')
            theRig.ValveClose('V1')
            theRig.ValveOpen('V4')
            theRig.PumpStart('B6', param.WashoutRate50, param.WashoutVol50)
            time.sleep(param.WashoutTime50)
            theRig.ValveClose('V4')
            theRig.VibEngage()
            if Pause == True:
                raw_input('Press enter to continue')


        #Push Plasma to Mixing Chamber with Lysis Buffer
        print time.strftime('%H:%M:%S -', time.localtime()), 'Pushing Plasma to Mixing Chamber with ',\
                param.PlasmaPushVol,'uL @',param.PlasmaPushRate,'uL/min'
        theRig.ValveOpen('V1')
        theRig.ValveClose('V2')
        theRig.ValveClose('V3')
        theRig.PumpStart('B1', param.PlasmaPushRate, param.PlasmaPushVol)
        time.sleep(param.PlasmaPushTime)
        if Pause == True:
            raw_input('Press enter to continue')

        #Add Mags to Chamber While Mixing
        print time.strftime('%H:%M:%S -', time.localtime()), 'Adding Mags with',param.MagFlowVol,\
                'uL @',param.MagFlowRate,'uL/min. Mixing Step:', 1, 'of', param.MagMixingSteps
        theRig.VibrationStart(param.MagFlowTime,param.MagStartFreq,param.MagEndFreq,param.MagCycles)
        theRig.PumpStart('B4', param.MagFlowRate, param.MagFlowVol)
        time.sleep(param.MagFlowTime)
        if Pause == True:
            raw_input('Press enter to continue')

        if param.ExtraMixing == False:
            # Mix and Incubate Mags
            i = 2
            print time.strftime('%H:%M:%S -', time.localtime()), 'Mixing and Incubating Mags for ', param.MagMixingInc, ' Seconds'
            while i <= param.MagMixingSteps:
                    i = i + 1
                    time.sleep(param.MagMixingInc / param.MagMixingSteps)
                    print time.strftime('%H:%M:%S -', time.localtime()), 'Mixing Step:', i - 1, 'of', param.MagMixingSteps
                    theRig.VibrationStart(param.MagSweepTime, param.MagStartFreq, param.MagEndFreq, param.MagCycles)
            time.sleep(param.MagMixingInc / param.MagMixingSteps)

        if param.ExtraMixing == True:
            i = 2
            print time.strftime('%H:%M:%S -', time.localtime()), 'Mixing & Incubating Full Sandwiches for', \
                param.MagMixingInc, ' seconds'
            while i <= param.MagMixingSteps:
                print time.strftime('%H:%M:%S -', time.localtime()), 'Mixing Step:', i, 'of ', param.MagMixingSteps
                i = i + 1
                theRig.VibrationStart(param.MagSweepTime, param.MagStartFreq, param.MagEndFreq,
                                      param.MagCycles)
                time.sleep(param.MagMixingInc / (param.MagMixingSteps-1))

        # Pulldown Mags
        print time.strftime('%H:%M:%S -', time.localtime()), 'Pulling Down Mags'
        theRig.MagnetEngage()
        time.sleep(0.5)
        theRig.VibRetract()
        time.sleep(param.PulldownTime)
        if Pause == True:
                raw_input('Press enter to continue')

        #Empty Chamber
        print time.strftime('%H:%M:%S -', time.localtime()), 'Emptying Chamber with',param.WashoutVol50,'uL @',param.WashoutRate50,'uL/min '
        theRig.ValveOpen('V2')
        theRig.ValveOpen('V4')
        theRig.ValveClose('V1')
        theRig.PumpStart('B6', param.WashoutRate50, param.WashoutVol50)
        time.sleep(param.WashoutTime50)
        theRig.ValveClose('V4')
        theRig.VibEngage()
        if Pause == True:
            raw_input('Press enter to continue')

        #Add Wash Buffer to Chamber
        print time.strftime('%H:%M:%S -', time.localtime()), 'Adding wash buffer to half sandwiches with',\
                param.WashVol,'uL @',param.WashRate,'uL/min'
        theRig.ValveOpen('V1')
        theRig.ValveClose('V2')
        theRig.PumpStart('B1', param.WashRate, param.WashVol)
        time.sleep(param.WashTime)
        if Pause == True:
            raw_input('Press enter to continue')

        # Mixing and Resuspend Half Sandwiches
        i = 1
        print time.strftime('%H:%M:%S -', time.localtime()), 'Mixing/Washing Half Sandwiches'
        theRig.MagnetRetract()
        while i <= param.OtherMixingSteps:
            i = i + 1
            print time.strftime('%H:%M:%S -', time.localtime()), 'Mixing Step:', i - 1, 'of ', param.OtherMixingSteps
            theRig.VibrationStart(param.OtherSweepTime, param.OtherStartFreq, param.OtherEndFreq, param.OtherCycles)
            time.sleep(param.OtherMixingPause)

        # Pulldown Half Sandwiches
        print time.strftime('%H:%M:%S -', time.localtime()), 'Pulling Down Half Sandwiches'
        theRig.MagnetEngage()
        time.sleep(0.5)
        theRig.VibRetract()
        time.sleep(param.PulldownTime)
        if Pause == True:
            raw_input('Press enter to continue')

        #Empty Chamber
        print time.strftime('%H:%M:%S -', time.localtime()), 'Emptying Chamber with',param.WashoutVol100,'uL @',\
                param.WashoutRate100,'uL/min'
        theRig.ValveOpen('V2')
        theRig.ValveClose('V1')
        theRig.ValveOpen('V4')
        theRig.PumpStart('B6', param.WashoutRate100, param.WashoutVol100)
        time.sleep(param.WashoutTime100)
        theRig.ValveClose('V4')
        theRig.VibEngage()
        if Pause == True:
            raw_input('Press enter to continue')

        #Add Silver to Chamber
        print time.strftime('%H:%M:%S -', time.localtime()), 'Adding Silver with',param.SilverVol,'uL @',\
                param.SilverRate,'uL/min'
        theRig.ValveOpen('V1')
        theRig.ValveClose('V2')
        theRig.PumpStart('B5', param.SilverRate,param.SilverVol)
        time.sleep(param.SilverTime)
        if Pause == True:
            raw_input('Press enter to continue')

        #Mix Resuspend and Incubate Full Sandwiches
        i = 1
        print time.strftime('%H:%M:%S -', time.localtime()), 'Mixing & Incubating Full Sandwiches for',\
                param.SilverMixingInc,' seconds'
        theRig.MagnetRetract()
        while i <= param.SilverMixingSteps:
            print time.strftime('%H:%M:%S -', time.localtime()), 'Mixing Step:', i , 'of ', param.SilverMixingSteps
            i = i + 1
            theRig.VibrationStart(param.SilverSweepTime, param.SilverStartFreq, param.SilverEndFreq, param.SilverCycles)
            time.sleep(param.SilverMixingInc / param.SilverMixingSteps)

        # Pulldown Sandwiches
        print time.strftime('%H:%M:%S -', time.localtime()), 'Pulling Down Full Sandwiches'
        theRig.MagnetEngage()
        time.sleep(0.5)
        theRig.VibRetract()
        time.sleep(param.PulldownTime)
        if Pause == True:
            raw_input('Press enter to continue')

        #Empty Chamber
        print time.strftime('%H:%M:%S -', time.localtime()), 'Emptying Chamber with',param.WashoutVol50,\
                'uL @',param.WashoutRate50,'uL/min'
        theRig.ValveOpen('V2')
        theRig.ValveClose('V1')
        theRig.ValveOpen('V4')
        theRig.PumpStart('B6', param.WashoutRate50, param.WashoutVol50)
        time.sleep(param.WashoutTime50)
        theRig.ValveClose('V4')
        theRig.VibEngage()
        if Pause == True:
            raw_input('Press enter to continue')

        #Add Wash to Chamber
        print time.strftime('%H:%M:%S -', time.localtime()), 'Washing half sandwiches with',param.WashVol,\
                'uL @',param.WashRate,'uL/min'
        theRig.ValveOpen('V1')
        theRig.ValveClose('V2')
        theRig.PumpStart('B1', param.WashRate, param.WashVol)
        time.sleep(param.WashTime)
        if Pause == True:
            raw_input('Press enter to continue')

        #Mix Resuspend and Wash Full Sandwiches
        i = 1
        print time.strftime('%H:%M:%S -', time.localtime()), 'Mixing/Washing Full Sandwiches'
        theRig.MagnetRetract()
        while i <= param.OtherMixingSteps:
            i = i + 1
            print time.strftime('%H:%M:%S -', time.localtime()), 'Mixing Step:', i - 1
            theRig.VibrationStart(param.OtherSweepTime, param.OtherStartFreq, param.OtherEndFreq, param.OtherCycles)
            time.sleep(param.OtherMixingPause)

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
        # print time.strftime('%H:%M:%S -', time.localtime()), 'Emptying Mixing Chamber with',param.WashoutVol100,\
        #         'uL @',param.WashoutRate100,'uL/min '
        # theRig.ValveOpen('V2')
        # theRig.ValveClose('V1')
        # theRig.ValveOpen('V4')
        # theRig.PumpStart('B6', param.WashoutRate100, param.WashoutVol100)
        # time.sleep(param.WashoutTime100)
        # theRig.ValveClose('V4')
        # theRig.VibEngage()
        # if Pause == True:
        #     raw_input('Press enter to continue')
        #
        # if param.DispenseV2 == False:
        #     #Drain ASV Chamber
        #     theRig.ValveClose('V2')
        #     theRig.ValveOpen('V3')
        #     theRig.ValveOpen('V4')
        #     print time.strftime('%H:%M:%S -', time.localtime()), 'Emptying ASV Chamber with 50uL @ 100uL/min'
        #     theRig.PumpStart('B6', 100, 50)
        #     time.sleep(30)
        #     theRig.ValveClose('V4')
        #
        #     #Fill ASV Chamber w/ Elyte
        #     print time.strftime('%H:%M:%S -', time.localtime()), 'Filling ASV Chamber with 50uL @ 100uL/min'
        #     theRig.PumpStart('B2', 100, 50)
        #     time.sleep(30)
        #
        # #Fill Mixing Chamber with Elyte
        # print time.strftime('%H:%M:%S -', time.localtime()), 'Filling Mixing Chamber with 50uL @ 100uL/min'
        # theRig.ValveOpen('V1')
        # theRig.ValveClose('V3')
        # theRig.PumpStart('B2', 100, 60)
        # time.sleep(30)
        #
        # #Resuspend Sandwiches
        # i = 1
        # print time.strftime('%H:%M:%S -', time.localtime()), 'Mixing/Washing Full Sandwiches'
        # theRig.MagnetRetract()
        # while i <= param.OtherMixingSteps:
        #     i = i + 1
        #     print time.strftime('%H:%M:%S -', time.localtime()), 'Mixing Step:', i - 1
        #     theRig.VibrationStart(param.OtherSweepTime, param.OtherStartFreq, param.OtherEndFreq, param.OtherCycles)
        #     time.sleep(param.OtherMixingPause)
        #
        # if param.DispenseV2 == False:
        #     #Move to ASV Chamber
        #     print time.strftime('%H:%M:%S -', time.localtime()), 'Moving Sandwiches to ASV Chamber with',\
        #             param.MoveVol,'uL @',param.MoveRate,'uL/min'
        #     theRig.VibRetract()
        #     time.sleep(0.5)
        #     theRig.ValveOpen('V3')
        #     theRig.ValveClose('V1')
        #     theRig.ValveOpen('V4')
        #     theRig.PumpStart('B6',param.MoveRate,param.MoveVol)
        #     time.sleep(param.MoveTime)
        #     theRig.ValveClose('V4')
        #     if Pause == True:
        #         raw_input('Press enter to continue')
        #
        #     #Fill ASV Chamber with Electrolyte
        #     print time.strftime('%H:%M:%S -', time.localtime()), 'Filling ASV Chamber with',param.ElecVol,\
        #             'uL of Electrolyte at',param.ElecRate,'uL/min'
        #     theRig.PumpStart('B2',param.ElecRate, param.ElecVol)
        #     theRig.ValveClose('V1')
        #     time.sleep(param.ElecTime)
        #     if Pause == True:
        #         raw_input('Press enter to continue')
        #
        #     #Run ASV
        #     print time.strftime('%H:%M:%S -', time.localtime()), 'Wetting Electrode for', param.PreASVWait, 'seconds'
        #     time.sleep(param.PreASVWait)
        #     print time.strftime('%H:%M:%S -', time.localtime()), 'Running ASV'
        #     theRig.RunASV()
        #     print time.strftime('%H:%M:%S -', time.localtime()), 'Saving ASV'
        #     theRig.SaveASV(filepath,folder,filename)

        if param.DispenseV2 == True:
            theRig.VibRetract()
            print time.strftime('%H:%M:%S -', time.localtime()), 'Disconnect Sample Port and Place in Eppendorf '\
                    'Tube, Then Press Enter'
            raw_input()
            theRig.AllValvesClose()
            theRig.ValveOpen('V4')
            print time.strftime('%H:%M:%S -', time.localtime()), 'Draining Sample Through V2 to Eppendorf Tube'
            theRig.PumpStart('B6', param.DispenseFlowrate, param.DispenseVolume)
            time.sleep((param.DispenseVolume/param.DispenseFlowrate)*60)

        print time.strftime('%H:%M:%S -', time.localtime()), 'Assay Complete!'
        assayTime = round(((time.time()-startTime)/60),2)
        print 'Assay Time: '+str(assayTime)+' Minutes'
        stopAll(theRig)
        beep()
        time.sleep(0.1)
        airReset(theRig)
        time.sleep(0.1)
        beep()

##########
#
# Reset Air Syringe
#
##########
def airReset(theRig):
        raw_input('Ensure card is removed from rig and press Enter')
        print 'Resetting Air Syringe'
        theRig.ValveOpen('V4')
        theRig.PumpStart('B6', 1800, -1000)
        time.sleep(35)
        theRig.PumpStart('B6', 100, 5)
        time.sleep(3)
        theRig.PumpRate('B6', 100)
        return


##########
#
# Clean the Valves
#
##########
def clean(theRig):
        print 'This will guide you through cleaning the valves after use. You should also rinse the reagent tubes with ' \
              'DI Water followed by air\n'
        stopAll(theRig)
        print 'Opening Valve 1'
        theRig.ValveOpen('V1')
        raw_input('Wash Valve 1 with DI Water then dry with air, press enter when finished')
        theRig.ValveClose('V1')
        print 'Opening Valve 2'
        theRig.ValveOpen('V2')
        raw_input('Wash Valve 2 with DI Water then dry with air, press enter when finished')
        theRig.ValveClose('V2')
        print 'Opening Valve 3'
        theRig.ValveOpen('V3')
        raw_input('Wash Valve 3 with DI Water then dry with air, press enter when finished')
        theRig.ValveClose('V3')
        print 'Cleaning finished, be sure to clean the reagent lines'
        time.sleep(2)

##########
#
# Run a priming sequence
#
##########
def prime(theRig):
    print 'Ensure Card is Removed from Fixture'
    done = False
    while not done:
        a = raw_input('Choose Channel to Prime: 1, 2, 4, 5, (a)ll or (e)xit')
        if len(a)==0:
            pass
        elif a[0]=='1':
            raw_input('Press enter to start')
            theRig.PumpStart('B1',600)
            raw_input('Press enter to stop B1')
            theRig.PumpStop('B1')

        elif a[0]=='2':
            raw_input('Press enter to start')
            theRig.PumpStart('B2',600)
            raw_input('Press enter to stop B2')
            theRig.PumpStop('B2')

        elif a[0]=='4':
            raw_input('Press enter to start')
            theRig.PumpStart('B4',600)
            raw_input('Press enter to stop B4')
            theRig.PumpStop('B4')

        elif a[0]=='5':
            raw_input('Press enter to start')
            theRig.PumpStart('B5',600)
            raw_input('Press enter to stop B5')
            theRig.PumpStop('B5')

        elif a[0]=='a':
            raw_input('Press enter to start')
            print 'Starting Pumps'
            theRig.PumpStart('B1', 600)
            time.sleep(0.5)
            theRig.PumpStart('B2', 600)
            time.sleep(0.5)
            theRig.PumpStart('B4', 600)
            time.sleep(0.5)
            theRig.PumpStart('B5', 600)
            raw_input('Press enter to stop pumps')
            stopAll(theRig)

        elif a[0]=='e':
            print('Priming Complete!')
            done = True

        else:
            print 'Unknown Command'

##########
#
# Operate manually
#
##########

def doManual(theRig):
        
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

        repo = git.Repo(search_parent_directories=True)
        sha = repo.head.object.hexsha
        branch = repo.active_branch
        print '\n'
        print 'VERSION: ' + str(branch) + '_' + str(sha[:5])
        print '\n'

        db.setDebug(Debug)

        # Import Configuration from setup file
        config = ConfigParser.ConfigParser()
        config.read('setup.ini')
        config.sections()

        # Configure the Arduinos
        # (VibVal controller, Magnet Controller, Potentiostat)
        theRig=TestCardRig(config.get('ArduinoSetup','ComVibVal'),config.get('ArduinoSetup','ComMag'),
                           config.get('ArduinoSetup','ComASV'))

        if (connect(theRig) or Fakeout):
                global folder
                folder = ''
                done=False
                print '\n'
                if not Fakeout:
                    print 'CONNECTED TO FIXTURE'
                else:
                    print 'FAKING CONNECTION'
                print '\n'
                while folder =='':
                        print time.strftime("%b %d %Y", time.localtime())
                        folder = raw_input('Enter Output Folder Name (then press ENTER):')

                while not done:
                        print 'VERSION: ' + str(branch) + '_' + str(sha[:5])
                        print 'Output will be saved in: {}\{}\ '.format(filepath, folder)
                        a=raw_input('key to start: (a)ssay, (p)rime, (c)lean, pa(r)se folder, a(i)r reset,' \
                                    ' change (f)older, (q)uit')
                        # secretly, we can also turn debug messages on and off with 'd'
                        try:
                                if (a=='a'):
                                        assay(theRig)
                                elif(a=='p'):
                                        prime(theRig)
                                elif(a=='c'):
                                        clean(theRig)
                                elif (a=='f'):
                                        folder = raw_input('Enter Output Folder Name (then press ENTER):')
                                elif (a=='r'):
                                        theRig.ParseASV(filepath,folder)
                                elif (a=='i'):
                                        airReset(theRig)
                                elif (a=='m'):
                                        doManual(theRig)
                                elif (a=='t'):
                                        ardTest(theRig)
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
