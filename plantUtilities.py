#!/usr/bin/env python
__author__ = "Arana Fireheart"

from machine import ADC

levels = {"Wet": 0, "Damp": 1, "Moist": 2, "Dry": 3}
levelValues = {"Wet": [360, 420], "Damp": [420, 570], "Moist": [570, 620], "Dry": [620, 770]}
levelsValuesInOrder = ["Wet", "Damp", "Moist", "Dry"]


def uUrlEncode(dictionaryElement):
    separator = '&'
    combinedPairs = ["{0}={1}".format(valueItem, dictionaryElement[valueItem]) for valueItem in dictionaryElement]
    unifiedDictionary = separator.join(combinedPairs)
    encodedString = ''.join(
        character if character.isalpha() or character.isdigit() else '%{0:02x}'.format(ord(character)) for character in
        unifiedDictionary)
    # print(encodedString)
    return encodedString


class AnalogInWithHysteresis(object):
    def __init__(self, inputSpecifier, levelValues, hysteresisValue):
        self.currentHysteresisValue = hysteresisValue
        self.inputPinSpecifier = inputSpecifier
        self.levelValues = levelValues
        self.levelCodes = list(self.levelValues.keys())
        self.moistureSensor = ADC(self.inputPinSpecifier)
        self.previousSensorValue = 0  # Start with 'off the spectrum' values, to insure that they differ by hysterisis value.
        self.currentInputState = 1000
        self.currentInputState = self.updateCurrentSensorValue()

    def __str__(self):
        return "Pin: {0} State: {1}".format(self.inputPinSpecifier, self.currentInputState)

    def getLevelFromSensorValue(self, sensorValue):
        for level in levelValues:
            values = levelValues[level]
            if values[0] < sensorValue < values[1]:
                print("Sensor Value: {0} Level: {1}".format(sensorValue, level))
                return level

    def updateCurrentSensorValue(self):
        currentSensorReading = self.moistureSensor.read()
        # lowerValue, upperValue = self.levelValues[self.currentInputState]
        # if not(upperValue >= currentSensorReading >= lowerValue):   # Sensor value has traveled
        #                                                             # out of the current Wetness
        if abs(currentSensorReading - self.previousSensorValue) > self.getCurrentHysteresisValue():
            # value 'band' by more than
            # hysteresis value, now find new 'band'
            nextState = self.getLevelFromSensorValue(currentSensorReading)  # hysteresis value, now find new 'band'
            print("Current State: {0} Next State: {1}".format(self.currentInputState, nextState))
            self.currentInputState = nextState
            self.previousSensorValue = currentSensorReading
            print(
                "Current Sensor Reading: {0}; Current Level: {1}".format(currentSensorReading, self.currentInputState))
            return nextState
        else:
            return self.currentInputState  # Nothing changed enough

    def setCurrentHysteresisValue(self, newValue):
        if newValue > 0:
            self.currentHysteresisValue = newValue

    def getCurrentHysteresisValue(self):
        return self.currentHysteresisValue

    def setInputPinSpecifier(self, newValue):
        if newValue > 0:
            self.inputPinSpecifier = newValue

    def getInputPinSpecifier(self):
        return self.inputPinSpecifier

    def setLevelValues(self, newValues):
        if type(newValues) is dict:
            self.levelValues = newValues
        else:
            raise ValueError

    def getLevelValues(self):
        return self.levelValues

    def getCurrentInputState(self):
        return self.currentInputState

    def getCurrentInputStateValue(self):
        return levels[self.currentInputState]
