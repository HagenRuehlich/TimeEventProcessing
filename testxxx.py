# -*- coding: utf-8 -*-

import logging
import sys

   
      
if __name__ == "__main__":
    logging.basicConfig (
    filename = "/var/log/TimeEvents.log",
    level = logging.DEBUG,
    style = "{",
    format = "{asctime} [{levelname:8}] {module} {funcName} {lineno} {message}")
    platformStr = ", Platform: " + sys.platform
##    if ('-boot' in sys.argv):
##        logging.info ("Time event script start during boot" + platformStr)
##    else:
##        logging.info ("Time event script start manually" + platformStr)
    logging.info ("Test")
    logging.shutdown()
