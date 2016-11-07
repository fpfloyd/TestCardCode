
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
MagStartFreq = 90       #Magnet Mixing Start Frequency (hz)
MagEndFreq = 125        #Magnet Mixing End Frequency  (hz)
MagCycles = 2           #Number of Sweep Cycles
MagMixingSteps = 1      #Number of mixing steps
MagMixingInc = 180      #Time between mag mixing steps (sec)
SilverMixingInc = 180  #Time between Silver Mixing Steps (sec)
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
PreASVWait = 600
DissTime = 30
DissVolt = 1.1
DepoTime = 120
DepoVolt = -1.0
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



