# -*- coding: utf-8 -*-
import logging
import os
import time
import webbrowser
from mailserver import *
from networkDevices import *
from utilities import *
from confidental import *


SONNTAG    = 6
MONTAG     = 0
DIENSTAG   = 1
MITTWOCH   = 2
DONNERSTAG = 3
FREITAG    = 4
SAMSTAG    = 5


JANUAR     = 1
FEBRUAR    = 2
MAERZ      = 3
APRIL      = 4
MAI        = 5
JUNI       = 6
JULI       = 7
AUGUST     = 8
SEPTEMBER  = 9
OKTOBER    = 10
NOVEMBER   = 11
DEZEMBER   = 12




ANZAHL_FUNK_SIGNALE  = 5



"""This consts are for controlling email notification"""
EMAIL_NOTIFY_No         = 0
EMAIL_NOTIFY_Success    = 1
EMAIL_NOTIFY_Failure    = 2
EMAIL_NOTIFY_Always     = 3
    



def getWochenTagStr (iTag):
    if (iTag == 0):
        s = "MONDAY" 
    elif (iTag==1):
        s= "TUESDAY"
    elif (iTag == 2):
        s= "WEDNESDAY"
    elif (iTag == 3):
        s= "THURSDAY"
    elif (iTag == 4):
        s= "FRIDAY"
    elif (iTag == 5):
        s = "SATURDAY"
    elif (iTag == 6):
        s= "SUNDAY"
    else:
        s = "KEIN WOCHENTAG ERMITTELT"
    return s

#Codes für die Funksteckdosen
PLUG_SOCKET_A = "1"
PLUG_SOCKET_B = "2"
PLUG_SOCKET_C = "3"
SYSTEM_CODE = "10101"
HANDY_CHARGER = PLUG_SOCKET_A
CUP_BOARD_LIGHT_SOCKET = PLUG_SOCKET_C
WLAN_REPEATER = PLUG_SOCKET_B
SWITCH_ON = "1"
SWITCH_OFF = "0"

#Dictionary zur Konvertierung der Wochentage in Strings...
dWeekdayStr = {0 : "MONDAY", 1 : "TUESDAY", 2: "WEDNESDAY", 3: "THURSDAY", 4 : "FRIDAY", 5: "SATURDAY", 6: "SUNDAY"}
#Dictionary zur Namenskonvertierung der Funksteckdosen
dSocketName = {"A" : PLUG_SOCKET_A, "B" : PLUG_SOCKET_B, "C" : PLUG_SOCKET_C}
#Dictionary zur Namenskonvertierung der Funksiganle (ON/OFF)
dSocketSignal = {"ON": SWITCH_ON, "OFF" : SWITCH_OFF}
#Dictionary zur Komvertierung boolscher Werte..
dBool = {"YES": True, "NO":False}


#Allgemeine Klasse für Zeitereignisse
class CTimeEventInterface():
    def __init__(self, weekdays, hours, minute):
        pass
    def reset (self):
        pass
    def getMonth (self):
        pass
    def isDayInEvent (self, d):
        pass
    def reset (self):
        pass
    def isTimeInEvent (self, day, hour, minute):
        pass
    def execute (self, day, hour, minute):
        pass
    def getType (self):
        pass
    
#----------------------------------------------    
    





