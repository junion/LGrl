'''
Illustration of a mixed initiative name dialer with
100k names.

To run this dialog manager, see httpd.py

Part of the AT&T Statistical Dialog Toolkit (ASDT).

Jason D. Williams
jdw@research.att.com
www.research.att.com/people/Williams_Jason_D
'''

import logging.config
import logging
import threading
import Queue
from GlobalConfig import *
from DialogManager import SBSarsaDialogManager as DialogManager
from GalaxyFrames import *
    
class DialogThread(threading.Thread):
    def __init__(self,sessionID,inQueue,outQueue):
        threading.Thread.__init__(self)

        logging.config.fileConfig('E:/Development/LGrl-G/logging.conf')
        self.appLogger = logging.getLogger('DialogThread')
#        self.appLogger.info('DialogThread init')
        self.sessionID = sessionID
        self.msg_idx = 0
        self.utt_count = 0
        self.inQueue = inQueue
        self.outQueue = outQueue
        self.dialogManager = DialogManager()

        self.appLogger.info('Dialog thread %s created'%self.getName())
    
    def run(self):
        while True:
            frame = self.inQueue.get()
            
#            self.appLogger.info('Event:\n %s'%str(event))
            self.inQueue.task_done()
            message = {'type':'GALAXYACTIONCALL',
                       'data':intro%(self.sessionID,self.msg_idx,"welcome",self.utt_count)}
            self.appLogger.info('message:\n %s'%str(message))
#            self.appLogger.info('message:\n %s'%str(message))
#            message = {'type':'WAITINPUT'}
            self.outQueue.put(message)
                    
