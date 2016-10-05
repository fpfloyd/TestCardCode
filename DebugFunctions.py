#
# Module DebugFunctions
#
# A module containing some printing stuff we can turn on and off for debug purposes
#
# Aaron Oppenheimer
# Daktari Diagnostics
#
# ChangeLog
#		V0.9	20120726	Initial work
#		V1.0	20120821	Added ability to turn it on and off. Ship it!

debug=False

def PrintDebug(str):
	global debug
	if (debug):
		print "  -- "+str

def PrintListDB(list):
	global debug
	if (debug):
		print " -- "
		print (list)
		
def setDebug(d):
	global debug
	debug=d
	
def toggleDebug():
	global debug
	debug=not debug
	print("Debug: "+str(debug))
	
