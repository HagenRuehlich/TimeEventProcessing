# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ElementTree
import datetime
import logging
import os.path
# eigene Module in den globalen Namensraum einbinden, siehe PYthon Handbuch Seite 312
from xmlbase import *
from timeEventClasses import *

#------ CONSTS
XML_EVENT_FILE          = "events.xml"
XML_EVENT_TAG           = "EVENT"
XML_SOCKET_KEY          = "SOCKET_NO"
XML_SOCKET_SIGNAL       = "SOCKET_SIGNAL"
XML_WEEKDAYS            = "Weekdays"
XML_TIME                = "Time"
XML_COMMENT             = "Comment"
XML_EVENT_TYPE          = "Event Type"
XML_EVENT_ATTRIBUT      = "Event_Attribut"
XML_EXECUTE_ON_HOLIDAY  = "PUBLIC_HOLIDAY"
XML_URL                 = "URL"
XML_IP                  = "IP"
XML_EMAIL_NOTIFY_MODE   = "EMAIL_NOTIFY_MODE"
XML_EMAIL_RECEIVERS     = "EMAIL_RECEIVERS"

#--------------------

dEmailNotifyMode = {"NO" : EMAIL_NOTIFY_No, "SUCCESS" : EMAIL_NOTIFY_Success ,"FAILURE" : EMAIL_NOTIFY_Failure, "ALWAYS" : EMAIL_NOTIFY_Always}


def getEventFact ():
    return CXMLTimeEventFatory ()

class CAbstractTimeEventFatory ():
    def __init__(self):
        pass
    def getTimeEvents (self):
        raise NotImplementedError
    def produceEvents (self):
        """ Diese Methode bewirkt dass die Factors Events produiert und
            intern speichert.  Hier nur Interface dass in Subklassen implementiert werden muss"""
        raise NotImplementedError


        
class CTimeEventFatory (CAbstractTimeEventFatory):
    def __init__(self):
        self._Events = []
                                
    def getTimeEvents (self):
        return self._Events
        
