# peak finding algorithm. Just pass it an array of signal values. Return is a map of indices of the left, peak, and right of
# whatever peak is in there, plus a sum of all the signal in that peak.

class findPeaks:

    def findPeakPositions(self,data,startVoltage,endVoltage):
        """
        - find the max value in this range - that is the peak
        - find the min between the peak and the right side. From there, Work left toward the peak until the current
          rises 5% of the way to the peak. That is the right end of the peak. (5% is arbitrary -
          it's possible some other value would work just as well or better.)
        - from the peak, work left until the current drops below the value at the right end of the
          peak. That is the left end of the peak.
        - the noise floor is assumed to be a constant value, same as the value at the right end of the peak.
        """
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


        # OK, I think we're done here
        list = peakVolts, sum(data[leftPos:rightPos]),peakValue
        return list

