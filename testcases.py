# -*- coding: utf-8 -*-

import unittest
import time
from timeEventClasses import *
from timeController import *


#-----------------------------------
# Funktsteckdosen und Infrarot Test, auf dem Pi ausführen
#-----------------------------------

class CDeviceTest (unittest.TestCase):
    def singleSocketTest (self, pSocket):
        assert pSocket in [PLUG_SOCKET_A, PLUG_SOCKET_B, PLUG_SOCKET_C]
        oTest = CRadioSocketEvent ()
        oTest.setSocket (pSocket)
        oTest.setSignal (SWITCH_OFF)
        oTest.action ()
        time.sleep (5)
        oTest.setSignal (SWITCH_ON)
        oTest.action ()
        time.sleep (5)

    
    def allSocketsTest (self):
        time.sleep (10)
##        self.singleSocketTest(PLUG_SOCKET_A)
##        self.singleSocketTest(PLUG_SOCKET_B)
        self.singleSocketTest(PLUG_SOCKET_C)
        return True

##    def testAllSockets (self):
##        self.assertEqual (self.allSocketsTest(), True)

    def testHolidays (self):
        self.assertEqual (isDayHoliday (2019, 1, 1), True, "1. Januar IST ein Feiertag")
        self.assertEqual (isDayHoliday (2019, 1, 2), False, "2. Januar ist KEIN Feiertag")
        self.assertEqual (isDayHoliday (2019, 2, 7), False, "7. Februar ist KEIN Feiertag")
        self.assertEqual (isDayHoliday (2019, 2, 28), True, "28. Februar IST ein Feiertag")
        self.assertEqual (isDayHoliday (2019, 3, 6), False, "6th March is NOT a holiday")
        self.assertEqual (isDayHoliday (2019, 4, 11), True, "11th April IS a holiday")
        self.assertEqual (isDayHoliday (2019, 6, 7), True, "7th June IS a holiday")
        self.assertEqual (isDayHoliday (2019, 6, 19), False, "19thJume is NOT a holiday")
        self.assertEqual (isDayHoliday (2019, 9, 11), True, "11th September IS a holiday")
        self.assertEqual (isDayHoliday (2019, 9, 12), False, "12th September is NOT a holiday")
        self.assertEqual (isDayHoliday (2019, 12, 21), True, "21st December IS a holiday")
        self.assertEqual (isDayHoliday (2019, 12, 20), False, "20th December is NOT a holiday")
        self.assertEqual (isDayHoliday (2019, 4, 14), True, "14th April IS a holiday")
        self.assertEqual (isDayHoliday (2019, 4, 2), False, "3rd April is NOT a holiday")
        self.assertEqual (isDayHoliday (2019, 5, 25), True, "25th May is a holiday")
        self.assertEqual (isDayHoliday (2019, 9, 12), False, "12th September is not a holiday")
        self.assertEqual (isDayHoliday (2019, 10, 3), True, "3rd October is a holiday")
        self.assertEqual (isDayHoliday (2019, 6, 15), True, "15th June is a holiday")
        self.assertEqual (isDayHoliday (2019, 11, 1), True, "1. November ist ein Feiertag")
        self.assertRaises (AssertionError, isDayHoliday, 2019, 13, 32)

##    def testTVPower (self):
##        oTV = CTVdevice()
##        bIsAlreadyOn = oTV.ping()
##        if bIsAlreadyOn:
##            oTV.switchOff()
##        else:
##            oTV.switchOn()
        
         


if __name__ == "__main__":
    unittest.main()
