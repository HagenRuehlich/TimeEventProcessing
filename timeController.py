# -*- coding: utf-8 -*-
import time
import os
import webbrowser
import logging
import datetime
import timeEventClasses
from  xmlbase import CXmlBaseReader
from utilities import *
from timeEventFactory import getEventFact

import sys

#----Konstanten

XML_HOLIDAY_FILE        = "SchoolBankHolidays.xml"
XML_HOLIDAY_TYPE        = "TYPE"
XML_SCHOOL_HOLIDAYS     = "SCHOOL_HOLIDAYS"
XML_PUBLIC_HOLIDAY      = "PUBLIC_HOLIDAY"
XML_DATE                = "DATE"
XML_PERIOD              = "PERIOD"


CURRENT_YEAR = 2018



def processEvents ():
    logging.info ("Starte Eventverarbeitung")
    abbruch = False
    iInitialDay = getWochenTag()
#Event Factory holen...    
    evFact = getEventFact()
#Factory produziert Events...
    evFact.produceEvents()    
#"Produktionsminute" festhalten
    factMin = getMinute ()
    bIsHoliday = isTodayAHoliday()
    while (not abbruch):
        events = evFact.getTimeEvents()
        aktuellerWochenTag = getWochenTag()
        aktuelleMinute = getMinute ()
#Bei Tagesübergang alle Events zurück setzen
        if (aktuellerWochenTag != iInitialDay):
            iInitialDay = aktuellerWochenTag
            for i in range (0, len (events), 1):
                events[i].reset ()
        aktuelleStunde = getStunde()
        timeSituation = CTimeSituation (aktuellerWochenTag,aktuelleStunde, aktuelleMinute, bIsHoliday)
        checkAndExecuteEventList (events , timeSituation)
        time.sleep (5)

def checkAndExecuteEventList (pListEvents, pTimeSituation) :
    """ Verglicht die Events einer Liste mit einer konkreten, übergebene Situation und führt bei Treffern die 
        entsprechenden Ereignisse aus, liefert die Anzahl der tatsächlich ausgeführten Ereignisse zurück"""
    iReturn = 0
    assert (type (pListEvents) == list)
    assert (type (pTimeSituation) == CTimeSituation)
    for iCurrentEvent in range (0, len (pListEvents), 1):
        bExecuted = checkAndExecuteEvent (pListEvents[iCurrentEvent], pTimeSituation)
        if (bExecuted == True):
            iReturn = iReturn + 1
    return iReturn    
    
def checkAndExecuteEvent (pEvent, pTimeSituation) :
    """ Verglicht ein Event mit einer konkreten, übergebene Situation und führt bei Treffern das Event aus, liefert
         true wenn das Event ausgeführt wurde sonst false"""
    bReturn = False
    assert (isinstance (pEvent, timeEventClasses.CTimeEventInterface) == True)
    assert (type (pTimeSituation) == CTimeSituation)
    if (pEvent.isTimeInEvent (pTimeSituation.getWeekDay (), pTimeSituation.getHour(), pTimeSituation.getMinute())):
                if not (pTimeSituation.isHoliday() and not pEvent.executeOnHoliday()):
                    pEvent.execute(pTimeSituation.getWeekDay (), pTimeSituation.getHour(), pTimeSituation.getMinute())
                    bReturn = True               
    return bReturn                

class CTimeSituation ():
    """Beschreibt eine zeitliche Situation (Tag, Uhrzeit, Feitertag ja/nein"""
    def __init__(self, piWeekDay, piHour, piMinute, pbIsHoliday):
        assert (type (piWeekDay) == int)
        assert (type (piHour) == int)
        assert (type (piMinute) == int)
        assert (type (pbIsHoliday) == bool)
        self._iWeekDay = piWeekDay
        self._iHour = piHour
        self._iMinute = piMinute
        self._bIsHoliday = pbIsHoliday

    def getWeekDay (self):
        return self._iWeekDay

    def getHour (self):
        return self._iHour

    def getMinute (self):
        return self._iMinute

    def isHoliday (self):
        return self._bIsHoliday

    
                              


#-----------------
def getWochenTag():
    t = time.localtime()
    return t.tm_wday

def getStunde():
    t= time.localtime()
    return t.tm_hour
    
    
    

def getMinute ():
    t = time.localtime()
    return t.tm_min


def checkAbbruch ():
    return False

    
