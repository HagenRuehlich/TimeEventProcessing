# -*- coding: utf-8 -*-
import logging
import urllib.request
import urllib.error
import re
from networkDevices import *
from confidental import *
import logging

PM25  = 0
PM100 = 1


class CAirQualitySensor(CNetWorkDevice):
    """Diese Klasse stellt Basisdienste für das Lesen von XML Dateien
    zur Verfügung"""

    #Regular expressions needed to pase HTML side
    d_ValueSearchExpr = {PM25 : r"<td>PM2.5</td><td class='r'>.{1,5}&nbsp" , PM100: r"<td>PM10</td><td class='r'>.{1,5}&nbsp" }


    
    def __init__(self):
        CNetWorkDevice.__init__(self, "Feinstaubsensor")
        self._currentValues = [0.0, 0.0]
        

    def measure (self):
        """Returns the current PM2.5 and PM10 values"""
        bRes = False
        bRestPM25 = self.measureValue (PM25)
        bRestPM100 = self.measureValue (PM100)
        bRes = bRestPM25 and bRestPM100
        return bRes


    def getLastestResults (self)  :
        return self._currentValues
        

    def measureValue (self, iValueType):
        """reads one the possible values (PM2.5 or OM10) for the HTMl page the sensors provides in the local network"""
        assert type (iValueType) == int
        bRes = False
        req = urllib.request.Request ("http://" + dIP_Name["AirQualitySensor"] + "/values")
        try:
            f= urllib.request.urlopen (req)
        except urllib.error.URLError as e:
            logging.critical ('HtmlDownLoader download error:', e.reason)
            return bRes
        byteHTML = f.read ()
        f.close()
        sHTML = byteHTML.decode("utf8")
        #the strings containing the 2 value the sensor generates should appreare only one time in the HTML page
        iCheck = 0 
        for m in re.finditer (self.d_ValueSearchExpr [iValueType], sHTML, re.I):
            iCheck = iCheck + 1
            assert (iCheck == 1)
            sProcessStr= m.group(0)
            #sProcessStr should now look like: <td>PM2.5</td><td class='r'>5.3&nbsp
            sSplittedStr1 = sProcessStr.rsplit ("&")
            sSplittedStr2 = sSplittedStr1 [0].rsplit (">")
            #The last sub string represents the value...
            sValue = sSplittedStr2 [len (sSplittedStr2) - 1]
            if (sValue != ""):
                try:
                    self._currentValues [iValueType] = float (sValue)
                    bRes = True
                except ValueError:
                    bRes = False
                    logging.critical ("Could not read value from air quality sensors HTML side")                    
        return bRes
            
            
            

# r"<td># PM2.5</td><td class='r'>.{1,5}&nbsp"
# <td>PM# 10</td><td class='r'>9.6&nbsp
   
        
            
            
        
if __name__ == "__main__":
    oSensor = CAirQualitySensor()
    #just to make sure that this stuff if known at runtime..
    err = urllib.error.URLError ("Test")
    oSensor.measure ()
    aCurrentValues = oSensor.getLastestResults()
    print ("Aktuelle Werte: PM10 = " + str (aCurrentValues [PM100]) + " ,PM2,5 = " + str (aCurrentValues [PM25]))
    
    
