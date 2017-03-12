# -*- coding: utf-8 -*-


from smtplib import SMTP
from email.message import Message
from mailAccount import csMAILUSER
from mailAccount import csMAILPASSWORT

# REMOVE THIS BEFORE COMMITTING!!!
#-----------------------------------
csMAILUSER = "hagen.ruehlich@gmx.de"
csMAILPASSWORT = "h4OG5c3d1ge2x6N33oEE"

#-----------------------------------


class CMailServer () :
    """this class provides mails services"""
    def __init__(self):
        """the conctructor establishes the connection ()"""
        self._smtp = SMTP ()
        self.initiateConncection ()
        
        
    def __del__ (self):
        self._smtp.quit ()


    def initiateConncection (self):
        self._smtp.connect('mail.gmx.net', 587)
        self._smtp.ehlo()
        self._smtp.starttls()
        self._smtp.login (csMAILUSER, csMAILPASSWORT)


    def sendMail (self, psSubject, psMailText):
        msg = Message ()
        msg.set_payload (psMailText)
        msg["Subject"] = psSubject
        msg ["From"]= "Raspberry Pi Hagen Rühlich <raspberryPi.ruehlich@gmx.de>"
        msg ["To"] = "Hagen Rühlich" + "<" + csMAILUSER + ">" 
        self._smtp.sendmail ("Raspberry Pi Hagen Rühlich <raspberryPi.ruehlich@gmx.de>","Hagen Rühlich" + "<" + csMAILUSER + ">", msg.as_string())



def mailTest ():
    server = CMailServer ()
    server.sendMail ("Test Nachricht", "Hagens Raspberry Pi sendet dieses Test Nachricht")




if __name__ == "__main__":
    mailTest()
        
        
        
        
        
