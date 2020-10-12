#!/usr/bin/env python
__author__ = "Arana Fireheart"

from machine import Timer, sleep
from micropython import schedule

versionNumber = "0.1.3"


class TimeWarden(object):
    def __init__(self, startingTickValue):
        self.tickTock = Timer(-1)
        self.basicTimeUnit = startingTickValue
        self.currentTime = 0
        self.eventsList = {}
        self.rolloverTime = 0  # Once the 'latest' event has been processed, reset the time bask to zero.
        self.tickTock.init(period=self.basicTimeUnit, mode=Timer.PERIODIC, callback=self.processClick)

    def __del__(self):
        print("Deleting the timers")
        self.shutdown()

    def __str__(self):
        returnString = "Events: "
        returnString += str(self.eventsList)
        returnString += "\nTime unit: {0}; Current time: {1}; Rollover time: {2}".format(self.basicTimeUnit, self.currentTime, self.rolloverTime)
        return returnString

    @staticmethod
    def version():
        return versionNumber

    def registerEvent(self, eventData):
        # Events data is a dictionary where the key is the click count for firing the event.
        # and the value is a list of function/method names to call upon firing.
        # print("New event: {0}".format(eventData))
        # print("Current events: {0}".format(self.eventsList))
        # print("Incoming keys {0}".format(eventData.keys()))
        for newEvent in eventData.keys():
            if type(eventData[newEvent]) == list:  # Make sure that a list was passed in.
                if newEvent > self.rolloverTime:
                    self.rolloverTime = newEvent
                if newEvent in self.eventsList:
                    # print("found event: {0} {2} & type: {1}".format(newEvent, type(newEvent), eventData[newEvent]))
                    eventMethodsList = self.eventsList[newEvent]
                    eventMethodsList.extend(eventData[newEvent])
                    self.eventsList[newEvent] = eventMethodsList
                else:
                    # print("new event: {0} {2} & type: {1}".format(newEvent, type(newEvent), eventData[newEvent]))
                    self.eventsList[newEvent] = eventData[newEvent]
            else:
                raise ValueError

    def deregisterEvent(self, eventData):
        # Events data is a dictionary where the key is the click count for firing the event.
        # and the value is a list of function/method names to removed from firing.
        for searchEvent in eventData.keys():  # Find each clickTime for the event(s) to be removed
            if searchEvent in self.eventsList:  # If the clickTime is currently registered
                currentEvents = self.eventsList[searchEvent]
                if len(currentEvents) > 1:
                    for deadEvent in eventData[searchEvent]:  # Go find each method name to remove.
                        if deadEvent == self.rolloverTime:
                            temp = list(self.eventsList.keys())
                            self.rolloverTime = temp.sort()[-2]
                            # print("Deleted; {0} Latest: {1}".format(deadEvent, self.latestTime))
                        currentEvents.remove(deadEvent)
                    self.eventsList[searchEvent] = currentEvents
                else:  # This is the last at this time, remove the time
                    temp = list(self.eventsList.keys())
                    temp.sort()
                    self.rolloverTime = temp[-2]
                    # print("Deleted; {0} Latest: {1}".format(searchEvent, self.latestTime))
                    del self.eventsList[searchEvent]

    def clearAllEvents(self):
        self.eventsList.clear()

    def getCurrentTime(self):
        return self.currentTime

    def setCurrentTime(self, newTime):
        if newTime >= 0:
            self.currentTime = newTime

    def incrementCurrentTime(self, incrementValue=1):
        self.currentTime += incrementValue * self.getBasicTimeUnit()
        if self.currentTime > self.rolloverTime:
            # print("Counter reset from {0}".format(self.currentTime))
            self.currentTime = 0

    def getBasicTimeUnit(self):
        return self.basicTimeUnit

    def setBasicTimeUnit(self, newTimeUnit):
        if newTimeUnit >= 0:
            self.basicTimeUnit = newTimeUnit

    def processClick(self, dummyStuff):
        # print("Starting click processing")
        self.incrementCurrentTime()
        currentTime = self.getCurrentTime()
        timesList = list(self.eventsList.keys())
        timesList.sort()
        for timeValue in timesList:
            multiplier = currentTime // timeValue
            searchTime = currentTime // multiplier if multiplier != 0 else currentTime
            if currentTime % timeValue == 0 and searchTime in timesList:
                # print("Found an event to run! :-)")
                events = self.eventsList[searchTime]
                for event in events:
                    schedule(event, 'Event!')

    def shutdown(self):
        print("Shutting down timers")
        self.tickTock.deinit()
