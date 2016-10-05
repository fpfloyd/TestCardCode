#
# Class SyringePump
#
# A class allowing control of Chemyx syringe pump
#
# Aaron Oppenheimer
# Daktari Diagnostics
#
# ChangeLog
#		V0.9	20120726	Initial work
#       V1.0    20120906        Added ability to withdraw

import DebugFunctions as db
import serial
import time

class SyringePump:

	theComPort=""
	theConnection=None

	pumpDelay=0.5 #delay after pump communication

	def __init__(self, ComPort):
		self.theComPort=ComPort

	def Connect(self):
		db.PrintDebug("Connecting syringe pump on port "+str(self.theComPort))
		success=True
		
		try:
			self.theConnection=serial.Serial(self.theComPort,9600,serial.EIGHTBITS,serial.PARITY_NONE,serial.STOPBITS_ONE,1,False,False, writeTimeout=1)
		except:
			db.PrintDebug("No pump connection!")
			self.theConnection=None
			success=False
					
		return success
	
	def Disconnect(self):
		db.PrintDebug("Disconnecting syringe pump on port "+str(self.theComPort))
		if (self.theConnection):
			self.theConnection.close()

	def Configure(self, diameter):
		db.PrintDebug("Setting syringe pump on port "+str(self.theComPort)+" to diameter "+str(diameter))
		if (self.theConnection):
			self.theConnection.flushInput()
			self.theConnection.write("set diameter "+str(diameter)+"\r\n")
			db.PrintDebug("pump: "+self.theConnection.readline())
			time.sleep(self.pumpDelay)

	def SetRate(self, rate):
		db.PrintDebug("Setting rate syringe pump on port "+str(self.theComPort)+" to "+str(rate))
		if (self.theConnection):
			self.theConnection.flushInput()
			self.theConnection.write("set rate "+str(rate)+"\r\n")
			db.PrintDebug("pump: "+self.theConnection.readline())
			db.PrintDebug("pump: "+self.theConnection.readline())
			time.sleep(self.pumpDelay)

	def SetVolume(self, vol):
		db.PrintDebug("Setting volume syringe pump on port "+str(self.theComPort)+" to "+str(vol))
		if (self.theConnection):
			self.theConnection.flushInput()
			self.theConnection.write("set volume "+str(vol)+"\r\n")
			db.PrintDebug("pump: "+self.theConnection.readline())
			db.PrintDebug("pump: "+self.theConnection.readline())
			db.PrintDebug("pump: "+self.theConnection.readline())
			time.sleep(self.pumpDelay)

	def EnableWithdraw(self):
		db.PrintDebug("Withdrawing pump on port "+str(self.theComPort))
		if (self.theConnection):
			self.theConnection.flushInput()
			self.theConnection.write("set volume -100\r\n")
			db.PrintDebug("pump: "+self.theConnection.readline())
			db.PrintDebug("pump: "+self.theConnection.readline())
			db.PrintDebug("pump: "+self.theConnection.readline())
			time.sleep(self.pumpDelay)

	def DisableWithdraw(self):
		db.PrintDebug("Withdrawing pump on port "+str(self.theComPort))
		if (self.theConnection):
			self.theConnection.flushInput()
			self.theConnection.write("set volume 100\r\n")
			db.PrintDebug("pump: "+self.theConnection.readline())
			db.PrintDebug("pump: "+self.theConnection.readline())
			db.PrintDebug("pump: "+self.theConnection.readline())
			time.sleep(self.pumpDelay)

	def Start(self, rate):
		db.PrintDebug("Starting syringe pump on port "+str(self.theComPort)+" at rate "+str(rate))
		if (self.theConnection):
			self.theConnection.flushInput()
			self.theConnection.write("set rate "+str(rate)+"\r\n")
			db.PrintDebug("pump: "+self.theConnection.readline())
			db.PrintDebug("pump: "+self.theConnection.readline())
			time.sleep(self.pumpDelay)
			self.theConnection.write("start\r\n")
			db.PrintDebug("pump: "+self.theConnection.readline())
			db.PrintDebug("pump: "+self.theConnection.readline())
			time.sleep(self.pumpDelay)
		
	def Stop(self):
		db.PrintDebug("Stopping syringe pump on port "+str(self.theComPort))
		if (self.theConnection):
			self.theConnection.flushInput()
			self.theConnection.write("stop\r\n")
			db.PrintDebug("pump: "+self.theConnection.readline())
			time.sleep(self.pumpDelay)
