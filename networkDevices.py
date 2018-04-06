# -*- coding: utf-8 -*-

import os
import time
from infrared import *
from utilities import *

IP_TV = "192.168.178.31"
NAME_TV = "FernseherWohnzimmer"
NAME_FRITZ_BOX = "fritz.box"

class CNetWorkDevice ():
    def __init__(self, pName):
        if pName == "":
            raise ValueError
        self._name = pName
        
    def ping (self):
        """tries to ping the device, returs true is sucessful otherwise false"""
        bResult = False
        #Check if the device answers a ping...
        eOsType = getOsType ()
        if (eOsType == OS_LINUX):
            if os.system("ping -c 1 " + self._name) == 0:
                bResult = True
        elif (eOsType == OS_WINDOWS):
            # This implementation doesn't work for Windows, the os.system call results alwayse in True
            # Solution the output of this call has to be piped and analysed, only if the the string "TTL" can be find, the ping was successful..
            if os.system("ping -n 1 " + self._name) == 0:
                bResult = True
        else:
            raise OSError
        return bResult

class CTVdevice (CNetWorkDevice):    
    """Represents the TV device in the network"""
    def __init__(self):
        CNetWorkDevice.__init__(self, NAME_TV)
        
        
    def switchOn (self):
        """ switches on the TV"""
        self.switch (True)

    def switchOff (self):
        self.switch (False)
            
            
    def switch (self, pbOn):
        assert type (pbOn) == bool
        bPinb = self.ping()
        if bPinb != pbOn:
            oIR = CInfraredTransmitterTv ()
            oIR.sendTvKey (KEY_POWER)
            time.sleep (45)

    def sendKey (self, psKey):
        """sendet die übergebene Taste"""
        assert (type (psKey) == str)
        #KEY_POWER will be processed, please use methods switchOn and switchOff
        if psKey == KEY_POWER:
            raise ValueError
        oIr = CInfraredTransmitterTv ()
        oIr.sendTvKey (psKey)
        time.sleep (6)
        
            
        
    
        
        
        


