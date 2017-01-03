# -*- coding: utf-8 -*-
import os
import time



DEBUG = 0



def debugMessage (zeile, ausgabe):
    if (DEBUG > 0):
       print (str (zeile) + " " + ausgabe)
    return

def getLogger ():
    return CFileLog ("TimeEvents.log", 10000)

# An abstract class providing an interface for logging....
class CLog ():
    def __init__(self):
        return
        
    def addEntry (self):
        return
    
            
            
class CFileLog (CLog):
    def __init__(self, pFileName, pMaxLogSize):
        CLog.__init__ (self)
        self.mFileName = pFileName
        self.mMaxLogSize = pMaxLogSize

    def getTimeStampStr (self):
        t = time.localtime()
        tStr = str (t.tm_mday) + "." + str (t.tm_mon) + "." + " "
        tStr = tStr + str (t.tm_hour) + ":" + str (t.tm_min)
        return tStr

    def cleanUpLogFile (self):
        # Make sure that the log file does not exceed the defined maximum size...
        #Check if file exists already ...
        if os.path.isfile(self.mFileName):
            fileSize = os.path.getsize (self.mFileName)
            if (fileSize > self.mMaxLogSize):
                os.remove (self.mFileName)
                return True
        return False    
             
    def addEntry (self, pEntry):
        newLogFileCreated = self.cleanUpLogFile ()
        #File öffen
        try:
            file = open (self.mFileName, "a")
            if (newLogFileCreated == True):
                file.write (self.getTimeStampStr() + " " + "New Log file created\n")
            #Generate date and time for the entry...
            entryStr = self.getTimeStampStr() + " " + pEntry + "\n"
            file.write (entryStr)
            file.close ()
        except:
            print ("Can't open log file")