class CTimeEvent (CTimeEventInterface):
    def __init__(self):
        self._Type = "ABSTRACT"
        self._Comment = ""
        self._Weekdays = []
        self._Hour = -1
        self._Minute = -1
        self._LastEventDay = -1
        self._LastEventHour = -1
        self._LastMinute = - 1
        self._ExecuteOnHoliday = False

    def init (self, weekdays, hours, minute):
        self._Weekdays = weekdays
        self._Hour = hours
        self._Minute = minute
        self._LastEventDay = -1
        self._LastEventHour = -1
        self._LastMinute = - 1
        
    def copyFromTimeEvent (self, pTimeEvent):
        """ Übernimmt die Time Event Wert vom übergebenen Objekt """      
        self._Comment = pTimeEvent.getComment()
        self._Weekdays = pTimeEvent.getWeekdays()
        self._Hour = pTimeEvent.getHour ()
        self._Minute = pTimeEvent.getMinute ()
        self._ExecuteOnHoliday= pTimeEvent.executeOnHoliday ()
    

    def reset (self):
        logging.info ("Event reset")
        self._LastEventDay = -1
        self._LastEventHour = -1
        self._LastMinute = - 1
    
    def getComment (self):
        """ Gibt den aktuellen Kommentar als String zu diesem Event zurück"""    
        return self._Comment
      
    def setComment (self, psComment):
        """Setzt den Event Kommentar, dieser muss als String übergeben werden"""
        self._Comment = psComment
        

    def getWeekdays (self):
        return self._Weekdays

    def getHour (self):
        return self._Hour

    def getMinute (self):
        return self._Minute         
    
    def setHour (self, hour):
        self._Hour = hour

    def setMinute (self, minute):
        self._Minute = minute

    def executeOnHoliday (self):
        return self._ExecuteOnHoliday
        
    def SetExeOnHoliday (self, pbExeOnHoliday):
       self._ExecuteOnHoliday = pbExeOnHoliday
      

    def isDayInEvent (self, d):
         if (d in self._Weekdays):
            return True
         else:
            return False
        
    def isHourInEvent (self, h):
        if (h == self._Hour):
            return True
        else:
            return False
        
    def isMinuteInEvent (self, m):
        if (m == self._Minute):
            return True
        else:
            return False
        
    def isTimeInEvent (self, day, hour, minute):
        if (day in self._Weekdays):
            if (hour == self._Hour):
                if (minute == self._Minute):
                    return True
        return False       
             
            
                 
        

    def execute (self, day, hour, minute):
        if ((day == self._LastEventDay) and (hour == self._LastEventHour) and minute == self._LastMinute):
            return
        else:
            self._LastEventDay = day
            self._LastEventHour = hour
            self._LastMinute = minute
            logging.info ("Event has to be executed")
            self.action ()
              
#Abstrakte Methode
    def action (self):
        logging.error ("Pure virtual method called of class CTimeEvent")
        raise NotImplemented

    def getType (self):
        return self._Type

                        
#Ende Klasse CTimeEvent
#Klasse zum Schalten von Funktsteckdosen
class CRadioSocketEvent (CTimeEvent):
    def __init__(self):
        CTimeEvent.__init__(self)
        self._Type = "SOCKET"
        self._Socket = -1
        self._Signal = -1

    def init (self, weekdays, hours, minute, pSocket, pSignal):    
#Es gibt nur 2 zugelassene Werte für Signale: Ein und Aus....        
        if ((pSignal != SWITCH_ON) and (pSignal != SWITCH_OFF)):
            raise ValueError
        CTimeEvent.init (self, weekdays, hours, minute)
        self._Socket = pSocket
        self._Signal = pSignal

    def setSignal (self, signal):
         self._Signal = signal

    def getSignal (self):
        return self._Signal

    def getSocket (self):
        return self._Socket

    def setSocket (self, socket):
         self._Socket = socket  

    def preSwitchOnAction (self):
        return   
        
    def postSwitchOnAction (self):
        return

    def sentCommand (self, command):
        logging.info ("Send command " + command)
        if (getOsType () == OS_LINUX):
            for i in range (1, ANZAHL_FUNK_SIGNALE, 1):
                os.system (command)
                logging.info ( "Sendebefehl abgesetzt")
        
    def getComand (self):
        return "/home/pi/rcswitch-pi/send"
        
    def action (self):      
        if (self._Signal == SWITCH_ON):
            self.preSwitchOnAction ()
        parStr = " " + SYSTEM_CODE + " " + str (self._Socket) + " " + str (self._Signal)
        self.sentCommand (self.getComand () + parStr)
        if (self._Signal == SWITCH_ON):
            self.postSwitchOnAction ()
        
           
