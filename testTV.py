# -*- coding: utf-8 -*-

import unittest
import time
from timeEventClasses import *
from timeController import *
from networkDevices import *
from utilities import *


#-----------------------------------
# For Testing the TV remote controlling
#-----------------------------------

class CTVTest (unittest.TestCase):
    
    def testTVPower (self):
        #time.sleep (100)
        logging.info ("Testsequence for TV start...")
        oInfoEvent = CInfoScreenEvent ()
        oInfoEvent.setSignal (SWITCH_OFF)
        oInfoEvent.prepareTV ()
##        oInfoEvent.action ()
##        oTv = CTVdevice ()
##        oTv.switchOn()

        
         


if __name__ == "__main__":
    import logging
    initLogger ()
    unittest.main()
