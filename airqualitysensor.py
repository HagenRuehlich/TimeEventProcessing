# -*- coding: utf-8 -*-
import logging
import urllib.request
import re
from networkDevices import *

PM25  = 0
PM100 = 1


class CAirQualitySensor(CNetWorkDevice):
    """Diese Klasse stellt Basisdienste für das Lesen von XML Dateien
    zur Verfügung"""
    def __init__(self):
        CNetWorkDevice.__init__(self, "Feinstaubsensor")
        self._currentValues = [0.0, 0.0]
        

    def measure (self):
        """Returns the current PM2.5 and PM10 values"""
        req = urllib.request.Request ("http://192.168.178.86/values")
        bRes = False
        f= urllib.request.urlopen (req)
        byteHTML = f.read ()
        f.close()
        sHTML = byteHTML.decode("utf8")
        #the strings containing the 2 value the sensor generates should appreare only one time in the HTML page
        iCheck = 0 
        for m in re.finditer (r"<td>PM2.5</td><td class='r'>.{1,5}&nbsp", sHTML, re.I):
            iCheck = iCheck + 1
            assert (iCheck == 1)
            sProcessStr= m.group(0)
            #sProcessStr should now look like: <td>PM2.5</td><td class='r'>5.3&nbsp
            sSplittedStr1 = sProcessStr.rsplit ("&")
            sSplittedStr2 = sSplittedStr1 [0].rsplit (">")
            #The last sub string represents the value...
            sValue = sSplittedStr2 [len (sSplittedStr2) - 1]
            if (sValue != ""): 
                
            value = float ()
        return bRes    
            
            
            

# r"<td># PM2.5</td><td class='r'>.{1,5}&nbsp"
# <td>PM# 10</td><td class='r'>9.6&nbsp
   
        
            
            
        
if __name__ == "__main__":
    oSensor = CAirQualitySensor()
    oSensor.getCurrentValues ()
