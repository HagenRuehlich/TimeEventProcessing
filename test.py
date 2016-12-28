# -*- coding: utf-8 -*-

import logging
import sys

   
      
if __name__ == "__main__":
    logfilename = '/var/log/TimeEvents.log'
    logging.basicConfig(filename=logfilename, level=logging.DEBUG,
                          format="%(asctime)s [%(levelname)-8s] [%(module)s:%(funcName)s]: %(message)s",
                          datefmt="%d.%m.%Y %H:%M:%S")
    platformStr = ", Platform: " + sys.platform
    if ('-boot' in sys.argv):
        logging.info ("Time event script start during boot" + platformStr)
    else:
        logging.info ("Time event script start manually" + platformStr)
##    file = open ("/var/log/DebugTimeEvents.log", "a")
##    file.write ("debug")
##    file.close ()
    logging.shutdown()
