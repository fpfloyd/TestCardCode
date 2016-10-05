import ASV_plot as ASV

thePotentiostat = {}

def __init__(self):
    self.thePotentiostat = ASV('/dev/cu.usbmodem851611')
    self.thePotentiostat.Connect()

ASV.RunASV()
