# -*- coding: utf-8 -*-
import unittest
from timeEventFactory import getEventFact
from timeEventClasses import *
from  timeController import *

class CNetworkDeviceStatusCheckEventTest (unittest.TestCase):
    def testNetworkDevice (self):
        oEvent = CNetworkDeviceStatusCheckEvent ()
        oEvent.init ([MONTAG], 20, 0, "192.168.178.1", EMAIL_NOTIFY_Always)
        oEvent.action()
        
        

class CTimeControllerTest (unittest.TestCase):
    def testTimeController (self):
        #Event Factory holen...
        evFact = getEventFact()
        #Factory produziert Events...
        evFact.produceEvents()
        events = evFact.getTimeEvents()
        assert (type (events) == list)
        listOfTestSituations = self.getTestSituations ()
        assert (type (listOfTestSituations) == list)
        iExecutedTotal = 0
        for iCurrentTestSituation in range (0, len (listOfTestSituations), 1):
            iExecuted = checkAndExecuteEventList (events, listOfTestSituations [iCurrentTestSituation ])
            iExecutedTotal = iExecutedTotal + iExecuted
        self.assertEqual (iExecutedTotal, 1)    
            

    def getTestSituations (self) :
        """This function emulates dates and times, this enables to test the events defined in the XMl file independently from current date and time """
        listOfSituations = []
        #Event has to be executed
        mondayMorining = CTimeSituation (MONTAG, 5, 45, False)
        listOfSituations.append (mondayMorining)
        #This event not: Sunday
        listOfSituations.append (CTimeSituation (SONNTAG, 6, 0, False))
        #This event not: Holiday!
        listOfSituations.append (CTimeSituation (MITTWOCH, 6, 0, True))
        listOfSituations.append (CTimeSituation (MONTAG, 11, 35, False))
        #listOfSituations.append (CTimeSituation (FREITAG, 8, 0, False))
        #listOfSituations.append (CTimeSituation (FREITAG, 12, 0, False))
        return listOfSituations
            


if __name__ == "__main__":
    unittest.main()
