#
# Class ParseASV
#
# A class allowing the program to easily parse data when user prompts
#
# Eric Evje / Fred Floyd
# Daktari Diagnostics
#
# ChangeLog
#               20160928        Initial Work, modified code from 20150928_ASV_Celestica_Parser_D2.py


import DebugFunctions as db
import re
import csv
import os


class ParseASV:


        def ParseASV(self,filepath,folder):
            db.PrintDebug("Parsing ASV Data")
            # Assign variables from cmd line user input, and open writeable file
            # folderDirectory = raw_input("Enter Directory for Folder to Analyze: ")
            # outfile = raw_input("Enter .csv filename to be written to: ")

            # read in folder with data and pass to list
            folderDirectory = "{}\{}".format(filepath,folder)
            fileList = os.listdir(folderDirectory)
            db.PrintListDB(fileList)

            # make counter variable for counting number of file in parser
            i = 0
            j = 0
            # make counter for finding blank lists
            counter = 0

            # create list of list for value storage
            sweepMatrix = [[]]
            sweepMatrix.append([])

            dissolutionMatrix = [[]]
            dissolutionMatrix.append([])

            depositionMatrix = [[]]
            depositionMatrix.append([])

            # create list for headers
            headerList = []
            depdisHeaderList = []

            # Open each file in the folder successively
            # change directory to folder directory
            os.chdir(folderDirectory)
            for filename in fileList:
                rawData = open(filename, 'r')
                db.PrintListDB(filename)
                if len(sweepMatrix[0]) == 0:
                    writeVoltage = True
                    writeTimeDep = True
                    writeTimeDis = True

                # Parse through file
                for line in rawData:
                    dissolution = re.search('Dissolution phase\. Polarization voltage = \s*(\S*) Volts', line)
                    deposition = re.search('Deposition phase\. Polarization voltage =\s*(\S*) Volts', line)
                    ramp = re.search('Sweep phase\. Linear ramp up to\s*(\S*) Volts.', line)
                    sweep = re.search('Cell voltage:\s*(\S*) Volts,	Cell current:\s*(\S*) uA', line)
                    Dis_dep = re.search('Time \(S\): (\S*)\s*ADC voltage:\s*\S* Volts,	Cell current:\s*(\S*) uA',
                                        line)

                    # assign values to appropriate list
                    if dissolution != None:
                        dissolutionValue = dissolution.group(1)
                        db.PrintDebug(dissolutionValue)

                        dissolutionCounter = 1
                        depositionCounter = 0

                    if deposition != None:
                        depositionValue = deposition.group(1)
                        db.PrintDebug(depositionValue)

                        dissolutionCounter = 0
                        depositionCounter = 1

                    if ramp != None:
                        rampValue = ramp.group(1)
                        db.PrintDebug(rampValue)
                    if sweep != None:
                        counter = 1

                        # assign variables to voltage if it has not already been done
                        if writeVoltage == True:
                            sweepMatrix[0].append(sweep.group(1))

                        # assign variables to the list corresponding to the file that is opened
                        sweepMatrix[i + 1].append(sweep.group(2))

                    if Dis_dep != None:
                        counter = 1
                        if dissolutionCounter == 1:

                            if writeTimeDis == True:
                                dissolutionMatrix[0].append(Dis_dep.group(1))

                            dissolutionMatrix[j + 1].append(Dis_dep.group(2))

                        if depositionCounter == 1:

                            if writeTimeDep == True:
                                depositionMatrix[0].append(Dis_dep.group(1))

                            depositionMatrix[j + 1].append(Dis_dep.group(2))

                # append filename to header list only if there was data in the file
                if counter == 1:
                    filename = re.sub('.txt', '', filename)
                    headerList.append(filename)
                    depdisHeaderList.append(filename)
                    db.PrintListDB(headerList)
                    counter = 0

                # add empty list to list of lists
                sweepMatrix.append([])
                dissolutionMatrix.append([])
                dissolutionMatrix.append([])
                depositionMatrix.append([])
                depositionMatrix.append([])

                writeVoltage = False
                writeTimeDep = False
                writeTimeDis = False

                i = i + 1
                j = j + 1

                rawData.close()

            # remove empty lists from list of lists
            fullMatrix = filter(None, sweepMatrix)
            # transpose matrix
            transposedMatrix = zip(*fullMatrix)

            filterDepositionMatrix = filter(None, depositionMatrix)
            transposedDepositionMatrix = zip(*filterDepositionMatrix)

            filterDissolutionMatrix = filter(None, dissolutionMatrix)
            transposedDissolutionMatrix = zip(*filterDissolutionMatrix)

            # write sweep information to csv file
            with open('sweep.csv', "wb") as f:
                writer = csv.writer(f)
                headerList = ",".join(headerList)
                f.write("voltage (V)," + str(headerList) + "\n")
                writer.writerows(transposedMatrix)

            # write deposition information to csv file
            with open('Deposition.csv', "wb") as f:
                depdisHeaderList = ",".join(depdisHeaderList)
                writer = csv.writer(f)
                f.write("ramp Finishing Value (V)," + str(rampValue) + "\n")
                f.write("Time (s)," + str(depdisHeaderList) + "\n")
                writer.writerows(transposedDepositionMatrix)

            # write dissolution information to csv file
            with open('Dissolution.csv', "wb") as f:
                writer = csv.writer(f)
                f.write("Time (s)," + str(depdisHeaderList) + "\n")
                writer.writerows(transposedDissolutionMatrix)

            with open('Summary.csv', "wb") as f:
                writer = csv.writer(f)
                f.write("Dissolution Voltage (V)," + str(dissolutionValue) + "\n")
                f.write("Deposition Voltage (V)," + str(depositionValue) + "\n")
                f.write("ramp Finishing Value (V)," + str(rampValue) + "\n")
                print "Folder Successfully Parsed"
