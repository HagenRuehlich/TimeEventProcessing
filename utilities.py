# -*- coding: utf-8 -*-

import logging
import subprocess
import sys

def getDayFromString (psDate):
    """ Die Funktion erwartet eine String mit einer Datumangabe im Format
        "23.06." und liefert daraus den Tag als Integer zurück  """
    assert type (psDate)  == str
    return getDayOrMonthFromString (psDate, 0)

def getMonthFromString (psDate):
    """ Die Funktion erwartet eine String mit einer Datumangabe im Format
        "23.06." und liefert daraus den Monat als Integer zurück  """
    assert type (psDate)  == str
    return getDayOrMonthFromString (psDate, 1)


def getDayOrMonthFromString (psDate, piDayOrMonth):
    """ Die Funktion erwartet eine String mit einer Datumangabe im Format
        "23.06." und liefert daraus entweder den Tag (piDayOrMonth = 0)oder den Monat
        (piDayOrMonth = 1) Integer zurück  """
    assert type (piDayOrMonth)  == int
    assert ((piDayOrMonth >= 0) and (piDayOrMonth < 2))
    assert type (psDate)  == str
    iReturn = 0
    sDateStrs = psDate.split (".")
    assert len (sDateStrs) >= 2
    #Führende Leerzeichen und "0" abtrennen, z.B. bei "01"
    sDateStrs [piDayOrMonth].lstrip ()
    sDateStrs [piDayOrMonth].lstrip ("0")
    iReturn = int (sDateStrs [piDayOrMonth])
    return iReturn
        
    
def reBoot ():
    command = "/usr/bin/sudo /sbin/shutdown -r now"        
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print (output)

def initLogger ():
    logfilename = '/var/log/TimeEvents.log'
    logging.basicConfig(filename=logfilename, level=logging.DEBUG,
                          format="%(asctime)s [%(levelname)-8s] [%(module)s:%(funcName)s]: %(message)s",
                          datefmt="%d.%m.%Y %H:%M:%S")
    platformStr = ", Platform: " + sys.platform
    if ('-boot' in sys.argv):
        logging.info ("Time event script start during boot" + platformStr)
    else:
        logging.info ("Time event script start manually" + platformStr)

    
