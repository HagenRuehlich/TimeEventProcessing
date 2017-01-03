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

##    def testHolidays (self):
##        self.assertEqual (isDayHoliday (2016, 1, 1), True, "1. Januar IST ein Feiertag")
##        self.assertEqual (isDayHoliday (2016, 1, 2), False, "2. Januar ist KEIN Feiertag")
##        self.assertEqual (isDayHoliday (2016, 2, 7), False, "7. Februar ist KEIN Feiertag")
##        self.assertEqual (isDayHoliday (2016, 2, 8), True, "8. Februar IST ein Feiertag")
##        self.assertEqual (isDayHoliday (2016, 2, 11), True, "11. Februar IST ein Feiertag")
##        self.assertEqual (isDayHoliday (2016, 2, 13), False, "13. Februar ist KEIN Feiertag")
##        self.assertEqual (isDayHoliday (2016, 3, 20), False, "20. März ist KEIN Feiertag")
##        self.assertEqual (isDayHoliday (2016, 3, 22), True, "22. März IST ein Feiertag")
##        self.assertEqual (isDayHoliday (2016, 4, 2), False, "4. April ist KEIN Feiertag")
##        self.assertEqual (isDayHoliday (2016, 5, 16), False, "16. Mai ist KEIN Feiertag")
##        self.assertEqual (isDayHoliday (2016, 5, 17), True, "17. Mai IST ein Feiertag")
##        self.assertEqual (isDayHoliday (2016, 5, 28), True, "28. Mai IST ein Feiertag")
##        self.assertEqual (isDayHoliday (2016, 5, 29), False, "29. Mai ist KEIN Feiertag")
##        self.assertEqual (isDayHoliday (2016, 7, 19), False, "19. Juli ist KEIN Feiertag")
##        self.assertEqual (isDayHoliday (2016, 7, 20), True, "20. Juli ist EIN Feiertag")
##        self.assertEqual (isDayHoliday (2016, 9, 12), True, "12. September ist EIN Feiertag")
##        self.assertEqual (isDayHoliday (2016, 9, 13), False, "13. September ist KEIN Feiertag")
##        self.assertEqual (isDayHoliday (2016, 10, 3), True, "3. Oktober ist ein Feiertag")
##        self.assertEqual (isDayHoliday (2016, 11, 1), True, "1. November ist ein Feiertag")
##        self.assertRaises (AssertionError, isDayHoliday, 2016, 13, 32)

    def testTVPower (self):
        oTV = CTVdevice()
        bIsAlreadyOn = oTV.ping()
        if bIsAlreadyOn:
            oTV.switchOff()
        else:
            oTV.switchOn()
        
         


if __name__ == "__main__":
    unittest.main()
