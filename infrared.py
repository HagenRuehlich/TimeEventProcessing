# -*- coding: utf-8 -*-
import logging
import os

KEY_POWER   =  "KEY_POWER"
KEY_HOME    =  "KEY_HOME"
KEY_OK      =  "KEY_OK"
KEY_LEFT    =  "KEY_LEFT"
KEY_RIGHT   =  "KEY_RIGHT"
KEY_UP      =  "KEY_UP"
KEY_DOWN    =  "KEY_DOWN"
KEY_0       =  "KEY_0"
KEY_1       =  "KEY_1"
KEY_2       =  "KEY_2"
KEY_3       =  "KEY_3"      
KEY_4       =  "KEY_4"
KEY_5       =  "KEY_5"
KEY_6       =  "KEY_6"   
KEY_7       =  "KEY_7"   
KEY_8       =  "KEY_8"   
KEY_9       =  "KEY_9"   

class CInfraredTransmitterTv ():
    """Klasse stellt ein Interface zum Senden Infrarot bereit"""
    def __init__(self):
        self.restartDaemon()

    def __del__(self):
        """Destruktor beendet den Dienst wieder...."""
        self.stopDaemon()

    def startDaemon (self):
        os.system ("/etc/init.d/lirc start")
        logging.info ("LIRC daemon gestartet")    

    def stopDaemon (self):
        os.system ("/etc/init.d/lirc stop")
        logging.info ("LIRC daemon gestoppt")

    def restartDaemon(self):
        self.stopDaemon()
        self.startDaemon()    

    def sendTvKey (self, psKey):
        """sendet die übergebene Taste"""
        assert (type (psKey) == str)
        logging.info ("Teste " + psKey + " send to TV")
        sCommand = "irsend SEND_ONCE Philips_TV" + " " + psKey
        os.system (sCommand)

    
        
    
    

