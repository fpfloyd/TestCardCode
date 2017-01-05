# peak finding algorithm. Just pass it an array of signal values. Return is a map of indices of the left, peak, and right of
# whatever peak is in there, plus a sum of all the signal in that peak.
import numpy
import matplotlib.pyplot as plt
class findPeaks:

    def findPeakPositions(self,rawData,startVoltage,endVoltage,stepTimeUS):
        """
        - find the max value in this range - that is the peak
        - find the min between the peak and the right side. From there, Work left toward the peak until the current
          rises 5% of the way to the peak. That is the right end of the peak. (5% is arbitrary -
          it's possible some other value would work just as well or better.)
        - from the peak, work left until the current drops below the value at the right end of the
          peak. That is the left end of the peak.
        - the noise floor is assumed to be a constant value, same as the value at the right end of the peak.
        """

        #Adjust data to only look for peaks in a certain voltage range
        rangeStart = -0.9
        rangeEnd = -0.1
        stepSize = round((float(endVoltage) - float(startVoltage)) / (len(rawData)-1),3)
        startData = int((float(rangeStart) - float(startVoltage))/stepSize)
        endData = int(len(rawData) - (float(endVoltage)-float(rangeEnd))/stepSize)
        data = rawData[startData:endData]

        peakValue = max(data)
        peakPos = data.index(peakValue)

        valleyValue = min(data[peakPos:])
        valleyPos = data[peakPos:].index(valleyValue) + peakPos

        # now, move left until we are climbing the curve
        targetValue = valleyValue + ((peakValue - valleyValue) * .05)
        while (data[valleyPos] < targetValue and valleyPos > peakPos):
            valleyPos = valleyPos - 1

        # at this point, we know where the rise starts - call that the right side
        rightPos = valleyPos

        # the left pos is the point at which the value to the left of the peak dips to the
        # value at the right side (since we're just going to call that the noise floor

        leftPos = peakPos
        while (leftPos > 0 and data[leftPos] > targetValue):
            leftPos = leftPos - 1


        stepSize = (float(endVoltage)-float(startVoltage))/(len(data)-1)
        stepSize = round(stepSize,3)
        peakVolts = (float(startVoltage)+(peakPos*stepSize))

        #find are with respect to curve, not zero
        sweepStep = float(stepTimeUS)/1000000.0 #convert step size from uS to S
        sweepTime = sweepStep * (rightPos-leftPos)
        #baseArea = 0.5 * (data[rightPos]-data[leftPos])*(rightPos-leftPos)+(data[rightPos]*(rightPos-leftPos))
        peakArea = sum(data[leftPos:rightPos])*sweepTime
        # plt.plot(data)
        # plt.interactive(False)
        # plt.plot()
        # plt.show()

        #lets find peak height frome baseline
        if rightPos - leftPos != 0:
            slope = (data[rightPos]-data[leftPos])/(rightPos-leftPos)
            peakCurrent = peakValue-data[leftPos] +(slope*(peakPos-leftPos))
        else:
            peakCurrent = '0'
            peakArea = '0'
            peakVolts = '0'


        # OK, I think we're done here
        list = peakVolts, peakArea, peakCurrent
        return list

