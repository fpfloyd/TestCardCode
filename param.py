
##########
#
# ASSAY PARAMETERS
#
##########

#TESTING PARAMETERS
DispenseV2 = False
DispenseFlowrate = 100
DispenseVolume = 300
oldCode = False

if oldCode == True:
    WashoutVolPre = 110
    WashoutTimePre = (WashoutVolPre * 60.0/100)+2
else:
    WashoutVolPre = 200
    WashoutTimePre = 130

#Prime Parameters
PrimeRate=100
B1PrimeVol=0
B2PrimeVol=0
B3PrimeVol=0
B4PrimeVol=4
B5PrimeVol=3


#ASV PRIME PARAMETERS
ASVPrimeRate=100        #ASV Prime Flowrate (uL/min)
ASVPrimeVol=50         #ASV Prime Volume (uL)

#TRANSFER CHANNEL PARAMETERS
TXPrimeRate=100         #Transfer channel prime flowrate (uL/min)
TXPrimeVol=5           #Transfer channel prime volume (uL)

#Valve 3 Prime parameter
V3PrimeRate=100         #Valve 3 Prime rate
V3PrimeVol=100          #Valve 3 prime volume

#PLASMA FLOW PARAMETERS
PlasmaPushRate=100      #Flowrate for plasma being pushed to mixing chamber (uL/min)
PlasmaPushVol=46        #Plasma Push Volume (uL) [subtracted 25uL to remove lysis buffer]

#DILLUTION AND MAG ADDITION PARAMETERS
MagFlowRate=100         #Flowrate for mag beads being pushed into mixing chamber (uL/min)
MagFlowVol=30           #Mag Bead volume (uL)

#MAG MIX PARAMETERS
MagSweepTime = 30       #Magnet Mixing Sweep Time (sec)
MagStartFreq = 60       #Magnet Mixing Start Frequency (hz)
MagEndFreq = 90         #Magnet Mixing End Frequency  (hz)
MagCycles = 1           #Number of Sweep Cycles
MagMixingSteps = 1      #Number of mixing steps
MagMixingInc = 30      #Mag Incubation Time (sec)
MagMixingPause = (MagCycles * MagSweepTime) + 10 #Sweep Time is not exact


#SILVER MIX PARAMETERS
SilverSweepTime = 30
SilverStartFreq = 60
SilverEndFreq = 90
SilverCycles = 1
SilverMixingSteps= 1    #Number of Silver Mixing Steps
SilverMixingInc = 30     #Silver Incubation Time (sec)
SilverMixingPause = (SilverCycles * SilverSweepTime) + 10 #Sweep Time is not exact

#Other MIX PARAMETERS
OtherSweepTime = 30
OtherStartFreq = 60
OtherEndFreq = 90
OtherCycles = 1
OtherMixingSteps= 1   #Number of Silver Mixing Steps
OtherMixingPause = (SilverCycles * SilverSweepTime) + 10 #Sweep Time is not exact

#PULLDOWN AND WASHOUT PARAMETERS
PulldownTime=40         #Time for mags to pull down
WashoutRate100=100      #Air flowrate for 100 uL(uL/min)
WashoutVol100=170       #Air Volume for 100 uL (uL)
PulldownTime1=10        #Time for mags to pull down
WashoutRate50=100       #Air flowrate (uL/min)
WashoutVol50=120        #Air volume for 50uL (uL/min)

#WASH PARAMETERS
WashRate=100
WashVol=50

#SILVER ADDITION PARAMETERS
SilverRate=100
SilverVol=50

#DETECTION CHAMBER PARAMETERS
SandwichRate=100     #Sandwich Resuspension Flowrate (uL/min)
SandwichVol=50       #Sandwich Resuspension Time (sec)
MoveRate=50          #Sandwich Move Flowrate (uL/min)
MoveVol=175          #Sandwich Move Flow Time (sec)
ElecRate=50          #Electrolyte Flowrate (uL/min)
ElecVol=40           #Electrolyte Flow Time (sec)

#ASV PARAMETERS
PreASVWait = 600
DissTime = 30
DissVolt = 0.8
DepoTime = 120
DepoVolt = -0.9
StartSweep = -1
EndSweep = 0.1
SweepStep = 100
SweepInc = 10000
DissGain = 2
DepoGain = 4
SweepGain = 4


##########
#
# Calculate Syringe Pump Times (No feedback from pump)
#
##########
ExtraTime=2             #Extra time after the syringe pump finishes
ASVPrimeTime=(ASVPrimeVol*60.0/ASVPrimeRate)+ExtraTime
TXPrimeTime=(TXPrimeVol*60.0/TXPrimeRate)+ExtraTime
V3PrimeTime=(V3PrimeVol*60.0/V3PrimeRate)+ExtraTime
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



