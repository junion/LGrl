'''
Illustration of a mixed initiative name dialer with
100k names.

To run this dialog manager, see httpd.py

Part of the AT&T Statistical Dialog Toolkit (ASDT).

Jason D. Williams
jdw@research.att.com
www.research.att.com/people/Williams_Jason_D
'''

if (__name__ == '__main__'):
    exit('To run this dialog manager, see httpd.py')

import logging.config
import logging
from GlobalConfig import *
from DB import InitDB
from DialogManager import OpenDialogManager as DialogManager

def GetDM():
    InitConfig()
    config = GetConfig()
    config.read(['config-100k-open.conf'])
    logging.config.fileConfig('logging.conf')
    InitDB()
    dm = DialogManager()
    return dm