"""Class for status checking of network devices"""
class CNetworkDeviceStatusCheckEvent (CTimeEvent):
    def __init__(self):
        CTimeEvent.__init__(self)
        self._sIP = ""
        self._eMailNotifyMode = EMAIL_NOTIFY_No
        self._mailReceivers = []
        
    def init (self, piWeekdays, piHours, piMinute, psIP, peMailNotifyMode):
        self._sIP = psIP
        self._eMailNotifyMode = peMailNotifyMode
        CTimeEvent.init (self, piWeekdays, piHours, piMinute)
      
    def setIP (self, psIP):
        self._sIP = psIP

    def setEmailNotifyMode (self, peMailNotifyMode):
        self._eMailNotifyMode = peMailNotifyMode

    def addMailReceiver (self, psMailReceiver):
        assert type (psMailReceiver) == str
        self._mailReceivers.append (psMailReceiver)
        
    def sendMail (self, psSubject, psMailText):
        assert type (psSubject) == str
        assert type (psMailText) == str
        oMailServer = CMailServer()
        msg = CMailFromHagen (self._mailReceivers, psSubject, psMailText)
        oMailServer.sendMail (msg)
            
            
        
        
        
    def action (self):
        assert self._sIP in dIP_Name.keys ()
        #No IPs required here, devive name doesn't require constant IPs...
        sNetDeviceName = dIP_Name [self._sIP]
        oDevice = CNetWorkDevice (sNetDeviceName)
        bRes = oDevice.ping()
        if (bRes == False):
            logging.info ( "Ping zu Netzwerkgerät " + sNetDeviceName + " nicht erfolgreich")
            if (self._eMailNotifyMode == EMAIL_NOTIFY_Failure or self._eMailNotifyMode == EMAIL_NOTIFY_Always):
                self.sendMail ("Ping zu Netzwerkgerät " + sNetDeviceName + " nicht erfolgreich", "Gesendet von Objekt der Klasse CNetworkDeviceStatusCheckEvent")
        else:
            logging.info ( "Ping zu Netzwerkgerät " + sNetDeviceName + " erfolgreich")
            if (self._eMailNotifyMode == EMAIL_NOTIFY_Success or self._eMailNotifyMode == EMAIL_NOTIFY_Always):
                self.sendMail ("Ping zu Netzwerkgerät " + sNetDeviceName + " erfolgreich", "Gesendet von Objekt der Klasse CNetworkDeviceStatusCheckEvent")
                
            
            
               
                
            
        
        
        
#Klasse zum InfoScreen schalten
class CInfoScreenEvent (CTimeEvent):
    def __init__(self):      
        CTimeEvent.__init__(self)
        self._Type = "SCREEN"
        self._Signal = ""
        self._Url = ""

    def init (self, weekdays, hour, minute):    
        CTimeEvent.init (self, weekdays, hour, minute)

    def setSignal (self, piSignal):
        assert type (piSignal) == str
        self._Signal = piSignal

    def setUrl (self, psUrl):
        assert type (psUrl) == str
        self._Url = psUrl

    def aktivateHDMIoutput (self):
        """ activces the HDMI output, please refer to
            https://www.elektronik-kompendium.de/sites/raspberry-pi/2002141.htm"""
        os.system("/opt/vc/bin/tvservice -p; sudo /bin/chvt 2; sudo /bin/chvt 1")

    def prepareTV (self):
        """ Ensures that TV is on and switches to HDMI input source of the Pi"""
        self.aktivateHDMIoutput ()
        time.sleep (1)
##        os.system ("startx")
##        time.sleep (1)
        oTv = CTVdevice()
        oTv.switchOn ()
        oTv.sendKey (KEY_HOME)
        oTv.sendKey (KEY_DOWN)
        oTv.sendKey (KEY_DOWN)
        oTv.sendKey (KEY_DOWN)
        oTv.sendKey (KEY_LEFT)
        oTv.sendKey (KEY_LEFT)
        oTv.sendKey (KEY_LEFT)
        oTv.sendKey (KEY_OK)
        
    def startInfoScreen(self):
        assert (self._Url != "")
        logging.info ("Start website " + self._Url)
        webbrowser.open (self._Url)

    def stopInfoScreen (self):
        reBoot ()
        
    def resetTv (self):
        """Resets den TV this way that the Kabel Deutschland Receiver is the
            active HDMI source"""
        oTv = CTVdevice()
        oTv.sendKey (KEY_DOWN)
        oTv.sendKey (KEY_DOWN)
        oTv.sendKey (KEY_RIGHT)
        oTv.sendKey (KEY_RIGHT)
        oTv.sendKey (KEY_RIGHT)
        oTv.sendKey (KEY_UP)
        oTv.sendKey (KEY_OK)
        oTv.switchOff ()
         
    
    def action (self):
        """ Inital wird zunähcst nur der Fernseher ein und ausgeschaltet"""
        assert ((self._Signal == SWITCH_ON) or (self._Signal == SWITCH_OFF))
        if (self._Signal == SWITCH_ON):
            self.prepareTV ()
            self.startInfoScreen ()
        else:
            self.resetTv ()
            #self.stopInfoScreen ()
            
            
            
        