class CTimeFrame():
    """ Klasse zur Repräsentation eines Zeitrahmens  """
    def __init__(self, pYearStart, pDayStart, pMonthStart, pYearEnd, pDayEnd, pMonthEnd):
        assert ((pDayStart > 0)   and (pDayStart < 32))
        assert ((pDayEnd > 0)     and (pDayEnd < 32))
        assert ((pMonthStart > 0) and (pMonthStart < 13))
        assert ((pMonthEnd > 0)   and (pMonthEnd < 13))
        self._begin = datetime.date (pYearStart, pMonthStart, pDayStart)
        self._end = datetime.date (pYearEnd, pMonthEnd, pDayEnd)
        
    def isDayInTimeFrame(self, pYear, pDay, pMonth):
        """Prüft ob sich der übergebene Tag im des Zeitrahmens befindet, d.h. auch wenn er mit Anfangs- oder Endtag dieses
           dieses Zeitraums zusammenfällt wird true geliefert"""
        assert ((pDay > 0)     and (pDay < 32))
        assert ((pMonth > 0) and (pMonth < 13))
        bResult = False
        dCheckDay = datetime.date (pYear, pMonth, pDay)
        if not (dCheckDay < self._begin):
            if not (dCheckDay > self._end):
                bResult = True
        return bResult

class CHolidayXmlReader (CXmlBaseReader):
    """Klasse zum Lesen der XML Datei für Schulferien und Feiertage"""
    def __init__(self):
        CXmlBaseReader.__init__(self, XML_HOLIDAY_FILE)

    def readXmlBaseEntry (self, pXmmlBaseEntry, pDict):
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
        

        
def isDayHoliday (pYear, pMonth, pDay):
    """Prüft ob der übergebene Tag in die Schulferien fällt oder ein ofizieller Feiertag ist"""
    assert ((pMonth > 0) and (pMonth < 13))
    assert ((pDay > 0)   and (pDay < 32))
    logging.info ("Starte: isDayHoliday")
    bResult = False
    #Klasse zum Einlesen der Schulferien und Feiertags XML Datei initialisieren
    xmlReader = CXmlBaseReader(XML_HOLIDAY_FILE)
    # Die Daten aus der XML Datei als Dictionary Liste holen
    listOfDict = xmlReader.readXmlFile()
    assert isinstance (listOfDict, list)
    #Jede Feiertag bzw. jede Ferienperiode wird durch eine Dictionary repräsentiert, der übergebene Tag wird mit diesen
    #der Reihe nach abgelichen
    logging.info ("Anzahl der Einträge in Feiertags XML: " + str (len (listOfDict)))
    for dDict in listOfDict:
        #Prüfen ob Feiertag oder Ferienperiode...
        if (dDict [XML_HOLIDAY_TYPE] == XML_SCHOOL_HOLIDAYS):
            # Aktueller Dictionary Eintrag ist eine Ferienperiode
            sPeriod = ""
            sPeriod = dDict.get (XML_PERIOD, "")
            assert sPeriod != ""
            #In 2 Strings zerlegen, einer für Start der Periode, der andere für das Ende
            sPeriodParts = sPeriod.split ("-")
            assert len (sPeriodParts) == 2
            #Den Starttag weiter in Tag und Monat zerlegen
            iStartDay = getDayFromString (sPeriodParts [0])
            iStartMonth = getMonthFromString (sPeriodParts [0])
            #Den Endtag weiter in Tag und Monat zerlegen
            iEndDay = getDayFromString (sPeriodParts [1])
            iEndMonth = getMonthFromString (sPeriodParts [1])
            timeFrame = CTimeFrame(CURRENT_YEAR, iStartDay, iStartMonth, CURRENT_YEAR, iEndDay, iEndMonth)
            bResult = timeFrame.isDayInTimeFrame (pYear, pDay, pMonth)
            if bResult :
                return bResult
        elif (dDict [XML_HOLIDAY_TYPE] ==  XML_PUBLIC_HOLIDAY):
            # Aktueller Dictionary Eintrag ist offizieller Feiertag
            sDate = dDict.get (XML_DATE, "")
            assert sDate != ""
            iDay = getDayFromString (sDate)
            iMonth = getMonthFromString (sDate)
            if ((iDay == pDay) and (iMonth == pMonth)):
                bResult = True
                return bResult
        else:
            #Wenn weder Ferienperiode noch offizieller Feiertag als Type
            #eingetragen sind, Exception werfen
            logging.error ("Wrong Value for holiday type in XML file")                
            raise ValueError ("Wrong Value for holiday type in XML file")          
    return bResult
        


def isTodayAHoliday():
    """Prüft ob der aktuelle Tag ein offizieller Feiertag ist oder in den Schulferien liegt. In diesen Fällen wird true
    zurückgegeben sonst false. Datenbasis ist eine XML Datei"""
    bResult = False
    #Prüfen ob der Tag in den Schulferien liegt...
    t = time.localtime()
    bResult = isDayHoliday (t.tm_year, t.tm_mon, t.tm_mday)
    return bResult


            
                    
   
      
if __name__ == "__main__":
    initLogger ()  
    processEvents ()
    logging.shutdown()
