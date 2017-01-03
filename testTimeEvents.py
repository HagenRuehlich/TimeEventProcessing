# -*- coding: utf-8 -*-
import unittest
from timeEventFactory import getEventFact
import timeEventClasses
from  timeController import *

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
        listOfSituations = []
        mondayMorining = CTimeSituation (6, 22, 30, False)
        listOfSituations.append (mondayMorining)
        #listOfSituations.append (CTimeSituation (3, 7, 10, False))
        #listOfSituations.append (CTimeSituation (4, 21, 34, False))
        #listOfSituations.append (CTimeSituation (6, 22, 30, False))
        #listOfSituations.append (CTimeSituation (4, 8, 0, False))
        #listOfSituations.append (CTimeSituation (4, 12, 0, False))
        return listOfSituations
            


if __name__ == "__main__":
    unittest.main()
