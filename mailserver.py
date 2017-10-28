# -*- coding: utf-8 -*-

import logging
from smtplib import SMTP
from email.message import Message
from confidental import *



class CMailFromHagen ():
    """Represet a mail sent from Hagens account... """
    def __init__ (self, plReceivers, psSubject, psMailText):
        assert type (plReceivers) == list
        assert type (psSubject)   == str
        assert type (psMailText)  == str    
        self._lReceivers = plReceivers
        self._sSubject = psSubject
        #_sMailText suuports plain ASCII only
        try:
            testStr= psMailText.encode ('ascii')
        except:
            logging.critical("Mail text contains non ACSII characters")
        self._sMailText = psMailText

    def getReceivers (self) :
        return self._lReceivers

    def getSubject (self):
        return self._sSubject

    def getMailText (self):
        return self._sMailText
        



class CMailServer () :
    """this class provides mails services"""
    def __init__(self):
        self._bIsInitiated = True
        try:
            """the conctructor establishes the connection ()"""
            self._smtp = SMTP ()
            self.initiateConncection ()
        except:
            self._bIsInitiated = False
            logging.error ("Mailserver initialization failed")
            
            
        
        
    def __del__ (self):
        if self._bIsInitiated == True :
            self._smtp.quit ()


    def initiateConncection (self):
        self._smtp.connect('mail.gmx.net', 587)
        self._smtp.ehlo()
        self._smtp.starttls()
        self._smtp.login (csMAILUSER, csMAILPASSWORT)

        
    def sendMail (self, pMail):
        assert type (pMail) == CMailFromHagen
        if self._bIsInitiated == True :
            msg = Message ()
            msg.set_payload (pMail.getMailText())
            msg ["Subject"] = pMail.getSubject ()
            msg ["From"]= "Raspberry Pi Hagen Rühlich <raspberryPi.ruehlich@gmx.de>"
            receivers = pMail.getReceivers ()
            
            for res in receivers:
                self._smtp.sendmail ("Raspberry Pi Hagen Rühlich <raspberryPi.ruehlich@gmx.de>", res, msg.as_string())
            
    

##    def sendMail (self, psSubject, psMailText):
##        if self._bIsInitiated == True :
##            msg = Message ()
##            msg.set_payload (psMailText)
##            msg["Subject"] = psSubject
##            msg ["From"]= "Raspberry Pi Hagen Rühlich <raspberryPi.ruehlich@gmx.de>"
##            msg ["To"] = "Hagen Rühlich" + "<" + csMAILUSER + ">"
##            self._smtp.sendmail ("Raspberry Pi Hagen Rühlich <raspberryPi.ruehlich@gmx.de>","Hagen Rühlich" + "<" + csMAILUSER + ">", msg.as_string())



def mailTest ():
    receivers = [csMAIL_ADRESS_KATHRIN, csMAIL_ADRESS_HAGEN]
    msg = CMailFromHagen (receivers, "Testnachricht von Hagens Raspberry Pi",  "Das ist nur eine Testnachricht. Danke für Dein Verstaendnis.  Beste Grusse von Hagen")
    server = CMailServer ()
    server.sendMail (msg)




if __name__ == "__main__":
    mailTest()
        
        
        
        
        