class CXMLTimeEventFatory (CTimeEventFatory):
    """ Diese Klasse liefert dem Programm die Events, welche aus einer festdefinierten XML Datei gelesen werden.
        Als Hilfsfunktion kann die XML Datei auch geschrieben werden"""
    def __init__(self):
        CTimeEventFatory.__init__(self)
        #Speichert die Zeit wann das XML gelesen wurde
        self._ReadTimeXML = datetime.datetime (2012,1,1)

    def produceEvents (self):
        """Diese Methode bewirkt dass die Factors Events produiert, hier geschiet das durch Einlesen einer XML Datei """
        self.readXMLFile()
        #Lesezeit speichern
        self._ReadTimeXML = datetime.datetime.now()

    def getTimeEvents (self):
        # Aktuelle Zeit ermitteln
        currentTime = datetime.datetime.now()
        #Differenz bilden
        timeDelta = currentTime - self._ReadTimeXML
        # Die Zeitdifferenz in Sekunden ermitteln
        timeDeltaSec = timeDelta.total_seconds()
        # Alle min XML Datei neu lesen
        if (timeDeltaSec > 600):
            self._ReadTimeXML = currentTime
            self.readXMLFile()        
        return self._Events    
        
    def readXMLFile (self):
        """ Liest Events aus einer fest definierten XML Datei in eine Liste ein"""
        logging.info ("Starte Einlesen der XML Datei")
        #Die Liste der vorhandenen Events leeren...
        self._Events = []
        #Eine List von Dictionaries nimmt die Events auf, d.h. jedes Event wird in ein Dictionary eingelesen
        lListOfDictionaries = []
        #Prüfen ob die Datei existiert...
        if not os.path.isfile (XML_EVENT_FILE):
            logging.error (XML_EVENT_FILE + " nicht gefunden")
            raise IOError
        # XML Datei in Baumstruktur einlesen
        tree = ElementTree.parse (XML_EVENT_FILE)
        eventXMLdict = tree.getroot()
        #jedes Element die entsprechenden Einträge ins Dictionary schreiben
        for xmlEvent in eventXMLdict:
            #Zunächst wird der XML Inhalt in ein Dictionary gelesen...
            dEventDictionary = {}
            #alle Einträge 
            for xmlTag in xmlEvent:
                tagKey   = xmlTag.find(XML_KEY)
                tagValue = xmlTag.find(XML_VALUE)
                # Einträge im Dictionary bestehen aus Paaren Schlüssel / Wert....
                dEventDictionary [self.readXMLelement (tagKey)] = self.readXMLelement (tagValue)
            #Das eben gelesene Dictionary zur Liste hinzufügen
            lListOfDictionaries.append (dEventDictionary)
        #Für jedes Dictionary ein Eventobjekt generieren     
        for dEventDict in lListOfDictionaries:
            self.generateEventObjFromDict (dEventDict)
        sAnz = str (len (self._Events))
        logging.info ("Einlesen der XML Datei beendet. " + sAnz + " Events gelesen")
        
    def convertWeekDaysToStr (self, pEvent):
        """Konvertiert die Wochentage des übergebenen Time Events in einen String und gibt diesen zurück
         """
        sWeekDays= ""
        weekDays = pEvent.getWeekdays()
        for i in range (0, len (weekDays), 1):
            if i==0:
                sWeekDays = sWeekDays + dWeekdayStr [weekDays [i]]
            else:
                sWeekDays = sWeekDays + ";" + dWeekdayStr [weekDays [i]]
        return sWeekDays
        
    def addTimeEventToXMLTree (self, pEvent, pEventXMLEntry):
        """ Diese Methode schreibt den Time Eventanteil von spezialisierteren Klassen wie
        Socket Events in die XML Struktur, als kein vollständiges Event
        Parameter:
        pEvent: der Ereignis (ein Time Event Derivat
        pEventXMLEntry: XML Elementtag für das Event, dieser muss bereits angelegt sein"""
        #Den Event Komentar schreiben...
        eventAttribut = ElementTree.SubElement (pEventXMLEntry, XML_EVENT_ATTRIBUT)
        keyTyp = ElementTree.SubElement (eventAttribut, XML_KEY, {"typ":"str"})
        keyTyp.text= XML_COMMENT
        value= ElementTree.SubElement (eventAttribut, XML_VALUE, {"typ":"str"})
        value.text = pEvent.getComment ()
        #Die Wochentage per String in die Struktur schreiben....
        eventAttribut = ElementTree.SubElement (pEventXMLEntry, XML_EVENT_ATTRIBUT)
        keyTyp = ElementTree.SubElement (eventAttribut, XML_KEY, {"typ":"str"})
        keyTyp.text= XML_WEEKDAYS
        value= ElementTree.SubElement (eventAttribut, XML_VALUE, {"typ":"str"})
        value.text = self.convertWeekDaysToStr (pEvent)
        #Stunden und Minuten zum einem "Uhrzeit-String" zusammenfassen und schreiben
        timeStr = ""
        hours = pEvent.getHours()
        minutes = pEvent.getMinutes()
        minuteStr= str (minutes[0])
        if minutes[0] < 10 :
            minuteStr = "0" + minuteStr
        timeStr = str(hours[0]) + ":" + minuteStr
        eventAttribut = ElementTree.SubElement (pEventXMLEntry, XML_EVENT_ATTRIBUT)
        keyTyp = ElementTree.SubElement (eventAttribut, XML_KEY, {"typ":"str"})
        keyTyp.text= XML_TIME
        value= ElementTree.SubElement (eventAttribut, XML_VALUE, {"typ":"str"})
        value.text = timeStr
            
            
            
        

    def addSocketEventToXMLTree (self, pEvent, pDictionary):
        socketEventEntry = ElementTree.SubElement (pDictionary, XML_EVENT_TAG)
        eventAttribut = ElementTree.SubElement (socketEventEntry, XML_EVENT_ATTRIBUT)
        keyTyp = ElementTree.SubElement (eventAttribut, XML_KEY, {"typ":"str"})
        keyTyp.text= XML_EVENT_TYPE
        value= ElementTree.SubElement (eventAttribut, XML_VALUE, {"typ":"str"})
        value.text = pEvent.getType()
        eventAttribut = ElementTree.SubElement (socketEventEntry, XML_EVENT_ATTRIBUT)
        keyTyp = ElementTree.SubElement (eventAttribut, XML_KEY, {"typ":"str"})
        keyTyp.text= XML_SOCKET_KEY
        value= ElementTree.SubElement (eventAttribut, XML_VALUE, {"typ":"int"})
        value.text = pEvent.getSocket()
        eventAttribut = ElementTree.SubElement (socketEventEntry, XML_EVENT_ATTRIBUT)
        keySig = ElementTree.SubElement (eventAttribut, XML_KEY, {"typ":"str"})
        keySig.text= XML_SOCKET_SIGNAL
        value= ElementTree.SubElement (eventAttribut, XML_VALUE, {"typ":"int"})
        value.text = pEvent.getSignal()
        self.addTimeEventToXMLTree (pEvent, socketEventEntry)
        
        

    def addEventToXMLTree (self, pEvent, pDictionary):
        #Type des Events ermitteln
        sType = pEvent.getType ()
        if sType == "SOCKET":
        #Socket Ereigniss ins XML aufnehmen
            self.addSocketEventToXMLTree (pEvent, pDictionary)
        #im ersten Implementierungsinkrement werden Socket Ereignisse ins XML aufgenommen
        else:
            pass
        
    def writeInitialXMLFile (self):
        #Events über Basisklassenmethode holen
        #events = CTimeEventFatory.getTimeEvents (self)
        #Wurzelelement des XML Trees anlegen
        dictionary = ElementTree.Element ("EVENT_LIST") 
        # Für jedes Element in der Liste einen Eintrag erzeugen
        #for i in range (0, len (self._Events), 1):
        #Testweise nur ein Element schreiben
        for i in range (0, 1, 1):
            self.addEventToXMLTree (self._Events[i], dictionary)
        #XML Datei schreiben    
        et = ElementTree.ElementTree (dictionary)
        et.write (XML_EVENT_FILE)

    def readXMLelement (self, pXMLelement):
        """ Liefert den Wert eines einzelnen XML Tags zurück, es wird vorausgesetzt dass der übergebene Tag ein Attribute
            mit der Bezeichung "typ" besitzt welches die Werte "str und "int" annehmen kann"""
        # Dictionary zur Typkonvertierung
        typen = {"int" : int, "str" : str}
        #Den Wert des Tag Attributes "typ" als String auslesen, zulässige Werte sind hier "str" oder "int" 
        typ = pXMLelement.get("typ", "str")
        try:
            value =  typen [typ](pXMLelement.text)
            return value
        except KeyError:
            pXMLelement.text
            
            
    def generateTimeEventObjFromDict (self, pEventDict):
        """ Generates a list of Time Events basing on the dictionary pEventDict """
        assert type (pEventDict) == dict
        lTimeEventList = []
        # Den Event kommentar auslesen
        sComment = pEventDict.get (XML_COMMENT, "")
        assert sComment != ""
        #Wochentage dekodieren
        sWeekDayStr = pEventDict.get (XML_WEEKDAYS, "")
        #Weekday Array vorbereiten
        aWeekDays = []
        assert sWeekDayStr != ""
        #Zu allen vorhandenen "Wochentagsschlüsseln" die "Stringwerte" holen und prüfen ob diese im dekodierten String vorkommen
        for iWeekDay in dWeekdayStr.keys ():
            sWeekDay = dWeekdayStr [iWeekDay]
            if sWeekDayStr.find (sWeekDay) != -1:
                aWeekDays.append (iWeekDay)
        #Uhrzeit auslesen und in Stunden und Minuten dekodieren
        sTimeStatements = ""        
        sTimeStatements =  pEventDict.get(XML_TIME, "")
        assert sTimeStatements != ""
        #It it possible that more than one time specification were made, they have to be sparated by ";"
        sSingleTimes = sTimeStatements.split (";")
        for sSingleTime in sSingleTimes :
            assert sSingleTime.find (":") != -1
            #Den String über seine "Wörter" und den Separator ":" teilen
            sTimes = sSingleTime.split (":")
            assert len (sTimes) == 2
            if sTimes [0] == "00":
                iHour = 0
            else:    
                iHour = int (sTimes [0])
            if sTimes [1] == "00":
                iMinute = 0
            else:
                try:
                    iMinute = int (sTimes [1])
                except ValueError:
                    logging.critical ("Integerkonvertierung fehlgeschlagen, Minuten-Angabe unzulässig: " + sTimes [1])
                    iMinute = 0
            oTimeEvent = CTimeEvent ()
            oTimeEvent.init (aWeekDays, iHour, iMinute)
            oTimeEvent.setComment (sComment)
            #Attribute "Ausführen an Feiertagen dekodieren
            bExeOnHoliday = False
            sExeOnHoliday = pEventDict.get (XML_EXECUTE_ON_HOLIDAY, "")
            if sExeOnHoliday != "" :
                if sExeOnHoliday in dBool.keys():
                    bExeOnHoliday = dBool [sExeOnHoliday]
                    oTimeEvent.SetExeOnHoliday (bExeOnHoliday)
                else:
                    logging.error ("Zulässiger Wert für Feiertagsausführung " + sExeOnHoliday)
            lTimeEventList.append (oTimeEvent)
        return lTimeEventList
        
        
        



    def generateEventObjFromDict (self, pEventDict):
       """ Setzt ein Dictionary in eine Eventobjekt um und fügt dieses in die Liste. ACHTUNG: wenn neue Eventtypen ver-
           arbeitet werden sollen, oder Attribute sich ändern, muss hier angepasst werden..."""
       assert type (pEventDict) == dict
       eventType = pEventDict.get (XML_EVENT_TYPE)
       assert ((eventType == "SOCKET") or (eventType == "SCREEN") or (eventType == "NETWORKCHECK"))       
       #Note in the XML struture several time specifictions per time event are supported, but not in these Python objects
       #so for each time specification in XML a deciated Python object has to be generated
       lTimeEventObj = self.generateTimeEventObjFromDict (pEventDict)
       assert type (lTimeEventObj) == list
       for timeEventObj in lTimeEventObj:
           #Prüfen ob Socket Event...
           if eventType == "SOCKET":
               #Das Siganl lesen, ein- oder ausschalten
               sSignal = pEventDict.get (XML_SOCKET_SIGNAL)
               #Sicherstellen dass das Siganl einen zulässigen Wert hat
               assert sSignal in dSocketSignal.keys()
               #in Integer konvertieren
               iSignal = dSocketSignal [sSignal]
               sSocket = pEventDict.get (XML_SOCKET_KEY)
               #Sicherstellen dass ein zulässiger Wert für die Funksteckdosen ID gelesen wurde
               assert sSocket in dSocketName.keys ()
               #in "Signalstring" konvertieren
               sSocketSigStr = dSocketName [str (sSocket)]           
               socketEventObj = CRadioSocketEvent ()
               socketEventObj.setSocket (sSocketSigStr)
               socketEventObj.setSignal (iSignal)
               socketEventObj.copyFromTimeEvent (timeEventObj)
               self._Events.append (socketEventObj)
           elif  eventType == "SCREEN":
               screenEventObj = CInfoScreenEvent ()
               screenEventObj.setSignal (iSignal)
               sUrl = pEventDict.get (XML_URL)
               assert type (sUrl) == str
               screenEventObj.setUrl(sUrl)
               screenEventObj.copyFromTimeEvent (timeEventObj)
               self._Events.append (screenEventObj)
           elif  eventType == "NETWORKCHECK":
               netTestObj = self.generateNetworkCheckEvent (pEventDict)
               assert type (netTestObj) == CNetworkDeviceStatusCheckEvent
               netTestObj.copyFromTimeEvent (timeEventObj)
               self._Events.append (netTestObj)
           else:
               raise ValueError
           
           
           
    def generateNetworkCheckEvent (self, pEventDict):
        """creates an returns an object representing a networks check. Object attributes will be set based on values in pEventDict """
        assert type (pEventDict) == dict
        netTestObj = CNetworkDeviceStatusCheckEvent ()
        sIP = pEventDict.get (XML_IP)
        assert (sIP != "")
        netTestObj.setIP (sIP)
        sEmailNotifyMode = pEventDict.get (XML_EMAIL_NOTIFY_MODE)
        assert sEmailNotifyMode in dEmailNotifyMode.keys ()
        eEmailNotifyMode =  dEmailNotifyMode [sEmailNotifyMode]
        netTestObj.setEmailNotifyMode (eEmailNotifyMode)
        sReceivers = pEventDict.get (XML_EMAIL_RECEIVERS)
        assert type (sReceivers) == str
        #Splitt into single receivers
        lReceiverList = sReceivers.split (";")
        assert type (lReceiverList) == list
        for sSingleReceiver in lReceiverList:
            assert sSingleReceiver in dName_MailAdress.keys ()
            sMailAdress = dName_MailAdress [sSingleReceiver]
            netTestObj.addMailReceiver (sMailAdress)
        return netTestObj

        
       

        

    

